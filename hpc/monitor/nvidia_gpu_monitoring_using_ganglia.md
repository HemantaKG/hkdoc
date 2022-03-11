# NVIDIA GPU monitoring using Gangali
- Ref: https://developer.nvidia.com/ganglia-monitoring-system
- Ref: https://github.com/ganglia/gmond_python_modules/tree/master/gpu/nvidia
- Ref: https://serverfault.com/questions/771854/ganglias-gpu-nvidia-module-do-we-need-to-patch-the-ganglia-webfrontend

## NVIDIA GPU monitoring plugin for gmond
First, install the Python Bindings for the NVIDIA Management Library:
````
tar -xvzf nvidia-ml-py-7.352.0.tar.gz
cd nvidia-ml-py-7.352.0
python setup.py install
````
NOTE: For the latest bindings see: http://pypi.python.org/pypi/nvidia-ml-py/

## Ganglia plugin configuration
Download and setup configuration and site file(s)
````
git clone https://github.com/ganglia/gmond_python_modules.git
````
- Copy gmond_python_modules/gpu/nvidia/python_modules/nvidia.py to {libdir}/ganglia/python_modules
- Copy gmond_python_modules/gpu/nvidia/conf.d/nvidia.pyconf to /etc/ganglia/conf.d
- Copy gmond_python_modules/gpu/nvidia/graph.d/* to {ganglia_webroot}/graph.d/

````
cp gmond_python_modules/gpu/nvidia/conf.d/nvidia.pyconf /etc/ganglia/conf.d/
cp gmond_python_modules/gpu/nvidia/python_module/nvidia.py /usr/lib/ganglia/python_modules/
cp gmond_python_modules/gpu/nvidia/graph.d/* /usr/share/ganglia-webfrontend/
````

also needed to add **modpython.conf** to tell ganglia's **modpython.so ** to load the **nvidia.py** module.

````
cat <<EOF | sudo tee /etc/ganglia/conf.d/modpython.conf
modules {
  module {
    name = "python_module"
    path = "/usr/lib/ganglia/modpython.so"
    params = "/usr/lib/ganglia/python_modules/"
  }
}
include ('/etc/ganglia/conf.d/*.pyconf')
EOF
````
NOTE: If you don't have **/etc/ganglia/conf.d/modpython.conf**
