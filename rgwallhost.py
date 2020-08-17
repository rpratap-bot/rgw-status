#!/usr/bin/python3
import subprocess
import logging
from datetime import datetime

dateTimeObj = datetime.now()
log_name = dateTimeObj.strftime("%d-%m-%Y")

logging.basicConfig(format='%(asctime)s :: %(message)s', level=logging.INFO,
                    filename=log_name+'.log', filemode='a')


def rgwhostlist():
    # cat /etc/ceph/ceph.conf | grep ^host | awk '{print $3}' - below cmds works as this one
    file_name = '/etc/ceph/ceph.conf'
    cat_file = subprocess.Popen(['cat', file_name], stdout=subprocess.PIPE, )
    grep_file = subprocess.Popen(['grep', '^host'], stdin=cat_file.stdout, stdout=subprocess.PIPE, )
    awk_val = '{print$3}'
    awk_file = subprocess.Popen(['awk', awk_val], stdin=grep_file.stdout, stdout=subprocess.PIPE)
    end_of_pipe = awk_file.stdout
    # capture the hostname in the list, later can be used for ssh
    rgw_host_list = []
    for rgwhost in end_of_pipe:
        rgw_host_list.append(rgwhost.decode('utf-8').strip())
    return rgw_host_list


def rgwall(cmd):
    host_list = rgwhostlist()
    print('Showing Current: {} status: '.format(cmd))
    for rgwhost in host_list:
        cmd_stat = "systemctl {} ceph-radosgw@rgw.{}.rgw0.service".format(cmd, rgwhost)
        check_stat = subprocess.Popen(["ssh", rgwhost,  cmd_stat], stdout=subprocess.PIPE)
        check_stat_val = check_stat.stdout
        for stat in check_stat_val:
            stat_val = stat.decode('utf-8').strip()
            print(stat_val)
            print(rgwhost)
            logging.info("status: {} :: Hostaname: {}".format(stat_val, rgwhost))


def rgwallisactive():
    cmd = 'is-active'
    rgwall(cmd)


def rgwallisenabled():
    cmd = 'is-enabled'
    rgwall(cmd)


def rgwallstatus():
    cmd = 'status'
    rgwall(cmd)


if __name__ == '__main__':
    print("*" * 40)
    rgwhostlist()
    print("*" * 40)
    # rgwall()
    print("*" * 40)
    rgwallisactive()
    print("*" * 40)
    # rgwallisenabled()
    print("*" * 40)
    # rgwallstatus()
