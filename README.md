# Disk wearout
Crucial SSD wearout checker for CheckMK

It uses smartctl to fetch info from the hosts and display the SSD's model, serial number, disk wearout percentage, number of available spare blocks on SSD and number of RAIN events.

WARN/CRIT on disk wearout percentage, parametrable via rule (default 95%/98%).
