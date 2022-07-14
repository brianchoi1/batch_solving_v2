import imp
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog, QApplication, QTextEdit, QDialog, QLabel, QLineEdit, QGridLayout
import system_moldflow as smf
import os
import time

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(400, 200, 450, 450)
        self.setWindowTitle("Moldflow remote solving")
        self.txtedt = QTextEdit(self)
        self.txtedt.setGeometry(10, 10, 430, 270)
        self.txtedt.setText("Moldflow remote solving opened")
        
        btn1 = QPushButton("Open", self)
        btn1.resize(100,100)
        btn1.move(30, 330)
        btn2 = QPushButton("Run", self)
        btn2.resize(100,100)
        btn2.move(130, 330)
        btn3 = QPushButton("Kill", self)
        btn3.resize(100,100)
        btn3.move(230, 330)
        btn4 = QPushButton("Check", self)
        btn4.resize(50,30)
        btn4.move(360, 330)
        btn5 = QPushButton("Setup", self)
        btn5.resize(50,30)
        btn5.move(360, 370)
        btn1.clicked.connect(self.pushButtonClicked)
        btn2.clicked.connect(self.pushButtonClicked2)
        btn3.clicked.connect(self.pushButtonClicked3)
        btn4.clicked.connect(self.pushButtonClicked4)
        btn5.clicked.connect(self.pushButtonClicked5)


    def pushButtonClicked(self):
        try:
            fname = QFileDialog.getOpenFileNames(self, filter='*.sdy')
            fname = fname[0]                                    # QFileDialog >> Tuple로 받아들여서 >> List로 변환
            self.fname_list0 = []
            self.fname_list = []
            self.c_dir = []
            self.c_dir.append(os.path.dirname(fname[0]))
            self.c_fld = []
            self.c_fld.append(str(self.c_dir[0]).split('/')[-1])
            for fname_item in fname:                            # 다중파일 선택 시 차례대로 파일이름추출
                self.fname_list.append(os.path.basename(fname_item))
            charac1 = '('
            charac2 = ')'
            charac = '()'
            ii = 0
            for fname_item in self.fname_list:
                if charac1 in fname_item or charac2 in fname_item:
                    oldpath = self.c_dir[0] + '/' + fname_item
                    for x in range(len(charac)):                        
                        fname_item = fname_item.replace(charac[x], "")
                    newpath = self.c_dir[0] + '/' + fname_item
                    os.rename(oldpath, newpath)
                    self.fname_list[ii] = fname_item
                self.txtedt.append(fname_item + '   is selected')
                ii += 1
            self.fselect = 1
            self.txtedt.verticalScrollBar().setValue(20000)
            return self.c_dir, self.c_fld, self.fname_list, self.fselect
        except:
            self.fselect = 0
            self.fname_list = []
            self.c_dir = []
            self.c_fld = []
            return self.c_dir, self.c_fld, self.fname_list, self.fselect

    def pushButtonClicked2(self):
        self.jobid_list = []
        try:
            c_fld = self.c_fld[0]
            self.txtedt.append("Run is submitted")
            login_key, msg_login_check = smf.login_check(smf.ssh, smf.ip, smf.id, smf.pw)
            self.txtedt.append(msg_login_check)
            self.txtedt.repaint()
            self.txtedt.verticalScrollBar().setValue(20000)
            time.sleep(5)
            for fname in self.fname_list:
                msg_sh_writing = smf.sh_writing(smf.cmd1, smf.cmd2, self.c_dir, fname)
            self.txtedt.append(msg_sh_writing)
            self.txtedt.repaint()
            self.txtedt.verticalScrollBar().setValue(20000)
            time.sleep(5)
            self.con, msg_making_folder = smf.making_folder(smf.ssh, login_key, c_fld, self.c_dir, smf.hpc_path_default, smf.id, self.fname_list)
            self.txtedt.append(msg_making_folder)
            self.txtedt.repaint()
            self.txtedt.verticalScrollBar().setValue(20000)
            time.sleep(5)
            msg_bash_shell = smf.bash_shell(self.con, smf.ssh, smf.hpc_path_default, c_fld, self.fname_list)
            self.txtedt.append(msg_bash_shell)
            self.txtedt.repaint()
            self.txtedt.verticalScrollBar().setValue(20000)
            time.sleep(5)
            for fname in self.fname_list:
                self.jobid_list.append(smf.job_check_setup(smf.hpc_path_default, self.c_dir, self.c_fld[0], fname, smf.id))
            return self.jobid_list
        except:
            self.txtedt.append("Files should be selected")
            self.txtedt.verticalScrollBar().setValue(20000)

    def pushButtonClicked3(self):
        try:
            smf.bkill(smf.ssh, smf.ip, smf.id, smf.pw)
            self.txtedt.append('Jobs are killed')
            self.txtedt.verticalScrollBar().setValue(20000)
        except:
            self.txtedt.append('Cant be killed')
            self.txtedt.verticalScrollBar().setValue(20000)
            return

    def pushButtonClicked4(self):
        try:
            i = len(self.fname_list)
            for job_id in self.jobid_list:
                txt_writing, i_left = smf.job_check(smf.hpc_path_default, self.c_dir, self.c_fld[0], job_id, self.fname_list, i)
                self.txtedt.append(txt_writing)
                self.txtedt.repaint()
                self.txtedt.verticalScrollBar().setValue(20000)
                # time.sleep(5)
                i = i_left
            return
        except:
            self.txtedt.append('No Jobs IDs')
            return

    def pushButtonClicked5(self):
        dlg = setupDialog()
        dlg.exec_()

class setupDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI_d()

    def setupUI_d(self):
        self.setGeometry(800, 200, 150, 100)
        self.setWindowTitle("Setup")

        label1 = QLabel("HPC ID: ")
        label2 = QLabel("HPC Password: ")
        label3 = QLabel("HPC CPUs: ")

        self.lineEdit1 = QLineEdit(smf.id,self)
        self.lineEdit2 = QLineEdit(smf.pw,self)
        self.lineEdit2.setFixedWidth(100)
        self.lineEdit2.setEchoMode(QLineEdit.Password)
        self.lineEdit3 = QLineEdit('4', self)
        self.pushButton1= QPushButton("OK")
        self.pushButton1.clicked.connect(self.pushButtonClicked)

        layout = QGridLayout()
        layout.addWidget(label1, 0, 0)
        layout.addWidget(self.lineEdit1, 0, 1)
        layout.addWidget(self.pushButton1, 0, 2)
        layout.addWidget(label2, 1, 0)
        layout.addWidget(self.lineEdit2, 1, 1)
        layout.addWidget(label3, 2, 0)
        layout.addWidget(self.lineEdit3, 2, 1)

        self.setLayout(layout)

    def pushButtonClicked(self):
        smf.id = (self.lineEdit1.text())
        smf.pw = (self.lineEdit2.text())
        smf.ncpu = (self.lineEdit3.text())
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()