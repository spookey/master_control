==============
Master Control
==============

Welcome to one central part of my home automation.

This script can:

    * switch wireless power sockets
    * connect to some bluetooth audio device
    * handle my external usb disks
    * start some apps (which need the disk to be mounted)
    * - or run scripts in a new terminal window
    * handle dependencies inbetween:
    * - unmount disk before switching power off
    * - kill apps before unmounting


It runs on macOS and requires some recent `python 3`.

To control the power sockets, full_power_ is used!


Some parts are in plain `Apple Script` as this was the only way I could
figure out how to automate bluetooth dialup.

There is some commandline with this scheme::

    shove {module} {action} [--{flags}]

So to prepare everything for listening to music, I type::

    shove start itunes --lift

**Flags**:

:--lift: If given, turns things on, if omitted things are turned off.
:--slow: Walk through the full dependency path (with duplicate actions).
:--dump: Just print the path without invoking any module.

.. _full_power: https://github.com/spookey/full_power
