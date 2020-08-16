# rgw-status

## Decription
1. The repo contains following rgwallhost.py script which captures the status of the rgw daemon in a file named with current date.
2. The repo conatins a output folder, which have some output of the previous output files generated.

### Pre-requisite
1. All rgw daemons must talk to each other with ssh-less, both with IP and hostname
2. The script must be run with the cephuser from which the cluster is deployed
3. Python3.6 and greater

### To do
1. Download the rgwallhost.py
2. Place at /user/homefolder, for eg my cephuser is bydefault set to root, so i have placed at /root/
3. chmod +x rgwallhost.py
4. to pre-check if everything is working fine. 
4.1 python3 rgwallhost.py
5. After above command gets executed, check a new file is created with current date. ls , eg - 13-08-2020

### Observation
1. Output file contains the status timestamp of the rgw daemons
