#!/bin/sh
# Sapy
# Copyright (C) 2018 stefano prina <stethewwolf@null.net>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# This script adds a menu item, icons for the current
# user. If possible, it will use the xdg-utils - or fall back to just creating
# and copying a desktop file to the user's dir.
# If called with the "-u" option, it will undo the changes.

# Resource name to use 
RESOURCE_NAME=sapy-stethewwolf

# Get absolute path from which this script file was executed
# (Could be changed to "pwd -P" to resolve symlinks to their target)
SCRIPT_PATH=$( cd $(dirname $0) ; pwd )
cd "${SCRIPT_PATH}"

#check if the user set the PREFIX
if [ -z $PREFIX ]; then
  PREFIX="$HOME/.local/bin"
fi

# Default mode is to do nothing and print help.
UNINSTALL=false
INSTALL=false
BUILD_INSTALL=false


# If possible, get location of the desktop folder. Default to ~/Desktop
XDG_DESKTOP_DIR="${HOME}/Desktop"
if [ -f "${XDG_CONFIG_HOME:-${HOME}/.config}/user-dirs.dirs" ]; then
  . "${XDG_CONFIG_HOME:-${HOME}/.config}/user-dirs.dirs"
fi

# Install using xdg-utils
xdg_install_f() {

  # Create a temp dir accessible by all users
  TMP_DIR=`mktemp --directory`

  # Create link in path
  ln -s $SCRIPT_PATH/sapy $PREFIX/sapy

  # Create *.desktop file using the existing template file
  sed -e "s,<BINARY_LOCATION>,${PREFIX},g" \
      -e "s,<ICON_NAME>,${RESOURCE_NAME},g" "${SCRIPT_PATH}/desktop.template" > "${TMP_DIR}/${RESOURCE_NAME}.desktop"

  # Install the icon files using name and resolutions
  xdg-icon-resource install --context apps --size 32 "${SCRIPT_PATH}/icon/icon.png" $RESOURCE_NAME

  # Install the created *.desktop file
  xdg-desktop-menu install "${TMP_DIR}/${RESOURCE_NAME}.desktop"

  # Create icon on the desktop
  xdg-desktop-icon install "${TMP_DIR}/${RESOURCE_NAME}.desktop"

  # Clean up
  rm "${TMP_DIR}/${RESOURCE_NAME}.desktop"
  rmdir "$TMP_DIR"

}

# Install by simply copying desktop file (fallback)
simple_install_f() {

  # Create a temp dir accessible by all users
  TMP_DIR=`mktemp --directory`

# Create link in path
  ln -s $SCRIPT_PATH/sapy $PREFIX/sapy

  # Create *.desktop file using the existing template file
  sed -e "s,<BINARY_LOCATION>,${PREFIX},g" \
      -e "s,<ICON_NAME>,${RESOURCE_NAME},g" "${SCRIPT_PATH}/desktop.template" > "${TMP_DIR}/${RESOURCE_NAME}.desktop"

  mkdir -p "${HOME}/.local/share/applications"
  cp "${TMP_DIR}/${RESOURCE_NAME}.desktop" "${HOME}/.local/share/applications/"

  # Copy desktop icon if desktop dir exists (was found)
  if [ -d "${XDG_DESKTOP_DIR}" ]; then
   cp "${TMP_DIR}/${RESOURCE_NAME}.desktop" "${XDG_DESKTOP_DIR}/"
   # Altering file permissions to avoid "Untrusted Application Launcher" error on Ubuntu
   chmod u+x "${XDG_DESKTOP_DIR}/${RESOURCE_NAME}.desktop"
  fi

  # Clean up temp dir
  rm "${TMP_DIR}/${RESOURCE_NAME}.desktop"
  rmdir "${TMP_DIR}"

}

# Uninstall using xdg-utils
xdg_uninstall_f() {

  # Clean PREFIX 
  if [ -f $PREFIX/sapy ];then
    rm -v $PREFIX/sapy
  fi

  # Remove *.desktop file
  xdg-desktop-menu uninstall ${RESOURCE_NAME}.desktop

  # Remove icon from desktop
  xdg-desktop-icon uninstall ${RESOURCE_NAME}.desktop

  # Remove icons
  xdg-icon-resource uninstall --size 32 ${RESOURCE_NAME}


}

# Uninstall by simply removing desktop files (fallback), incl. old one
simple_uninstall_f() {
  # Clean PREFIX 
  if [ -f $PREFIX/sapy ];then
    rm -v $PREFIX/sapy
  fi

  # delete legacy cruft .desktop file
  if [ -f "${HOME}/.local/share/applications/${RESOURCE_NAME}.desktop" ]; then
    rm -v "${HOME}/.local/share/applications/${RESOURCE_NAME}.desktop"
  fi

  if [ -f "${XDG_DESKTOP_DIR}/${RESOURCE_NAME}.desktop" ]; then
    rm -v "${XDG_DESKTOP_DIR}/${RESOURCE_NAME}.desktop"
  fi

}

# Update desktop file and mime databases (if possible)
updatedbs_f() {

  if [ -d "${HOME}/.local/share/applications" ]; then
    if command -v update-desktop-database > /dev/null; then
      update-desktop-database "${HOME}/.local/share/applications"
    fi
  fi
}

# Check availability of xdg-utils
xdg_exists_f() {

  if ! command -v xdg-desktop-menu > /dev/null; then return 1; fi
  if ! command -v xdg-desktop-icon > /dev/null; then return 1; fi
  return 0

}

