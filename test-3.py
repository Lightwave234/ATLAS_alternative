import json
import fileinput
import os
import subprocess
import re
import pandas as pd
import csv
def search_and_decrypt(data, js_app):
    check_file = os.stat(js_app).st_size

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
                #print(result)
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
                            try:
                                json_dict[key] = json.loads(value)
                            except:
                                json_dict[key] = value.strip(',')
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
data = {'sensor-test': [{'Device Type': 'KIWI', 'Decripted Information': '0X05, 0X04, 0X00, 0X34, 0X06, 0X04, 0X00, 0X37, 0X09, 0X65, 0X01, 0X6E, 0X0D, 0X73, 0X22, 0X91'}], 'Fcount Test': [{'Device Type': 'Industrial Sensor', 'Decripted Information': '0X00, 0XFF, 0X01, 0X6D'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0X20, 0XC7, 0XD7, 0XFC'}], 'LeapX Cold Room': [], 'Neptune Tundra RMA': [{'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X00, 0XB3, 0X04, 0X68, 0X7D, 0X00, 0XD3, 0X63, 0X00, 0XBD, 0X0E, 0X11'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X01, 0X11, 0X04, 0X68, 0X89'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X01, 0X1B, 0X04, 0X68, 0X7C'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0XBA, 0X4A, 0X00, 0X9E, 0XC6, 0X79, 0X53'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0XFE, 0X28, 0XF8, 0XE7, 0XCA, 0XCF, 0X16, 0X6D, 0XF0, 0X74, 0XCE, 0XF6, 0X9B, 0XC0, 0XD4, 0XE7, 0XC0, 0X43'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X04, 0X3E, 0X03, 0X67, 0X00, 0XEE, 0X04, 0X68, 0X2D'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X01, 0X39, 0X04, 0X68, 0X68, 0X00, 0XD3, 0X60, 0X00, 0XBD, 0X07, 0X12'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X00, 0XA8, 0X04, 0X68, 0XC3, 0X0B, 0X67, 0X00, 0XB4, 0X00, 0XD3, 0X62, 0X00, 0XBD, 0X05, 0X14'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X00, 0XE3, 0X04, 0X68, 0X56'}, {'Device Type': 'TUNDRA'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0XA8, 0X5C, 0XEA, 0X56, 0X83, 0X4E, 0X0E, 0X61, 0X6E, 0X53, 0X82, 0XEC, 0XEF, 0XD0, 0X1B, 0X32, 0X91, 0XE9'}, {'Device Type': 'Industrial Sensor'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0X32, 0X8E, 0XE3, 0XB0, 0XB7, 0XAF, 0XDA, 0X11, 0XD2, 0X24, 0X04, 0X18, 0X7B, 0X3F, 0XC9, 0X91, 0XB3, 0X4E'}], 'Pelican test': [{'Device Type': 'PELICAN', 'Decripted Information': '0X0A, 0X63, 0XEB, 0X89, 0X00, 0X41, 0XCC, 0XC3, 0X6F, 0XA4, 0X52, 0X86, 0XC6, 0X76, 0XC2, 0X25, 0XF7, 0X38, 0X37, 0X98, 0XBA, 0XBC, 0X64, 0X7F, 0XDA, 0X01, 0X74, 0X6D, 0XB0, 0X32, 0X19, 0X38, 0XA4, 0X65, 0X72, 0XAF, 0X44, 0X3F, 0XAC, 0X4E, 0XC6, 0X3A, 0XAE, 0X7C, 0XA8, 0X64, 0X54, 0XE2, 0XAF, 0XAD, 0X20, 0X99, 0X5F, 0X3F, 0XA7, 0X1C, 0XAD'}], 'NA Tests': [{'Device Type': 'TUNDRA', 'Decripted Information': '0XE7, 0XF1, 0X01, 0X45, 0XF1, 0X66, 0XF0, 0X88, 0X60, 0X8D, 0X83, 0XAD, 0X13, 0XC8'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X00, 0XD5, 0X04, 0X68, 0X53, 0X00, 0XD3, 0X63, 0X00, 0XBD, 0X08, 0X1D'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0XF6, 0X9A, 0X0F, 0XD1, 0XAD, 0X1D, 0X61, 0X37, 0X67, 0XE9, 0XF3, 0XF2, 0X7C, 0X2C'}, {'Device Type': 'PELICAN', 'Decripted Information': '0X00, 0XD3, 0X61, 0X00, 0XBD, 0X01, 0XD4, 0X00, 0X67, 0X01, 0X0E'}, {'Device Type': 'PELICAN', 'Decripted Information': '0XD2, 0X0A, 0X91, 0XA3, 0XE4, 0XDF, 0X35, 0X26, 0X7F, 0X63, 0XA4, 0XBE, 0XB2, 0X27, 0XD9, 0X1D, 0XF0, 0X52, 0X11, 0XF5, 0X99, 0XD6, 0XE3, 0XB4, 0X61, 0XA7, 0XD4, 0XAE, 0X61, 0XCE, 0XF4, 0X79, 0X01, 0XCE, 0X73, 0XD9, 0X3D, 0X32, 0X09, 0XC0, 0XE6, 0X1A, 0XA5, 0XA2, 0XF0, 0X51, 0X9D, 0XE6, 0X57, 0X9D, 0X64, 0X33, 0X1A, 0X4C, 0X4D, 0X85, 0X9C'}, {'Device Type': 'PELICAN', 'Decripted Information': '0X28, 0XFE, 0XC0, 0X44, 0XDD, 0X42, 0X47, 0X4F, 0X43, 0X52, 0X29'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X0B, 0X44, 0X03, 0X67, 0X00, 0XD8, 0X04, 0X68, 0X4F'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X00, 0XDE, 0X04, 0X68, 0X4F, 0X00, 0XD3, 0X62, 0X00, 0XBD, 0X07, 0X5A'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0XEE, 0X46, 0X1E, 0X5D, 0X63, 0XF4, 0X4B, 0XCF, 0X76, 0X3D, 0X0A, 0XC5, 0XF7, 0XD3'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X01, 0X02, 0X04, 0X68, 0X37, 0X00, 0XD3, 0X60, 0X00, 0XBD, 0X04, 0X43'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X00, 0XD5, 0X04, 0X68, 0X52'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0XFE, 0XCF, 0XD2, 0X39, 0X30, 0XF1, 0XF2, 0XBA, 0XEB, 0X93, 0X16, 0X17, 0XCA, 0X92'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X35, 0X31, 0X55, 0X61'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X45, 0X04, 0XB6, 0X9A, 0X5B, 0X79, 0X09'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X00, 0XB8, 0X04, 0X68, 0XAD, 0X00, 0XD3, 0X63, 0X00, 0XBD, 0X07, 0X8E'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X00, 0X9F, 0X04, 0X68, 0XC4'}, {'Device Type': 'COMFORT', 'Decripted Information': '0X03, 0X67, 0X00, 0XDA, 0X04, 0X68, 0X57, 0X00, 0XFF, 0X01, 0X16'}, {'Device Type': 'ORCA', 'Decripted Information': '0X00, 0X88, 0X3E, 0X67, 0X14, 0XBC, 0X06, 0X97, 0X38, 0X08, 0X66'}], 'EU Tests': [{'Device Type': 'Home Sensor', 'Decripted Information': '0XD0, 0X28, 0X55, 0X24, 0XF5, 0XDA, 0X44'}], 'Comfort Leak Tests': [{'Device Type': 'COMFORT', 'Decripted Information': '0X03, 0X67, 0X00, 0XE5, 0X04, 0X68, 0X4A, 0X00, 0XBA, 0X0B, 0XC6'}, {'Device Type': 'COMFORT', 'Decripted Information': '0X01, 0X00, 0XFF, 0X08, 0X04, 0X00, 0X01'}], 'Gecko Tests': [{'Device Type': 'COMFORT', 'Decripted Information': '0X03, 0X67, 0X00, 0XD9, 0X04, 0X68, 0X55, 0X00, 0XFF, 0X01, 0X2A'}, {'Device Type': 'COMFORT', 'Decripted Information': '0X03, 0X67, 0X00, 0XD7, 0X04, 0X68, 0X19, 0X00, 0XBA, 0X0B, 0X9C'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X30, 0X4C, 0XC5, 0XFC, 0XDF, 0XBF, 0X76, 0X47, 0X8D, 0XDC, 0X21, 0XE1, 0X7C, 0X7E, 0XD1'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0X7B, 0X7F, 0XB2, 0X03, 0X1E, 0X02, 0XB3'}], 'Tundra Reset Test': [{'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X00, 0XDC, 0X04, 0X68, 0X44'}], 'Ken Tundra': []}
print(data)
#for key, value in data.items():
#    for index, item in enumerate(value):
#        if item['Device Type'] == 'PELICAN':
#            #print(key)
#            #print(key,'\b:',item['Device Type'],'\b:')
#            out = search_and_decrypt(item['Decripted Information'], 'sparrow-pelican-v2.8-decoder.js')
#            out = json.loads(out)
#            merge = {**item, **out}
#            #merged_sub_dicts.append(merge)
#            print(key, merge)
for key, value in data.items():
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
print(data)

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
df = pd.DataFrame(rows, columns=['Main Key'] + list(all_keys))

# Convert to CSV
csv_file = 'merged_data.csv'
df.to_csv(csv_file, index=False)

print(f'Data written to {csv_file}')
# Collect all unique keys from the merged sub-dictionaries
all_keys = set()
for sub_dicts in data.values():
    for sub_dict in sub_dicts:
        all_keys.update(sub_dict.keys())

# Convert to CSV
csv_file = 'merged_data.csv'
df.to_csv(csv_file, index=False)

print(f'Data written to {csv_file}')