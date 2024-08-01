import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QLabel
from Widgets import  HexView,InputView
from SerialController import SerialController



class Example(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QGridLayout()
        # 创建并展示自定义控件
        self.sc = SerialController()
        main_layout.addWidget(self.sc,0,0)
        main_layout.addWidget(QLabel("111"),0,1)
        main_layout.addWidget(InputView(),1,1)
        # main_layout.addWidget(TextView("          1  2  3  4  5  6  7  8 |Dump\n00000010 11 22 33 44 55 66 77 88 abcdefgh"),1,0)
        self.hex = HexView(b"test Hello a s 1 "*200)
        self.sc.data_received.connect(self.hex.setText)
        main_layout.addWidget(self.hex,1,0)
        self.input = InputView()
        self.input.data_send.connect(self.sc.send_data)
        main_layout.addWidget(self.input,2,0)
        self.setLayout(main_layout)
    



if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    main_widget = Example()
    
    main_widget.show()
    
    sys.exit(app.exec())



