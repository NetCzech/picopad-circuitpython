# Import CircuitPython module
import os
import wifi
import socketpool
import time
import board
import digitalio
import adafruit_requests
import ssl

# Connect to the Wi-Fi, use settings.toml to configure SSID and Password
wifi.radio.connect(os.getenv('WIFI_SSID'), os.getenv('WIFI_PASSWORD'))
pool = socketpool.SocketPool(wifi.radio)
print("Connected to Wi-Fi")
print("IP Address: {}".format(wifi.radio.ipv4_address))
requests = adafruit_requests.Session(pool, ssl.create_default_context())
telegrambot = os.getenv("botToken")

# Telegram API URL
API_URL = "https://api.telegram.org/bot" + telegrambot

# Define LED pin
led = digitalio.DigitalInOut(board.GP13)
led.direction = digitalio.Direction.OUTPUT

# Define buzzer pin
buzzer = digitalio.DigitalInOut(board.GP15)
buzzer.direction = digitalio.Direction.OUTPUT

# Define AM132 sensor pin
pir = digitalio.DigitalInOut(board.GP28)
pir.direction = digitalio.Direction.INPUT

# Telegram bot initialization on Telegram API side
def init_bot():
    get_url = API_URL
    get_url += "/getMe"
    r = requests.get(get_url)
    return r.json()['ok']

first_read = True
update_id = 0

# Read new messages from the Telegram API
def read_message():
    global first_read
    global update_id
    global chat_id
    
    get_url = API_URL + "/getUpdates?limit=1&allowed_updates=[\"message\",\"callback_query\"]"
    if not first_read:
        get_url += "&offset={}".format(update_id)

    r = requests.get(get_url)
    
    try:
        update_id = r.json()['result'][0]['update_id']
        message = r.json()['result'][0]['message']['text']
        chat_id = r.json()['result'][0]['message']['chat']['id']

        print("Chat ID: {}\tMessage: {}".format(chat_id, message))

        first_read = False
        update_id += 1
        
        return chat_id, message

    except (IndexError, KeyError) as e:
        return False, False

# Send a message
def send_message(chat_id, message):
    get_url = API_URL
    get_url += "/sendMessage?chat_id={}&text={}".format(chat_id, message)
    r = requests.get(get_url)

# Initialization Telegram bot
chat_id = None

if init_bot() == False:
    print("\nTelegram bot failed")
else:
    print("\nTelegram bot ready!\n")
    chat_id, message_in = read_message()    

# Motion detection
motion_detected = False

while True:
    if pir.value and not motion_detected:
        print("ALARM! Motion detected!")
        motion_detected = True
        send_message(chat_id, "ALARM! Motion detected!")
        for _ in range(3):
            buzzer.value = True
            time.sleep(0.2)
            buzzer.value = False
            time.sleep(0.2)

    if pir.value:
        led.value = False
        time.sleep(0.1)
        led.value = True
        time.sleep(0.1)

    else:
        motion_detected = False
        led.value = True
        time.sleep(0.5)
        led.value = False
        time.sleep(0.5)
