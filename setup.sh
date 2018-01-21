#!/bin/bash
# Drone interface installer.
# Enter some more detailed description here.
#
# Done:
# Check if python is installed.
# - Install python.
# Check if pip is installed.
# - Install pip.
# Check if pySerial is installed.
# - Install pySerial.
# Check if pyMultiWii is installed.
# - Check if available.
# - - Download it.
# - Install pyMultiWii.
# Config the serial port.
# - Add user to group dialout.
# - Enable uart in /boot/config.txt
# - Remove console output on serial in /boot/cmdline.txt
# - Disable terminal on the serial port.
# Autostart for the server.
#
# To do:
# Config the wlan interface.

echo "DroneInterface changes the configuartion of the wlan interface and serial port. Are you sure you want to continue? [Y/N]:"
read choise

if [ "${choise,,}" == "n" ];
then
  echo User stopped installation.
fi

# Path from root to the application.
appDir=$(dirname $(readlink -f $0))
configPath="/boot/config.txt"

# Check internet conncetion. Could get usefull later.
if ! wget -q --spider --tries=5 --timeout=20 google.com
then
  echo "Please connect your RPi to the internet and try it again."
else
  echo "Internet connection available."
fi

# Update the RPi
sudo apt-get update
sudo apt-get upgrade

# # # # # # # # # # #
# Install packages #
# # # # # # # # # #

# declare -a pkgDep=("python" "python-pip" "python-serial" "git")
declare -a pkgDep=("python" "python-serial")
# declare -a modulDep=("pymultiwii")

echo "Check package dependencies..."
for pkg in "${pkgDep[@]}"
do
  if [ "" == "$(dpkg-query -W --showformat='${Status}\n' $pkg|grep "install ok installed")" ];
  then
    echo "Install package '$pkg'."
    sudo apt-get install $pkg
  else
    echo "'$pkg' already installed."
  fi
done


# # # # # # # # # # # # #
# Install python moduls #
# # # # # # # # # # # # #

# mspName="pyMultiWii"
# mspURL="https://github.com/alduxvm/pyMultiWii.git"
# mspPath="$appDir/$mspName"

# echo "Check python dependencies..."
# pipResult=$(pip show ${mspName,,})

# if [ -n "$pipResult" ];
# then
#  echo "'${mspName,,}' already installed."
# else
#  if [[ ! (-d "$mspPath") ]];
#  then
#    # Download multiwii serial protocol libaary.
#    echo "Download '${mspName,,}'..."
#    git clone https://github.com/alduxvm/pyMultiWii.git $mspPath &> /dev/null
#  fi
#  # Install the libary.
#  echo "Install '${mspName,,}'..."
#  pip install $mspPath/. &> /dev/null

  # Delete the downloaded files.
#  echo "Delete '${mspName,,}' installation files."
#  sudo rm -r $mspPath
# fi

echo "All dependencies installed."


# # # # # # # # # # # #
# Config serial port #
# # # # # # # # # # #

# Check that the user is in the group 'dialout'.
# Otherwise the user has no permission to use the serial port.
if [ "" == "$(id | grep -o "dialout")" ];
then
  echo "Add '$USER' to group \'dialout\'."
  # sudo usermod -a -G dialout $USER
else
  echo "'$USER' already in group 'dialout'."
fi

# Enable uart in the '/boot/config.txt'.
uartSetting="enable_uart=1"
uartLine=$(grep "enable_uart" /boot/config.txt)

if [ "$uartLine" == "" ];
then
  # No entrie for uart. Create it.
  echo "Create a uart entrie in the boot config."
  sudo sh -c "echo $uartSetting >> /boot/config.txt"
else
  # Just override the old setting.
  echo "Enable uart in the boot config."
  sudo sh -c "sed -i.bak "s/$uartLine/$uartSetting/g" /boot/config.txt"
fi

# Disable console output on the serial port in '/boot/cmdline.txt'.
# Find the entries that use serial port as output
entrie=$(sudo grep -o "\<[a-z]\+=\(tty\(AMA\|S\)\|serial\)0,[0-9]\+" /boot/cmdline.txt)
if [[ ! "$entrie" == "" ]];
then
  echo "Disable console output on serial port."
  sudo sh -c "sed -i.bak \"s/$entrie//g\" /boot/cmdline.txt"
  echo "test: $entrie"
  # Disable terminal on the serial port.
  serialAddr=$(grep -o "tyy\(AMA0\|S0\)\|serial0" <<< "$entrie")
  echo "Disable getty services for $serialAddr"
  sudo systemctl stop serial-getty@$serialAddr.service
  sudo systemctl disable serial-getty@$serialAddr.service
fi

# Check if we have to disable bluetooth too.
# Onboard BT is connected via serial port. Some tutorials recommend it.


# # # # # # # # # # # #
# Setup auto start  #
# # # # # # # # # #

# Add a the Run.py to /etc/rc.local
# Find the end of the file and add the command to start the script.
# Replace the hard coded dir path.
echo "Enable auto start for the server."
sedPath=$(sed 's:/:\\\/:g' <<< "$appDir" )
sudo sh -c "sed -i.bak \"s/^exit 0/echo Start drone interface\npython $sedPath\/Server\/Run.py \&\nexit 0/g\" /etc/rc.local"


# # # # # # # # # # # # #
# Config wlan interface #
# # # # # # # # # # # # #

# sudo apt-get install dnsmasq
# sudo apt-get install hostapd

# echo "Stop dns and host."
# sudo systemctl stop dnsmasq
# sudo systemctl stop hostapd

# echo "Edit wlan settings."
# wlanSetting=$'interface wlan0
# static ip_address=192.168.10.1/24'
# sudo sh -c "echo \"$wlanSetting\" >> /etc/dhcpcd.conf"

# echo "Restart dhcp service."
# sudo service dhcpcd restart

# echo "Edit dhcp settings."
# dhcpSettings=$'interface=wlan0
# dhcp-range=192.168.10.2,192.168.10.20,255.255.255.0,24h'
# sudo sh -c "echo \"$dhcpSettings\" >> /etc/dnsmasq.conf"

# echo "Edit hostapd."
# hostapdSettings=$'interface=wlan0
# driver=nl80211
# ssid=FlyPi
# hw_mode=g
# channel=7
# wmm_enabled=0
# macaddr_acl=0
# auth_algs=1
# ignore_broadcast_ssid=0
# wpa=2
# wpa_passphrase=HHNSEB-Drone
# wpa_key_mgmt=WPA-PSK
# wpa_pairwise=TKIP
# rsn_pairwise=CCMP'
# sudo sh -c "echo \"$hostapdSettings\" >> /etc/hostapd/hostapd.conf"

# echo "Edit daemon config"
# daemonSettings=$'DAEMON_CONF="/etc/hostapd/hostapd.conf"'
# sudo sh -c "echo \"$daemonSettings\" >> /etc/default/hostapd"

# echo "Start dns and hostapd service."
# sudo service hostapd start
# sudo service dnsmasq start

# Reboot the pi after the setup
sudo reboot
