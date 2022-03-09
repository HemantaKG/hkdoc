# Run Jupyter Notebook on Slurm Queue
This document enables you to run your Jupyter server on a Slurm node.
Here, Jupyter server is sbmited as a Slurm job. Jupyter server gets placed on a Slurm node with enough resources to host it.

For example here, We are creating a slurm job that runs jupyterlab on a Slurm node, for up to 1 days.
Once running, we are going to connect to the jupyterlab instance with SSH port forwarding from our local laptop.
Note: A tunnel must be created.

## SSH remote system/cluster
````
ssh <<user>>@<<icts-clustername>>.icts.res.in
````

## Create a Slurm job submit script file
First create a Slurm sbatch file
````
vim jupyterLab.sh

Paste the following text into your sbatch script, and save the file

#!/bin/bash
#SBATCH --job-name=jupyter
#SBATCH --partition=long
#SBATCH --time=2-00:00:00
#SBATCH --mem=50GB
#SBATCH --output=$HOME/jupyter/jupyter.log

source /share/anaconda3/bin/activate
export XDG_RUNTIME_DIR=""

cat /etc/hosts
jupyter lab --no-browser --ip=0.0.0.0 --port=8888

#EOF
````

Note: This tells Slurm to launch a Jupyter Lab server on the node with your requested resources, over port 8888.
Now we need to send this as a job to Slurm.

## Submit this sbatch to Slurm:
````
sbatch jupyterLab.sh
````
Note: Now, you can check that your job is running:
````
squeue -u $USER
````

Note:
Once it is running you can continue
Wait few minutes after your job starts for Jupyter to start.
Check the log output to find out the IP we need to use to create an SSH tunnel: (cat ~/jupyter.log)

## Create SSH Tunnel from your laptop
Then on your laptop, open a new Terminal Window and create an SSH tunnel:
````
ssh -L8888:10.10.0.12:8888 hemanta.kumar@mario.icts.res.in
````
Note: You must replace the IP address in the command below with your IP address from "~/jupyter.log" file.
Note: that whatever your log output says for IP you will need to use in the command above. DO NOT just copy and paste the example, you have to replace the IP address to be the one your log output specifies.

## Access Jupyter Notebook
On your laptop open a browser window and you can then browse to:
````
http://0.0.0.0:8888/?token=6af1318e48c14dece229846396ba5bff66cafb41ee171370
````
Note: Replace the “?token=x” part of the URL with your token from step 5
Note:
- You MUST copy the token from the log out put, and cannot just use the example above. It may take up to 10 minutes for the “jupyter.log” output to show you the text with your token.
- For the remainder of your job run, the IP and port will stay the same.
- If you close your laptop you will need to recreate an SSH Tunnel - you can reuse the “ssh -L8888” command above.
- If your job ends on ICTS cluster, you need to resubmit your slurm job, and then modify your SSH Tunnel command with the new IP address.
- If at any time port 8888 seems to already be in use, you can change the port (any above 1024) in your sbatch file, and in the corresponding commands for your SSH tunnel.

REF: https://nero-docs.stanford.edu/jupyter-slurm.html
