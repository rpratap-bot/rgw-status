#!/usr/bin/python3
import subprocess
import logging
import itertools
from datetime import datetime

dateTimeObj = datetime.now()
log_name = dateTimeObj.strftime("%Y-%m-%d")

logging.basicConfig(format='%(asctime)s :: %(message)s', level=logging.INFO,
                    filename='/var/log/'+log_name+'.log', filemode='a', datefmt='%Y-%m-%d %H:%M:%S')


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
    len_host_list = str(len(host_list))
    daily_log = '/var/log/{}.log'.format(log_name)
    print('Showing Current: {} status: '.format(cmd))
    for rgwhost in host_list:
        rgw_log = '/var/log/ceph/ceph-rgw-{}.rgw0.log'.format(rgwhost)
        cmd_stat = "systemctl {} ceph-radosgw@rgw.{}.rgw0.service".format(cmd, rgwhost)
        cmd_stat_rgw = "tail -n {} {}".format(len_host_list, rgw_log)
        # rgw_op_stat = rgwalldate(rgw_log, len_host_list, rgwhost="." )
        check_stat = subprocess.Popen(["ssh", rgwhost,  cmd_stat], stdout=subprocess.PIPE)
        check_stat_val = check_stat.stdout
        for stat in check_stat_val:
            stat_val = stat.decode('utf-8').strip()
            print(stat_val)
            print(rgwhost)
            logging.info("status: {} :: Hostaname: {}".format(stat_val, rgwhost))
        # check the log time of the current node, matching the hostname
        log_time = rgwcurrentlog(daily_log, len_host_list, rgwhost)
        print(log_time)
        # tail -n 3 rgw_log_file on each node
        date_stat = subprocess.Popen(["ssh", rgwhost, cmd_stat_rgw], stdout=subprocess.PIPE)
        date_stat_val = date_stat.stdout
        log_list = []
        for dates in date_stat_val:
            dates_val = dates.decode('utf-8').strip()
            # print(dates_val) # prints single list one by one
            # split whole content into single list
            log_list.append(dates_val.split(" "))
        # combining the list within list to a single list
        res = list(itertools.chain.from_iterable(log_list))
        print(res)
        # matching the dates from rgw_log and custom_log
        single_date = listtoset([i for i in res if i.startswith(log_name)])
        print(single_date)
        # matching the times from rgw_log and custom_log
        # need to configure this part for s3cmd rb
        # need to check something regarding radosgw-admin
        single_time = listtoset([i for i in res if i.startswith(log_time)])
        print(single_time)
        # checking whether http_status is also present in the list, for further confirmation
        single_http_stat = listtoset([i for i in res if i.startswith('http_status')])
        print(single_http_stat)
        # if all 3 are present, node is in working mode else in ideal state
        if single_date and single_time and single_http_stat:
            print("working")
        else:
            print("sleeping")
        star()


def rgwcurrentlog(filename, len_host_list, rgwhost):
    # tail -n len_host_list | grep rgwhost | awk '{print$2}'
    awk_val = '{print$2}'
    tail_file = subprocess.Popen(['tail', '-n', len_host_list, filename], stdout=subprocess.PIPE, )
    grep_date = subprocess.Popen(['grep', rgwhost], stdin=tail_file.stdout, stdout=subprocess.PIPE, )
    awk_file = subprocess.Popen(['awk', awk_val], stdin=grep_date.stdout, stdout=subprocess.PIPE)
    # print(awk_file) # <subprocess.Popen object at 0x7f7d357f9470>
    end_of_pipe = awk_file.stdout
    # print(end_of_pipe) # <_io.BufferedReader name=7>
    date_in_daily_conf = []
    for line in end_of_pipe:
        # print(line.decode('utf-8').strip())
        date_in_daily_conf.append(line.decode('utf-8').strip())
        return line.decode('utf-8').strip()


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
