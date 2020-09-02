#!/usr/bin/python3
import subprocess
import logging
import itertools
import configparser
from datetime import datetime

config = configparser.ConfigParser()

dateTimeObj = datetime.now()
log_name = dateTimeObj.strftime("%Y-%m-%d")

logging.basicConfig(format='%(asctime)s :: %(message)s', level=logging.INFO,
                    filename=log_name+'.log', filemode='a', datefmt='%Y-%m-%d %H:%M:%S')


def host_check():
    command = subprocess.run(['sudo', 'ansible', 'rgws', '--list-host', '-i', '/usr/share/ceph-ansible/hosts'],
                             stdout=subprocess.PIPE, )
    host_output = command.stdout.decode('utf-8').splitlines()
    host_list = []
    for host_val in host_output:
        host_list.append(host_val.strip(' '))
    rgw_host_list = host_list[1:]
    if rgw_host_list:
        return rgw_host_list
    else:
        command = subprocess.run(['sudo', 'ansible', 'rgws', '--list-host'], stdout=subprocess.PIPE, )
        host_output = command.stdout.decode('utf-8').splitlines()
        host_list = []
        for host_val in host_output:
            host_list.append(host_val.strip(' '))
        return rgw_host_list


def rgwall(cmd):
    host_list = host_check()
    print(host_list)
    len_host_list = '1'
    len_host_list1 = "150"
    daily_log = '{}.log'.format(log_name)
    instance_check = subprocess.Popen(['cat', '/usr/share/ceph-ansible/group_vars/all.yml'], stdout=subprocess.PIPE, )
    instance_check_final = subprocess.Popen(['grep', 'radosgw_num_instances:'], stdin=instance_check.stdout, stdout=subprocess.PIPE, )
    instance_val = instance_check_final.stdout
    rgw_inst_count = ""
    for val in instance_val:
        rgw_inst_count = val.decode('utf-8').strip('\n')
    # used for radosgw_num_instances
    if len(rgw_inst_count):
        rgw_inst_cf = rgw_inst_count[-1]
    else:
        rgw_inst_cf = 1
    rgw_inst_cf = int(rgw_inst_cf)
    for i in range(rgw_inst_cf):
        print(i)

    for rgw_host in host_list:
        hostget_1 = subprocess.run(['ssh', rgw_host, 'hostname'], stdout=subprocess.PIPE, )
        hostget_2 = hostget_1.stdout.decode('utf-8').strip('\n')
        print(hostget_2)
        for i in range(rgw_inst_cf):
            cmd_stat = "sudo systemctl is-active ceph-radosgw@rgw.{}.rgw{}.service".format(hostget_2, i)
            check_stat = subprocess.run(['ssh', rgw_host, cmd_stat], stdout=subprocess.PIPE, )
            check_stat_val = check_stat.stdout.decode('utf-8').strip('\n')
            print(hostget_2+".rgw"+str(i)+".service"+": "+check_stat_val)
            logging.info("Status: {} :: Hostname: {}".format(check_stat_val, hostget_2))

            rgw_log = '/var/log/ceph/ceph-rgw-{}.rgw{}.log'.format(hostget_2, i)
            cmd_stat_rgw = "sudo tail -n {} {}".format(len_host_list1, rgw_log)
            awk_val = '{print$2}'
            tail_file = subprocess.Popen(['sudo', 'tail', '-n', len_host_list, daily_log], stdout=subprocess.PIPE, )
            grep_date = subprocess.Popen(['grep', hostget_2], stdin=tail_file.stdout, stdout=subprocess.PIPE, )
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
                logging.info("JobStatus: {} :: Hostrgw: {}".format(status, hostget_2))
            else:
                status = "Sleeping"
                logging.info("JobStatus: {} :: Hostrgw: {}.rgw{}".format(status, hostget_2, i))
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
