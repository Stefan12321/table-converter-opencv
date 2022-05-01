import cv2
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QImage
from converter import parse_pic_to_excel_data, open_image


class Graphics(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.src = None
        self.data = None
        self.setAcceptDrops(True)
        self.resize(1280, 720)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            src = event.mimeData().urls()[0].toString()
            # print(src)
            if src.endswith(".png") or src.endswith(".pdf"):
                event.setDropAction(Qt.CopyAction)
                event.accept()
                self.draw_image(src)


        else:
            event.ignore()

    def draw_image(self, src):
        self.scene.clear()

        src = src.replace('file://', '')
        print(src)
        self.cv_image = open_image(src)
        saved_image = './data/saved_image.png'
        cv2.imwrite(saved_image, self.cv_image)
        self.image = QImage(saved_image)
        item = QGraphicsPixmapItem(QPixmap.fromImage(self.image))
        self.scene.addItem(item)

    def scan_image(self):
        self.scene.clear()
        self.data, cv_image = parse_pic_to_excel_data(self.cv_image)

        saved_image = './data/saved_image.png'
        cv2.imwrite(saved_image, self.cv_image)
        self.image = QImage(saved_image)
        item = QGraphicsPixmapItem(QPixmap.fromImage(self.image))
        self.scene.addItem(item)

    def rotate_image(self) -> None:
        self.scene.clear()
        self.cv_image = cv2.rotate(self.cv_image, cv2.ROTATE_90_CLOCKWISE)
        print(self.cv_image.shape)
        self.scene.setSceneRect(QRectF(0, 0, self.cv_image.shape[1], self.cv_image.shape[0]))
        print(self.scene.sceneRect())
        saved_image = './data/saved_image.png'
        cv2.imwrite(saved_image, self.cv_image)
        self.image = QImage(saved_image)
        item = QGraphicsPixmapItem(QPixmap.fromImage(self.image))
        self.scene.addItem(item)