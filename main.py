from mainwindow import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog
import imghdr
import sys
import os
from manager import decode, encode


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.img_btn.clicked.connect(self.img_btn_clicked)
        self.ui.msg_btn.clicked.connect(self.msg_btn_clicked)

        self.ui.simg_btn.clicked.connect(self.simg_btn_clicked)
        self.ui.key_btn.clicked.connect(self.key_btn_clicked)

        self.ui.hide_btn.clicked.connect(self.hide)
        self.ui.reveal_btn.clicked.connect(self.reveal)

        self.status = ''

    def img_btn_clicked(self):
        img_file_name = QFileDialog.getOpenFileName(self, 'Открыть изображение', '/home')[0]
        self.ui.img_path.setText(img_file_name)

    def msg_btn_clicked(self):
        msg_file_name = QFileDialog.getOpenFileName(self, 'Открыть сообщение', '/home')[0]
        self.ui.msg_path.setText(msg_file_name)

    def simg_btn_clicked(self):
        simg_file_name = QFileDialog.getOpenFileName(self, 'Открыть изображение', '/home')[0]
        self.ui.simg_path.setText(simg_file_name)

    def key_btn_clicked(self):
        key_file_name = QFileDialog.getOpenFileName(self, 'Открыть ключ', '/home')[0]
        self.ui.key_path.setText(key_file_name)

    def hide(self):
        image = self.ui.img_path.text()
        try:
            verify_img = imghdr.what(image)
            if not (verify_img in ['png', 'bmp', 'jpg', 'jpeg']):
                self.status += "Файл изображения неверный.<br>"
        except:
            self.status += "Файл изображения неверный.<br>"
        if image == '':
            self.status += 'Добавьте файл изображения.<br>'
        msg = self.ui.msg_path.text()
        if msg == '':
            if self.ui.msg_plain.toPlainText() == '':
                self.status += 'Добавьте файл сообщения или введите его в области.<br>'
            else:
                msg = self.ui.msg_plain.toPlainText()
        else:
            f_msg = open(msg)
            msg = f_msg.read()
        if msg == '':
            self.status += 'Файл сообщения пуст.<br>'
        N = self.ui.N.text()
        K = self.ui.K.text()
        if N == '':
            self.status += 'Введите значение N.<br>'
        if K == '':
            self.status += 'Введите значение K.<br>'
        if not isinstance(N, int) and N != '' and int(N) < 1:
            self.status += 'Значение N должно быть целым и >= 1.<br>'
        if not isinstance(K, int) and K != '' and int(K) < 1:
            self.status += 'Значение K должно быть целым и >= N.<br>'
        output = os.path.dirname(image) + 'steg_i.png'

        if self.status == '':
            self.ui.status.setText(self.status)
            self.status += encode(image, msg, int(K), int(N), output)
            if 'Встраивание прошло успешно.<br>' in self.status:
                self.ui.status.setText("<font color='Green'>" + self.status + "</font>")
            else:
                self.ui.status.setText("<font color='Red'>" + self.status + "</font>")
        else:
            self.ui.status.setText("<font color='Red'>" + self.status + "</font>")
        self.status = ''

    def reveal(self):
        image = self.ui.simg_path.text()
        if image == '':
            self.status += "Добавьте файл изображения.<br>"
        try:
            verify_img = imghdr.what(image)
            if not (verify_img in ['png', 'bmp', 'jpg', 'jpeg']):
                self.status += 'Файл изображения неверный.<br>'
        except:
            self.status += 'Файл изображения неверный.<br>'
        key = self.ui.key_path.text()
        if key == '':
            self.status += 'Добавьте файл с ключом.<br>'
        output = os.path.dirname(image) + '/output_msg'

        if self.status == '':
            self.status = decode(image, key, output)
            if 'Расшифровка прошла успешно.<br>' in self.status:
                self.ui.status.setText("<font color='Green'>" + self.status + "</font>")
            else:
                self.ui.status.setText("<font color='Red'>" + self.status + "</font>")
        else:
            self.ui.status.setText("<font color='Red'>" + self.status + "</font>")
        self.status = ''


app = QtWidgets.QApplication([])
application = Main()
application.show()

sys.exit(app.exec())