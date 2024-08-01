import serial
from serial.tools import list_ports
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy, QMessageBox
from PyQt6.QtCore import pyqtSignal, QTimer
from Resources import R
from Widgets import LabeledComboBox

class SerialController(QWidget):
    data_received = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.serial_port = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.read_data)

        self.init_ui()

    def init_ui(self):
        label_width = 40
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setVerticalSpacing(0)
        grid_layout.setHorizontalSpacing(5)

        self.port_combo_box = LabeledComboBox(R.getString("serial_port", "port"), self.get_available_ports())
        self.port_combo_box.label.setFixedWidth(label_width)
        grid_layout.addWidget(self.port_combo_box, 0, 0)

        self.baudrate_combo_box = LabeledComboBox(R.getString("serial_baudrate", "baudrate"), ["9600", "115200"])
        self.baudrate_combo_box.label.setFixedWidth(label_width)
        grid_layout.addWidget(self.baudrate_combo_box, 0, 1)

        self.stopbit_combo_box = LabeledComboBox(R.getString("serial_stopbit", "stopbit"), ["1", "2"])
        self.stopbit_combo_box.label.setFixedWidth(label_width)
        grid_layout.addWidget(self.stopbit_combo_box, 0, 2)

        self.databit_combo_box = LabeledComboBox(R.getString("serial_databit", "databit"), ["8", "7"])
        self.databit_combo_box.label.setFixedWidth(label_width)
        grid_layout.addWidget(self.databit_combo_box, 1, 0)

        self.checkbit_combo_box = LabeledComboBox(R.getString("serial_checkbit", "checkbit"), ["None", "Even", "Odd"])
        self.checkbit_combo_box.label.setFixedWidth(label_width)
        grid_layout.addWidget(self.checkbit_combo_box, 1, 1)

        self.toggle_button = QPushButton(R.getString("serial_open", "open port"))
        self.toggle_button.clicked.connect(self.open_port)
        grid_layout.addWidget(self.toggle_button, 1, 2)

        self.setLayout(grid_layout)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def get_available_ports(self):
        ports = list_ports.comports()
        return [port.device for port in ports]

    def open_port(self):
        try:
            self.serial_port = serial.Serial(
                port=self.port_combo_box.current_text(),
                baudrate=int(self.baudrate_combo_box.current_text()),
                stopbits=int(self.stopbit_combo_box.current_text()),
                bytesize=int(self.databit_combo_box.current_text()),
                parity=self.checkbit_combo_box.current_text()[0].capitalize() if self.checkbit_combo_box.current_text() != "None" else serial.PARITY_NONE,
                timeout=1
            )
            if self.serial_port.is_open:
                print(f"Opened {self.port_combo_box.current_text()}")
                self.toggle_button.clicked.disconnect()
                self.toggle_button.clicked.connect(self.close_port)
                self.toggle_button.setText(R.getString("serial_close", "close port"))
                self.timer.start(100)  # Start the timer to read data every 100 ms
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def close_port(self):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            print(f"Closed {self.port_combo_box.current_text()}")
            self.toggle_button.clicked.disconnect()
            self.toggle_button.clicked.connect(self.open_port)
            self.toggle_button.setText(R.getString("serial_open", "open port"))
            self.timer.stop()  # Stop the timer when the port is closed

    def send_data(self, data):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.write(data.encode())

    def read_data(self):
        if self.serial_port and self.serial_port.is_open:
            if self.serial_port.in_waiting > 0:
                data = self.serial_port.read(self.serial_port.in_waiting).decode()
                self.data_received.emit(data)

    def update_ports(self):
        current_port = self.port_combo_box.current_text() if self.serial_port and self.serial_port.is_open else None
        ports = self.get_available_ports()
        self.port_combo_box.update_items(ports)
        if current_port and current_port in ports:
            self.port_combo_box.set_current_text(current_port)
