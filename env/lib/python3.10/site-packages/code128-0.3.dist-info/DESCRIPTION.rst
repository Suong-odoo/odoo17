README
======

Overview
--------
code128 is a simple library to create Code-128 barcodes.

useful links:
~~~~~~~~~~~~~
`Python Package Index
<https://pypi.python.org/pypi/code128/>`_

`Repository
<https://bitbucket.org/01100101/code128/overview/>`_ with latest source

License
~~~~~~~

Copyright (c) 2014-2015 Felix Knopf

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License in the LICENSE.txt for more details.

What's New
-----------
0.3
~~~~
Graphical User Interface

0.2
~~~
Command Line Interface; PyPI integration


Features
---------
* optimal codes (use code128C to encode long sequences of digits; lazy switch between Code128A and B)
* full latin-1 charset is supported
* no additional libraries needed for svg output
* output as PIL Image objects (PIL requiered)
* command line tool and gui

Setup
-----
This is a pure python package, for this the following steps are optional.
A copy of the package (folder *code128* in the source archive) in your directory will also work for this specific project.
The instructions below ensure that the library is available for every python module and from the command line.

Note, that some Linux Systems use *python3* and *pip3* to distinguish from their Python2 versions.

For Windwos users without a Python installation there is also a 'stand-alone' version available.

Dependencies
~~~~~~~~~~~~
* **Python3** (Tested with 3.3 and 3.4, other versions should work, too)
* **setuptools** to use the setup script or pip, usually preinstalled
* *optional*: **PIL**, or compatible fork (**Pillow** is recommended) to save barcodes as raster graphics

Let *pip* do the work
~~~~~~~~~~~~~~~~~~~~~

::

	$ pip install -i https://testpypi.python.org/pypi code128 --pre

Windows Users
~~~~~~~~~~~~~
A convenient graphical installer is provided for the final releases.


build from source
~~~~~~~~~~~~~~~~~
download the zip archive or tarball, extract it and install with (you may need root access):

::

	$ python ./code128-[version]/setup.py install


Usage
-----

with Python
~~~~~~~~~~~

.. code:: python

	import code128

	code128.image("Hello World").save("Hello World.png")  # with PIL present

	with open("Hello World.svg", "w") as f:
		f.write(code128.svg("Hello World"))


from shell
~~~~~~~~~~
Code128 provides a command line interface. If you installed the library, simply type
::

	$ code128 "Hello World" "Hello World.svg"

The packet also defines a *__main__.py* entry point, so 
::

	$ python ~/spam/eggs/code128 "Hello World" "Hello World.svg"

will work, too.

The GUI
~~~~~~~
::

	$ code128w

will start the graphical mode, where you can preview your codes.
This needs PIL and tkinter.

Contribution
~~~~~~~~~~~~
Use the `Issue Tracker
<https://bitbucket.org/01100101/code128/issues?status=new&status=open/>`_ on Bitbucket to report bugs, request a feature, etc.

If you want to contribute some code, feel free to create a `pull request
<https://bitbucket.org/01100101/code128/pull-requests/>`_.

