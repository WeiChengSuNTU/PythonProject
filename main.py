from PyQt6 import QtWidgets, QtGui, QtCore
from main_window import Ui_MainWindow
import csv
import configparser
import promptgenerator
import chat_GPT
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))


#讀取config.ini獲得api_key
config = configparser.ConfigParser()
config.read("config.ini")
api_key = config.get('Settings', 'api_key')



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.on_button_click)

    #顯示輸出照片的函式
    def show_images(self, image_paths):

        scene = QtWidgets.QGraphicsScene(self)


        image_height = self.ui.graphicsView.height()


        image_width = 200  

        # 設定每張圖片的水平間距
        horizontal_spacing = 10

        #給定照片位置x方向的初始值
        x_position = 0

        #從image_paths中依序讀取推薦路徑
        for relative_path in image_paths:

            #判斷relative_path是否存在 以避免錯誤的path造成程式無法運作
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


    #按鍵被按下時要執行的函式：
    def on_button_click(self):
        user_prompt = "" #給定prompt字串，將作為GPT的輸入
        text_content = self.ui.textEdit.toPlainText() #獲取使用者在文字方匡中的輸入
        user_prompt = promptgenerator.prompt_gen(text_content) #藉由promptgenerator.py中的prompt_gen函式生成prompt
        try:
            GPTresponse = chat_GPT.GPT_func(api_key, user_prompt) #將api_key和user_prompt傳給chat_GPT.py中GPT_func
        except Exception as e:
            return f"Error: {e}" #如果失敗 錯誤輸出

        GPTresponse = GPTresponse.split() #將chatGPT的回答切分成id list
        print(GPTresponse)
        image_paths = [] #建立list存放輸出照片的檔案途徑
        with open("data/clothes.csv") as csvfile:
            clothes_list = csv.reader(csvfile) #將csv檔讀取成list
            next(clothes_list)

            #依序從clothes_list讀取cloth 並辨認其輸出id 是否在GPT所推薦的 id list中（GPTresponse）
            for cloth in clothes_list:

                #如果id符合 在image_pathes中新增相對應的照片path
                if cloth[0] in GPTresponse:
                    image_paths.append(cloth[1])
                    print(cloth[1])

        #將image_paths傳給show_images函式
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
