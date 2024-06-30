#!/bin/bash
# Hole das Verzeichnis des aktuellen Skripts
#sleep 3
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
sudo ./pi5_fancontrol_cli.sh remove
sudo ./pi5_fancontrol_cli.sh install