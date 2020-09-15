#!/usr/bin/python3
import subprocess
import logging
import itertools
import configparser
import paramiko
from datetime import datetime

config = configparser.ConfigParser()

dateTimeObj = datetime.now()
log_name = dateTimeObj.strftime("%Y-%m-%d")

logging.basicConfig(format='%(asctime)s :: %(message)s', level=logging.INFO,
                    filename=log_name+'.log', filemode='a', datefmt='%Y-%m-%d %H:%M:%S')
# change the username and password as the machine
username = "cephuser"
password = "cephuser"

# check for the numbers of rgw hosts from the ansible node
def host_check():
    command = subprocess.run(['sudo', 'ansible', 'rgws', '--list-host', ], stdout=subprocess.PIPE, )
    host_output = command.stdout.decode('utf-8').splitlines()
    host_list = []
    for host_val in host_output:
        host_list.append(host_val.strip(' '))
    rgw_host_list = host_list[1:]
    if rgw_host_list:
        return rgw_host_list
    else:
        command = subprocess.run(['sudo', 'ansible', 'rgws', '--list-host', '-i', '/usr/share/ceph-ansible/hosts'], stdout=subprocess.PIPE, )
        host_output = command.stdout.decode('utf-8').splitlines()
        host_list = []
        for host_val in host_output:
            host_list.append(host_val.strip(' '))
        rgw_host_list = host_list[1:]
        return rgw_host_list


def rgwall(cmd):
    host_list = host_check()
    print(host_list)
    len_host_list = '1'
    len_host_list1 = "150"
    daily_log = '{}.log'.format(log_name)
    # ssh to particular host one by one and check the status and job
    logging.getLogger("paramiko").setLevel(logging.WARNING)
    for rgw_host in host_list:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(hostname=rgw_host, username=username, password=password)
        except:
            print("[!] Cannot connect to SSH Server")
            exit()
        # Setup sftp connection and transmit this script
        sftp = client.open_sftp()
        sftp.put('hostandlog.py', '/tmp/hostandlog.py')
        sftp.close()
        stdout = client.exec_command('python3 /tmp/hostandlog.py')[1]
        host_list = []
        log_list = []
        count = 0
        # take back the value from the hostandlog.py and separate that to two different list file
        # 1st list = hostname and 2nd list = log file name
        for line in stdout:
            # Process each line in the remote output
            if count % 2 == 0:
                host_list.append(line.strip('\n'))
                count += 1
            else:
                log_list.append(line.strip('\n'))
                count += 1
        print(host_list)
        # print(log_list)
        total_rgw_instance = len(log_list)
        client.close()

        for i in range(total_rgw_instance):
            # check rgw status and hostname and log that in log file
            cmd_stat = "sudo systemctl is-active ceph-radosgw@rgw.{}.rgw{}.service".format(host_list[0], i)
            check_stat = subprocess.run(['ssh', rgw_host, cmd_stat], stdout=subprocess.PIPE, )
            check_stat_val = check_stat.stdout.decode('utf-8').strip('\n')
            print(host_list[0]+".rgw"+str(i)+".service"+": "+check_stat_val)
            logging.info("Status: {} :: Hostname: {}".format(check_stat_val, host_list[0]))
            # grep last 150 lines from the rgw_log file
            rgw_log = '/var/log/ceph/ceph-rgw-{}.rgw{}.log'.format(host_list[0], i)
            cmd_stat_rgw = "sudo tail -n {} {}".format(len_host_list1, rgw_log)
            # grep the time from the daily log file and put that in a list
            awk_val = '{print$2}'
            tail_file = subprocess.Popen(['sudo', 'tail', '-n', len_host_list, daily_log], stdout=subprocess.PIPE, )
            grep_date = subprocess.Popen(['grep', host_list[0]], stdin=tail_file.stdout, stdout=subprocess.PIPE, )
            awk_file = subprocess.Popen(['awk', awk_val], stdin=grep_date.stdout, stdout=subprocess.PIPE)
            end_of_pipe = awk_file.stdout
            date_in_daily_conf = []
            log_time = ""
            for line in end_of_pipe:
                date_in_daily_conf.append(line.decode('utf-8').strip())
                log_time = line.decode('utf-8').strip()
            # prints log time of each instance
            print(log_time)

            date_stat = subprocess.Popen(["ssh", rgw_host, cmd_stat_rgw], stdout=subprocess.PIPE)
            date_stat_val = date_stat.stdout
            log_list = []
            for dates in date_stat_val:
                dates_val = dates.decode('utf-8').strip()
                # print(dates_val) # prints single list one by one
                # split whole content into single list
                log_list.append(dates_val.split(" "))
            # combining the list within list to a single list
            res = list(itertools.chain.from_iterable(log_list))
            # matching the dates from rgw_log and custom_log
            single_date = listtoset([i for i in res if i.startswith(log_name)])
            print(single_date)
            # matching the times from rgw_log and custom_log
            # need to configure this part for s3cmd rb & radosgw-admin cmds
            single_time = listtoset([i for i in res if i.startswith(log_time)])
            print(single_time)
            # checking whether http_status is also present in the list, for further confirmation
            single_http_stat = listtoset([i for i in res if i.startswith('http_status')])
            print(single_http_stat)
            # if all 3 are present, node is in working mode else in ideal state
            if single_date and single_time and single_http_stat:
                status = "Working"
                logging.info("JobStatus: {} :: Hostrgw: {}".format(status, host_list[0]))
            else:
                status = "Sleeping"
                logging.info("JobStatus: {} :: Hostrgw: {}.rgw{}".format(status, host_list[0], i))
            star()


def listtoset(list_input):
    return set(list_input)


def rgwallisactive():
    cmd = 'is-active'
    rgwall(cmd)


def rgwallisenabled():
    cmd = 'is-enabled'
    rgwall(cmd)


def rgwallstatus():
    cmd = 'status'
    rgwall(cmd)


def star():
    print("*" * 40)


if __name__ == '__main__':
    rgwallisactive()
