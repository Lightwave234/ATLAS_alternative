from requests.auth import HTTPBasicAuth
#from requests import status_codes
#from requests import *
from getpass import *
from time import *
from os import *
from datetime import *
from pytz import *
import pandas as pd
import requests
import json
import csv
# set adress system
ADDRESS = 'https://lorawan-ns-na.tektelic.com/api/'
ADDRESS_SPLIT = ADDRESS.split("/")[2]
print("\u001b[2J\u001b[0;0H")
USERNAME = "lbarnowski@tektelic.com"#str(input("Username: "))
PASSWORD = "L@7erp0inter"#str(getpass("Password: "))
jsonList = {
    'username': USERNAME,
    'password': PASSWORD
}
def login(): # this function will log into the NS 
    while True:
        response_token = requests.post(f"{ADDRESS}auth/login", json = jsonList)
        if response_token.status_code == 200:
            print(f"[UPDATE] server login successful at: {ADDRESS_SPLIT}")
            token = response_token.json()['token']
            return token
            break
        else:
            print(f"[UPDATE] server connection faliture.\nERROR: [{response_token.status_code}]\n", "Retrying")
token = login()
print(token)
#def get_sensor_info():
headers = {
    'Content-type' : 'application/json',
    'X-Authorization': f'Bearer {token}'
}
# this function will return the specified NS application and then search the output for the App Name, Sensor names, DEVEUI, APPEUI
def get_active_applications():
    """
    This function will return all the currently exisiting applications
    :param: None
    :return: this will return all infromation in regard to the application.
    """
    while True:
        try:
            response_applications = requests.get(f"{ADDRESS}customer/applications", headers = headers, timeout = 10)
            if response_applications.status_code == 200:
                print(f"[UPDATE] connection achived, data found at {ADDRESS_SPLIT}")
                applications_list = response_applications.json()
                return applications_list
            else:
                print(f"[UPDATE] connection not found.\nERROR: [{response_applications.status_code}]")
            break
        except:
            print("[UPDATE] can't acess applications, retrying...")
apps = get_active_applications()
print(apps)
# this function returns all the speifications that a device has based on it's ID
def get_sensor_info(end_device_id):
    """
    Returns a json of real-time packets
    :param end_device_id (str): searches for the RTP's using the device's id
    :return: None
    """
    while True:
        try:
            # generate current epoch time
            TZ = 'MST' # this will use the current timezone
            current_epoch_time = int(datetime.now(timezone(TZ)).timestamp()) * 1000 # this system will generate a current epoch time
            print("Curent epoch time:",current_epoch_time)
            print(f"Connecting to: {ADDRESS}device/{end_device_id}/log?lastMillis={current_epoch_time}&limit=100&lastIndex=9223372036854775807...")
            response_device = requests.get(f"{ADDRESS}device/{end_device_id}/log?lastMillis={current_epoch_time}&limit=100&lastIndex=9223372036854775807", headers = headers, timeout = 10)
            try:
                print(f"[UPDATE] connection achived, data found at {ADDRESS_SPLIT}")
                device_specs = response_device.json()
                return device_specs
            except:
                print(f"[UPDATE] device either not found or bad ID used.\nERROR: [{response_device.status_code}]")
            break
        except:
            print("[UPDATE] can't acess device, retrying...")
device_specs = get_sensor_info("f14f94e0-1aa3-11ee-a7be-7974d8fad914")
print(device_specs)
#get_sensor_info("f14f94e0-1aa3-11ee-a7be-7974d8fad914")
def disp(list):
    for item in list:
        print(item)
# this function will read out all the data from a specific value 
def search_key(json_to_use, value):
    """
    This function will print out the keys associated with a specific value from a JSON list
    :param json_to_use: specify the name of the json list to use in the program
    :param value: set a specific value to look for in the json
    :return: the key results of the value specifed
    """
    results = []
    for item in json_to_use:
        if value in item:
        #for key, value in json_to_use.items():
            results.append(item[value])
    return results
# this function returns the second item in a likned list (in this case for the application name, and getting it's id)
def serch_nested_list(nested_list, name):
    """
    this will search the nested list for the item after the name
    :param nested_list: this is the nested list to use (this will not work on regular lists)
    :param name: this is where to put the name of the item to find
    :return: this will return the item [index][1] after item [index][0] where the item's name is 
    """
    for sublist in nested_list:
        if sublist[0] == name:
            return sublist[1]
    return None
# this function will make a CSV file, based on the json list provided    
def CSV_make(list_to_use, filename = 'New.csv'):
    if filename == None:
        filename = 'New.csv'
    df = pd.DataFrame(list_to_use)
    df.to_csv(filename, index = False)
    print(f"CSV file {filename} has been created")

def header(text): # this is just a function that will create a boarder around a title or line of text
    ts = get_terminal_size()
    print(f"{'-' * ts.columns}\n{text}\n{'-' * ts.columns}")
### Main code ###
print("\u001b[2J\u001b[H")
header("Tektelic NS Shell Interface")
names = []
ids = []
# get the payload information
PayLoads = search_key(device_specs, "rawPayload")
for item in PayLoads:
    print(item)
# get the aplication id's
application_ID = search_key(apps, "id")
for item in application_ID:
    print(item["id"])
    ids.append(item["id"])
# get the respective application names
application_NAME = search_key(apps, "name")
for item in application_NAME:
    print(item)
    names.append(item)
# this will combine the application names with their respective ids
namesAndIds = zip(names, ids)
namesAndIds_list = list(namesAndIds)
namesAndIds_list = [list(t) for t in namesAndIds_list]
print(namesAndIds_list)
restult_id = serch_nested_list(namesAndIds_list, "Pelican test")
print(restult_id)
# this just puts some of the json data into csv files
CSV_make(device_specs, "KIWI-logs.csv")
CSV_make(PayLoads, "Raw-Payloads.csv")
CSV_make(apps, "appdata.csv")