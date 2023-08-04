import fileinput
from os import *
def replace_line(file_path, search_line, replacement_line):
    with fileinput.FileInput(file_path, inplace=True, backup='.bak') as file:
        for line in file:
            if search_line in line:
                line = replacement_line + '\n'
            print(line, end='')

# Usage
hex_string = '0X05, 0X04, 0X00, 0X34, 0X06, 0X04, 0X00, 0X36, 0X09, 0X65, 0X01, 0X86, 0X0D, 0X73, 0X23, 0X41'#'0X03, 0X67, 0X01, 0X36, 0X04, 0X68, 0X69, 0X00, 0XD3, 0X60, 0X00, 0XBD, 0X05, 0X1C'
file_path = 'comfort-vivid-v2.2-decoder.js'
search_line = '	var bytes = convertToUint8Array(input.bytes);'
replacement_line = f'	var bytes = convertToUint8Array([{hex_string}]);'

replace_line(file_path, search_line, replacement_line)
system(f'node {file_path}')