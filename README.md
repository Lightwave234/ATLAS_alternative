# ATLAS_alternative
this is a program that localizes the process of decrypting and decodeing information from the Network Server

### Dependancies ###
Python 	v3.10.6 or later
NodeJS 	v12.22.9 or later
npm 	v8.5.1 or later
pip 	v22.0.2 or later

# python modules
requests      	   2.31.0
requests-auth      7.0.0
pandas             2.0.3
pytz               2023.3

# nodejs tools
lora-packet

### setup ###

Windows:
run either setup.cmd or setup.ps1 with

for setup.cmd:
run setup.cmd and accept installing node and python
you will then be prompeted with an install or uninstall page (I/U)
if you have everything, just hit ctrl+c to terminate the process

for setup.ps1:
you must be have administrative permissions in order to install everything
run the command ./setup.ps1 -i to install the depndancies, or use ./setup.ps1 -u to uninstall the application dependancies

Linux:
for linux, just run the setup.sh application

in the terminal, type ./setup.sh -i to install the depndancies, and ./setup.sh -u to uninstall the application depndancies

### useage of the application ###
before using this, make sure that all the devices are set to their right device modle (only for the fifteen known types)
type 'python3.10 atlas_alternative.py' into the shell and enter your credentials for the network server:
example:
username: you@tektelic.com
password: 123ABC$#
The program will then fetch all the data from the NS, and beging the decodeing process
after this is done, a CSV file with all the device information will be created
(for different decoders there are different ports, in the JS decoders, set the varable 'port' to the right value to get the right output)

### Bugs and possible errors ###
if the user's cedentials are written incorrectly, the program will immedatly crash and display a 401 error
if there is mantiance on the NS, or your internet connection is fluxuating or unstable, a 503 error may occure
there isn't an automatic way of changing the port type (10/100) so the user may need to change that manually in the diffent decoder scripts
the passthrough may need some work for devices that may not be Hardcoded in the main program.
