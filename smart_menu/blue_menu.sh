#!/bin/bash

# while-menu-dialog: A menu-driven system information program

DIALOG_CANCEL=1
DIALOG_ESC=255
HEIGHT=0        # Let dialog calculate the height
WIDTH=0         # Let dialog calculate the width
MENU_HEIGHT=0   # Let dialog calculate the menu height
CURRENT_WORKSPACE='/mnt/c/Users/EG/march/fresh_electron'
LATEST_SOURCE='/mnt/c/Users/EG/electron-vue-example'

# Function to display results (currently unused)
display_result() {
  dialog --title "$1" \
    --no-collapse \
    --msgbox "$result" 0 0
}

# Infinite loop to display the menu until the user exits
while true; do
  # Capture the user's selection using 'dialog'
  exec 3>&1
  selection=$(dialog \
    --backtitle "Main Directory Menu" \
    --title "Menu" \
    --clear \
    --cancel-label "Exit" \
    --menu "Please select:" $HEIGHT $WIDTH $MENU_HEIGHT \
    "0" "Exit this menu" \
    "p" "Open Pickleball Dashboard" \
    "1" "Clean all but users" \
    "f" "Open Flash Menu (includes matrix project with fonts)" \
    "2" "Edit this menu" \
    "j" "VSCode projects" \
    "k" "MCBA System Dashboard" \
    "a" "Clean all but admin" \
    "c" "Clean keep users and conversations" \
    "m" "Start monitor" \
    2>&1 1>&3)
  exit_status=$?
  exec 3>&-

  # Handle exit conditions from 'dialog'
  case $exit_status in
    $DIALOG_CANCEL)
      clear
      echo "Program terminated."
      exit
      ;;
    $DIALOG_ESC)
      clear
      echo "Program aborted." >&2
      exit 1
      ;;
  esac

  # Exit if selection is empty (prevents infinite loop)
  if [ -z "$selection" ]; then
    clear
    echo "No selection made. Exiting."
    exit
  fi

  # Process the user's selection
  case $selection in
    0)
      clear
      echo "Exiting the menu. Goodbye!"
      break
      ;;
    1)
      echo "Cleaning all but users..."
      cd /mnt/c/Users/EG/Desktop/2022/july/1st_week/vite-vue-electron/src/typescript_source/concrete/commands/delete_html_logs/
      ./clean_but_keep_users.sh
      cd - >/dev/null
      ;;
    f)
      echo "Opening flash menu..."
      cd /home/adamsl/linuxBash
      ./flash_menu.sh
      ;;
    2)
      echo "Editing the menu in VSCode..."
      cd /home/adamsl/linuxBash
      code .
      cd - >/dev/null
      ;;
    j)
      echo "Opening VSCode projects..."
      cd /home/adamsl/linuxBash
      ./vscode_projects.sh
      ;;
    k)
      echo "Starting MCBA System Dashboard..."
      cd /home/adamsl/linuxBash
      python3 mcba_system_dashboard.py
      ;;
    a)
      echo "Cleaning all but admin..."
      cd /home/adamsl/linuxBash
      ./clean_all_but_admin.sh
      ;;
    c)
      echo "Cleaning and keeping users and conversations..."
      cd /home/adamsl/linuxBash
      ./clean_keep_users_conversatons.sh
      ;;
    m)
      echo "Starting monitor..."
      # Add the command to start monitor here
      ;;
    p)
      echo "Starting Pickleball Dashboard..."
      cd /home/adamsl/linuxBash/pickle_ball
      python3 pickleball_dashboard.py
      ;;
    *)
      echo "Invalid selection. Please try again."
      ;;
  esac
done
