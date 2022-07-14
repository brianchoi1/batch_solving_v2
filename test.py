import re

job_read = open('D:\workothers\moldflow_solving\job.txt', "r")
dd = re.findall('\d+', job_read.read())
jobid = str(re.findall('\d+', job_read.read())[0])
print(jobid)
# import os

# path = 'D:/workothers/moldflow_solving'
# file = '2gate_3t_thin_(copy)_(copy_2).sdy'

# os.rename(path+'/'+file, path+'/'+'2gate_3t_thin_(copy)_(c.sdy')
# print('dd')


# fname_list = ['2gate_3t_thin_(copy)_(copy_2).sdy', '3d_3g_25s.sdy']
# charac1 = ')'
# charac2 = ')'
# charac = '()'
# for fname in fname_list:
#     if charac1 in fname or charac2 in fname:
#         print('exist')
#     print('nono')
            # for fname_item in self.fname_list:
            #     if charac1 or charac2 in fname_item:

# fname_list2 = []
# charac = '('
# dd = range(len(charac))
# charac2 = ')'
# for fname in fname_list:
#     if charac in fname:
#         print('exist')    
#     if charac2 in fname:
#         print('exxxxx')
#     else:
#         print('none')
    
#     for x in range(len(charac)):
#         fname = fname.replace(charac[x], "")
#     # for x in range(len(charac2)):
#         # fname = fname.replace(charac2[x], "")
#     fname_list2.append(fname)

# print(fname)

# fname = 'job_2gate_3t_thin_(copy)_(copy_2).sdy'
# fname = str(fname).split('.') 
# fname = str(fname).split(')') 
# print(fname)
#===================================================================================================================


# import paramiko
# ssh = paramiko.SSHClient() 
# ip = 'hpc.lge.com'
# id = 'jaeyoung.choi'
# pw = '1111'
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())       # hpc 접속키 획득
# login_validation = ssh.connect(ip, 22, id, pw)                  # 로그인 유효성 확인
# ssh.exec_command('. /etc/profile;. ~/.bash_profile;. ~/.bashrc; bkill 0')

#===================================================================================================================


# import imp
# import sys
# from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog, QApplication, QTextEdit
# import system_moldflow as smf
# import os
# import time

# # class QText(QWidget):
# #     def __init__(self):
# #         super().__init__()
# #         self.setupUI()

# #     def setupUI(self):
# #         self.txtedt = QTextEdit(self)
# #         self.txtedt.setGeometry(10, 10, 430, 270)
# #         self.txtedt.setText("Moldflow remote solving opened")

# class MyWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         # msg=''
#         self.setupUI()

#     def setupUI(self):
#         self.setGeometry(400, 200, 450, 450)
#         self.setWindowTitle("Moldflow remote solving")
#         self.txtedt = QTextEdit(self)
#         self.txtedt.setGeometry(10, 10, 430, 270)
#         self.txtedt.setText("Moldflow remote solving opened")
#         # self.txtedt.append(msg)
#         btn1 = QPushButton("Open", self)
#         btn1.resize(100,100)
#         btn1.move(30, 330)
#         btn2 = QPushButton("Run", self)
#         btn2.resize(100,100)
#         btn2.move(130, 330)
#         btn3 = QPushButton("Kill", self)
#         btn3.resize(100,100)
#         btn3.move(230, 330)
#         btn3 = QPushButton("Setup", self)
#         btn3.resize(50,30)
#         btn3.move(360, 330)
#         btn1.clicked.connect(pushbtn.pushButtonClicked)
#         # btn2.clicked.connect(pushbtn.pushButtonClicked2)
#     # def pushButtonClicked(self):
#     #     msg = 'ddq'
#     #     self.setupUI(msg)

# class pushbtn():
# #     # mmm = MyWindow()
#     def pushButtonClicked(self):
#         self.txtedt = QTextEdit(self)
#         self.txtedt.setGeometry(10, 10, 430, 270)
# #         mmm = MyWindow()
# #         mmm.txtedt.append('ddd')


#     # def pushButtonClicked2(self):


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     app.exec_()