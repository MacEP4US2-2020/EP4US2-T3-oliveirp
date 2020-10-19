# Tutorial 3 Pi Vision Data Transfer Python program 
# Adapted from example tutorial code given by Guha Ganesh
# Last Modified: October 18, 2020
# Program Purpose: Upload data extracted from the ESP32 Devkit and upload to the OSIsoft server

# Import packages
import serial 

# Additional Imports for OSIsoft
import datetime
import json
import requests
import sys
import time
import warnings
import urllib3 
urllib3.disable_warnings() # used to solve import request issues

from requests.packages.urllib3.exceptions import InsecureRequestWarning

# DO NOT CHANGE THE VALUES BELOW UNLESS TOLD TO DO SO
# CONNECTION TO ACADEMIC HUB MAY STOP IF INCORRECT VALUES ARE PROVIDED
APIM_KEY = '918bb2cf4b0643c49b5b8464632c77b6'
DEFAULT_OMF_URL = 'https://academicpi.azure-api.net/iotprojects/messages'
PRODUCER_TOKEN = "mcmaster_lab"

# OMF Messages generated and sent below are compliant with the following specification:
#   The OSIsoft Message Format, v1.0: http://omf-docs.osisoft.com/en/v1.0/
#

# To avoid certificates and deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


####################################################################################################
####################################################################################################
##################################### EP4US2 SMART SYSTEMS #########################################
###################################### START CODING HERE ###########################################
####################################################################################################
####################################################################################################

'''The code was modified so that the when a new value is read all the previous values are not erased. 
Before when a new line was read the previous values would be reset to 0. The previous values are now 
saved to a variable called prev_values which is set to 0 initially before any values are read. When
the new values are read they are saved in the same JSON format that is sent to the server and the 
previous values are retrieved everytime. This allows for the proper graphing of the variables
without having them reset to 0.'''



arduino = serial.Serial('COM8', baudrate=9600, parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=3)
f = open("data.txt","w")

prev_values = 0 #initiazlie prev_values variable for when it is run the first time

#extra parameter was added for previous data
def create_data_values_stream_message(target_stream_id,prev_data_values):


    #Assign variables (attributes) in your case it will be the sensor data that you want to send

    #generic timestamp (you can remove this if you want, but the code below grabs the timestamp)
    timestamp = datetime.datetime.utcnow().isoformat() + 'Z'

    #Sensor Data Variables
    
    #If previous values were not already recorded set them to 0
    if prev_values == 0:
        dhtTempC = 0 
        dhtTempF = 0 
        dhtHum = 0 
        dsTempC = 0
        dsTempF = 0
        ambientLight = 0 
    #set the values to their previously recorded values
    else:
        dhtTempC = prev_data_values[0]['values'][0]['DHT Temperature C']
        dhtTempF = prev_data_values[0]['values'][0]['DHT Temperature F']
        dhtHum = prev_data_values[0]['values'][0]['DHT Humidity']
        dsTempC = prev_data_values[0]['values'][0]['DS18B20 Temperature C']
        dsTempF = prev_data_values[0]['values'][0]['DS18B20 Temperature F']
        ambientLight = prev_data_values[0]['values'][0]['Ambient Light']    
    
    nextLine = arduino.readline() # reads the next line from arduino
    data = nextLine.decode('utf-8') # converts byte values
    
    f.write(data)
    
    #data.split arranges the string into an array with elements that are spliced based on the spaces in the string
    
    label = data.split()[0] + data.split()[1] #determines which sensor data variable (ambient light, DHT Temp in F, etc.)
    value = data.split()[2]                   #the value of the specific sensor data variable
    
    print(label)                             #I have commented out all the print statements because it is messy and unclear to me
    print(value)                             #I found it much more useful to just print this out.
    



    #checks the incoming data for the variable and stores it under the appropriate python variable name
    
    if "TemperatureC:" == label:
        dsTempC = float(value)

    if "TemperatureF:" == label:
        dsTempF = float(value)

    if "LightSensor:" == label:
        ambientLight = float(value)

    #My DHT current does not work but I plan to get a new one from Peter this week

        

    #Pi Vision requires the data to be in a JSON format, so the following code will assign the values you just read from the text file to a JSON format
    data_values_json = [
        {
            "containerid": target_stream_id,
            "values": [
                {
                    "Time": timestamp,
                    "DHT Temperature C": dhtTempC,
                    "DHT Temperature F": dhtTempF,
                    "DHT Humidity": dhtHum,
                    "Ambient Light": ambientLight,
                    "DS18B20 Temperature C": dsTempC,
                    "DS18B20 Temperature F": dsTempF,
                }
            ]
        }
    ]
    return data_values_json

####################################################################################################
####################################################################################################
##################################### EP4US2 SMART SYSTEMS #########################################
###################################### STOP CODING HERE ############################################
############################# SCROLL DOWN FOR THE LAST CODE CHANGE #################################
####################################################################################################
####################################################################################################



