# rgw-status

## Decription
1. The repo contains rgwallhost.py script which captures the status of the rgw daemon in a file named as current-date.log.
2. The repo contains hostandlog.py which captures the hostname and logfilename from the desired logged in system.

### Pre-requisite
1. The script must be run with the ansible_user from the installer node from where the cluster is deployed.
2. Python3.6 and greater

### To do
1. git clone the repo.
    - git clone -b fixingBranch https://github.com/rpratap-bot/rgw-status.git
2. Setup a Python 3 virtual environment.
    - python3 -m venv <path/to/venv>
    - source <path/to/venv>/bin/activate
3. Install requirements 
    - pip3 install -r requirements.txt
4. python3 rgwallhost.py -u ansible_uname -p ansible_user_password.
5. After above command gets executed, check a new log file is created with current date in -  ~/2020-09-01.log
6. cronatb -e //set for the cronjob for every 5 min
7. x/5 x x x x /usr/bin/python3 /home/user_name/rgwallhost.py

### Observation
1. Output file contains the ssh status :: rgw-node-name ::  timestamp of the rgw daemons
2. Output file contains the job status :: rgw-instance-name ::  timestamp of the rgw daemons


