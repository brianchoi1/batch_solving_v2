import time
import paramiko
import os
import re

ssh = paramiko.SSHClient()                                  #paramiko 셋업
hpc_path_default = '/nas/users/HA'                          #hpc기본주소세팅
path = './'                                                 #경로 접미사
data = open('setting.1').readlines()                        #setting파일 한줄씩 읽어서 변수지정
data = [line.rstrip('\n') for line in data]                 #엔터 제거 공백 제거
ip = 'hpc.lge.com'                                          #hpc주소
id = str(data[1])                                           #아이디 저장
pw = str(data[2])                                           #비번 저장
cmd1 = '. /etc/profile;. ~/.bash_profile;. ~/.bashrc; '   #hpc 기본명령어 
cmd2 = data[0]                                               #solver call
ncpu = 4

def login_check(ssh, ip, id, pw):
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())       # hpc 접속키 획득
    login_validation = ssh.connect(ip, 22, id, pw)                  # 로그인 유효성 확인
    try:
        if login_validation is None:
            login_key = 1
            txt_writing = 'login sucessed'
        else:
            login_key = 0
            txt_writing = 'login failed'
        return login_key, txt_writing
    except:
        txt_writing = 'login failed'
        return txt_writing

def sh_writing(cmd1, cmd2, c_dir, fname):
    try:
        fname = str(fname).split('.')        
        f = open(c_dir[0] + '/' + fname[0] + '.sh', 'w', encoding='utf-8')
        f.write(cmd1 + cmd2 + ' ' + fname[0] + '.' + fname[-1] + ' 2>&1 > job_' + fname[0] + '.txt')
        f.close()
        txt_writing = 'shell script is created'
        return txt_writing
    except:
        txt_writing = 'failed to create shell scripts'
        return txt_writing

def making_folder(ssh, login_key, c_fld, c_dir, hpc_path_default, id, fname_list):
    if login_key == 1:
        ssh.exec_command('mkdir ' + hpc_path_default + '/' + id + '/' + c_fld)
        sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        time.sleep(5)
        try:
            for fname in fname_list:
                upload_file(sftp, c_fld, c_dir, hpc_path_default, id, fname)
                upload_sh(sftp, c_fld, c_dir, hpc_path_default, id, fname)
            con = 1
            txt_writing = 'files are uploaded on HPC'
            return con, txt_writing
        except:
            con = 0
            txt_writing = 'False'
            return con, txt_writing
    else:
        con = 0
        txt_writing = 'Not connected'
        return con, txt_writing

def upload_file(sftp, c_fld, c_dir, hpc_path_default, id, fname):
    sftp.put(c_dir[0] + '/' + fname, hpc_path_default + '/' + id + '/' + c_fld + '/' + fname)
    return
def upload_sh(sftp, c_fld, c_dir, hpc_path_default, id, fname):
    fname = str(fname).split('.')[0]
    sftp.put(c_dir[0] + '/' + fname + '.sh', hpc_path_default + '/' + id + '/' + c_fld + '/' + fname + '.sh')
    return

def bash_shell(con, ssh, hpc_path_default, c_fld, fname_list):
    if con == 1:
        for fname in fname_list:
            ssh_chmod(ssh, hpc_path_default, c_fld)
            ssh_bash(ssh, hpc_path_default, c_fld, fname)
        txt_writing = 'bash run!!'
    else:
        txt_writing = 'fail to run'
    return txt_writing
def ssh_chmod(ssh, hpc_path_default, c_fld):
    ssh.exec_command('chmod -R 777 ' + hpc_path_default + '/' + id + '/' + c_fld)
    return
def ssh_bash(ssh, hpc_path_default, c_fld, fname):
    fname = str(fname).split('.')[0]
    ssh.exec_command('cd ' + hpc_path_default + '/' + id + '/' + c_fld + ';' + hpc_path_default + '/' + id +'/' + c_fld + '/' + fname + '.sh')
    return

######################################################################################################################

def bkill(ssh, ip, id, pw):
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    ssh.connect(ip, 22, id, pw) 
    ssh.exec_command('. /etc/profile;. ~/.bash_profile;. ~/.bashrc; bkill 0')

######################################################################################################################

def job_check_setup(hpc_path_default, c_dir, c_fld, fname, id):
    fname = str(fname).split('.')[0]  
    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    time.sleep(5)
    sftp.get(hpc_path_default + '/' + id + '/' + c_fld + '/' + 'job_' + fname + '.txt', c_dir[0] + '/job_' + fname + '.txt')
    time.sleep(5)
    job_read = open(c_dir[0] + '/job_' + fname + '.txt', "r")
    jobid = str(re.findall('\d+', job_read.read())[-1])
    return jobid

def job_check(hpc_path_default, c_dir, c_fld, job_id, fname_list, i):
    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    ref_string = ["PEND", "RUN", "EXIT", "UNKWN", "DONE"]
    b3 = []
    ssh.exec_command('cd ' + hpc_path_default + '/' + id + '/' + c_fld + ';. /etc/profile;. ~/.bash_profile;. ~/.bashrc; bjobs ' + job_id + ' 2>&1 > ' + job_id + '_status.txt')
    time.sleep(5)
    sftp.get(hpc_path_default + '/' + id + '/' + c_fld + '/' + job_id + '_status.txt', c_dir[0] + '/' + job_id + '_status.txt')
    time.sleep(5)
    f = open(c_dir[0] + '/' + job_id + '_status.txt', "r")
    f_status = f.read()
    f_status_list = f_status.split()
    b3 = list(set(ref_string).intersection(f_status_list))
    b3 = (''.join(b3))
    if b3 == "PEND" or b3 == "UNKWN":
        txt_writing = '|>>>>>>>>>>>>>>>>>>>>|   ' + fname_list[i-1] + '   is   ' + b3 +'   |>>>>>>>>>>>>>>>>>>>>|'
    elif b3 == "RUN":
        txt_writing = '|>>>>>>>>>>>>>>>>>>>>|   ' + fname_list[i-1] + '   is   ' + b3 +'   |>>>>>>>>>>>>>>>>>>>>|'
    elif b3 == "EXIT" or b3 == "DONE":
        txt_writing = '|>>>>>>>>>>>>>>>>>>>>|   ' + fname_list[i-1] + '   is   ' + b3 +'   |>>>>>>>>>>>>>>>>>>>>|'
        # time.sleep(100)
        # stdin, stdout, stderr = ssh.exec_command('cd ' + hpc_path_default + '/' + id + '/' + c_fld + ';. /etc/profile;. ~/.bash_profile;. ~/.bashrc; ls')
        # file_list = []
        # for line in stdout:
        #     file_list.append(line)
        #     sp_line = line.split('\n')
        #     sftp.get(hpc_path_default + '/' + id + '/' + c_fld + '/' + sp_line[0], c_dir[0] + '/' + sp_line[0])
    i -= 1
    return txt_writing, i

