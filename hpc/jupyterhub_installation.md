===== JupyterHub Installation =====
==== JupyterHub installation with Python 2 as an additional kernel  ====
Assuming you are using **pip**, you can install the **ipykernel** package with Python 2, and then install the **kernelspec**, so Jupyter knows how to start the kernel
<code>
# install the kernel package for Python 2
python2 -m pip install --upgrade ipykernel
# register the Python 2 kernelspec
python2 -m ipykernel install
</code>
A totally complete installation of JupyterHub, notebook servers, and kernels for both Python 2 and 3 (need sudo access)
<code>
python3 -m pip install jupyterhub notebook ipykernel
# register Python 3 kernel (not technically necessary at this point, but a good idea)
python3 -m ipykernel install

# install the kernel package for Python 2
python2 -m pip install ipykernel
# register Python 2 kernel
python2 -m ipykernel install 

npm install -g configurable-http-proxy
</code>
And you can install whatever packages you want for Python 3 and/or Python 2 in the usual ways
== Run JupyterHub ==
Run JupyterHub as a background job using screen or any other way you wish
<code>
screen
jupyterhub
</code>
Ref: [[https://github.com/jupyter/jupyter/issues/71]]
==== JupyterHub default installation i.e. with only Python3 kernel ====
Ref: [[http://jupyterhub.readthedocs.io/en/latest/quickstart.html| JupyterHub quickstart]]
==== How to access Jupyter Notebook remotely ====
<code>jupyter notebook --no-browser --ip=172.16.40.27 --port=8881</code>
  * Ref: [[http://jupyter-notebook.readthedocs.io/en/stable/public_server.html]]
  * Ref: [[https://coderwall.com/p/ohk6cg/remote-access-to-ipython-notebooks-via-ssh]]