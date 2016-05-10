# Exercise 1
by Niklas Hösl

## Setting up the PI
As we got a completely empty PI we had to flash it with Minibian, a minimal raspian image. The steps to do this were:
1. Download the archived image here https://minibianpi.wordpress.com/ and unzip it
2. Download and install *win32diskimager* (https://sourceforge.net/projects/win32diskimager/)
3. Plug-in the SD card of the PI into the PC
4. Open *win32diskimager* and flash the SD card with the img-file from the archive
5. Put the SD card back into the PI, connect the power cable and connect the ethernet cable.

With this setup the PI should be ready. Because we were a lot of people in the class we set static IP addresses for our PIs. This can be done by changing the config in the ``` /etc/network/interfaces ``` file from dynamic:
```sh
iface eth0 inet dhcp
```
to static:
```sh
iface eth0 inet static
address 192.168.3.12
netmask 255.255.255.0
gateway 192.168.3.1
```
When setting a static IP it is also helpful to set a namesever, otherwise you and your apt-get may have a bad time. Do this by adding e.g. the Google DNS to the ``` /etc/resolv.conf ``` file:
```sh
nameserver 8.8.8.8
```

Now everything should be setup to connect with the PI from your PC via SSH. On Windows you therefore should use PuTTY.
Add the IP of the PI as host name, select SSH (Port 22) and hit the connect button. Hit OK on every message box that comes up and you should see a login dialog. For our configuration the user is ```root``` and the password is ```raspberry```.

### Errors / Mistakes that came up
* I tried to connect to the PI via the TTY serial cable over USB. I had to install a driver to have my PC recognize the cable. But than PC give me a warning that the USB port needs more energy than the PC can provide. After that I wanted to remove the USB cable. This was already so hot that I nearly burned my finger and also the cable nearly melt down. I have no idea why that happened, but it hurt!
* The PI was not recognized by the network. I replaced it with another PI then everything worked fine.

## First Blinky example

Here I needed to install some packages. Before I could do that I had to update the package manager, install ```sudo``` and partition the SD card to use the whole 8GB of memory with ```raspi-config``` (using the first option).

```sh
apt-get update
apt-get upgrade
apt-get install sudo
apt-get install raspi-config
raspi-config
```

Next I followed this tutorial to setup wiringPi: http://wiringpi.com/download-and-install/.
1. Install GIT: 
```sh
sudo apt-get install git-core
```

2. Clone the wiringPI repo, pull the origin and build the whole thing:
```sh
git clone git://git.drogon.net/wiringPi
cd wiringPi
git pull origin
./build
```

3.  See if the installation was successful with this showing some useful information:
```sh
gpio -v
```

Now we could use the library with the Blinky example (http://wiringpi.com/examples/blink/):

I used the ```examples/blink.c``` file from the GIT repo without changing a single line of code. The code is this:

```c
#include <stdio.h>
#include <wiringPi.h>
// LED Pin - wiringPi pin 0 is BCM_GPIO 17.
#define	LED	0
int main (void)
{
  printf ("Raspberry Pi blink\n") ;
  wiringPiSetup () ;
  pinMode (LED, OUTPUT) ;
  for (;;)
  {
    digitalWrite (LED, HIGH) ;	// On
    delay (500) ;		// mS
    digitalWrite (LED, LOW) ;	// Off
    delay (500) ;
  }
  return 0 ;
}
```

It sets the Port 0 (which is the GPIO 17 on the breadboard) as output port and periodically sets the voltage of this port to high and low, which lets the LED blink.

The wired setup looks like this:

![Wiring 1](http://rwrBrille.at/wp-content/uploads/2016/05/WP_20160510_14_39_48_Pro.jpg)

The used resistor is 330Ω (Colors: Orange, Orange, Brown, Gold).

### Errors / Mistakes that came up
* I put in the connector cable between the PI and the breadboard wrong. Therefore it didn't work at first. See the attached picture to see how it is right.
* I forgot to configure the PI to use the full 8GB of storage. Therefore I ran out of memory and could not even install the raspi-config package. ULNO then needed to partition the SD card with his machine.

## Mail exercise
This was the most tricky exercise. Not because of the actual task, but because of the libraries of the tutorial. We had to rebuild the tutorial that is described here: https://learn.adafruit.com/raspberry-pi-e-mail-notifier-using-leds.
It basically checks your mails every minute and lights up the yellow LED (in the tutorial it is green) when there are unread messages or the red LED otherwise.

First of all we had to install these packages:
* Python PIP: The Pything Package Manager
* IMAPlib2: A library for the IMAP protocol
* RPi.GPIO: A library to access the GPIO pins of the PI

```sh
apt-get install python-pip
pip install imaplib2
pip install RPi.GPIO
```

Then we wired up the breadboard like this:

![Wiring 2](http://rwrBrille.at/wp-content/uploads/2016/05/WP_20160510_19_54_16_Pro.jpg)

Again two 330Ω resistors were used. 

Next we ran the script with ```./checkmail2.py```. Note: Before running it the first time you may have to add execution rights with ```chmod +x checkmail2.py```. The script is available in this GIT folder.

The tricky thing was, that the tutorial did not say anything about installing the *RPi.GPIO* library. Also it told us to install the *imapclient*, which always led to an SSL error, which nobody of us could resolve.

I then used the *imaplib2* library, which had a similar interface (but not the same) and rebuild the loading of the mails using some code provided here: http://www.programcreek.com/python/example/2875/imaplib.IMAP4_SSL

### Errors / Mistakes that came up
* During the day somewhen an error with PIP come up. I couldn't install any package anymore. I fixed this with the following command: 
```sh
pip install --no-use-wheel --upgrade distribute
```
* Many errors with the *imapclient* library came up. But because I finally used the *imaplib2* library I don't want to point them out here.