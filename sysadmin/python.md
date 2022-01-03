==== setuptools error: python package source installation ====
If the 'setuptools' throwing any error, (or) python package installation fails while using source installation method of any python package using 'setup.py' installation script file.
<color #ed1c24>ERROR:</color>
      File "/usr/lib/python2.7/site-packages/setuptools/command/easy_install.py", line 701, in process_distribution distreq.project_name, distreq.specs, requirement.extras
      TypeError: __init__() takes exactly 2 arguments (4 given)
<color #22b14c>RESOLVE:</color>
[[https://github.com/pypa/pip/issues/1917|Ref1]];

reinstall setuptools package
    sudo yum reinstall python-setuptools
upgrade setuptools package using 'pip'
    sudo pip install --upgrade setuptools
check setuptools info 
    sudo pip show setuptools