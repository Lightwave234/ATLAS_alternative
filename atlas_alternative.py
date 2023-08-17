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
            print(f"\r\033[A<UPDATE> server connection faliture.\nERROR: [{response_token.status_code}]\n", "Retrying...")
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
            #timeout = 15
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
            #timeout += 5
            #print("\r\033[A<UPDATE> can't acess device, retrying...")
            pass
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
def search_and_decrypt(data, js_app):
    check_file = stat(js_app).st_size

    while True:
        if check_file != 0:
            search_line = " var bytes = convertToUint8Array([]);"
            replacement_line = f"   var bytes = convertToUint8Array([{data}]);"
            
            with fileinput.FileInput(js_app, inplace=True, backup='.bak') as file:
                for line in file:
                    if search_line in line:
                        line = replacement_line + '\n'
                    print(line, end='')

            result = subprocess.run(f'node {js_app}', capture_output=True, text=True, shell=True, cwd=None)
            try:
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
                for item in result_stdout:
                    if item == '{':
                        continue
                    elif item == '}':
                        break
                    elif ':' in item:
                        #key, value = item.split(':')
                        #json_dict[key.strip()] = value.strip(',')

                        key, value = item.split(':')
                        key = key.strip()
                        if value.strip().startswith('['):
                            # Handling array values
                            json_dict[key] = json.loads(value)
                        else:
                            json_dict[key] = value.strip(',')

                    else:
                        value = item.strip(',')
                        #json_dict[key] += ' ' + value if key is not None else value
                        if key is not None:
                            # Concatenate non-string values
                            json_dict[key] += ' ' + value
                new_result = json.dumps(json_dict, indent=2)
                new_result = new_result.replace('\n', '')
                return new_result
        else:
            break
    #print(item)
    #fileName = "kiwi-clover-v2.0-decoder.js"
    #line_number_to_mod = 4
    #new_line_content = f"    var bytes = convertToUint8Array([{item}]);"
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
    ##system('node kiwi-clover-v2.0-decoder.js')
    #output = run_extern_program('node kiwi-clover-v2.0-decoder.js')
    #json_string = ''.join(output)
    ##json_object = json.loads(json_string)
    ##print(f"{key}:", json_object)
    ##print(f"{key}:", output)
    ##print(type(output))
    #print(json_string)
#if item.startswith("0X05"):
#    print(f"{key}:", output)
### Main code ###
#if __name__ == "__main__":
#def main():
#print("\u001b[2J\u001b[H")
sys.stdout.write("\u001b[2J\u001b[H\033[?25l")
sys.stdout.flush()
header("Tektelic NS Shell Interface")
#start_spinner("Fetching apps...")
apps = get_active_applications() # get all the avalable apps
#stop_spinner()
application_INFO = search_key(apps, "id") # sort out every key that starts with 'id'
application_NAME = search_key(apps, "name")
application_ID = search_key(application_INFO, "id") # sort every sub-key that stars with key
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
    #start_spinner("Searching for application...")
    device_data = get_device_from_app_ID(id, "data") # search under the data key
    #stop_spinner()
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
    sub_data = [
        {
            "Device Type": device,
            "AppSKey": app,
            "NwkSKey": net,
            "Device ID": dev_id
        }
    for device, app, net, dev_id in zip(devices, apps, nets, dev_ids)
    ]
    #print(sub_data)
    appData.append(sub_data)
for key, value in zip(dev_names, appData):
        if key in data:
            data[key].append(value)
        else:
            data[key] = value
