# 🎮 Minecraft Player Tracking Overlay

A real-time Minecraft overlay that tracks player statistics and provides automated alerts in-game.

## 📥 Installation

### Prerequisites
- Python
- Minecraft Client

### Setup
1. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Minecraft log path:**
   - Locate your Minecraft client's `latest.log` file
   - Update the `log_path` variable on **line 258** in `main.py`

3. **Launch the application:**
   ```bash
   python main.py
   ```

## 🚀 Getting Started

### Essential First Step
To avoid global chat spam, create a party before starting:
```minecraft
/p invite [username]
```
*You can invite any player (online or offline) to access party chat with no delay.*

### Basic Usage
1. Start Minecraft client
2. Run the Python program
3. Type `-help` in chat to view all available commands

---

## 🎯 Features & Commands

### 📊 Player Statistics Tracking

#### **FKDR Tracking**
Track players with high monthly FKDR ratios:
```minecraft
-toggle fkdr [number]
```
**Example:** `-toggle fkdr 5.0` flags players with FKDR above 5.0

#### **Level Tracking**
Monitor high-level players:
```minecraft
-toggle lvl [number]
```
**Example:** `-toggle lvl 200` flags players above level 200

#### **Nick Tracking**
Automatically detects nicked players (enabled by default):
```minecraft
-toggle nick
```

### 🎮 How to Activate Tracking
After entering commands:
1. Open chat and press `Spacebar` once
2. Press `Tab` to populate server player list
3. The overlay will automatically scan and track players

---

## 📸 Examples

### Initial Setup
<img width="415" height="57" alt="Party Setup" src="https://github.com/user-attachments/assets/05e8baf2-9485-48ca-856d-08b8bddecc79" />

### Program Startup
<img width="626" height="38" alt="Initial Message" src="https://github.com/user-attachments/assets/d652161b-229e-443d-9b50-ed133105a3a6" />

### Help Command
<img width="647" height="168" alt="Help Menu" src="https://github.com/user-attachments/assets/149ee5b2-7308-4d4f-b5ec-75f9e1b34844" />

### FKDR Tracking in Action
<img width="644" height="164" alt="FKDR Tracking" src="https://github.com/user-attachments/assets/0d4a45bd-33ec-4e1d-ad09-d85e22da3a99" />

---

## ⚡ Quick Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `-help` | Show all commands & current settings | `-help` |
| `-toggle fkdr [num]` | Track players with FKDR above value | `-toggle fkdr 3.5` |
| `-toggle lvl [num]` | Track players above level | `-toggle lvl 150` |
| `-toggle nick` | Toggle nick detection | `-toggle nick` |

---

## 💡 Pro Tips
- Always use party chat to avoid chat delays
- The overlay works best when you can tab-complete player names

**Type `-help` in-game to see your current configuration and all available options!**
