# Thu, 9/17/20

## Set up virtual environment in which to run polarization animation

    cd ~/Documents/Projects/git_stuff_ECEn360/ECEn360_W16/plane_waves
    (base)
    $ python -m venv .venv --prompt "polarization"
    (base)
    $ source .venv/bin/activate
    (polarization) (base)
    $ python --version
    Python 3.7.4
    (polarization) (base)
    $ pip install pyqtgraph pyopengl numpy PyQt5
    (polarization) (base)
    $ pip freeze > requirements.txt
    (polarization) (base)
    (polarization) (base)
    $ cat requirements.txt
    numpy==1.19.2
    PyOpenGL==3.1.5
    PyQt5==5.15.1
    PyQt5-sip==12.8.1
    pyqtgraph==0.11.0
    
    (polarization) (base)
    $ python polarization_animation.py
    
