# What is Drone Interface?
Enter a simple description of the software here.

## Installation
The following text provides a basic installtion guide for the software.

#### Install Raspbian
Download Raspbian OS from www.raspberrypi.org/downloads/.  
Use a SD card formatter (Etcher, www.etcher.io) to install the OS on the SD Card.

#### Enable usb ssh
Create a new file called "ssh", without a file extension, on the boot partition of the SD card.  
Open the config.txt on the boot partition and add the following line:  
`dtoverlay=dwc2`

Now open the cmdline.txt and add the line:  
`modules-load=dwc2,g_ether`

#### Connect to a wlan with internet access.
To install the server, internet access is required.  
Plug the SD card into the Raspberry Pi. Connect the Pi with a USB cable to your PC.  
Don't use the USB power port. USB ssh doesn't work on the power port.

Download and install PuTTY(http://www.putty.org).
Open PuTTY, enter  
`raspberrypi.local`  
as hostname and click on the "Open" button.

Default ssh login:
```
user: pi    
password: raspberry
```

Enter the command:  
`sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`

Go to the bottom of the file and add:
```
network={  
    ssid="NETWORK_NAME"
    psk="NETWORK_PASSWORD"  
}
```

Replace NETWORK_NAME and NETWORK_PASSWORD with the name and password of your network.  
Now shutdown the wlan interface with:  
`sudo ifdown wlan0`  

and then restart it with:  
`sudo ifup wlan0`

#### Install the server
Download this repo and unzip it.

Download and install WinSCP(https://winscp.net/eng/docs/lang:de) on your PC to copy the software to the Pi. Use the same settings as for PuTTY and connect to the Pi.

Copy the folder `DroneInterface` on the Pi.

Now execute the command in the PuTTY terminal to install the server.  
`bash DroneInterface/setup.sh`

The Raspberry Pi reboots after the installation and provides a wireless network.  
```
SSID: FlyPi
Password: HHNSEB
```
