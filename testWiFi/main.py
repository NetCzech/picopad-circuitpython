import os, time, sys, ipaddress, wifi

print("Connecting to WiFi")

try:
    # Connect to the WIFI, use settings.toml to configure SSID and Password
    wifi.radio.connect(os.getenv('WIFI_SSID'), os.getenv('WIFI_PASSWORD'))
    print("Connected to WiFi")
except Exception as e:
    # Handle connection error
    # For this example we will simply print a message and exit the program
    print("Failed to connect, adorting.")
    print("Error:\n", str(e))
    sys.exit()

# Prints your MAC (Media Access Control) address
print("MAC addr:", [hex(i) for i in wifi.radio.mac_address])

# Prints your IP address
print("IP address is", wifi.radio.ipv4_address)