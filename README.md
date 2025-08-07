#  Smart Posture Corrector Wearable Device

A wearable solution that monitors posture in real-time and helps users maintain a healthy posture by providing haptic feedback and posture tracking via Telegram.

---

##  Overview

Poor posture can lead to chronic pain, muscle strain, and long-term health issues. This device aims to solve that by:

- Detecting bad posture using motion sensors.
- Alerting the user via vibration if bad posture is maintained.
- Tracking and scoring posture over time.
- Providing posture score and visual reports via Telegram.

---

##  Objectives

- Real-time posture monitoring using sensors.
- Vibration alerts for bad posture held beyond 10 seconds.
- Dynamic posture score tracking.
- Telegram interface for user interaction:
  - `/status` to get current posture score.
  - `/graph` to get a visual graph of posture scores.

---

##  Hardware Components

| Component        | Purpose                          |
|------------------|----------------------------------|
| Raspberry Pi 4B  | Main processing unit             |
| MPU6050          | Posture tracking (gyro + accel)  |
| Touch Sensor     | System ON/OFF toggle             |
| Vibration Motor  | Haptic feedback for bad posture  |
| Power Supply     | Power the system                 |

---

##  Software & Tools

- Python
- [MPU6050 Library](https://github.com/Tijndagamer/mpu6050)
- NumPy, Matplotlib (for plotting)
- [Telebot API (pyTelegramBotAPI)](https://github.com/eternnoir/pyTelegramBotAPI)

---

##  System Architecture

1. **Posture Detection**  
   MPU6050 reads accelerometer and gyroscope data.

2. **Bad Posture Alert**  
   If bad posture persists for over 10s, the vibration motor is triggered for 5s.

3. **Posture Score Calculation**  
   - Starts at 100.
   - Reduces with prolonged bad posture.
   - Includes small fluctuations for realism.

4. **Telegram Bot**  
   - `/status`: Sends current posture score.
   - `/graph`: Sends a graph image of score history.
   - Sends real-time alerts and system status.

---

##  How It Works

1. User toggles system ON/OFF using a touch sensor.
2. MPU6050 continuously reads posture data.
3. On detecting poor posture:
   - A timer starts.
   - If sustained beyond 10 seconds, user is vibrated.
   - Score decreases accordingly.
4. Telegram bot sends alerts and handles user commands.
5. User can request posture score or score graph at any time.

---

##  Results

- Accurate detection of bad posture.
- Instant vibration alert improves awareness.
- Smooth and responsive Telegram bot interface.
- Realistic, time-based posture scoring.

---

##  Challenges

- Defining accurate posture thresholds.
- Maintaining stable, realistic scoring.
- Ensuring lag-free Telegram communication.

---

##  Future Improvements

-  Develop a mobile app UI.
-  Integrate machine learning for smarter posture classification.
-  Battery optimization.
- ☁ Add cloud-based storage and analytics.

---

##  References

- [MPU6050 Datasheet](https://invensense.tdk.com/products/motion-tracking/6-axis/mpu-6050/)
- [Raspberry Pi Pinout](https://pinout.xyz/)
- [Telegram Bot API Docs](https://core.telegram.org/bots/api)
- [pyTelegramBotAPI GitHub](https://github.com/eternnoir/pyTelegramBotAPI)
- [Matplotlib Docs](https://matplotlib.org/stable/contents.html)
- [NumPy Docs](https://numpy.org/)

---

##  Project Status

✅ Fully functional prototype  
📈 Real-time posture tracking and scoring  
📬 Telegram integration complete

---

Feel free to contribute or suggest improvements!
