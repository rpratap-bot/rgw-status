#!/usr/bin/python3
import configparser
import subprocess
config = configparser.ConfigParser()


def hostlog():
    file_name = '/etc/ceph/ceph.conf'
    config.read(file_name)
    all_instances = config.sections()
    # get all the IPs and take the first value which is the IPv4
    hostget_1 = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE, )
    awk_val = '{print $1}'
    hostget_2 = subprocess.Popen(['awk', awk_val], stdin=hostget_1.stdout, stdout=subprocess.PIPE)
    end_of_pipe = hostget_2.stdout
    host_name=[]
    for line in end_of_pipe:
        host_name.append(line.decode('utf-8').strip())
    # list of hostIP , so return the hostIP to a string variable
    host_val = " "
    for i in host_name:
        host_val = i
    # grep the IPv4 from /etc/hosts and cut the last hostname as matching to the host of the system
    hostget_1 = subprocess.Popen(['cat', '/etc/hosts'], stdout=subprocess.PIPE, )
    hostget_2 = subprocess.Popen(['grep', host_val], stdin=hostget_1.stdout, stdout=subprocess.PIPE)
    awk_val = '{print $3}'
    hostget_3 = subprocess.Popen(['awk', awk_val], stdin=hostget_2.stdout, stdout=subprocess.PIPE)
    end_of_pipe = hostget_3.stdout
    host_name=[]
    for line in end_of_pipe:
        host_name.append(line.decode('utf-8').strip())
    # list of hostname , so return the hostname to a string variable
    host_val = " "
    for i in host_name:
        host_val = i
    # match the hostname from the ceph.conf file
    matching = [s for s in all_instances if host_val in s]
    # it will nX2  values, where n >= 1, n = rgw_num_instances
    for i in matching:
        host = config[i]['host']
        log_file = config[i]['log file']
        print(host)
        print(log_file)


if __name__ == '__main__':
    hostlog()

