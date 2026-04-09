# importing necessary libraries
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
import time

# list of devices to connect to
devices = [
    {"host": "192.168.1.1", "device_type": "cisco_ios", "username": "admin", "password": "cisco"},
    {"host": "192.168.1.2", "device_type": "juniper_junos", "username": "admin", "password": "juniper"},
    {"host": "127.0.0.1", "device_type": "linux", "username": "gutu", "password": "1989"},
]

# loop through each device in the list
for device in devices:
    # print the device type and host
    print(f"\nConnecting to: {device['device_type']} using {device['host']}")

    retries = 3 # number of retries to connect to the device
    for attempt in range(1, retries + 1): # loop through each attempt
        try: # try to connect to the device
            print(f"Attempt {attempt}...") # print the attempt number

            conn = ConnectHandler(**device, timeout=5) # connect to the device
            # select the command to send to the device based on the device type
            if device["device_type"] == "linux":
                command = "uname -a"
            elif device["device_type"] == "cisco_ios":
                command = "show ip interface brief" # show the IP interface brief
            else:
                command = "show interfaces terse" # show the interfaces terse

            output = conn.send_command(command) # send the command to the device
            print(output) # print the output of the command

            conn.disconnect() # disconnect from the device
            break  # success → exit retry loop
        except NetmikoTimeoutException:
            print(f"❌ Timeout on attempt {attempt}") # print the timeout error

        except NetmikoAuthenticationException:
            print(f"❌ Auth failed → no point retrying")
            break  # stop retrying if credentials are wrong

        except Exception as e:
            print(f"❌ Other error: {e}") # print a generic error
        time.sleep(2)  # wait before retry
    else:
        print(f"🚨 Failed to connect to {device['host']} after {retries} attempts") # print the failure to connect to the device
