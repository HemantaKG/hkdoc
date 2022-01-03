===== Python "pip/pip2" installation: (python version 2.7.12) =====
    sudo apt install python-pip
python "pip3" installation : (python version 3.5.2)
    sudo apt install python3-pip
pip upgrade:
    Sudo pip install --upgrade pip
===== Installs packages for your local use OR local install =====
use the flag '--user' with pip install command as
    pip install --user <<package name>>
===== Python package installation into a separate location =====
    pip install --install-option="--prefix=<<path to the location>>" <<package name>>
NOTE: To explore "PYTHONPATH" update '/etc/bashrc' file
    nano /etc/bashrc
    export PYTHONPATH=$PYTHONPATH:/share/pypkg/lib/python2.7/site-packages:/share/pypkg/lib64/python2.7/site-packages:/share/pypkg/bin

===== Python "Virtualenv" installation =====
    sudo pip install virtualenv
createing python virtual env:
    virtualenv virtualenvname
activate virtual env:
    source ~/virtualenvname/bin/activate
deactivate virtual env:
    deactivate
python 3.5 virtual env configure:
install python3-venv:
    sudo apt install python3-venv
create python3 vitualenv:
    python3.5 -m venv py35commenv
activate virtual env:
    . py35commenv/bin/activate
deactivate virtual env:
    deactivate
===== Inatall "ipython" in virtualenv =====
	pip install ipython
	pip install numpy (FOR OTHER PY PCK)
List all python packages that installated on system:
    pip list --format=columns
    pip list --format=legacy
===== Jupyter Note of installation =====
    pip install jupyter
NOTE: install "jupyter notebook" in each virtual env, local otheriwise pck import cann't possible.