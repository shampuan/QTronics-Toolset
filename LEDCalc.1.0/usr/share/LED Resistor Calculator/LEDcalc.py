#!/usr/bin/env python3
import sys
import os
import math

# GNOME environment scaling/styling
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QColor, QFont
from PyQt5.QtCore import Qt

class LEDResistorCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        circuit_path = os.path.join(base_path, "icons", "LEDcalc.png")
        app_icon_path = os.path.join(base_path, "icons", "ledres.png")

        self.setWindowTitle('LED Resistor Calculator')
        self.setWindowIcon(QIcon(app_icon_path))
        
        # Compact window size
        self.setFixedSize(500, 430) 
        
        main_layout = QHBoxLayout()

        # Left Panel - Circuit Diagram
        self.image_label = QLabel(self)
        pixmap = QPixmap(circuit_path)
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap.scaled(200, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.image_label.setText("Circuit image\nnot found")
        
        main_layout.addWidget(self.image_label)

        # Right Panel - Controls
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(10, 5, 10, 5)
        right_layout.setSpacing(2)

        right_layout.addWidget(QLabel("Source Voltage (Vs) [Volt]:"))
        self.vs_input = QLineEdit()
        right_layout.addWidget(self.vs_input)

        right_layout.addWidget(QLabel("LED Forward Voltage (Vf) [Volt]:"))
        self.vf_input = QLineEdit()
        right_layout.addWidget(self.vf_input)

        right_layout.addWidget(QLabel("Number of LEDs in Series:"))
        self.led_count_input = QLineEdit()
        self.led_count_input.setText("1")
        right_layout.addWidget(self.led_count_input)

        right_layout.addWidget(QLabel("LED Forward Current (If) [mA]:"))
        self.if_input = QLineEdit()
        right_layout.addWidget(self.if_input)

        font_bold = QFont()
        font_bold.setBold(True)

        self.calc_res_label = QLabel("Calculated Resistance: -")
        right_layout.addWidget(self.calc_res_label)
        
        self.std_res_label = QLabel("Suggested Standard (E24): -")
        self.std_res_label.setFont(font_bold)
        right_layout.addWidget(self.std_res_label)

        self.long_life_calc_label = QLabel("Long Life Calculated: -")
        right_layout.addWidget(self.long_life_calc_label)
        
        self.long_life_std_label = QLabel("Long Life Standard (E24): -")
        self.long_life_std_label.setFont(font_bold)
        palette_long = self.long_life_std_label.palette()
        palette_long.setColor(QPalette.WindowText, QColor(0, 120, 0)) 
        self.long_life_std_label.setPalette(palette_long)
        right_layout.addWidget(self.long_life_std_label)

        # English Info Text
        info_text = QLabel(
            "Calculated resistance is based on the formula for maximum brightness. "
            "For longer LED life, you can sacrifice some brightness by using up to "
            "double the resistance value."
        )
        info_text.setWordWrap(True)
        info_text.setStyleSheet("font-size: 10px; color: #555;")
        right_layout.addWidget(info_text)

        # Calculate Button
        self.calc_button = QPushButton("Calculate")
        self.calc_button.setAutoFillBackground(True)
        calc_palette = self.calc_button.palette()
        calc_palette.setColor(QPalette.Button, QColor(139, 0, 0)) 
        calc_palette.setColor(QPalette.ButtonText, Qt.white)      
        self.calc_button.setPalette(calc_palette)
        self.calc_button.setFont(font_bold)
        self.calc_button.clicked.connect(self.calculate_resistor)
        right_layout.addWidget(self.calc_button)

        # About Button
        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.show_about)
        right_layout.addWidget(self.about_button)

        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

    def parse_float(self, text):
        return float(text.replace(',', '.'))

    def find_nearest_standard_e24(self, value):
        if value <= 0: return 0
        # E24 standard base values
        e24_base = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 
                    3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]
        
        exponent = math.floor(math.log10(value))
        multiplier = 10 ** exponent
        base_value = value / multiplier
        
        potential_bases = e24_base + [10.0]
        nearest_base = min(potential_bases, key=lambda x: abs(x - base_value))
        
        return round(nearest_base * multiplier, 2)

    def calculate_resistor(self):
        try:
            vs = self.parse_float(self.vs_input.text())
            vf = self.parse_float(self.vf_input.text())
            count = int(self.led_count_input.text())
            if_ma = self.parse_float(self.if_input.text())
            
            total_vf = vf * count
            if vs <= total_vf:
                QMessageBox.warning(self, "Input Error", "Source voltage must be greater than total LED voltage.")
                return
                
            res_val = (vs - total_vf) / (if_ma / 1000)
            std_val = self.find_nearest_standard_e24(res_val)
            
            long_res_val = res_val * 2
            long_std_val = self.find_nearest_standard_e24(long_res_val)
            
            self.calc_res_label.setText(f"Calculated Resistance: {res_val:.2f} Ω")
            self.std_res_label.setText(f"Suggested Standard (E24): {std_val} Ω")
            self.long_life_calc_label.setText(f"Long Life Calculated: {long_res_val:.2f} Ω")
            self.long_life_std_label.setText(f"Long Life Standard (E24): {long_std_val} Ω")
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please enter valid numerical values.")

    def show_about(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        app_icon_path = os.path.join(base_path, "icons", "ledres.png")
        
        # English About Content with bold labels
        about_text = (
            "<h3>About LED Resistor Calculator</h3><hr>"
            "<b>Version:</b> 1.0<br>"
            "<b>License:</b> GNU GPLv3<br>"
            "<b>UI:</b> Python3-PyQt5<br>"
            "<b>Developer:</b> A. Serhat KILIÇOĞLU (shampuan)<br>"
            "<b>Github:</b> <a href='http://www.github.com/shampuan'>www.github.com/shampuan</a><hr>"
            "This program calculates the resistor value required to run LEDs safely.<br><br>"
            "<i>This program comes with no warranty.</i><hr>"
            "Copyright: (C) 2026 - A. Serhat KILIÇOĞLU"
        )
        
        msg = QMessageBox(self)
        msg.setWindowTitle("About")
        msg.setTextFormat(Qt.RichText)
        msg.setText(about_text)
        pixmap = QPixmap(app_icon_path)
        if not pixmap.isNull():
            msg.setIconPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        ok_button = msg.addButton(QMessageBox.Ok)
        ok_button.setText("OK")
        msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion") 
    ex = LEDResistorCalculator()
    ex.show()
    sys.exit(app.exec_())