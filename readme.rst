==============
Master Control
==============

Welcome to one central part of my home automation.

This shell script can:
    * control wireless power sockets
    * connect to some bluetooth audio device
    * handle my external usb disk
    * start some apps (which needs the disk to be mounted)
    * handle dependencies inbetween
      (unmount disk before switching power off;
      kill apps before unmounting; etc.)


It runs on macOS and requires `bash 4`.

To control the power sockets,
`full_power <https://github.com/spookey/full_power>`_
is used!

Some parts are in plain `Apple Script` as this was the only way I could
figure out how to automate bluetooth dialup.

If invoked directly it will install a bunch of files in ``~/bin``.

Those files each source ``master_control.sh`` and then call one specific
function::

    power_full_light_desk.command
    power_full_store_disk.command
    power_null_light_desk.command
    power_null_store_disk.command
    store_mount.command
    store_umount.command
    ...

I then use Alfred to launch them.
The default values used can be changed in ``config.sh``.
