card10 BLE file dropper
=======================

[card10](https://card10.badge.events.ccc.de/) it the badge from [CCCamp 2019](https://events.ccc.de/camp/2019/wiki/Main_Page).
This "smart watch" is Bluetooth Low Energy (BLE) enabled. In order to flash new firmware and apps, users can upload
files using Bluetooth. At the time of the event it was possible to upload files without authentication (just by
connecting). I've noticed this issue and thought it would be fun to write a little tool, which uploads an empty file
named "@IIIIkarusWasHere" (the file name length is very limited). I went around the camp and "infected" some devices.
Some users actually found the file and Tweeted about it ([1](https://twitter.com/mindfuckup/status/1164668902615523330),
[2](https://twitter.com/Duenengeist/status/1164830657396088833), [3](https://twitter.com/Isopoda/status/1164905104123793409)).



Usage
-----

Configure the script by editing the parameters defined at the top of `card10-file-dropper.py`. If not already done by
your system, you have to enable and power on Bluetooth. On Arch Linux this is done by entering the following lines.
```
sudo systemctl start bluetooth.service
bluetoothctl power on
```
Then run the script with root privileges. (Why? See https://github.com/IanHarvey/bluepy/issues/313)
```
sudo ./card10-file-dropper.py
```
Stop the script using CTRL+c.


Example Output
--------------

```
[*] Starting scanner for 3.0 seconds.
[*] Scan finished. Found 48 devices.
[*] Connecting to ca:4d:10:d5:5a:00.
[*] Trying to write file.
[+] File written to ca:4d:10:d5:5a:00.
[*] Starting scanner for 3.0 seconds.
^C
[*] Shutting down.
[*] The following devices have been infected:
[+] Infected device ca:4d:10:d5:5a:00.

```