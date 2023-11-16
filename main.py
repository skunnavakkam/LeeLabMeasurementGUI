import rich
import os
import re
import visa
import datetime
import sys
import tqdm
from API.smu2450 import API as smuAPI


# helpers
def format_voltage_input(input_str: str) -> float:
    regex = "^[.?\d]+"
    match = float(re.findall(regex, input_str)[0])

    regex2 = "[a-z]+"
    match2 = re.findall(regex2, input_str.lower())[0]

    ret = match * {"v": 1, "mv": 1e-3, "uv": 1e-6, "nv": 1e-9}[match2]
    return ret

def format_current_input(input_str: str) -> float:
    regex = "^[.?\d]+"
    match = float(re.findall(regex, input_str)[0])

    regex2 = "[a-z]+"
    match2 = re.findall(regex2, input_str.lower())[0]

    ret = match * {"a": 1, "ma": 1e-3, "ua": 1e-6, "na": 1e-9}[match2]
    return ret
    

def format_voltage_output(voltage: float) -> str:
    return voltage

def format_current_output(current: float) -> str:
    return current


# Keithely Functions



if __name__ == "__main__":
    print(
'''
#######################
# BASIC DOCUMENTATION #
#######################

This is a basic sweeper for the keithley SMU 2450 and our spectrum analyzer. 
Requirements:
    - Matplotlib
    - visa
For entering voltage/amplitude, using '15ma' or '15ua' or '15nv'.
Spaces/Casing are ignored. Decimals are ok. Only milli, micro, and nano are supported. 
I haven't implemented any safety yet. Don't screw up :)
Press enter to continue. '''
    )
    input()
    while True:
        min_voltage = format_voltage_input(input("Enter min voltage: "))
        max_voltage = format_voltage_input(input("Enter max voltage: "))
        number_of_steps = int(input("Enter number of steps: "))
        current_limit = format_current_input(input("Enter current limit: "))
        
        for i in range(5): 
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
        print(
f'''
These are the settings you've entered.
Min voltage: {format_voltage_output(min_voltage)}
Max voltage: {format_voltage_output(max_voltage)}
Number of steps: {number_of_steps}
Current limit: {format_current_output(current_limit)}''')
        if input("Do you wish to continue? [Y/n]: ").strip().lower() in ("y", ""):
            break
        else: 
            for i in range(6): 
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
    
    print("")
    print("Connecting to devices")
    # SMU2450
    smu = smuAPI()
    if smu.discover_and_connect() is False:
        print("Keithely Sourcemeter 2450 is not connect. Killing run")
        raise Exception("No Keithely found")
    smu.set_current_limit_mA(current_limit*1e3)
    smu.set_source_voltage()


    print("")
    print("Starting Sweep...")
    dir_string = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # os.mkdir(dir_string)
    print(f"Saving in directory {dir_string}")

    vrange = max_voltage - min_voltage
    voltage_list = []
    current_list = []
    for step in tqdm(range(number_of_steps)):
        curr_voltage = min_voltage + (vrange / number_of_steps)
        voltage_list.append(curr_voltage)
        smu.set_voltage(curr_voltage)


    

    

        