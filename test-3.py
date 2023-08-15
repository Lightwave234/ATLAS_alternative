import json
import fileinput
import os
def serch_and_decript(data, js_app):
    check_file = os.stat(js_app).st_size
    print(data)
    while True:
        if check_file != 0:
            search_line = "	var bytes = convertToUint8Array([]);"
            replacement_line = f"	var bytes = convertToUint8Array([{data}]);"
            with fileinput.FileInput(js_app, inplace=True, backup='.bak') as file:
                for line in file:
                    if search_line in line:
                        line = replacement_line + '\n'
                    print(line, end='')
                    #return line
            os.system(f"node {js_app}")
            break
        else:
            pass
# Data to be written
data = {'sensor-test': [{'Device Type': 'KIWI', 'Decripted Information': '0X05, 0X04, 0X00, 0X34, 0X06, 0X04, 0X00, 0X37, 0X09, 0X65, 0X02, 0XF2, 0X0D, 0X73, 0X22, 0XE2'}], 'Fcount Test': [{'Device Type': 'Industrial Sensor', 'Decripted Information': '0X00, 0XFF, 0X01, 0X6D'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0X20, 0XC7, 0XD7, 0XFC'}], 'LeapX Cold Room': [], 'Neptune Tundra RMA': [{'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X00, 0XB3, 0X04, 0X68, 0X7D, 0X00, 0XD3, 0X63, 0X00, 0XBD, 0X0E, 0X11'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X01, 0X11, 0X04, 0X68, 0X89'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X01, 0X1B, 0X04, 0X68, 0X7C'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0XBA, 0X4A, 0X00, 0X9E, 0XC6, 0X79, 0X53'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0XFE, 0X28, 0XF8, 0XE7, 0XCA, 0XCF, 0X16, 0X6D, 0XF0, 0X74, 0XCE, 0XF6, 0X9B, 0XC0, 0XD4, 0XE7, 0XC0, 0X43'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X04, 0X3E, 0X03, 0X67, 0X00, 0XEE, 0X04, 0X68, 0X2D'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X01, 0X39, 0X04, 0X68, 0X68, 0X00, 0XD3, 0X60, 0X00, 0XBD, 0X07, 0X12'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X00, 0XA8, 0X04, 0X68, 0XC3, 0X0B, 0X67, 0X00, 0XB4, 0X00, 0XD3, 0X62, 0X00, 0XBD, 0X05, 0X14'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X00, 0XE3, 0X04, 0X68, 0X56'}, {'Device Type': 'TUNDRA'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0XA8, 0X5C, 0XEA, 0X56, 0X83, 0X4E, 0X0E, 0X61, 0X6E, 0X53, 0X82, 0XEC, 0XEF, 0XD0, 0X1B, 0X32, 0X91, 0XE9'}, {'Device Type': 'Industrial Sensor'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0X32, 0X8E, 0XE3, 0XB0, 0XB7, 0XAF, 0XDA, 0X11, 0XD2, 0X24, 0X04, 0X18, 0X7B, 0X3F, 0XC9, 0X91, 0XB3, 0X4E'}], 'Pelican test': [{'Device Type': 'PELICAN', 'Decripted Information': '0X0A, 0X44, 0XAF, 0X44, 0XFA, 0X0D, 0XB8, 0XCB, 0X16, 0X11, 0X04, 0X7F, 0X31, 0X59, 0XC1, 0X56, 0X74, 0X71, 0X30, 0XCC, 0X86, 0XBF, 0X76, 0X53, 0XFB, 0XF2, 0XE6, 0XE8, 0XB8, 0X6E, 0X22, 0X25, 0X04, 0XD5, 0XB4, 0XB2, 0X36, 0XF0, 0X3E, 0X26, 0XA5, 0XFD, 0XB0, 0X33, 0X2D, 0X94, 0X49, 0X05, 0X06, 0XAF, 0X4F, 0XF0, 0XC6, 0X9A, 0X62, 0XFC, 0XAF'}], 'NA Tests': [{'Device Type': 'Industrial Sensor', 'Decripted Information': '0XE7, 0XF1, 0X01, 0X45, 0XF1, 0X66, 0XF0, 0X88, 0X60, 0X8D, 0X83, 0XAD, 0X13, 0XC8'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0X03, 0X67, 0X00, 0XD5, 0X04, 0X68, 0X53, 0X00, 0XD3, 0X63, 0X00, 0XBD, 0X08, 0X1D'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0XF6, 0X9A, 0X0F, 0XD1, 0XAD, 0X1D, 0X61, 0X37, 0X67, 0XE9, 0XF3, 0XF2, 0X7C, 0X2C'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0X00, 0XD3, 0X61, 0X00, 0XBD, 0X01, 0XD4, 0X00, 0X67, 0X01, 0X0E'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0XF8, 0XEE, 0X84, 0XD5, 0XE4, 0X44, 0XA5, 0X34, 0X3B, 0X90, 0X4D, 0X22, 0X6C, 0XFC, 0X6B, 0X4F, 0X2A, 0XC6, 0X15, 0XE3, 0XCD, 0X77, 0XFD, 0XB8, 0X24, 0XCE, 0X63, 0X81, 0X89, 0X95, 0X66, 0X17, 0XD3, 0XAD, 0XB6, 0X4B, 0X9F, 0X01, 0X25, 0XC0, 0X26, 0XA9, 0X6E, 0X9F, 0XE6, 0X8C, 0XE1, 0X6D, 0X4C, 0X9A, 0XEB, 0X49, 0XFF, 0X80, 0X32, 0X2E, 0X3A'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0X5A, 0XDC, 0XF2, 0X29, 0X77, 0X68, 0XCC, 0X53, 0X23, 0X06, 0X12'}, {'Device Type': 'Home Sensor', 'Decripted Information': '0X0B, 0X44, 0X03, 0X67, 0X00, 0XD8, 0X04, 0X68, 0X4F'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0X03, 0X67, 0X00, 0XE5, 0X04, 0X68, 0X53, 0X00, 0XD3, 0X62, 0X00, 0XBD, 0X06, 0X9C'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0XEE, 0X46, 0X1E, 0X5D, 0X63, 0XF4, 0X4B, 0XCF, 0X76, 0X3D, 0X0A, 0XC5, 0XF7, 0XD3'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0X03, 0X67, 0X01, 0X02, 0X04, 0X68, 0X37, 0X00, 0XD3, 0X60, 0X00, 0XBD, 0X04, 0X43'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0X03, 0X67, 0X00, 0XD5, 0X04, 0X68, 0X52'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0XFE, 0XCF, 0XD2, 0X39, 0X30, 0XF1, 0XF2, 0XBA, 0XEB, 0X93, 0X16, 0X17, 0XCA, 0X92'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0X35, 0X31, 0X55, 0X61'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0X1F, 0X83, 0XE8, 0X0D, 0X82, 0XBA, 0XFA'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0X03, 0X67, 0X00, 0XB8, 0X04, 0X68, 0XAD, 0X00, 0XD3, 0X63, 0X00, 0XBD, 0X07, 0X8E'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0X03, 0X67, 0X00, 0X9F, 0X04, 0X68, 0XC4'}, {'Device Type': 'Home Sensor', 'Decripted Information': '0X03, 0X67, 0X00, 0XDA, 0X04, 0X68, 0X60, 0X00, 0XFF, 0X01, 0X16'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0X00, 0X88, 0X3E, 0X67, 0X14, 0XBC, 0X06, 0X97, 0X38, 0X08, 0X66'}], 'EU Tests': [{'Device Type': 'PELICAN', 'Decripted Information': '0X0A, 0X0A, 0X6B, 0XCD, 0X37, 0XEF, 0XA2, 0XB4, 0X63, 0X27, 0XC0, 0XD9, 0X83, 0X57, 0XB4, 0X47, 0X2A, 0X77, 0XE2, 0X30, 0XF7, 0XB3, 0XD0, 0X2E, 0XAB, 0X8F, 0X98, 0X49, 0XB0, 0X4A, 0X8F, 0XA7, 0XBC, 0X65, 0X49, 0XAE, 0X5A, 0XB2, 0X0E, 0X5D, 0XB8, 0X01, 0XAC, 0X6D, 0X65, 0X98, 0XB6, 0XC6, 0X48, 0XAB, 0XD0, 0X2E, 0XAB, 0X8F, 0X9B, 0XB5, 0XAB'}, {'Device Type': 'Home Sensor', 'Decripted Information': '0XD0, 0X28, 0X55, 0X24, 0XF5, 0XDA, 0X44'}], 'Comfort Leak Tests': [{'Device Type': 'COMFORT', 'Decripted Information': '0X03, 0X67, 0X00, 0XF6, 0X04, 0X68, 0X4B, 0X00, 0XBA, 0X0B, 0XBE'}, {'Device Type': 'COMFORT', 'Decripted Information': '0X01, 0X00, 0XFF, 0X08, 0X04, 0X00, 0X01'}], 'Gecko Tests': [{'Device Type': 'COMFORT', 'Decripted Information': '0X03, 0X67, 0X00, 0XD9, 0X04, 0X68, 0X5E, 0X00, 0XFF, 0X01, 0X2A'}, {'Device Type': 'COMFORT', 'Decripted Information': '0X03, 0X67, 0X00, 0XD7, 0X04, 0X68, 0X19, 0X00, 0XBA, 0X0B, 0X9C'}, {'Device Type': 'TUNDRA', 'Decripted Information': '0X30, 0X4C, 0XC5, 0XFC, 0XDF, 0XBF, 0X76, 0X47, 0X8D, 0XDC, 0X21, 0XE1, 0X7C, 0X7E, 0XD1'}, {'Device Type': 'Industrial Sensor', 'Decripted Information': '0X7B, 0X7F, 0XB2, 0X03, 0X1E, 0X02, 0XB3'}], 'Tundra Reset Test': [{'Device Type': 'TUNDRA', 'Decripted Information': '0X03, 0X67, 0X00, 0XDC, 0X04, 0X68, 0X44'}], 'Ken Tundra': []}
for key, value in data.items():
    #print(value)
    for index, item in enumerate(value):
        try:
            #print(item['Device Type'],'\b:',item['Decripted Information'])
            if item['Device Type'] == "KIWI" or item['Device Type'] == "CLOVER":
                serch_and_decript(item['Decripted Information'], 'kiwi-clover-v2.0-decoder.js')
            elif item['Device Type'] == "AURA" or item['Device Type'] == "FLUX":
                print(item['Decripted Information'])
            elif item['Device Type'] == "BREEZE" or item['Device Type'] == "BREEZE-V":
                print(item['Decripted Information'])
            elif item['Device Type'] == "COMFORT" or item['Device Type'] == "VIVID":
                print(item['Decripted Information'])
            elif item['Device Type'] == "SEAL" or item['Device Type'] == "SEAL Ex":
                print(item['Decripted Information'])
            elif item['Device Type'] == "SPARROW" or item['Device Type'] == "PELICAN":
                print(item['Decripted Information'])
            elif item['Device Type'] == "TUNDRA":
                serch_and_decript(item['Decripted Information'], 'tundra-v2.1-decoder.js')
            elif item['Device Type'] == "ORCA":
                print(item['Decripted Information'])
            elif item['Device Type'] == "eDoctor":
                print(item['Decripted Information'])
            else:
                pass
        except:
            pass