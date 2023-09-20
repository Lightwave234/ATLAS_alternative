#!/usr/bin/python3.10
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
import threading
import sys
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
            print(f"\r\033[A<UPDATE> server connection faliture.\nERROR: [{response_token.status_code}]\n", "Retrying...")
            exit()
token = login()
print(token)
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
                print(f"<UPDATE> connection achived, data found at: {ADDRESS_SPLIT}")
                applications_list = response_applications.json()
                return applications_list
            else:
                print(f"\r\033[A<UPDATE> connection not found.\nERROR: [{response_applications.status_code}]")
            break
        except:
            print("\r\033[A<UPDATE> can't acess applications, retrying...")
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
            #print("Curent epoch time:",current_epoch_time)
            str = f"{ADDRESS}device/{end_device_id}/log?lastMillis={current_epoch_time}&limit=100&lastIndex=9223372036854775807"
            #print(f"Connecting to: {str}...")
            start_spinner(f"Connecting to: {str}...")
            response_device = requests.get(f"{str}", headers = headers, timeout = 20)
            try:
                stop_spinner()
                print(f"<UPDATE> connection achived, data found at: {str}")
                device_specs = response_device.json()
                return device_specs
            except:
                print(f"<UPDATE> device either not found or bad ID used.\nERROR: [{response_device.status_code}]")
            break
        except:
            #print("\r\033[A<UPDATE> can't acess device, retrying...")
            pass
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
            #print(f"Connecting to: {str}...")
            start_spinner(f"Connecting to: {str}...")
            response_data = requests.get(str, headers = headers, timeout = 20)
            try:
                stop_spinner()
                print(f"<UPDATE> connection achived, data found at: {str}")
                application_data = response_data.json()
                return application_data[value]
            except:
                print(f"<UPDATE> device either not found or bad ID used.\nERROR: [{response_data.status_code}]")
            break
        except:
            #print(f"<UPDATE> can't acess application, retrying...")
            pass
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
def header(text):
    """
    This function will create a line of text that is surrounded by a boarder that extends across the shell
    :param text: this is where the text is located
    :return: None
    """
    ts = get_terminal_size()
    print(f"{'-' * ts.columns}\n{text.center(int(ts.columns))}\n{'-' * ts.columns}")
### This section is just to indicate if cirtan things are working ###
spinner_active = False
spinner_thread = None
def loading_spinner(text, delay=0.1):
    while spinner_active:
        for char in '|/-\\':
            sys.stdout.write('\r' + f'{text} {char}')
            sys.stdout.flush()
            sleep(delay)
def start_spinner(text="Loading:", delay=0.1):
    global spinner_active, spinner_thread
    if not spinner_active:
        # Start the spinner in a separate thread (only once)
        spinner_active = True
        spinner_thread = threading.Thread(target=loading_spinner, args=(text, delay))
        spinner_thread.daemon = True
        spinner_thread.start()
def stop_spinner():
    global spinner_active
    if spinner_active:
        spinner_active = False
        spinner_thread.join()
        #sys.stdout.write('\n')
        sys.stdout.write('\n\r\033[A')
        sys.stdout.flush()
### ###
# This function will run a JS docoder while also replacing some information in the scrpit it's useing before executing and collecting the ouput
def search_and_decrypt(data, js_app):
    """
    This function will run a JS docoder while also replacing some information in the scrpit it's useing before executing and collecting the ouput
    :param app name: This takes a string of the application name, that will be used in the execution
    :param hex string: This is where the hexidecimal string is used as new input data for the JS decoders
    :return: new result JSON
    """
    check_file = stat(js_app).st_size
    while True:
        if check_file != 0:                                                         # make sure that the file isn't empty
            search_line = " var bytes = convertToUint8Array([]);"                   # line to look for in the JS app
            replacement_line = f"   var bytes = convertToUint8Array([{data}]);"     # line to replace with in the JS script
            with fileinput.FileInput(js_app, inplace=True, backup='.bak') as file:  # write to and creat a backup of the JS script
                for line in file:
                    if search_line in line:
                        line = replacement_line + '\n'
                    print(line, end='')
            while True:
                result = subprocess.run(f'node {js_app}', capture_output=True, text=True, shell=True, cwd=None) # execute the specified script
                if result != 0: # as long as the output isn't empty, run these lines of code
                    try: # if this conversion system fails, go to the other one
                        result_stdout = result.stdout.strip().split(', ')
                        json_dict = {}
                        for item in result_stdout:
                            key, value = item.split(': ')
                            key = key.strip('{}')
                            json_dict[key] = value.strip('{}')
                        new_result = json.dumps(json_dict, indent=2)
                        new_result = new_result.replace('\n', '')
                        return new_result
                    except:
                        result_stdout = result.stdout.strip().split('\n')
                        json_dict = {}
                        key = None
                        # look for the start and stop of the output
                        for item in result_stdout:
                            if item == '{':
                                continue
                            elif item == '}':
                                break
                            elif ':' in item:
                                key, value = item.split(':')
                                key = key.strip()
                                if value.strip().startswith('['):
                                    # handle the array values
                                    try:
                                        json_dict[key] = json.loads(value)
                                    except:
                                        json_dict[key] = value.strip(',')
                                else:
                                    json_dict[key] = value.strip(',')
                            else:
                                value = item.strip(',')
                                if key is not None:
                                    # Concatenate non-string values
                                    json_dict[key] += ' ' + value
                        new_result = json.dumps(json_dict, indent=2)
                        new_result = new_result.replace('\n', '')
                        return new_result
                    break
                else:
                    return None
        else:
            break
