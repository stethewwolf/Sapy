#!/bin/bash

# inspired by https://github.com/arduino/Arduino/blob/master/build/linux/dist/install.sh

# This script adds a menu item and icons for sapy for the current
# user. If possible, it will use the xdg-utils - or fall back to just
# copying a desktop file to the user's dir.
# If called with the "-u" option, it will undo the changes.

# Get absolute path from which this script file was executed
# (Could be changed to "pwd -P" to resolve symlinks to their target)
SCRIPT_PATH=$( cd $(dirname $0) ; pwd )
cd "${SCRIPT_PATH}"

# Default mode is to install.
UNINSTALL=false

RESOURCE_NAME="eu.stethewwolf.sapy"

HICOLOR_FOLDER=${HOME}.local/share/icons/hicolor/


# Install python modules
python_install_f() {
    pip3 install -r requirements.txt
    python3 setup.py install --user
}

# Install using xdg-utils
xdg_install_f() {
  # Install the icon files using name and resolutions

  xdg-icon-resource install --novendor --context apps --size 32 "${SCRIPT_PATH}/icons/32x32/eu.stethewwolf.sapy.png" $RESOURCE_NAME
  xdg-icon-resource install --novendor --context apps --size 48 "${SCRIPT_PATH}/icons/48x48/eu.stethewwolf.sapy.png" $RESOURCE_NAME
  xdg-icon-resource install --novendor --context apps --size 128 "${SCRIPT_PATH}/icons/128x128/eu.stethewwolf.sapy.png" $RESOURCE_NAME


  # Install the created *.desktop file
  xdg-desktop-menu install --novendor "${SCRIPT_PATH}/${RESOURCE_NAME}.desktop"

  # Create icon on the desktop
  xdg-desktop-icon install --novendor "${SCRIPT_PATH}/${RESOURCE_NAME}.desktop"

  if [ x${SUDO_USER} != x ]; then
   chown ${SUDO_USER} "${XDG_DESKTOP_DIR}/${RESOURCE_NAME}.desktop"
  fi
}

# Install by simply copying desktop file (fallback)
simple_install_f() {

  mkdir -p "${HOME}/.local/share/applications"
  cp "${SCRIPT_PATH}/${RESOURCE_NAME}.desktop" "${HOME}/.local/share/applications/"

  # Copy desktop icon if desktop dir exists (was found)
  if [ -d "${XDG_DESKTOP_DIR}" ]; then
   cp "${SCRIPT_PATH}/${RESOURCE_NAME}.desktop" "${XDG_DESKTOP_DIR}/"
   # Altering file permissions to avoid "Untrusted Application Launcher" error on Ubuntu
   chmod u+x "${XDG_DESKTOP_DIR}/${RESOURCE_NAME}.desktop"
   if [ x${SUDO_USER} != x ]; then
    chown ${SUDO_USER} "${XDG_DESKTOP_DIR}/${RESOURCE_NAME}.desktop"
   fi
  fi
  
  mkdir -p ${HICOLOR_FOLDER}/32x32/apps/
  cp "${SCRIPT_PATH}/icons/32x32/eu.stethewwolf.sapy.png"  "${HICOLOR_FOLDER}/32x32/apps/"
  mkdir -p ${HICOLOR_FOLDER}/48x48/apps/
  cp "${SCRIPT_PATH}/icons/48x48/eu.stethewwolf.sapy.png" "${HICOLOR_FOLDER}/48x48/apps/"
  mkdir -p ${HICOLOR_FOLDER}/128x128/apps/
  cp "${SCRIPT_PATH}/icons/128x128/eu.stethewwolf.sapy.png" "${HICOLOR_FOLDER}/128x128/apps/"
}

