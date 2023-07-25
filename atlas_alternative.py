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
import re
import fileinput
#import io
# set adress system
ADDRESS = 'https://lorawan-ns-na.tektelic.com/api/'
ADDRESS_SPLIT = ADDRESS.split("/")[2]
print("\u001b[2J\u001b[0;0H")
USERNAME = input("Username: ")
PASSWORD = getpass("Password: ")
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
            print(f"<UPDATE> server connection faliture.\nERROR: [{response_token.status_code}]\n", "Retrying...")
            exit()
token = login()
print(token)
#def get_sensor_info():
headers = { # these are just 
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
            #timeout = 15
            # generate current epoch time
            TZ = 'MST' # this will use the current timezone
            current_epoch_time = int(datetime.now(timezone(TZ)).timestamp()) * 1000 # this system will generate a current epoch time
            print("Curent epoch time:",current_epoch_time)
            str = f"{ADDRESS}device/{end_device_id}/log?lastMillis={current_epoch_time}&limit=100&lastIndex=9223372036854775807"
            print(f"Connecting to: {str}...")
            response_device = requests.get(f"{str}", headers = headers, timeout = 20)
            try:
                print(f"<UPDATE> connection achived, data found at: {str}")
                device_specs = response_device.json()
                return device_specs
            except:
                print(f"<UPDATE> device either not found or bad ID used.\nERROR: [{response_device.status_code}]")
            break
        except:
            #timeout += 5
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
# this class should get the nwkSKey, appKey, and cntmsb
#class get_specs:
#    def __init__(self, applicationID):
#        self.applicationID = applicationID
#        self.output = get_device_from_app_ID(self.applicationID, "data")
#    def allinfo(self):
#        if len(self.output) != 0:
#            return self.output
#    def NwkSKey(self):
#        if len(self.output) != 0:
#            return self.output[0]["nwkSKey"]
#    def AppSKey(self):
#        if len(self.output) != 0:
#            return self.output[0]["appSKey"]
#    def cntmsb(self): # I still need some clarification on what this means
#        pass
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
def CSV_make(list_to_use, filename = 'new.csv'):
    """
    This function will create a csv using a list or json, and store the data in a csv file
    :param list_to_use: specify the list/json
    :param filename: give the file a name (optional), if no name is specified, the output will default to a file named 'new.csv'
    :retun: None
    """
    if filename == None:
        filename = 'New.csv'
    df = pd.DataFrame(list_to_use)
    df.to_csv(filename, index = False)
    print(f"CSV file {filename} has been created")
# this function will return the output from an external os command
def run_extern_program(command):
    """
    This will execute an external command from shell, and retun the output
    :param program: Specify the command or program from the shell to use, and their arguments
    :return output_lines: this is the output string that the program or command will return after execution
    """
    result = subprocess.run(command, capture_output = True, text = True, shell = True)
    ouput = result.stdout.strip().split('\n')
    return ouput
# this function should get the name of an aplication
#def app_names():
#    apps = get_active_applications()
#    print(apps)
# this is just a function that will create a boarder around a title or line of text
def header(text):
    """
    This function will create a line of text that is surrounded by a boarder that extends across the shell
    :param text: this is where the text is located
    :return: None
    """
    ts = get_terminal_size()
    print(f"{'-' * ts.columns}\n{text.center(int(ts.columns))}\n{'-' * ts.columns}")
def generate_unique_key(key, counter):
    if counter == 0:
        return 0
    else:
        return f"{key}({counter})"
### Main code ###
print("\u001b[2J\u001b[H")
header("Tektelic NS Shell Interface")
apps = get_active_applications() # get all the avalable apps
print(apps)
application_INFO = search_key(apps, "id") # sort out every key that starts with 'id'
application_ID = search_key(application_INFO, "id") # sort every sub-key that stars with key
data = {}
counter = {}
device_id_list = []
device_names   = []
#names = set(device_names)
for id in application_ID: # get the application ID
#for index, id in enumerate(application_ID):
    subItem = {}
    device_data = get_device_from_app_ID(id, "data") # search under the data key
    #print(device_data)
    name = search_key(device_data, "name")
    print(name)
    ### get the device name ###
    device_name = search_key(device_data, "deviceModelName") # serch under the subkey 'deviceModelName' to get the device name
    #print(device_name,f"\nList length: {len(device_name)} items")
    #if len(device_name) != 0:
    if device_name in device_names:
        pass
    else:
        device_names.extend(device_name) # sore the device names in a list
    ### end: get the device name ###
    ### get the appSKey of the application ###
    AppSKey = search_key(device_data, "appSKey")
    for index, value in enumerate(AppSKey):
        subItem['AppSKey'] = AppSKey
        key = AppSKey[index]
        subItem['AppSKey'] = key
    ### end: get the appSKey of the application ###
    ### get the nwkSKey of the application ###
    NwkSKey = search_key(device_data, "nwkSKey")
    #subItem['NwkSKey'] = NwkSKey
    for index, value in enumerate(NwkSKey):
        key = NwkSKey[index]
        subItem['NwkSKey'] = key
    ### end: get the nwkSKey of the application ###
    device_INFO = search_key(device_data, "id") # search the 'id' key, for the device information
    device_ID = search_key(device_INFO, "id") # search the sub-key 'id' for the device ID
    #subItem['device_ID'] = device_ID
    for index, value in enumerate(device_ID):
        key = device_ID[index]
        subItem['device_ID'] = key
    print(device_ID,'\n',len(device_ID))
    print(device_name,'\n',len(device_name))
    print(AppSKey,'\n',len(AppSKey))
    print(NwkSKey,'\n',len(NwkSKey))
    #print(len(subItem))
    #print(subItem)
    #device_id_list.append(subItem)
    #print('device_names:',len(device_names))
    #print('device_id_list:',len(device_id_list))
    device_id_list.append(subItem)
    for key, value in zip(name, subItem):
        if key in data:
            data[key].append(value)
        else:
            data[key] = [value]
print(data)
#print(len(device_id_list))
#print(device_id_list)
#print(len(device_names))
#print(device_names)
### ###
#for key, value in zip(name, subItem):
#    if key in data:
#        data[key].append(value)
#    else:
#        data[key] = [value]
#print(data)
#for key, value in zip(device_names, device_id_list):
#    if key in data:
#        if key not in counter:
#            counter[key] = 1
#            new_key = generate_unique_key(key, counter[key])
#        else:
#            counter[key] += 1
#            new_key = generate_unique_key(key, counter[key])
#    else:
#        new_key = key
#    data[new_key] = value
#print(data)
#app_names()
    #subItem.reverse()
    #print(device_names,'\n',device_id_list)
#for key, value in zip(device_names, device_id_list):
#    # If the key already exists in the dictionary, append the value to the existing list
#    if key in data:
#        data[key].append(value)
#    else: # otherwise create a new list with the value of the first element
#        data[key] = [value]
#    if key in data:
#        if key not in 
#print(data)

### refrence, do not delete ###
#for item in device_id_list: 
#    sublist = []
#    for device_id in item:
#        device_specs = get_sensor_info(device_id) # this is where the devices are logged into
#        #print(device_specs)
#        rawPayload = search_key(device_specs, "rawPayload") # this is where to get the payloads
#        #print(rawPayload)
#        sublist.append(rawPayload) # store all the raw payloads into a sub-list to later be used with the NwkSKeys and AppSKeys
#    rawPayload_list.append(sublist) # put the sblist into a larger list
#for item in application_ID: # for every item in the application_ID list, identify, but do not use blanks
#    if len(item) != 0:
#    #if not len(item):
#        appSpecs = get_specs(item) # assign the id to an object, and then pull out specific info
#        if not appSpecs.NwkSKey():
#            pass
#        else:
#            NwkSKeys.append(appSpecs.NwkSKey())
#        if not appSpecs.AppSKey():
#            pass
#        else:
#            AppSKeys.append(appSpecs.AppSKey())
#print("Secret NwkSKeys:\n",NwkSKeys,f"\n{len(NwkSKeys)} total items.\nSecret AppSKeys:\n",AppSKeys,f"\n{len(AppSKeys)} total items.")
#i = 0
#for sublist in rawPayload_list:
#    decode_items = []
#    for j, item in enumerate(sublist):
#        output = run_extern_program(f"lora-packet-decode --nwkkey {NwkSKeys[i]} --appkey {AppSKeys[i]} --base64 {item}")
#        decode_items.append(output)
#    i += 1
#    FRMPayload_decript.append(decode_items)
####
#print("FRMPayload_decript has:",len(FRMPayload_decript),"items")
####
#for sublist in FRMPayload_decript:
#    for item in sublist:
#        for subitem in item:
#            try:
#                modified_text = re.findall(r'[0-9-A-F]+', item[15])
#                if len(modified_text) == 0:
#                    pass
#                else:
#                    decrpited_info.append(modified_text[0])
#            except:
#                pass
#for item in decrpited_info:
#    hex_starting_with_0 = {s for s in decrpited_info if s.startswith('0')}
#    unique_hex = list(set(hex_starting_with_0))
#for item in unique_hex:
#    pairs = [item[i:i+2] for i in range(0, len(item), 2)]
#    converted_item = ', '.join([f"0X{pair}" for pair in pairs])
#    hex.append(converted_item)
#print(hex)
#print(device_names)
#for item in hex:
#    print(item)
#for item in device_names:
#    print(item)
##for item in hex:
##    print(item)
#### this is where I will pass one of the arguments into the application before executing it ###
##file = open(r"C:\Users\lbarnowski\documents\src\new.txt", "r")
#fileName = "kiwi-clover-v2.0-decoder.js"
#line_number_to_mod = 4
#new_line_content = "    var bytes = convertToUint8Array([]);"
#try:
#    for line_number, line in enumerate(fileinput.input(fileName, inplace = True, backup = '.bak'), 1):
#        if line_number == line_number_to_mod:
#            print(new_line_content)
#        else:
#            print(line, end = "")
#except FileNotFoundError:
#    print("file not found")
#except Exception as e:
#    print("Error occured while modifying the file")