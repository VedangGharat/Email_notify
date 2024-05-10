# TASI_DSSDW Repository

## Introduction
This repository is for integrating all folders, scripts, and files from existing repositories including SQL_TEST, SSIS_TEST, and SFTP_Validator. The structure of this repository is definitely not the final version. It requires contributions from the DSSDW team to improve and evolve.

## Guide
### Clone a Repository Locally
- Ensure that you've already paired access tokens and SSH Keys
- Open your Gitbash, and type: `$ cd C:/Users/[user_name]/source/repos`
- Navigate to GITASI and copy the HTTP url of your target repo
- Go back to Gitbash and type: `$ git clone http://10.100.10.119:9000/DSS-DW/TASI_DSSDW.git`

### Multi-root Workspaces
- Multi-root Workspaces help you work on several related repositories at one time
  - Click `File > Add Folder to Workspace` and add a new root folder
  - Click the `EXPLORER` icon `(Ctrl+Shift+E)` on the left, you should see a new folder has been added
  - Click the `Source Control` icon `(Ctrl+Shift+G)` on the letf to double check if a new repo has been added automatically

### Python Virtual Environment 
- Set up
  - Navigate to the directory: `cd C:/Users/[user_name]/source/repos/[repo_name]`
  - Create a vitual environment: `py -m venv .venv`
  - Activate a virtual environment: `.venv\Scripts\activate`
    - While a virtual environment is activated, pip will install packages into that specific environment
  - Upgrade pip: `py -m pip install --upgrade pip`
  - (Optional) Deactivate virtual environment: `deactivate`
- Install Packages
  - After the virtual environment is activated, install packages: `pip3 install -r requirements.txt`
- Update Package List
  - After the virtual environment is activated and new packages are installed, freeze dependencies: `py -m pip freeze > requirements.txt`
    - This will create a requirements.txt file, that can re-create the exact versions of all packages installed in an environment
    
### .gitignore File
- .venv

