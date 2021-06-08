Cloning of a Raspberry PI formatted SD Card (Meteobike)
===============

If you have a working system with SD card for one Meteobike, you may want to clone the SD-card to equip multiple systems the same way. The following procedure describes the cloning of a SD-Card for a Raspberry PI using a Mac and the `Terminal` program.

Insert the SD card in the card slot of your computer (or an adapter). 

Open `Terminal` on a Mac. Type `diskutil list` into the command line to see the current disks and partitions. 

  imac:~ yourname$ diskutil list
  
The result may look like:
  /dev/disk0 (internal):
     #:                       TYPE NAME                    SIZE       IDENTIFIER
     0:      GUID_partition_scheme                         500.3 GB   disk0
     1:                        EFI EFI                     314.6 MB   disk0s1
     2:                 Apple_APFS Container disk1         500.0 GB   disk0s2
  
  /dev/disk1 (synthesized):
     #:                       TYPE NAME                    SIZE       IDENTIFIER
     0:      APFS Container Scheme -                      +500.0 GB   disk1
                                   Physical Store disk0s2
    1:                APFS Volume Macintosh HD            131.7 GB   disk1s1
    2:                APFS Volume Preboot                 24.3 MB    disk1s2
     3:                APFS Volume Recovery                519.6 MB   disk1s3 
     4:                APFS Volume VM                      4.3 GB     disk1s4

  /dev/disk2 (internal, physical):
     #:                       TYPE NAME                    SIZE       IDENTIFIER
     0:     FDisk_partition_scheme                        *31.9 GB    disk2
     1:             Windows_FAT_16 RECOVERY                1.8 GB     disk2s1
     2:                      Linux                         33.6 MB    disk2s5
     3:             Windows_FAT_32 boot                    72.4 MB    disk2s6
     4:                      Linux                         30.0 GB    disk2s7
   
Here `/dev/disk2`refers to a 32 GB SD Card. You can tell based on name, size and formatting.

If you instead of `/dev/diskN` use `/dev/rdiskN`, where `N` is the muber, the process of copying is much faster. The letter "r" stands for "für "raw".

Then copy the raw content from the SD card into a disk image, here called `sdcard.img`

imac:~ yourname$ sudo dd if=/dev/rdisk2 of=/Users/yourname/Desktop/sdcard.img bs=1m
Password:
30436+1 records in
30436+1 records out
31914983424 bytes transferred in 372.269240 secs (85730917 bytes/sec)
imac:~ yourname$

You don't need an unmount command, just insert the SD card into the Mac via the slot or an adapter and then check in the terminal which disc number corresponds to the SD card. In the example it is `disk2` but could be different on each system.

Copying back on an empty SD card (or one that will be overwritten) is done accordingly with the command:

sudo dd if=/Users/christen/Desktop/sdcard.img of=/dev/rdisk2 bs=1m

`bs=1`
