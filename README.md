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
    `ssh pi@172.26.40.246`
- Make sure venv is activated (if not already): 
```
source ~/build18/venv/bin/activate
```
- Install python dependencies:
```bash
pip install -r requirements.txt
```

## ROS2
- ROS2 pre-compiled for Raspberry PI on Jazzy:
```bash
wget https://s3.ap-northeast-1.wasabisys.com/download-raw/dpkg/ros2-desktop/debian/bookworm/ros-jazzy-desktop-0.3.2_20240525_arm64.deb
sudo apt install ./ros-jazzy-desktop-0.3.2_20240525_arm64.deb
```