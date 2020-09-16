# rgw-status

## Decription
1. The repo contains rgwallhost.py script which captures the status of the rgw daemon in a file named as current-date.log.
2. The repo conatins hostandlog.py which captures the hostname and logfilename from the desired logged in system.

### Pre-requisite
1. The script must be run with the ansible_user from the installer node from where the cluster is deployed.
2. Python3.6 and greater

### To do
1. git clone the repo.
2. Place at /user/homefolder, for eg uname=cephuser, so place in /home/cephuser/file{1..2}.py
3. sudo chmod +x rgwallhost.py , sudo chmod +x hostandlog.py
4. python3 rgwallhost.py ansible_uname ansible_user_password.
5. After above command gets executed, check a new log file is created with current date in -  ~/2020-09-01.log
6. cronatb -e //set for the cronjob for every 5 min
7. x/5 x x x x /usr/bin/python3 /home/user_name/rgwallhost.py

### Observation
1. Output file contains the ssh status :: rgw-node-name ::  timestamp of the rgw daemons
2. Output file contains the job status :: rgw-instance-name ::  timestamp of the rgw daemons


