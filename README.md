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
Restart=always
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
sudo journalctl -u build18.service -f
# Restart
sudo systemctl restart build18.service
```