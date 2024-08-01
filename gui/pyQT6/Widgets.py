import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout,QCheckBox, QScrollArea,QPlainTextEdit, QHBoxLayout, QVBoxLayout, QComboBox, QPushButton, QLabel,QSizePolicy
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QMargins,pyqtSignal
from Resources import R

class LabeledComboBox(QWidget):
    def __init__(self, label_text, items, parent=None):
        super().__init__(parent)

        # 创建布局
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)

        # 创建标签
        self.label = QLabel(label_text)
        layout.addWidget(self.label)

        # 创建组合框
        self.combo_box = QComboBox()
        self.combo_box.addItems(items)
        self.combo_box.setEditable(True)
        self.combo_box.setMinimumWidth(90)
        self.combo_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.combo_box)

        self.setLayout(layout)

    def current_text(self):
        return self.combo_box.currentText()


class HexView(QWidget):
    def __init__(self, *args):
        super().__init__(None)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        monospace_font = QFont("Courier New", 12)
        heading = QLabel("         0  1  2  3  4  5  6  7   8  9  A  B  C  D  E  F  |------DUMP-----|  ")
        heading.setFont(monospace_font)
        heading.setContentsMargins(QMargins(10, 0, 2, 0))
        layout.addWidget(heading)
        
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        self.text.setFont(monospace_font)
        
        if len(args) == 1 and isinstance(args[0], str):
            self.setText(args[0].encode('utf-8'))
        elif len(args) == 1 and isinstance(args[0], bytes):
            self.setText(args[0])
        # scroll_area.setWidget(self.text)
        layout.addWidget(self.text)

        self.setLayout(layout)
        # self.setFont(monospace_font)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setStyleSheet("""
            HexView {
                border: 2px solid black;  /* 设置边框宽度和颜色 */
                padding: 10px;  /* 内边距 */
                border-radius: 5px;  /* 圆角边框 */
            }
        """)

    def setText(self,data):
        if isinstance(data,str):
            data = data.encode('utf-8')
        if not isinstance(data,bytes):
            return
        lines = []
        for i in range(0, len(data), 16):
            line = data[i:i+16]  # 取出当前16个字节
            hex_bytes = [f"{byte:02X}" for byte in line]
            # 在第8个字节后插入一个空格
            if len(hex_bytes) > 8:
                hex_bytes.insert(8, "")
            hex_line = " ".join(hex_bytes)
            # 如果不足16字节，补齐空格
            hex_line = hex_line.ljust(48)  # 调整补齐长度

            # 生成ASCII表示，不可见字符用点代替
            ascii_line = "".join(chr(byte) if 32 <= byte <= 126 else '.' for byte in line)
            line_with_offset = f"{i:08X} {hex_line}  {ascii_line}"
            lines.append(line_with_offset)
        text = "\n".join(lines)
        self.text.setPlainText(text)


    class HexLine(QLabel):
        def __init__(self, integer_value: int, byte_array: bytes, parent=None):
            super().__init__(parent)
            self.setFont(QFont("Courier New", 12))  # 设置等宽字体以便更好地显示字节数组
            byte_array_hex = ''.join(f'{byte:02X} ' for byte in byte_array)
            byte_array_str = ''.join(chr(byte) if chr(byte).isprintable() else '.' for byte in byte_array)
            self.setText(f"{integer_value:08X} {byte_array_hex}{byte_array_str}")

class InputView(QWidget):
    data_send = pyqtSignal(str)
    def click_to_send(self):
        self.data_send.emit(self.data.toPlainText())
    def __init__(self):
        super().__init__(None)
        

        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        monospace_font = QFont("Courier New",12)
        self.data = QPlainTextEdit()
        self.data.setFont(monospace_font)
        self.data.setPlainText("test")
        

        layout_buttons = QHBoxLayout()
        layout_buttons.setContentsMargins(0,0,0,0)
        layout_buttons.setSpacing(0)

        self.send = QPushButton(R.getString("serial_send", "send"))
        self.send.clicked.connect(self.click_to_send)
        self.isHex = QCheckBox(R.getString("serial_isHex", "Hex"))
        self.timer = LabeledComboBox(R.getString("serial_timer", "timer"),["0","100","200"])

        layout_buttons.addWidget(self.send)
        layout_buttons.addStretch(1)
        layout_buttons.addWidget(self.timer)
        layout_buttons.addStretch(1)
        layout_buttons.addWidget(self.isHex)

        layout.addWidget(self.data)
        layout.addLayout(layout_buttons)
        self.setLayout(layout)
        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 创建并展示自定义控件
    window = SerialController()
    window.show()
    
    sys.exit(app.exec())
