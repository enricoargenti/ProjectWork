# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import json 
import os
import asyncio
#from dotenv import load_dotenv
# per installare la libreria di azure basta inserire nel terminale la seguente riga di comando: pip3 install azure-iot-device
from azure.iot.device.aio import IoTHubDeviceClient
import datetime
import time
# per installare la libreria per la comunicazione seriale basta inserie nel terminale la seguente riga di comando 
import serial

# create an serial object
serialport = serial.Serial(port = "COM2", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

#load_dotenv("connectionstring.env")
# per rendere il codice più sicuro, sarebbe meglio mettere la connection string del device iot come variabile di ambiente, cosi non è visibile nel codice.
# per aggiungere la variabile di ambiente nella powershell (il terminale powershell aperto dentro in nostro progetto), basta inserire la seguente riga di comando:
# $env:IOTHUB_DEVICE_CONNECTION_STRING='<inserisci_la_stringa_di_connessione_del_device_IoT>'
def message_received_callback(message):
    print("Received message from serial port:")
    print(f"    {message.data.decode('ASCII')}")
    serialport.write(message.data)

class OpenDoorRequest:
    def __init__(self, Id,DoorId,DeviceId,DeviceGeneratedCode,CloudGeneratedCode,AccessRequestTime):
        self.Id = Id
        self.DoorId = DoorId
        self.DeviceId = DeviceId
        self.DeviceGeneratedCode = DeviceGeneratedCode
        self.CloudGeneratedCode = CloudGeneratedCode
        self.AccessRequestTime = AccessRequestTime

class DateTimeEncoder(json.JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()

async def main():
    # Fetch the connection string from an environment variable
    #conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
    conn_str = "HostName=Pi-Cloud.azure-devices.net;DeviceId=Device2;SharedAccessKey=WVGFS0B04eSzeV1QhtcK1LKywrBb7aq8C1dQGLH9TKw="
    device_id = "Device2"
    # Create instance of the device client using the connection string
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)
    device_client.on_message_received = message_received_callback
    # Connect the device client.
    await device_client.connect()

    
    
    
    #print("Sending message...")

    while (True):
        Id = None
        DoorId = input("DoorId: ")
        DeviceId = device_id
        DeviceGeneratedCode = input("DeviceGeneratedCode: ")
        CloudGeneratedCode = None
        AccessRequestTime = datetime.datetime.now()
        

        openDoorRequest = OpenDoorRequest(Id,int(f"{DoorId}"), DeviceId, DeviceGeneratedCode, CloudGeneratedCode, AccessRequestTime)
        message = json.dumps(openDoorRequest.__dict__, indent=6, cls= DateTimeEncoder)

        await device_client.send_message(message)
        print("Message successfully sent!")
        time.sleep(1)
    
        

    # Finally, shut down the client
    await device_client.shutdown()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()


