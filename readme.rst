==============
Master Control
==============

Welcome to one central part of my home automation.

modules
=======

lib
---

The `lib`_ module can:

    * switch wireless power sockets
    * connect to some bluetooth audio device
    * handle my external usb disks
    * start some applications (which need the disk to be mounted)
    * - or run scripts in a new terminal window
    * handle dependencies in between:
    * - unmount disk before switching power off
    * - kill applications before unmount


It runs on macOS and requires some recent `python 3`.

Some parts are in plain `Apple Script` as this was the only way I could
figure out how to automate bluetooth dialup.

For more information visit the `project description`_.
To control the power sockets, full_power_ is used!

    * The main entry point is the `shove`_ command.

ext
---

The `ext`_ module resuses parts of `lib`_ and extends it to provide:

    * the `install`_ command to setup some helpers.
    * the `color`_ command to set the light of full_power_.

launchers
=========

shove
-----

There is some commandline with this scheme::

    shove {module} {action} [--{flags}]

* Use ``shove --help`` or ``shove {module} --help`` to see which
  **modules** and **actions** are available.

* Valid **flags** are:

:--lift: If given, turns things on, if omitted things are turned off.
:--slow: Walk through the full dependency path (with duplicate actions).
:--dump: Just print the path without invoking any module.

So to prepare everything for listening to music, I type::

    shove start itunes -l


install
-------

Use the ``install`` command to create some helper files::

    ./install {what} {where}

* **Where** specifies the full output file location.

* Valid **what** values are:

:alfwf: Generate some *info.plist* for alfred workflow with all triggers.
:volwf: Generate some *info.plist* for alfred workflow to control volume.
:zcomp: Generate a *_shove* file which is then be used as zsh completion.


color
-----

Split the day in one or more **hi** **points**.
The light is set to value between **lo** and **hi** according to current time::

    ./color {points} [--{hi} 0xffffff] [--{lo} 0x000000]

* **Points** must be a number bigger or equal than one.
* **hi**, **lo** color values can be entered
  as *HEX* if prefixed with ``0x``.


.. _project description: https://www.der-beweis.de/build/master_control
.. _full_power: https://github.com/spookey/full_power