#print(data)
for key, value in data.items():
    for sub_key, sub_value in enumerate(value):
        app_id = sub_value.get("Device ID")
        if app_id != None:
            device_specs = get_sensor_info(app_id)
            while True:
                try:
                    rawPayload = search_key(device_specs, "rawPayload")
                    break
                except:
                    pass
            del sub_value["Device ID"]
            sub_value["Raw Payloads"] = rawPayload
        app_key = sub_value.get("AppSKey")
        net_key = sub_value.get("NwkSKey")
        payload = sub_value.get("Raw Payloads")
        decripted_items = []
        try:
            for index, item in enumerate(payload):
                try:
                    output = run_extern_program(f"lora-packet-decode --nwkkey {net_key} --appkey {app_key} --base64 {item}")
                    print(f"Colleting item: {index}\r\033[A")
                    try:
                        modified_text = re.findall(r'[0-9-A-F]+', output[15])
                        pairs = [modified_text[0][i:i+2] for i in range(0, len(modified_text[0]), 2)]
                        converted_item = ', '.join([f"0X{pair}" for pair in pairs])
                        decripted_items.append(converted_item)
                    except:
                        pass
                except:
                    pass
        except:
            pass
        del sub_value["AppSKey"]
        del sub_value["NwkSKey"]
        del sub_value["Raw Payloads"]
        try:
            sub_value["Decripted Information"] = decripted_items[0]
        except:
            pass
#print(data)
for key, value in data.items():
    print(key)
    merged_sub_dicts = []
    for index, item in enumerate(value):
    #for item in value:
        try:
            if item['Device Type'] == "KIWI" or item['Device Type'] == "CLOVER":
                out = search_and_decrypt(item['Decripted Information'], 'kiwi-clover-v2.0-decoder.js')
                out = json.loads(out)
                merge = {**item, **out}
                merged_sub_dicts.append(merge)
                print(key, merge)
            elif item['Device Type'] == "AURA" or item['Device Type'] == "FLUX":
                out = search_and_decrypt(item['Decripted Information'], 'aura-flux-decoder.js')
                out = json.loads(out)
                merge = {**item, **out}
                merged_sub_dicts.append(merge)
                print(key, merge)
            elif item['Device Type'] == "BREEZE" or item['Device Type'] == "BREEZE-V":
                out = search_and_decrypt(item['Decripted Information'], 'breeze-v1.0-decoder.js')
                out = json.loads(out)
                merge = {**item, **out}
                merged_sub_dicts.append(merge)
                print(key, merge)
            elif item['Device Type'] == "COMFORT" or item['Device Type'] == "VIVID":
                out = search_and_decrypt(item['Decripted Information'], 'comfort-vivid-v2.2-decoder.js')
                out = json.loads(out)
                merge = {**item, **out}
                merged_sub_dicts.append(merge)
                print(key, merge)
            elif item['Device Type'] == "SEAL" or item['Device Type'] == "SEAL Ex":
                out = search_and_decrypt(item['Decripted Information'], 'seal-v0.8-decoder.js')
                out = json.loads(out)
                merge = {**item, **out}
                merged_sub_dicts.append(merge)
                print(key, merge)
            elif item['Device Type'] == "SPARROW" or item['Device Type'] == "PELICAN":
                print(key)
                #print(key,'\b:',item['Device Type'],'\b:')
                out = search_and_decrypt(item['Decripted Information'], 'sparrow-pelican-v2.8-decoder.js')
                out = json.loads(out)
                merge = {**item, **out}
                merged_sub_dicts.append(merge)
                print(key, merge)
            elif item['Device Type'] == "TUNDRA":
                #print(key,'\b:',item['Device Type'],'\b:')
                out = search_and_decrypt(item['Decripted Information'], 'tundra-v2.1-decoder.js')
                out = json.loads(out)
                merge = {**item, **out}
                merged_sub_dicts.append(merge)
                print(key, merge)
            elif item['Device Type'] == "ORCA":
                #print(key,'\b:',item['Device Type'],'\b:')
                out = search_and_decrypt(item['Decripted Information'], 'orca-v0.14-decoder.js')
                out = json.loads(out)
                merge = {**item, **out}
                merged_sub_dicts.append(merge)
                print(key, merge)
            elif item['Device Type'] == "eDoctor":
                out = search_and_decrypt(item['Decripted Information'], 'edoctor-v0.15-decoder.js')
                out = json.loads(out)
                merge = {**item, **out}
                merged_sub_dicts.append(merge)
                print(key, merge)
            else:
                out = search_and_decrypt(item['Decripted Information'], 'passthrough.js')
                out = json.loads(out)
                merge = {**item, **out}
                merged_sub_dicts.append(merge)
                print(key, merge)
        except:
            pass
    #print(merged_sub_dicts)
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

print(f'Data written to {csv_file}')
sys.stdout.write("\033[?25h")
sys.stdout.flush()