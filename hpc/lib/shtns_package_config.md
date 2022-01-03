# install the "shtns" package locally as follow

### step1: First source "base" conda envirolment
```maekdown
source /opt/anaconda3/bin/activate
```

### step2: create a local python envirolment using conda and install some basic required packages
```markdown
conda create --prefix $HOME/<<name>> python numpy scipy matplotlib ipython
```

### step3: activate the above created python envirolment
```markdown
source activate <<name>>
```

### step4: install "shtns" in local python envirolment
```maekdown
conda install -c conda-forge shtns
conda install -c conda-forge/label/cf202003 shtns
```

### to deactivate the python environment
```markdown
conda deactivate
conda deactivate
```

NOTE:
1. you always need to activate the python environment to use it
2. you can install any package using conda or pip into the above create python environment 
