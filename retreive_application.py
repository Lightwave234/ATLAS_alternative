#from requests import status_codes
from requests import *                  # use requests libbrary
from requests.auth import HTTPBasicAuth # use authinicate 
#from nsapi.nsapi import NetworkServer
#from nsapi import NetworkServer
import requests                         # pull the requests library
import getpass                          # libbrary not found in pip, possibly either pre-installed, 
import time
### my modules ###
from sys import *
from time import *
from json import *
from os import *
### end my modules ###
NSADDRESS = 'https://lorawan-ns-na.tektelic.com/api/'   # hardcode the api location URL
NSADDRESS_SPLIT = NSADDRESS.split("/")[2]               # use this to pull out the 'lorawan-ns-na.tektelic.com'
'''
username= input("Enter username: ")
passwd= getpass.getpass("Enter password: ")
application_name_list= input("Enter the Application name: ")
'''
# get the user personal information in order to authenticate acess to the site
USER_NAME = input() # user account or email (hardcoded for developers)
USER_PASSWORD = input() # user password (hardcoded for developers)


def login_to_server(): # test to see if a connection to the server has been successfully established
    response_token = requests.post(f"{NSADDRESS}auth/login", json = {'username': USER_NAME, 'password': USER_PASSWORD}) # this will send a post request to the specified URL after initalizing it. Dcitionary 'json' sould store the user's name and password.
    if response_token.status_code == 200:                                        # this will check if the response token is 200. If the response is 200, the connection is stable 
        print(f"[Analyzer] Successfully login to the server: {NSADDRESS_SPLIT}") # this will prompt the user with a sucess status when entering 'lorawan-ns-na.tektelic.com'
        token = response_token.json()['token']                                   # get the authintication token
        #print(token)
        return token
    else: # if a connection cannot be established for any reason, prompt the user with the server ststue (Ex: 401, 404, 500)
        print(f"Could not establish a connection, HTTP Status Code: {response_token.status_code}, Retrying")
token = login_to_server()   # set the function to 'token' varable
print(token)                # print to screen if there is a sucess or failure

headers = { # creat arguments to use when inializing the request script
  'Content-type' : 'application/json', # calls the content type
  'X-Authorization': f'Bearer {token}' # calls the X-Authorization useing the aquired token
  }

def applications(): # get the avalable applications that can be used in the API
    response_applications = requests.get(f"{NSADDRESS}customer/applications", headers = headers, timeout = 1) # access the site and use the arguments set in the 'headers' dictionary. After that, get the reasource
    #response_applications = requests.get(f"{NSADDRESS}customers/devices", headers = headers, timeout = 1)
    try:
        print(f"[Analyzer] Succesfully got applications list from {NSADDRESS_SPLIT}".format(NSADDRESS_SPLIT)) # if this was a successful connection, let the user know so
        applications_list = response_applications.json()                                                      # append all the applications to a list from json format, and then return it to the main function
        return applications_list
    except:                                                                                                   # However, if there is no sucess, let the user know what status code there is  
        print(f"[Analyzer] Could not retrieve the applications list, HTTP Status Code: {response_applications.status_code}".format(response_applications.status_code))

applications_list = applications() # store the returnd applcations from NS in a main list and then print them to the screen
print(applications_list)
### My code  ###
print("\n### My code ###\n")
### Get all the devices from specified application ID ###
def get_device_from_ID(applicationID):
    #applicationID = '23ee7bc0-1aa2-11ee-8ee2-c19b4fa5a9aa'
    response_devices = requests.get(f"{NSADDRESS}application/{applicationID}/devices", headers = headers, timeout = 1) # access the site and use the arguments set in the 'headers' dictionary. After that, get the reasource
    #response_applications = requests.get(f"{NSADDRESS}customers/devices", headers = headers, timeout = 1)
    try:
        print(f"[Analyzer] Succesfully got devices list from {NSADDRESS_SPLIT}".format(NSADDRESS_SPLIT)) # if this was a successful connection, let the user know so
        devices_list = response_devices.json()                                                           # append all the devices to a list from json format, and then return it to the main function
        return devices_list
    except:                                                                                              # However, if there is no sucess, let the user know what status code there is  
        print(f"[Analyzer] Could not retrieve the applications list, HTTP Status Code: {response_devices.status_code}".format(response_devices.status_code))
devices_list = get_device_from_ID('23ee7bc0-1aa2-11ee-8ee2-c19b4fa5a9aa')
print(devices_list)
### List all the items in a list or dictionary with sub items included ###
def get_API_list_information(listToUse):
    #ts = get_terminal_size()
    print(f"\nLength of list: {len(listToUse)} items\n")                        # prompt user with the ammount of items avalable
    #print('-' * ts.columns)                                                    # this should draw a barrier around the items
    if isinstance(listToUse, list):                                             # detect of if the list is a list object
        for item in listToUse:                                                  # scan every item in the main list
            boarder(f"Item: {listToUse.index(item) + 1}")                       # promt the user with the item number
            for key, value in item.items():                                     # check over the dictionary tiems
                if isinstance(value, dict):                                     # if the item is another dictionary, say so and display the items
                    print(f"Items in {key}: ")
                    for sub_key, sub_value in value.items():                    # this hleps to list the sub-dictionary items
                        print(f"    {sub_key}: {sub_value}")                    # use a tab to make the sub-items stand out
                elif isinstance(value, list):
                    for item in value:
                        print(item)
                else:                                                           # if the items are not dictionaries, print their values as is
                    print(f"{key}: {value}")
    elif isinstance(listToUse, dict):                                           # detect if the list is a dictornary oject
        for key, value in listToUse.items():                                    # print out the main items
            if isinstance(value, list):                                         # check if the item is a list, if it is, than print out the sub-items
                print(f"Items in: {key}")
                #print(key, ":", value[0], )
#                for sub_key, sub_value in key:
#                    print(f"Items in: {sub_key}")
#                    print(f"    {sub_key}: {sub_value}")
                for item in value:
                    if isinstance(item, list):                                  # check if sub-item is a list
                        for item in key:
                            print(item)
                    elif isinstance(item, dict):                                # check if sub-item is a dictionary
                        for sub_key, sub_value in item.items():
                            print(f"    {sub_key}: {sub_value}")
                    else:                                                       # if the item is neither one or the other, it could just be another dictionary item
                        print(key, ":", value)
            elif isinstance(value, dict):                                       # check if the item is a dictionary
                print(f"{key} is dict")
                pass
            else:
                print(key, ":", value)                                          # if the item is neither one or the other, it could just be another dictionary item
        #print(listToUse['data'])
    else:
        print("[Analyzer] No list could be found")                              # if there is no list specified, output that there is no list items
def boarder(stringInTheMiddle): # this is just a function that will create a boarder around a title or line of text
    ts = get_terminal_size()
    print(f"{'-' * ts.columns}\n{stringInTheMiddle}\n{'-' * ts.columns}")
get_API_list_information(applications_list)
get_API_list_information(devices_list)
### Newer code ###
def is_device_active(EUI):
    print(EUI)