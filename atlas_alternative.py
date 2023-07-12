from requests.auth import HTTPBasicAuth
from time import *
from os import *
from datetime import *
from pytz import *
from getpass import *
import pandas as pd
import requests
import json
import csv
import subprocess
# set adress system
ADDRESS = 'https://lorawan-ns-na.tektelic.com/api/'
ADDRESS_SPLIT = ADDRESS.split("/")[2]
print("\u001b[2J\u001b[0;0H")
USERNAME = 'lbarnowski@tektelic.com'#input("Username: ")
PASSWORD = 'L@7erp0inter'#getpass("Password: ")
jsonList = {
    'username': USERNAME,
    'password': PASSWORD
}
def login(): # this function will log into the NS 
    while True:
        response_token = requests.post(f"{ADDRESS}auth/login", json = jsonList)
        if response_token.status_code == 200:
            print(f"<UPDATE> server login successful at: {ADDRESS_SPLIT}")
            token = response_token.json()['token']
            return token
            break
        else:
            print(f"<UPDATE> server connection faliture.\nERROR: [{response_token.status_code}]\n", "Retrying")
token = login()
print(token)
#def get_sensor_info():
headers = {
    'Content-type' : 'application/json',
    'X-Authorization': f'Bearer {token}'
}
# this function will return the specified NS application and then search the output for the App Name and oter important infromation
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
                print(f"<UPDATE> connection achived, data found at {ADDRESS_SPLIT}")
                applications_list = response_applications.json()
                return applications_list
            else:
                print(f"<UPDATE> connection not found.\nERROR: [{response_applications.status_code}]")
            break
        except:
            print("<UPDATE> can't acess applications, retrying...")
#apps = get_active_applications()
#print(apps)
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
            str = f"{ADDRESS}device/{end_device_id}/log?lastMillis={current_epoch_time}&limit=100&lastIndex=9223372036854775807"
            print(f"Connecting to: {str}...")
            response_device = requests.get(f"{str}", headers = headers, timeout = 15)
            try:
                print(f"<UPDATE> connection achived, data found at: {str}")
                device_specs = response_device.json()
                return device_specs
            except:
                print(f"<UPDATE> device either not found or bad ID used.\nERROR: [{response_device.status_code}]")
            break
        except:
            print("<UPDATE> can't acess device, retrying...")
#device_specs = get_sensor_info("f14f94e0-1aa3-11ee-a7be-7974d8fad914") # this contains the device's id, not to be confued with the aplication id
#print(device_specs)
# this function will get all the data from the aplication id, and return the deice id
def get_device_from_app_ID(applicationID, value):
    """
    This function will return all the information that is associated with the application id
    :param applicationID: this is the application id that will be searched
    :param value: this specifies which item to look for
    :return application_data: this will retun the application data
    """
    while True:
        try:
            str = f"{ADDRESS}application/{applicationID}/devices"
            print(f"Connecting to: {str}...")
            response_data = requests.get(str, headers = headers, timeout = 20)
            try:
                print(f"<UPDATE> connection achived, data found at: {str}")
                application_data = response_data.json()
                return application_data[value]
            except:
                print(f"<UPDATE> device either not found or bad ID used.\nERROR: [{response_data.status_code}]")
            break
        except:
            print(f"<UPDATE> can't acess application, retrying...")
#app_data = get_device_from_app_ID('23ee7bc0-1aa2-11ee-8ee2-c19b4fa5a9aa', "data")
#print(app_data)
#get_sensor_info("f14f94e0-1aa3-11ee-a7be-7974d8fad914")
class get_specs:
    def __init__(self, applicationID):
        self.applicationID = applicationID
        output = get_device_from_app_ID(self.applicationID, "data")
        return output
    def newKKey(self):
        output = get_device_from_app_ID(self.applicationID, "data")
        return output["nwkSKey"]
    def appKey(self):
        output = get_device_from_app_ID(self.applicationID, "data")
        return output["appKey"]
    def cntmsb(self):
        #output = get_device_from_app_ID(self.applicationID, "data")
        #return output[""]
        pass
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
# this function will return the output from an external os command
def run_extern_program(program, *args):
    if args != None:
        process = program + args
    else:
        process = program
    result = subprocess.run(process, capture_output = True, text = True) # execute the program and capture its output
    output_lines = result.stdout.splitlines()
    return output_lines
def header(text): # this is just a function that will create a boarder around a title or line of text
    ts = get_terminal_size()
    print(f"{'-' * ts.columns}\n{text}\n{'-' * ts.columns}")
### Main code ###
print("\u001b[2J\u001b[H")
header("Tektelic NS Shell Interface")
apps = get_active_applications()
application_INFO = search_key(apps, "id")
application_ID = search_key(application_INFO, "id")
i = 0
device_id_list = []
rawPayload_list = []
for id in application_ID:
    device_data = get_device_from_app_ID(application_ID[i], "data")
    device_INFO = search_key(device_data, "id")
    device_ID = search_key(device_INFO, "id")
    print(device_ID)
    if len(device_ID) != 0:
        device_id_list.extend(device_ID)
        #app_id_list.append(app_ID[0])
        #print(app_ID[0])
    i += 1
print(device_id_list,f"\n{len(device_id_list)} total items.")
for device_id in device_id_list:
    device_specs = get_sensor_info(device_id)
    #print(device_specs)
    rawPayload = search_key(device_specs, "rawPayload")
    print(rawPayload)
    rawPayload_list.append(rawPayload)
print(rawPayload_list,f"\n{len(rawPayload_list)} total items.")
#for item in rawPayload_list:
run_extern_program("lora-packet-decode","")