# Shows a description of the available options
display_help_f() {
  printf "\nThis script will add a Saoy desktop shortcut, menu item,\n"
  printf "icons for the current user.\n"
  if ! xdg_exists_f; then
    printf "\nxdg-utils are recommended to be installed, so this script can use them.\n"
  fi
  printf "\nOptional arguments are:\n\n"
  printf "\t-i, --install\t\tAdd shortcut, menu item and icons; files containde in $SCRIPT_PATH will be used.\n\n"
  printf "\t-b, --build-install\tBuild a binary, install it on \$PREFIX=$PREFIX and add shortcut, menu item and icons.\n\n"
  printf "\t-u, --uninstall\t\tRemoves shortcut, menu item and icons.\n\n"
  printf "\t-h, --help\t\tShows this help again.\n\n"

  printf "In order to change the install path export PREFIX befor run install"
}

# Build binary
build_sapy_binary_f() {
  if [ ! -d $PREFIX ]; then
    mkdir -p $PREFIX
  fi

  $SCRIPT_PATH/build.sh install $PREFIX
}

# Install build binary using xdg-utils
xdg_build_install_f() {

  # Create a temp dir accessible by all users
  TMP_DIR=`mktemp --directory`

  # Create *.desktop file using the existing template file
  sed -e "s,<BINARY_LOCATION>,${PREFIX},g" \
      -e "s,<ICON_NAME>,${RESOURCE_NAME},g" "${SCRIPT_PATH}/desktop.template" > "${TMP_DIR}/${RESOURCE_NAME}.desktop"

  # Install the icon files using name and resolutions
  xdg-icon-resource install --context apps --size 32 "${SCRIPT_PATH}/icon/icon.png" $RESOURCE_NAME

  # Install the created *.desktop file
  xdg-desktop-menu install "${TMP_DIR}/${RESOURCE_NAME}.desktop"

  # Create icon on the desktop
  xdg-desktop-icon install "${TMP_DIR}/${RESOURCE_NAME}.desktop"

  # Clean up
  rm "${TMP_DIR}/${RESOURCE_NAME}.desktop"
  rmdir "$TMP_DIR"
}

# Install by simply copying desktop file (fallback)
simple_build_install_f() {

  # Create a temp dir accessible by all users
  TMP_DIR=`mktemp --directory`

  # Create *.desktop file using the existing template file
  sed -e "s,<BINARY_LOCATION>,${PREFIX},g" \
      -e "s,<ICON_NAME>,${RESOURCE_NAME},g" "${SCRIPT_PATH}/desktop.template" > "${TMP_DIR}/${RESOURCE_NAME}.desktop"

  mkdir -p "${HOME}/.local/share/applications"
  cp "${TMP_DIR}/${RESOURCE_NAME}.desktop" "${HOME}/.local/share/applications/"

  # Copy desktop icon if desktop dir exists (was found)
  if [ -d "${XDG_DESKTOP_DIR}" ]; then
   cp "${TMP_DIR}/${RESOURCE_NAME}.desktop" "${XDG_DESKTOP_DIR}/"
   # Altering file permissions to avoid "Untrusted Application Launcher" error on Ubuntu
   chmod u+x "${XDG_DESKTOP_DIR}/${RESOURCE_NAME}.desktop"
  fi

  # Clean up temp dir
  rm "${TMP_DIR}/${RESOURCE_NAME}.desktop"
  rmdir "${TMP_DIR}"

}


# Check for provided arguments
while [ $# -gt 0 ] ; do
  ARG="${1}"
  case $ARG in
      -u|--uninstall)
        UNINSTALL=true
        shift
      ;;
      -i|--install)
        INSTALL=true
        shift
      ;;
      -b|--build-install)
        BUILD_INSTALL=true
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

# If possible, use xdg-utils, if not, use a more basic approach
if xdg_exists_f; then
  if [ ${UNINSTALL} = true ]; then
    printf "Removing desktop shortcut and menu item for Sapy..."
    xdg_uninstall_f
    simple_uninstall_f
    updatedbs_f
    printf " done!\n"
 
  elif [ ${INSTALL} = true ]; then
    printf "Adding desktop shortcut, menu item for Sapy..."
    xdg_uninstall_f
    simple_uninstall_f
    xdg_install_f
    updatedbs_f
    printf " done!\n"
 
  elif [ ${BUILD_INSTALL} = true ]; then
    printf "Building and adding desktop shortcut, menu item for Sapy..."
    xdg_uninstall_f
    simple_uninstall_f
    build_sapy_binary_f
    xdg_build_install_f
    updatedbs_f
    printf " done!\n"
 
  else
    display_help_f
  fi
else
  if [ ${UNINSTALL} = true ]; then
    printf "Removing desktop shortcut and menu item for Sapy..."
    simple_uninstall_f
    updatedbs_f
    printf " done!\n"
 
  elif [ ${INSTALL} = true ]; then
    printf "Adding desktop shortcut and menu item for Sapy..."
    simple_uninstall_f
    simple_install_f
    updatedbs_f
    printf " done!\n"
 
  elif [ ${BUILD_INSTALL} = true ]; then
    printf "Building and adding desktop shortcut, menu item for Sapy..."
    simple_uninstall_f
    build_sapy_binary_f
    simple_build_install_f
    updatedbs_f
    printf " done!\n"
  else
    display_help_f
  fi
fi

exit 0