# Uninstall using xdg-utils
xdg_uninstall_f() {

  # Remove *.desktop file
  xdg-desktop-menu uninstall ${RESOURCE_NAME}.desktop

  # Remove icon from desktop
  xdg-desktop-icon uninstall ${RESOURCE_NAME}.desktop

  # Remove icons
  xdg-icon-resource uninstall --size 32 ${RESOURCE_NAME}
  xdg-icon-resource uninstall --size 48 ${RESOURCE_NAME}
  xdg-icon-resource uninstall --size 128 ${RESOURCE_NAME}
}

# Uninstall by simply removing desktop files (fallback), incl. old one
simple_uninstall_f() {
  # delete legacy cruft .desktop file
  if [ -f "${HOME}/.local/share/applications/${RESOURCE_NAME}.desktop" ]; then
    rm "${HOME}/.local/share/applications/${RESOURCE_NAME}.desktop"
  fi

  if [ -f "${HOME}/.local/share/metainfo/${RESOURCE_NAME}.appdata.xml" ]; then
    rm "${HOME}/.local/share/metainfo/${RESOURCE_NAME}.appdata.xml"
  fi

  if [ -f "${XDG_DESKTOP_DIR}/${RESOURCE_NAME}.desktop" ]; then
    rm "${XDG_DESKTOP_DIR}/${RESOURCE_NAME}.desktop"
  fi
  
  if [ -f "${HICOLOR_FOLDER}/32x32/apps/eu.stethewwolf.sapy.png" ]; then
    rm "${HICOLOR_FOLDER}/32x32/apps/eu.stethewwolf.sapy.png"
  fi
  
    if [ -f "${HICOLOR_FOLDER}/48x48/apps/eu.stethewwolf.sapy.png" ]; then
    rm "${HICOLOR_FOLDER}/48x48/apps/eu.stethewwolf.sapy.png"
  fi
  
  if [ -f "${HICOLOR_FOLDER}/128x128/apps/eu.stethewwolf.sapy.png" ]; then
    rm "${HICOLOR_FOLDER}/128x128/apps/eu.stethewwolf.sapy.png"
  fi
}

# Removel python module
python_uninstall_f() {
    pip3 uninstall sapy -y
    # delete command line entry 
    if [ -f "${HOME}/.local/bin/sapy" ]; then
        rm "${HOME}/.local/bin/sapy"
    fi
}

# Check availability of xdg-utils
xdg_exists_f() {

  if ! command -v xdg-icon-resource > /dev/null; then return 1; fi
  if ! command -v xdg-desktop-menu > /dev/null; then return 1; fi
  if ! command -v xdg-desktop-icon > /dev/null; then return 1; fi
  if ! command -v xdg-mime > /dev/null; then return 1; fi
  return 0

}

# Shows a description of the available options
display_help_f() {
  printf "\nThis script will add a sapy desktop shortcut, menu item,\n"
  printf "icons and file associations for the current user.\n"
  if ! xdg_exists_f; then
    printf "\nxdg-utils are recommended to be installed, so this script can use them.\n"
  fi
  printf "\nOptional arguments are:\n\n"
  printf "\t-u, --uninstall\t\tRemoves shortcut, menu item and icons.\n\n"
  printf "\t-h, --help\t\tShows this help again.\n\n"
}

# Check for provided arguments
while [ $# -gt 0 ] ; do
  ARG="${1}"
  case $ARG in
      -u|--uninstall)
        UNINSTALL=true
        shift
      ;;
      -h|--help)
        display_help_f
        exit 0
      ;;
      *)
        printf "\nInvalid option -- '${ARG}'\n"
        display_help_f
        exit 1
      ;;
  esac
done

printf "Removing sapy"
python_uninstall_f
xdg_uninstall_f
simple_uninstall_f

if [ ${UNINSTALL} = false ]; then
    printf "Installing sapy"
    # If possible, use xdg-utils, if not, use a more basic approach
    python_install_f
    if xdg_exists_f; then
        xdg_install_f
    else
        simple_install_f
    fi
fi

printf " done!\n"

exit 0
