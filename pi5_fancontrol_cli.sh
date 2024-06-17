#!/bin/bash

SERVICE_NAME_CONTROL="pi5fancontrol"
SERVICE_FILE_CONTROL="/lib/systemd/system/${SERVICE_NAME_CONTROL}.service"
SCRIPT_FILE_CONTROL="/usr/local/sbin/fan_control5.py"

SERVICE_NAME_TACHO="pi5fantacho"
SERVICE_FILE_TACHO="/lib/systemd/system/${SERVICE_NAME_TACHO}.service"
SCRIPT_FILE_TACHO="/usr/local/sbin/read_fan_speed5.py"

install_service() {
    echo "Installing $SERVICE_NAME_CONTROL service..."
    sudo cp pi5fancontrol.service $SERVICE_FILE_CONTROL
    sudo cp fan_control5.py $SCRIPT_FILE_CONTROL
    sudo chmod 644 $SERVICE_FILE_CONTROL
    sudo chmod +x $SCRIPT_FILE_CONTROL
    sudo systemctl daemon-reload
    sudo systemctl enable $SERVICE_NAME_CONTROL
    sudo systemctl start $SERVICE_NAME_CONTROL
    echo "$SERVICE_NAME_CONTROL service installed and started."

    echo "Installing $SERVICE_NAME_TACHO service..."
    sudo cp pi5fantacho.service $SERVICE_FILE_TACHO
    sudo cp read_fan_speed5.py $SCRIPT_FILE_TACHO
    sudo chmod 644 $SERVICE_FILE_TACHO
    sudo chmod +x $SCRIPT_FILE_TACHO
    sudo systemctl daemon-reload
    sudo systemctl enable $SERVICE_NAME_TACHO
    sudo systemctl start $SERVICE_NAME_TACHO
    echo "$SERVICE_NAME_TACHO service installed and started."
}

check_status() {
    echo "Checking status of $SERVICE_NAME_CONTROL service..."
    sudo systemctl status $SERVICE_NAME_CONTROL
    echo "Checking status of $SERVICE_NAME_TACHO service..."
    sudo systemctl status $SERVICE_NAME_TACHO
}

remove_service() {
    echo "Removing $SERVICE_NAME_CONTROL service..."
    sudo systemctl stop $SERVICE_NAME_CONTROL
    sudo systemctl disable $SERVICE_NAME_CONTROL
    sudo systemctl daemon-reload
    sudo rm $SCRIPT_FILE_CONTROL
    sudo rm $SERVICE_FILE_CONTROL
    echo "$SERVICE_NAME_CONTROL service removed."

    echo "Removing $SERVICE_NAME_TACHO service..."
    sudo systemctl stop $SERVICE_NAME_TACHO
    sudo systemctl disable $SERVICE_NAME_TACHO
    sudo systemctl daemon-reload
    sudo rm $SCRIPT_FILE_TACHO
    sudo rm $SERVICE_FILE_TACHO
    echo "$SERVICE_NAME_TACHO service removed."
}

show_tacho() {
    ./read_rpm_from_service.py
}

print_help() {
    echo "Usage: $0 {install|status|remove|rpm}"
    echo "install  - Install and start the $SERVICE_NAME_CONTROL &  $SERVICE_NAME_TACHO service"
    echo "status   - Check the status of the $SERVICE_NAME_CONTROL & $SERVICE_NAME_TACHO service"
    echo "remove   - Stop and remove the $SERVICE_NAME_CONTROL & $SERVICE_NAME_TACHO service"
    echo "rpm    - Shows the current fanspeed"
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
    rpm)
        show_tacho
        ;;
    *)
        print_help
        ;;
esac