### Main code ###
sys.stdout.write("\u001b[2J\u001b[H\033[?25l")
sys.stdout.flush()
header("Tektelic NS Shell Interface")
apps = get_active_applications() # Get all the avalable applications from the network server
application_INFO = search_key(apps, "id") # Sort out every key that starts with the key 'id'
application_NAME = search_key(apps, "name")
application_ID = search_key(application_INFO, "id") # Sort every sub-key that stars with the key 'id'
data      = {}
appData   = []
dev_names = []
for name in application_NAME:
    dev_names.append(name)
for id in application_ID: # get the application ID 
    subItem = {}
    devices = []
    apps    = []
    nets    = []
    dev_ids = []
    device_data = get_device_from_app_ID(id, "data") # Search under the 'data' key
    ### get the device names ###
    device_name = search_key(device_data, "deviceModelName")
    for index, value in enumerate(device_name):
        devices.append(value)
    ### end: get the device names ###
    ### get the appSKey of the application ###
    AppSKey = search_key(device_data, "appSKey")
    for index, value in enumerate(AppSKey):
        apps.append(value)
    ### end: get the appSKey of the application ###
    ### get the nwkSKey of the application ###
    NwkSKey = search_key(device_data, "nwkSKey")
    for index, value in enumerate(NwkSKey):
        nets.append(value)
    ### end: get the nwkSKey of the application ###
    device_INFO = search_key(device_data, "id") # search the 'id' key, for the device information
    device_ID = search_key(device_INFO, "id") # search the sub-key 'id' for the device ID
    for index, value in enumerate(device_ID):
        dev_ids.append(value)
    ### Put all the respective key information into these keys ###
    sub_data = [
        {
            "Device Type": device,
            "AppSKey": app,
            "NwkSKey": net,
            "Device ID": dev_id
        }
    for device, app, net, dev_id in zip(devices, apps, nets, dev_ids) # assemble them together
    ]
    appData.append(sub_data)
### Assign the Main keys with the sub data of the devices ###
for key, value in zip(dev_names, appData):
        if key in data:
            data[key].append(value)
        else:
            data[key] = value
hex = []
for key, value in data.items():
    for sub_key, sub_value in enumerate(value):
        app_id = sub_value.get("Device ID")
        if app_id != None:
            device_specs = get_sensor_info(app_id)
            while True:
                try:
                    rawPayload = search_key(device_specs, "rawPayload") # search for the key 'rawPayload' and retun their value
                    break
                except:
                    pass
            del sub_value["Device ID"] # delete this as it's no longer usefull
            sub_value["Raw Payloads"] = rawPayload # replace it with this
        # load the values of these keys to varables
        app_key = sub_value.get("AppSKey")
        net_key = sub_value.get("NwkSKey")
        payload = sub_value.get("Raw Payloads")
        decripted_items = []
        try:
            for index, item in enumerate(payload):
                try:
                    output = run_extern_program(f"lora-packet-decode --nwkkey {net_key} --appkey {app_key} --base64 {item}") # This will take the raw payloads and conver them into an encrypted hexedecimal format
                    print(f"Colleting item: {index}\r\033[A") # This is just to display the ammount of items that are coolected during this process
                    #hex.append(output)
                    try:
                        modified_text = re.findall(r'[0-9-A-F]+', output[15]) # This just makes sure that the output only contains these items and nothing else that may get in the way of the decoer
                        #fport = re.findall(r'[0-9-A-F]+', output[13])
                        #hex.append(output[13])
                        ### ###
                        search_item = "FPort"
                        for index, item in enumerate(hex):
                            if search_item in item:
                                print(f"Found '{search_item}' at index {index}")
                                print("Matching line:", item)
                                hex.append(item)
                                break
                            else:
                                print(f"'{search_item}' not found in the list")
                                break
                        ### ###
                        #hex.append(output)
                        pairs = [modified_text[0][i:i+2] for i in range(0, len(modified_text[0]), 2)] # split the lines of hex into pairs
                        converted_item = ', '.join([f"0X{pair}" for pair in pairs]) # include a '0X' at the front of each pair
                        decripted_items.append(converted_item) # add them to a sub-liat that will be used in the main Dictionary
                    except:
                        pass
                except:
                    pass
        except:
            pass
        # delete these items as they no longer serve any purpose
        del sub_value["AppSKey"]
        del sub_value["NwkSKey"]
        del sub_value["Raw Payloads"]
        try: # include the first item from the decoded items as the rest will return the same output
            sub_value["Decrypted Information"] = decripted_items[0]
        except:
            pass
