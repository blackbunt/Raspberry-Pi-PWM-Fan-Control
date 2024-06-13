Install

    sudo cp pifancontrol.service /lib/systemd/system/pifancontrol.service
    sudo cp fan_control.py /usr/local/sbin/
    sudo chmod 644 /lib/systemd/system/pifancontrol.service
    sudo chmod +x /usr/local/sbin/fan_control.py
    sudo systemctl daemon-reload
    sudo systemctl enable pifancontrol.service
    sudo systemctl start pifancontrol.service

Check status

    sudo service pifancontrol status
      

Remove / Uninstall

    sudo systemctl stop pifancontrol.service
    sudo systemctl disable pifancontrol.service
    sudo systemctl daemon-reload
    sudo rm /usr/local/sbin/fan_control.py
    sudo rm /lib/systemd/system/pifancontrol.service
