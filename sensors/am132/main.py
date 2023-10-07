import time
import board
import digitalio

led = digitalio.DigitalInOut(board.GP13)
led.direction = digitalio.Direction.OUTPUT
buzzer = digitalio.DigitalInOut(board.GP15)
buzzer.direction = digitalio.Direction.OUTPUT
pir = digitalio.DigitalInOut(board.GP28)
pir.direction = digitalio.Direction.INPUT

motion_detected = False

while True:
    if pir.value and not motion_detected:
        print("ALARM! Motion detected!")
        motion_detected = True
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
