import sys, os
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QGraphicsView, \
    QGraphicsScene, QGraphicsEllipseItem, QGraphicsPixmapItem
from PyQt5.QtCore import Qt, QUrl
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QPen, QColor, QImage

from converter import parse_pic_to_excel_data, open_image, save
from user_interface import Ui_MainWindow


class AppDemo(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.add_functions()

    def add_functions(self):
        self.pushButton.clicked.connect(
            lambda: self.save_file(self.graphicsView.src, self.graphicsView.data) if self.graphicsView.src is not None else None)
        self.pushButton_2.clicked.connect(lambda: self.graphicsView.scan_image())
        self.pushButton_3.clicked.connect(lambda: self.graphicsView.rotate_image())

    def getSelectedItem(self):
        item = QListWidgetItem(self.graphicsView.currentItem())
        return item.text()

    def save_file(self, filename, data):
        print('save')
        save(filename, data)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = AppDemo()
    demo.show()

    sys.exit(app.exec_())