# ************************************************************************
def sendOMFMessageToEndPoint(relay_url, message_type, omf_data, echo=True):
    try:
        msg_header = {'producertoken': producer_token,
                      'messagetype': message_type,
                      'action': 'create',
                      'messageformat': 'JSON',
                      'omfversion': '1.0',
                      'connection': 'keep-alive',
                      'Ocp-Apim-Subscription-Key': APIM_KEY}
        data = json.dumps(omf_data)
        if echo:
            pass
            #print('> ------ Message sent begin -------')
            #print('>> Headers:', msg_header)
            #print('>> Message: ', data)
            #print('> ------ Message sent end   -------')
        response = requests.post(relay_url, headers=msg_header, data=data, verify=False, timeout=30)
        if echo:
            pass
            #print('< ------ Response received begin -------')
            #print('>> Status code:', response.status_code)
            #print('>> Headers:', response.headers)
            #print('>> Message: ', response.text)
            #print('< ------ Response received end -------')
        #print('Response from relay from the initial "{0}" message: {1} {2} (len={3})'.format(message_type,
                                                                                             #response.status_code,
                                                                                             #response.text, len(data)))
        return response.status_code
    except Exception as e:
        #print(str(datetime.datetime.now()) + " An error occurred during web request: " + str(e))
        return 500

####################################################################################################
####################################################################################################
##################################### EP4US2 SMART SYSTEMS #########################################
###################################### START CODING HERE ###########################################
####################################################################################################
####################################################################################################

#dont change anything in this
types = [
    {
        "id": "type_Oliveira_Pedro_Tutorial3",#you need to change your ID to 'type_Oliveira_Pedro_Tutorial3', please change them for the references below as well
        "type": "object",
        "classification": "static",
        "properties": {
            "Name": {
                "type": "string",
                "isindex": True
            },
            "Location": {
                "type": "string"
            }
        }
    },
    #You set the different types of Sensor data that you are sending here.
    #Assign them below and keep them as a number type
    {
        "id": "type_measurement_v9",
        "type": "object",
        "classification": "dynamic",
        "properties": {
            "Time": {
                "format": "date-time",
                "type": "string",
                "isindex": True
            },
            "DHT Temperature C": {
                "type": "number"
            },
            "DHT Temperature F": {
                "type": "number"
            },
            "DHT Humidity": {
                "type": "number"
            },
            "Ambient Light": {
                "type": "number"
            },
            "DS18B20 Temperature C": {
                "type": "number"
            },
            "DS18B20 Temperature F": {
                "type": "number"
            },
        }
    }
]


def container_value(name):
    containers = [{
        "id": "measurement%s" % name,
        "typeid": "type_measurement_v9"     #version changed
    }]
    return containers


def static_value(name):
    static_data = [{
        "typeid": "type_Oliveira_Pedro_Tutorial3",
        "values": [{
            "Name": "Oliveira_Pedro_Tutorial3-%s" % name,
            "Location": "Hamilton, ON"
        }]
    }]
    return static_data


def link_value(name):
    link_data = [{
        "typeid": "__Link",
        "values": [{
            "source": {
                "typeid": "type_Oliveira_Pedro_Tutorial3",
                "index": "_ROOT"
            },
            "target": {
                "typeid": "type_Oliveira_Pedro_Tutorial3",
                "index": "Oliveira_Pedro_Tutorial3-%s" % name
            }
        }, {
            "source": {
                "typeid": "type_Oliveira_Pedro_Tutorial3",
                "index": "Oliveira_Pedro_Tutorial3-%s" % name
            },
            "target": {
                "containerid": "measurement%s" % name
            }
        }]
    }]
    return link_data

####################################################################################################
####################################################################################################
##################################### EP4US2 SMART SYSTEMS #########################################
###################################### STOP CODING HERE ############################################
####################################################################################################
####################################################################################################


if __name__ == "__main__":
    #print("Enter custom URL for Relay, or <ENTER> for Academic Hub:\n  >> ", end='')
    #relay_url = input()
    #if len(relay_url) == 0:
    relay_url = DEFAULT_OMF_URL
    producer_token = PRODUCER_TOKEN
    #print("@@@ current producertoken= %s" % producer_token)

    #print("> Enter a word to name test tank element in AF: ", end='')
    #name_input = input()
    af_name = "V9.0"                                 #version changed
    if len(af_name) == 0:
        pass
        #print("\n >>> Input word cannot be empty. Stopping.")
    else:
        if sendOMFMessageToEndPoint(relay_url, "Type", types) > 202:
            sys.exit(1)
        # time.sleep(1)
        if sendOMFMessageToEndPoint(relay_url, "Container", container_value(af_name)) > 202:
            sys.exit(1)
        # time.sleep(1)
        if sendOMFMessageToEndPoint(relay_url, "Data", static_value(af_name)) > 202:
            sys.exit(1)
        # time.sleep(1)
        if sendOMFMessageToEndPoint(relay_url, "Data", link_value(af_name)) > 202:
            sys.exit(1)
        # time.sleep(1)
        # ************************************************************************
        while True:
            values = create_data_values_stream_message("measurement%s" % af_name,prev_values)
            prev_values = values
            if sendOMFMessageToEndPoint(relay_url, "Data", values) > 202:
                sys.exit(1)
            time.sleep(1)