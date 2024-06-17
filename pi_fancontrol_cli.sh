#!/bin/bash

SERVICE_NAME="pifancontrol"
SERVICE_FILE="/lib/systemd/system/${SERVICE_NAME}.service"
SCRIPT_FILE="/usr/local/sbin/fan_control.py"

install_service() {
    echo "Installing $SERVICE_NAME service..."
    sudo cp pifancontrol.service $SERVICE_FILE
    sudo cp fan_control.py $SCRIPT_FILE
    sudo chmod 644 $SERVICE_FILE
    sudo chmod +x $SCRIPT_FILE
    sudo systemctl daemon-reload
    sudo systemctl enable $SERVICE_NAME
    sudo systemctl start $SERVICE_NAME
    echo "$SERVICE_NAME service installed and started."
}

check_status() {
    echo "Checking status of $SERVICE_NAME service..."
    sudo systemctl status $SERVICE_NAME
}

remove_service() {
    echo "Removing $SERVICE_NAME service..."
    sudo systemctl stop $SERVICE_NAME
    sudo systemctl disable $SERVICE_NAME
    sudo systemctl daemon-reload
    sudo rm $SCRIPT_FILE
    sudo rm $SERVICE_FILE
    echo "$SERVICE_NAME service removed."
}

print_help() {
    echo "Usage: $0 {install|status|remove}"
    echo "install  - Install and start the $SERVICE_NAME service"
    echo "status   - Check the status of the $SERVICE_NAME service"
    echo "remove   - Stop and remove the $SERVICE_NAME service"
}

case "$1" in
    install)
        install_service
        ;;
    status)
        check_status
        ;;
    remove)
        remove_service
        ;;
    *)
        print_help
        ;;
esac
