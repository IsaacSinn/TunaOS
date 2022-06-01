import subprocess  # Used to run Putty.
import os # To check that the path of the files defined in the config file exist
import sys # Used for the menu
import time # Used for the menu delay
from infi.devicemanager import DeviceManager # Used for the retrievement of Device manager information

dm = DeviceManager()
dm.root.rescan()
devs = dm.all_devices # Get all the devices to a list called devs

speed = "0"

FileName = os.path.basename(__file__).split('.')[0]

Config_file = 'C:\\Python\\'+FileName+'\\Config.txt'  # Load config.txt to our script

# Checks if the Config file exist in the expected folder. If not, the program is terminated
if not os.path.exists(Config_file):
    print('Configuration file : ' + Config_file + ' not found')
    input('Press enter to exit the program and check the location of the Config file')
    sys.exit()

# copy all the paremetesd value of the Config file in a dictionary

array_dict = dict([('param', 'value')])
with open(Config_file, 'r') as file:
    for line in file:
        line2 = line.strip('\n')
        if '=' in line2:
            parameter = line2.split('=')[0].strip()
            value = str(line2.split('=')[1]).strip()
            array_dict[parameter] = value
file.close()

# Extract the info from the dictionary and copy to a variable to be used in the script

file_puttypath = array_dict['file_puttypath']
file_br1 = array_dict['file_br1']
file_br1_desc = array_dict['file_br1_desc']
file_br2 = array_dict['file_br2']
file_br2_desc = array_dict['file_br2_desc']
file_br3 = array_dict['file_br3']
file_br3_desc = array_dict['file_br3_desc']
file_br4 = array_dict['file_br4']
file_br4_desc = array_dict['file_br4_desc']

# Check if the user have configured the path of the putty.exe file

if not os.path.exists(file_puttypath):
    print('Configuration file : ' + file_puttypath + ' not found')
    input('Press enter to exit the program and check the location of the putty.exe file')
    sys.exit()

# Search on the device manager list if we have a match for USB Serial

for d in devs:
    if  "USB Serial Port" in d.description : # USB Serial Port have been found and the if statement is true
        str = d.__str__()
        COMport = str.split('(', 1)[1].split(')')[0] # Splitting the COM information from the string which is between the two (COMx)
        i=1
        break
    else: # If statement is false
        i=0

# Create a menu for the user to choose bautrate. The information is retrieved from the Config.txt file

def menu():
    global speed
    print("************ Select bautrate MENU **************")
    choice = input("""
            1: """ + file_br1 + """ """ + file_br1_desc + """
            2: """ + file_br2 + """ """ + file_br2_desc + """
            3: """ + file_br3 + """ """ + file_br3_desc + """
            4: """ + file_br4 + """ """ + file_br4_desc + """
            5: Quit
    Please enter your choice and press enter: """)
    if choice == "1":
        command = file_puttypath + ' -serial ' + COMport + ' -sercfg ' + file_br1 + ',8,n,1,N'
        # print (command)
        subprocess.Popen(command)  # Execute Putty with the parameters of the COM port we found.
    elif choice == "2":
        command = file_puttypath + ' -serial ' + COMport + ' -sercfg ' + file_br2 + ',8,n,1,N'
        # print (command)
        subprocess.Popen(command)  # Execute Putty with the parameters of the COM port we found.
    elif choice == "3":
        command = file_puttypath + ' -serial ' + COMport + ' -sercfg ' + file_br3 + ',8,n,1,N'
        # print (command)
        subprocess.Popen(command)  # Execute Putty with the parameters of the COM port we found.
    elif choice == "4":
        command = file_puttypath + ' -serial ' + COMport + ' -sercfg ' + file_br4 + ',8,n,1,N'
        # print (command)
        subprocess.Popen(command)  # Execute Putty with the parameters of the COM port we found.
    elif choice == "5":
        sys.exit
    else:
        print("You must only select either 1,2,3,4 or 5")
        print("Please try again")
        time.sleep(3)
        print()
        menu()

# Summarise the code and run if statements for each scenario (USB serial found, Not found, Error)

if i == 1:
    print("#########################\n"
          "####### K9-Serial #######\n"
          "#########################\n")
    print("Captain! ",d.description, "has been located on :", COMport)
    menu()
elif i ==0:
    print("#########################\n"
          "####### K9-Serial #######\n"
          "#########################\n")
    print ("USB Serial Not found \nPlease check physical connection.")
    print ()
    input("Press enter to exit")
else:
    print("#########################\n"
          "####### K9-Serial #######\n"
          "#########################\n")
    print("Error\n Dont know what went wrong. Good Luck :)")
    input("Press enter to exit")