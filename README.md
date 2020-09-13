# rgw-status

## Decription
1. The repo contains following rgwallhost.py script which captures the status of the rgw daemon in a file named as current-date.log.
2. The repo conatins a output folder, which have some output of the previous output files generated. (Have changed a lot)

### Pre-requisite
1. The script must be run with the ansible_user from the installer node from where the cluster is deployed
2. Python3.6 and greater

### To do
1. Download the rgwallhost.py
2. Place at /user/homefolder, for eg uname=cephuser, so place in /home/cephuser/file.py
3. chmod +x rgwallhost.py
4. python3 rgwallhost.py  or sudo python3 rgwallhost.py (if there is any password issue, try to add/remove sudo from the py file).
5. After above command gets executed, check a new log file is created with current date in -  ~/2020-09-01.log
7. cronatb -e //set for the cronjob for every 5 min
8. x/5 x x x x /usr/bin/python3 /home/user_name/rgwallhost.py

### Observation
1. Output file contains the ssh status :: rgw-node-name ::  timestamp of the rgw daemons
2. Output file contains the job status :: rgw-instance-name ::  timestamp of the rgw daemons

### Work-Around
1. If the script fails foe --list-host option , try to interchange the line 18 with line 28 and re run the script.
2. Trying to fihure out this issue for magna and rhos d vms, will update in few days, for now this is the work around.
