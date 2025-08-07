import time
import threading
import RPi.GPIO as GPIO
from mpu6050 import mpu6050
import telebot
import matplotlib.pyplot as plt
import numpy as np

# Telegram Bot Token (Replace with your actual bot token)
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"
bot = telebot.TeleBot(BOT_TOKEN)

# Define GPIO Pins
TOUCH_SENSOR_PIN = 17
MOTOR_PIN = 18

# Posture reference ranges
POSTURE_RANGES = {
    "accel_x": (-2.46, 2.53),
    "accel_y": (-2.32, 2.24),
    "accel_z": (-2.83, 10.94),
    "gyro_x": (-10.48, 10.45),
    "gyro_y": (-10.24, 10.97),
    "gyro_z": (-10.18, 10.86),
}

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TOUCH_SENSOR_PIN, GPIO.IN)
GPIO.setup(MOTOR_PIN, GPIO.OUT)
GPIO.output(MOTOR_PIN, GPIO.LOW)

# Initialize MPU6050
sensor = mpu6050(0x68)

# System variables
system_on = False
bad_posture_start = None
BAD_POSTURE_DURATION = 10  # 10 sec to trigger vibration
VIBRATION_DURATION = 5  # Vibrate for 5 sec
POSTURE_CHECK_INTERVAL = 1  # Every second
posture_score = 100.00
bad_posture_time = 0
history = []  # Store posture history
start_time = None  # Track system uptime

def is_bad_posture(accel, gyro):
    """Check if posture is out of allowed range."""
    for axis, (min_val, max_val) in POSTURE_RANGES.items():
        sensor_val = accel[axis[-1]] if "accel" in axis else gyro[axis[-1]]
        if not (min_val <= sensor_val <= max_val):
            return True
    return False

@bot.message_handler(commands=['status'])
def send_status(message):
    bot.send_message(message.chat.id, f"Posture Score: {posture_score:.2f}/100")

@bot.message_handler(commands=['graph'])
def send_graph(message):
    if not history:
        bot.send_message(message.chat.id, "No posture data available yet.")
        return

    timestamps = np.arange(len(history))
    plt.figure()
    plt.plot(timestamps, history, label='Posture Score', color='b')
    plt.xlabel("Time")
    plt.ylabel("Score")
    plt.title("Posture Score Over Time")
    plt.legend()
    plt.savefig("posture_graph.png")
    plt.close()
    bot.send_photo(message.chat.id, open("posture_graph.png", "rb"))

# Start Telegram Bot in a separate thread
def run_bot():
    bot.polling(non_stop=True)

bot_thread = threading.Thread(target=run_bot, daemon=True)
bot_thread.start()

try:
    while True:
        if GPIO.input(TOUCH_SENSOR_PIN) == GPIO.HIGH:
            system_on = not system_on  # Toggle system ON/OFF
            if system_on:
                start_time = time.time()  # Start uptime tracking
                bot.send_message(CHAT_ID, "🔵 System is now ON. Monitoring posture...")
            else:
                if start_time:
                    uptime = time.time() - start_time
                    bot.send_message(CHAT_ID, f"🔴 System is OFF. Worked for {uptime:.2f} seconds.")
                start_time = None  # Reset uptime tracking
            print(f"System {'ON' if system_on else 'OFF'}")
            time.sleep(0.5)

        if system_on:
            accel_data = sensor.get_accel_data()
            gyro_data = sensor.get_gyro_data()

            if is_bad_posture(accel_data, gyro_data):
                if bad_posture_start is None:
                    bad_posture_start = time.time()
                elif time.time() - bad_posture_start >= BAD_POSTURE_DURATION:
                    print("Bad posture detected! Vibrating...")
                    GPIO.output(MOTOR_PIN, GPIO.HIGH)
                    time.sleep(VIBRATION_DURATION)
                    GPIO.output(MOTOR_PIN, GPIO.LOW)
                    bad_posture_time += BAD_POSTURE_DURATION
                    posture_score = max(0, round(100 - (bad_posture_time / 300 * 100), 2))  # Normalize to 5 min scale
                    bot.send_message(CHAT_ID, f"⚠️ Bad posture detected! Your score: {posture_score:.2f}/100")
                    bad_posture_start = None
            else:
                # Make the posture score slightly volatile
                posture_score = min(100, max(0, posture_score + round(np.random.uniform(-1.5, 1.5), 2)))
                bad_posture_start = None

            history.append(posture_score)

        time.sleep(POSTURE_CHECK_INTERVAL)

except KeyboardInterrupt:
    if system_on and start_time:
        uptime = time.time() - start_time
        bot.send_message(CHAT_ID, f"🔴 System is OFF. Worked for {uptime:.2f} seconds.")
    print("Exiting...")
    GPIO.cleanup()
