## Non-Python Visualization

For a 2D interactive polarization visualization/animation click [here](https://rawgit.com/gregnordin/Polarization/master/polarization_2d.html).
The corresponding github respository is [here](https://github.com/gregnordin/Polarization).

## Python Visualizations and Codes

To run any of the python codes in this directory (such as `polarization_animation.py`) you need to have Python installed on your computer. If you don't already have python installed, follow these instructions:

__Windows__

1. Download [Anaconda Python](https://www.continuum.io/downloads), which is a free python distribution with many included packages. I recommend Python 3.5 and downloading the 64-bit graphical installer (unless of course you have a 32-bit system, in which case choose the 32-bit installer).
2. Run installer. Choose default options. If you don't want to mess with typing your password for a global installation, choose to install for your user account.
3. Open the Anaconda Prompt application (in Windows 7, click on Start menu and begin typing "Anaconda" and it should show up).
4. Type `conda install pyqtgraph` and select `y` at the prompt to install the pyqtgraph package.
5. Type `conda install pyopengl` and select `y` at the prompt to install the pyopengl package.
6. Now navigate in Anaconda Prompt to the folder in which `polarization_animation.py` is located, i.e., `cd <path to directory>`. If you don't know how to use a command line to change your working directory, you will need to look it up online.
7. Type `python polarization_animation.py` and the animation should run.

Note: I tested the above on Windows 7 and it worked fine. Should be the same for later versions of Windows.

__Mac OS X/Linux__

1. Should be the same as for Windows except download the appropriate installer and use your operating system's native command line tool (`Terminal` for Mac OS X).
