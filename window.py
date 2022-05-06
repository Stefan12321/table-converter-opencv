import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QFileDialog

from web_table_parser.view.converter import save
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
        self.action.triggered.connect(lambda: self.open_file())

    def getSelectedItem(self):
        item = QListWidgetItem(self.graphicsView.currentItem())
        return item.text()

    def save_file(self, filename, data):
        print('save')
        save(filename, data)

    def open_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file')
        print(fname)
        self.graphicsView.draw_image(fname[0])


if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = AppDemo()
    demo.show()

    sys.exit(app.exec_())
