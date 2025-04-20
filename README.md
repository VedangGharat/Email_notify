# TASI_DSSDW Repository

## Introduction
This repository is for integrating all folders, scripts, and files from existing repositories including SQL_TEST, SSIS_TEST, and SFTP_Validator. The structure of this repository is definitely not the final version. It requires contributions from the DSSDW team to improve and evolve.

## Guide
### Clone a Repository Locally
- Ensure that you've already paired access tokens and SSH Keys
- Open your Gitbash, and type: `$ cd C:/Users/[user_name]/source/repos`
- Navigate to GITASI and copy the HTTP url of your target repo
- Go back to Gitbash and type: `$ git clone http://10.100.10.119:9000/DSS-DW/TASI_DSSDW.git`

### Create a New Branch
- Navigate to the GITASI page of your target repo
- Click the link "[number] Branches" located below the repo description
- Create a new branch from the Default Branch
- Follow branch naming conventions as listed [here](#branch-introduction)

### Switch to a Branch
- Navigate into the directory of the cloned repo
- Open Gitbash and type `$ git fetch` to retrieve up-to-date repo changes
- To confirm the branch is available, type `$ git branch -a` to view all local and remote branches
- To switch to the branch, type `$ git checkout [branch name]`

### Sync a Branch / Compare a folder or file between your local test branch and the remote Dev branch
- Right-click a folder or a file
- Click "Open Changes"
- Click "Open Changes with Branch or Tag"
- Choose a branch to compare with

### VS Code Multi-root Workspaces
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

### Branch Introduction
- Prod/TASI_DSSDW
  - Hold the stable and tested version of the code that is ready to be deployed to a production
  - Only accept Pull Requests / Merge Requests from the Dev branch: `Dev/TASI_DSSDW`
  - No parallel development on the Prod branch
- Dev/TASI_DSSDW
  - A branch where ongoing development work takes place
  - It is used for integrating and testing new features, bug fixes, and other changes before they are considered stable and ready for deployment to a production environment
  - Multiple feature branches may be created from the Dev branch to work on different features simultaneously
  - Only accept Pull Requests / Merge Requests from the Feature branches
- Feature/Issue_Name (e.g., Feature/Python_Virtual_Env_Setup)
  - Implement a new feature or work on a specific development task within a project
  - It is used to isolate changes related to a particular feature, allowing developers to work on these changes independently without affecting the main Dev or Prod branch until the feature is completed and tested
  - A remote feature branch should be prepared for a PR and a code review 
- Test/IssueName_DevelopersInitial (e.g., Test/Python_Virtual_Env_Setup_HZ)
  - The Test branch can serve as a safe zone for developers to experiment with code in the repository
  - The Test branch cannot be used for a PR submission; It can only be a local branch