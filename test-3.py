import json
import fileinput
import os
import subprocess
import re
import pandas as pd
def serch_and_decript(data, js_app):
    check_file = os.stat(js_app).st_size
    #print(data)
    while True:
        if check_file != 0:
            #search_line = "	var bytes = convertToUint8Array([]);"
            #replacement_line = f"	var bytes = convertToUint8Array([{data}]);"
            search_line = " var bytes = convertToUint8Array([]);"
            replacement_line = f"   var bytes = convertToUint8Array([{data}]);"
            with fileinput.FileInput(js_app, inplace=True, backup='.bak') as file:
                for line in file:
                    if search_line in line:
                        line = replacement_line + '\n'
                    print(line, end='')
                    #return line
            result = subprocess.run(f'node {js_app}', capture_output = True, text = True, shell = True, cwd = None)
            result = result.stdout.strip().split('\n')
            json_dict = {}
            key = None
            for item in result:
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
            result = json.dumps(json_dict, indent=2)
            result = result.replace('\n', '')
            #result = '[' + result + ']'
            return result
        else:
            break
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
data = {'sensor-test': [{'Device Type': 'KIWI', 'Decripted Information': '0X05, 0X04, 0X00, 0X34, 0X06, 0X04, 0X00, 0X37, 0X09, 0X65, 0X01, 0X0B, 0X0D, 0X73, 0X23, 0X16'}], 'Fcount Test': [{'Device Type': 'Industrial Sensor', 'Decripted Information': '0X00, 0XFF, 0X01, 0X6D'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0X20, 0XC7, 0XD7, 0XFC'}], 'LeapX Cold Room': [], 'Neptune Tundra RMA': [{'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X00, 0XB3, 0X04, 0X68, 0X7D, 0X00, 0XD3, 0X63, 0X00, 0XBD, 0X0E, 0X11'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X01, 0X11, 0X04, 0X68, 0X89'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X01, 0X1B, 0X04, 0X68, 0X7C'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0XBA, 0X4A, 0X00, 0X9E, 0XC6, 0X79, 0X53'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0XFE, 0X28, 0XF8, 0XE7, 0XCA, 0XCF, 0X16, 0X6D, 0XF0, 0X74, 0XCE, 0XF6, 0X9B, 0XC0, 0XD4, 0XE7, 0XC0, 0X43'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X04, 0X3E, 0X03, 0X67, 0X00, 0XEE, 0X04, 0X68, 0X2D'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X01, 0X39, 0X04, 0X68, 0X68, 0X00, 0XD3, 0X60, 0X00, 0XBD, 0X07, 0X12'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X00, 0XA8, 0X04, 0X68, 0XC3, 0X0B, 0X67, 0X00, 0XB4, 0X00, 0XD3, 0X62, 0X00, 0XBD, 0X05, 0X14'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X00, 0XE3, 0X04, 0X68, 0X56'}, {'Device Type': 'TUNDRA'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0XA8, 0X5C, 0XEA, 0X56, 0X83, 0X4E, 0X0E, 0X61, 0X6E, 0X53, 0X82, 0XEC, 0XEF, 0XD0, 0X1B, 0X32, 0X91, 0XE9'}, {'Device Type': 'Industrial Sensor'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0X32, 0X8E, 0XE3, 0XB0, 0XB7, 0XAF, 0XDA, 0X11, 0XD2, 0X24, 0X04, 0X18, 0X7B, 0X3F, 0XC9, 0X91, 0XB3, 0X4E'}], 'Pelican test': [{'Device Type': 'PELICAN', 'Decripted Information': '0X0A, 0X70, 0XFF, 0XDB, 0XE6, 0X4F, 0X0B, 0XD5, 0X4C, 0XB1, 0X2B, 0XBD, 0X71, 0X98, 0XC9, 0X08, 0XA8, 0XAE, 0X35, 0X1E, 0XF7, 0XBE, 0X63, 0X7A, 0X81, 0X70, 0X53, 0XC2, 0XB6, 0X76, 0X65, 0XD2, 0X29, 0XF2, 0XEE, 0XB0, 0X74, 0X21, 0X24, 0XA9, 0XD9, 0X7B, 0XB0, 0X64, 0X7F, 0XDA, 0X01, 0X81, 0XD5, 0XAB, 0X64, 0X7F, 0XDA, 0X01, 0X82, 0X65, 0XAA'}], 'NA Tests': [{'Device Type': 'TUNDRA', 'Decripted Information': '0XE7, 0XF1, 0X01, 0X45, 0XF1, 0X66, 0XF0, 0X88, 0X60, 0X8D, 0X83, 0XAD, 0X13, 0XC8'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X00, 0XD5, 0X04, 0X68, 0X53, 0X00, 0XD3, 0X63, 0X00, 0XBD, 0X08, 0X1D'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0XF6, 0X9A, 0X0F, 0XD1, 0XAD, 0X1D, 0X61, 0X37, 0X67, 0XE9, 0XF3, 0XF2, 0X7C, 0X2C'}, {'Device Type': 'PELICAN', 'Decripted Information': '0X00, 0XD3, 0X61, 0X00, 0XBD, 0X01, 0XD4, 0X00, 0X67, 0X01, 0X0E'}, {'Device Type': 'PELICAN', 'Decripted Information': '0X3A, 0X96, 0X37, 0X55, 0X50, 0X0E, 0X31'}, {'Device Type': 'PELICAN', 'Decripted Information': '0XC0, 0X7A, 0X81, 0XAF, 0X59, 0XA6, 0XD6, 0X8A, 0XDA, 0X6B, 0XD8'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X0B, 0X44, 0X03, 0X67, 0X00, 0XD8, 0X04, 0X68, 0X4F'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X00, 0XD8, 0X04, 0X68, 0X53, 0X00, 0XD3, 0X62, 0X00, 0XBD, 0X06, 0X04'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0XEE, 0X46, 0X1E, 0X5D, 0X63, 0XF4, 0X4B, 0XCF, 0X76, 0X3D, 0X0A, 0XC5, 0XF7, 0XD3'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X01, 0X02, 0X04, 0X68, 0X37, 0X00, 0XD3, 0X60, 0X00, 0XBD, 0X04, 0X43'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X00, 0XD5, 0X04, 0X68, 0X52'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0XFE, 0XCF, 0XD2, 0X39, 0X30, 0XF1, 0XF2, 0XBA, 0XEB, 0X93, 0X16, 0X17, 0XCA, 0X92'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X35, 0X31, 0X55, 0X61'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X2F, 0XF7, 0X79, 0XC8, 0X0E, 0X2D, 0X5B'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X00, 0XB8, 0X04, 0X68, 0XAD, 0X00, 0XD3, 0X63, 0X00, 0XBD, 0X07, 0X8E'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X00, 0X9F, 0X04, 0X68, 0XC4'}, {'Device Type': 'COMFORT', 'Decripted Information': '0X03, 0X67, 0X00, 0XD5, 0X04, 0X68, 0X5C, 0X00, 0XFF, 0X01, 0X16'}, {'Device Type': 'ORCA', 'Decripted Information': '0X00, 0X88, 0X3E, 0X67, 0X14, 0XBC, 0X06, 0X97, 0X38, 0X08, 0X66'}], 'EU Tests': [{'Device Type': 'PELICAN', 'Decripted Information': '0X0A, 0X56, 0XD5, 0XB4, 0XC4, 0X0B, 0X8F, 0XBC, 0X5D, 0X00, 0XB0, 0X99, 0X3C, 0X2C, 0XB4, 0X1D, 0XC8, 0X7C, 0X23, 0XDE, 0X01, 0XB3, 0X51, 0X97, 0X3D, 0X6C, 0XDF, 0X9B, 0XB0, 0XD0, 0X2E, 0XAB, 0X8F, 0X98, 0X49, 0XAF, 0XD0, 0X2E, 0XAB, 0X8F, 0X94, 0XC3, 0XAE, 0XCA, 0X84, 0X0F, 0XF3, 0XE6, 0X67, 0XAD, 0X62, 0X1D, 0XC6, 0X0A, 0X37, 0XBC, 0XAB'}, {'Device Type': 'Home Sensor', 'Decripted Information': '0XD0, 0X28, 0X55, 0X24, 0XF5, 0XDA, 0X44'}], 'Comfort Leak Tests': [{'Device Type': 'COMFORT', 'Decripted Information': '0X03, 0X67, 0X00, 0XD7, 0X04, 0X68, 0X56, 0X00, 0XBA, 0X0B, 0XCA'}, {'Device Type': 'COMFORT', 'Decripted Information': '0X01, 0X00, 0XFF, 0X08, 0X04, 0X00, 0X01'}], 'Gecko Tests': [{'Device Type': 'COMFORT', 'Decripted Information': '0X03, 0X67, 0X00, 0XD4, 0X04, 0X68, 0X59, 0X00, 0XFF, 0X01, 0X2A'}, {'Device Type': 'COMFORT', 'Decripted Information': '0X03, 0X67, 0X00, 0XD7, 0X04, 0X68, 0X19, 0X00, 0XBA, 0X0B, 0X9C'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X30, 0X4C, 0XC5, 0XFC, 0XDF, 0XBF, 0X76, 0X47, 0X8D, 0XDC, 0X21, 0XE1, 0X7C, 0X7E, 0XD1'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0X7B, 0X7F, 0XB2, 0X03, 0X1E, 0X02, 0XB3'}], 'Tundra Reset Test': [{'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X00, 0XDC, 0X04, 0X68, 0X44'}], 'Ken Tundra': []}
for key, value in data.items():
    for index, item in enumerate(value):
        try:
            if item['Device Type'] == "KIWI" or item['Device Type'] == "CLOVER":
                #print(key,'\b:',item['Device Type'],'\b:')
                out = serch_and_decript(item['Decripted Information'], 'kiwi-clover-v2.0-decoder.js')
                print(out)
                out = json.loads(out)
                data = data[key][0]
                #item['Device informaiton'] = out
                #del item['Decripted Information']

            #elif item['Device Type'] == "AURA" or item['Device Type'] == "FLUX":
            #    pass
            #elif item['Device Type'] == "BREEZE" or item['Device Type'] == "BREEZE-V":
            #    pass
            #elif item['Device Type'] == "COMFORT" or item['Device Type'] == "VIVID":
            #    #print(key,'\b:',item['Device Type'],'\b:')
            #    out = serch_and_decript(item['Decripted Information'], 'comfort-vivid-v2.2-decoder.js')            
            #    del item['Decripted Information']
            #    item['device_informaiton'] = out
            #elif item['Device Type'] == "SEAL" or item['Device Type'] == "SEAL Ex":
            #    pass
            #elif item['Device Type'] == "SPARROW" or item['Device Type'] == "PELICAN":
            #    #print(key,'\b:',item['Device Type'],'\b:')
            #    out = serch_and_decript(item['Decripted Information'], 'sparrow-pelican-v2.8-decoder.js')
            #    del item['Decripted Information']
            #    item['device_informaiton'] = out
            #elif item['Device Type'] == "TUNDRA":
            #    #print(key,'\b:',item['Device Type'],'\b:')
            #    out = serch_and_decript(item['Decripted Information'], 'tundra-v2.1-decoder.js')
            #    del item['Decripted Information']
            #    item['device_informaiton'] = out
            #elif item['Device Type'] == "ORCA":
            #    #print(key,'\b:',item['Device Type'],'\b:')
            #    out = serch_and_decript(item['Decripted Information'], 'node orca-v0.14-decoder.js')
            #    del item['Decripted Information']
            #    item['device_informaiton'] = out
            #elif item['Device Type'] == "eDoctor":
            #    pass
            else:
                hex_values = item['Decripted Information'].split(", ")
                result_string = "".join([value[2:] for value in hex_values])
                print(key,'\b:',item['Device Type'],'\b:',result_string)
        except:
            pass
print(data)
flat_list = []
#for main_key, main_value in data.items():
#    for sub_dict in main_value:
#        flat_dict = {"main": main_key}
#        flat_dict.update(sub_dict)
#        flat_list.append(flat_dict)
#
## Convert the list of flattened dictionaries to a DataFrame
#df = pd.DataFrame(flat_list)
#
## Convert DataFrame to CSV
#df.to_csv("new.csv", index=False)
for main_key, main_value in data.items():
    for sub_dict in main_value:
        flat_dict = {"main": main_key}
        flat_dict.update(sub_dict)
        flat_list.append(flat_dict)

# Convert the list of flattened dictionaries to a DataFrame
df = pd.DataFrame(flat_list)

# Create individual CSV files based on the "main" key
for main_key in data.keys():
    subset_df = df[df["main"] == main_key]
    subset_df.to_csv(f"{main_key}.csv", index=False)