print(data)
for key, value in data.items():
    merged_sub_dicts = []
    for index, item in enumerate(value):
        try:
            ### This is where any of the fifteen devices are decoded, if there is a device modle that is not recognized by this code, it will be sent to the passthrough system (nothing actually decodes here) ###
            if item['Device Type'] == "KIWI" or item['Device Type'] == "CLOVER":
                out = search_and_decrypt(item['Decrypted Information'], 'kiwi-clover-v2.0-decoder.js')
                out = json.loads(out)
                merge = {**item, **out}
                merged_sub_dicts.append(merge)
            elif item['Device Type'] == "AURA" or item['Device Type'] == "FLUX":
                out = search_and_decrypt(item['Decrypted Information'], 'aura-flux-decoder.js')
                out = json.loads(out)
                merge = {**item, **out}
                merged_sub_dicts.append(merge)
            elif item['Device Type'] == "BREEZE" or item['Device Type'] == "BREEZE-V":
                out = search_and_decrypt(item['Decrypted Information'], 'breeze-v1.0-decoder.js')
                out = json.loads(out)
                merge = {**item, **out}
                merged_sub_dicts.append(merge)
            elif item['Device Type'] == "COMFORT" or item['Device Type'] == "VIVID":
                out = search_and_decrypt(item['Decrypted Information'], 'comfort-vivid-v2.2-decoder.js')
                out = json.loads(out)
                merge = {**item, **out}
                merged_sub_dicts.append(merge)
            elif item['Device Type'] == "SEAL" or item['Device Type'] == "SEAL Ex":
                out = search_and_decrypt(item['Decrypted Information'], 'seal-v0.8-decoder.js')
                out = json.loads(out)
                merge = {**item, **out}
                merged_sub_dicts.append(merge)
            elif item['Device Type'] == "SPARROW" or item['Device Type'] == "PELICAN": # this is the right script, and the infromation looks right, but I don't understand why there are errors that are present
                out = search_and_decrypt(item['Decrypted Information'], 'sparrow-pelican-v2.8-decoder.js')
                out = json.loads(out)
                merge = {**item, **out}
                merged_sub_dicts.append(merge)
            elif item['Device Type'] == "TUNDRA":
                out = search_and_decrypt(item['Decrypted Information'], 'tundra-v2.1-decoder.js')
                out = json.loads(out)
                merge = {**item, **out}
                merged_sub_dicts.append(merge)
            elif item['Device Type'] == "ORCA":
                out = search_and_decrypt(item['Decrypted Information'], 'orca-v0.14-decoder.js')
                out = json.loads(out)
                merge = {**item, **out}
                merged_sub_dicts.append(merge)
            elif item['Device Type'] == "eDoctor":
                out = search_and_decrypt(item['Decrypted Information'], 'edoctor-v0.15-decoder.js')
                out = json.loads(out)
                merge = {**item, **out}
                merged_sub_dicts.append(merge)
            else:
                out = search_and_decrypt(item['Decrypted Information'], 'passthrough.js')
                out = json.loads(out)
                merge = {**item, **out}
                merged_sub_dicts.append(merge)
        except:
            pass
    data[key] = merged_sub_dicts
# Collect all unique keys from the merged sub-dictionaries
all_keys = set()
for sub_dicts in data.values():
    for sub_dict in sub_dicts:
        all_keys.update(sub_dict.keys())
# Create a list of rows to be written to the CSV
rows = []
for main_key, sub_dicts in data.items():
    for sub_dict in sub_dicts:
        row = [main_key] + [sub_dict.get(key, '') for key in all_keys]
        rows.append(row)
# Convert to DataFrame
df = pd.DataFrame(rows, columns=['Application'] + list(all_keys))
# Convert to CSV
csv_file = 'merged_data.csv'
df.to_csv(csv_file, index=False)
print(data)
print(f'Data written to {csv_file}')
print(hex)
### ###
#search_item = "fport"
#for index, item in enumerate(hex):
#    if search_item in item:
#        print(f"Found '{search_item}' at index {index}")
#        print("Matching line:", item)
#        hex.append(item)
#        break
#    else:
#        print(f"'{search_item}' not found in the list")
#        break
### ###
sys.stdout.write("\033[?25h")
sys.stdout.flush()