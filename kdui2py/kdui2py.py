'''
Created on 2019年4月6日

@author: bkd
'''
import sys
import optparse
from os.path import expanduser,dirname,join,splitext,basename
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import  QWidget,QApplication,QFileDialog, QMessageBox
from PyQt5.uic.driver import Driver
from .fileutil import get_file_realpath

class kdui2py(QWidget):
    def __init__ (self):
        super().__init__()
        loadUi(get_file_realpath("kdui2py.ui"), self)
        self.preview_widget = QWidget()
    @pyqtSlot()
    def on_pb_convert_single_file_clicked(self):
        seleted_file,_ = QFileDialog.getOpenFileName(self, '转换单个文件', expanduser("~"), '*.ui', '')
        self.convert_single_file(seleted_file)
#     预览UI文件
    @pyqtSlot()
    def on_pb_preview_clicked(self):
        seleted_file,_ = QFileDialog.getOpenFileName(self, '转换单个文件', expanduser("~"), '*.ui', '')
        loadUi(seleted_file,self.preview_widget)
        self.preview_widget.show()
        
#         转换单个文件
    def convert_single_file(self,filename,preview = False):
        if filename :
            base_name = basename(filename)
            output_file = join(dirname(filename),splitext(base_name)[0]+"_ui" +".py")
#             complete sample : opts: {'preview': False, 'output': '/tmp/r.oo', 'execute': False, 'debug': False, 'indent': 4, 'import_from': None, 'from_imports': False, 'resource_suffix': '_ui'}
            opts = optparse.Values()
            opts.ensure_value("preview", preview)
            opts.ensure_value("execute", False)
            opts.ensure_value("debug", False)
            opts.ensure_value("indent", 4)
            opts.ensure_value("from_imports", False)
            opts.ensure_value("import_from", None)
            opts.ensure_value("resource_suffix", "_rc")
            opts.ensure_value("output", output_file)
            args =filename
            driver = Driver(opts,args)
            try:
                exit_status = driver.invoke()
                print(filename,output_file,exit_status)
#                 QMessageBox.information(self, "转换成功", str(exit_status), QMessageBox.Ok)
            except IOError as e:
                QMessageBox.warning(self, "转换异常", str(e), QMessageBox.Ok)
def main():
    app = QApplication(sys.argv)
    win = kdui2py()
    win.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()