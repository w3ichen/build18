# Build18 2025
Carnegie Mellon University's [build18](https://www.build18.org) 2025 hackathon.

## Underwater drone

## The Team
Team name: Robotron
- Ben Lee
- David Seong
- John Min
- Sidney Nimako
- Weichen Qiu

---

## Setting up systemctl
Using systemctl to start up launch program on reboot

Create and write to service file:
```bash
sudo vim /etc/systemd/system/build18.service
```
```bash
[Unit]
Description=build18 launch
After=network.target

[Service]
ExecStart=/home/pi/build18/launch.py
WorkingDirectory=/home/pi/build18
StandardOutput=inherit
StandardError=inherit
Restart=no
User=root
Group=root

[Install]
WantedBy=multi-user.target
```

Enable and start the service
```bash
sudo systemctl daemon-reload
sudo systemctl enable build18.service
sudo systemctl start build18.service
sudo systemctl status build18.service

# Get logs 
sudo journalctl -u build18.service -f -n 50
# Restart
sudo systemctl restart build18.service
```

## Connecting to Pi
- To connect to the pi, run:
    `ssh pi@172.26.40.246`. PWD: `pi`
- Make sure venv is activated (if not already): 
```
source ~/build18/venv/bin/activate
```
- Install python dependencies:
```bash
pip install -r requirements.txt
# OR
pip install -r requirements.txt --break-system-packages

```

## ROS2
- ROS2 pre-compiled for Raspberry PI on Jazzy:
```bash
wget https://s3.ap-northeast-1.wasabisys.com/download-raw/dpkg/ros2-desktop/debian/bookworm/ros-jazzy-desktop-0.3.2_20240525_arm64.deb
sudo apt install ./ros-jazzy-desktop-0.3.2_20240525_arm64.deb
```

## Opening VNC GUI Display
0. In VSCode, port forward, 6080
~~1. Visit vnc://172.26.40.246:5901~~
1. Visit http://localhost:6080/vnc.html
2. Enter password: `pipipi`
3. Click "Connect"
4. Run `rviz2` in the terminal

```bash
# systemctl services
# Check status
sudo systemctl status tigervnc.service
sudo systemctl status novnc.service
# Restart services
sudo systemctl daemon-reload
sudo systemctl restart tigervnc.service
sudo systemctl restart novnc.service
# Stop services
sudo systemctl stop tigervnc.service
sudo systemctl stop novnc.service
# Disable services
sudo systemctl disable tigervnc.service
sudo systemctl disable novnc.service
# Check logs
journalctl -u tigervnc.service
journalctl -u novnc.service

# Change files
sudo nano /etc/systemd/system/tigervnc.service
sudo nano /etc/systemd/system/novnc.service
```

## Opening rviz2 on PC
Set env vars:
```bash
export ROS_DOMAIN_ID=42
export ROS_AUTOMATIC_DISCOVERY_RANGE=LARGE_SUBNET
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export ROS_NETWORK_INTERFACE=wlan0
# Set to PI address
export ROS_MASTER_URI=http://172.26.40.246:11311

# Set the IP address of your PC
# On linux:
export ROS_HOSTNAME=$(hostname)
# On mac:
export ROS_HOSTNAME=$(ipconfig getifaddr en0)


# On mac, get your ip address:
ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}'

# Start rviz
ros2 run rviz2 rviz2
```

## I2C
To check I2C connections: `sudo i2cdetect -y 1`