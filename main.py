from PyQt6 import QtWidgets, QtGui, QtCore
from main_window import Ui_MainWindow
import csv
import configparser
import promptgenerator
import chat_GPT
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))


config = configparser.ConfigParser()
config.read("config.ini")
api_key = config.get('Settings', 'api_key')



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.on_button_click)

    def show_images(self, image_paths):

        scene = QtWidgets.QGraphicsScene(self)


        image_height = self.ui.graphicsView.height()


        image_width = 200  

        # 設定每張圖片的水平間距
        horizontal_spacing = 10

        x_position = 0

        for relative_path in image_paths:
            # 創建 QGraphicsPixmapItem 並載入圖片
            #image_path = os.path.relpath(relative_path, start=os.path.dirname(os.path.abspath(__file__)))
            #print(os.path.dirname(os.path.abspath(__file__)))
            #print(relative_path)
            if os.path.exists(relative_path):
                pixmap = QtGui.QPixmap(relative_path)
                pixmap = pixmap.scaled(image_width, image_height)
                item = QtWidgets.QGraphicsPixmapItem(pixmap)

                # 設定 item 的位置
                item.setPos(x_position, 0)

                # 將 item 加入 scene
                scene.addItem(item)

                # 計算下一張圖片的 x 位置
                x_position += image_width + horizontal_spacing

        # 設定 scene 到 graphicsView
        self.ui.graphicsView.setScene(scene)


    def on_button_click(self):
        user_prompt = ""
        text_content = self.ui.textEdit.toPlainText()
        user_prompt = promptgenerator.prompt_gen(text_content)
        try:
            GPTresponse = chat_GPT.GPT_func(api_key, user_prompt)
        except Exception as e:
            return f"Error: {e}"

        GPTresponse = GPTresponse.split()
        print(GPTresponse)
        image_paths = []
        with open("data/clothes.csv") as csvfile:
            clothes_list = csv.reader(csvfile)
            next(clothes_list)
            for cloth in clothes_list:
                if cloth[0] in GPTresponse:
                    image_paths.append(cloth[1])
                    print(cloth[1])

        #print(image_paths)
        self.show_images(image_paths)

if __name__ == "__main__":
    # 創建應用程式實例
    app = QtWidgets.QApplication([])

    # 創建主視窗
    main_window = MainWindow()

    # 顯示主視窗
    main_window.show()

    # 進入應用程式事件迴圈
    app.exec()
