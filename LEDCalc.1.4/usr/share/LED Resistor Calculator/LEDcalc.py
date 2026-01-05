#!/usr/bin/env python3
import sys
import os
import math

# GNOME environment scaling/styling
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox, QTabWidget)
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QColor, QFont
from PyQt5.QtCore import Qt

class LEDResistorCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.app_icon_path = os.path.join(base_path, "icons", "ledres.png")
        series_image_path = os.path.join(base_path, "icons", "LEDcalc.png")
        parallel_image_path = os.path.join(base_path, "icons", "paralel.png")

        self.setWindowTitle('LED Resistor Calculator')
        self.setWindowIcon(QIcon(self.app_icon_path))
        
        # Adjusted window size for formula and labels
        self.setFixedSize(550, 580) 
        
        main_layout = QVBoxLayout()
        self.tabs = QTabWidget()

        # Tab 1: Series Connection
        self.series_tab = QWidget()
        self.setup_series_tab(series_image_path)
        self.tabs.addTab(self.series_tab, "Series Connection")

        # Tab 2: Parallel Connection
        self.parallel_tab = QWidget()
        self.setup_parallel_tab(parallel_image_path)
        self.tabs.addTab(self.parallel_tab, "Parallel Connection")

        main_layout.addWidget(self.tabs)

        # About Button (Bottom)
        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.show_about)
        main_layout.addWidget(self.about_button)

        self.setLayout(main_layout)

    def setup_series_tab(self, image_path):
        layout = QHBoxLayout()
        
        # Left Panel - Image
        image_label = QLabel()
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            image_label.setPixmap(pixmap.scaled(200, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            image_label.setText("Series Image\nnot found")
        layout.addWidget(image_label)

        # Right Panel - Controls
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(10, 5, 10, 5)
        right_layout.setSpacing(2)

        # Formula Label
        formula_label = QLabel("Formula: R = (Vs - (Vf * count)) / If")
        formula_label.setStyleSheet("color: #00008B; font-weight: bold; margin-bottom: 5px;")
        right_layout.addWidget(formula_label)

        right_layout.addWidget(QLabel("Source Voltage (Vs) [Volt]:"))
        self.vs_input = QLineEdit()
        right_layout.addWidget(self.vs_input)

        right_layout.addWidget(QLabel("LED Forward Voltage (Vf) [Volt]:"))
        self.vf_input = QLineEdit()
        right_layout.addWidget(self.vf_input)

        right_layout.addWidget(QLabel("Number of LEDs in Series:"))
        self.led_count_input = QLineEdit("1")
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

        self.pwr_res_label = QLabel("Resistor Power Dissipation: -")
        self.pwr_res_label.setFont(font_bold)
        right_layout.addWidget(self.pwr_res_label)

        self.long_life_calc_label = QLabel("Long Life Calculated: -")
        right_layout.addWidget(self.long_life_calc_label)
        
        self.long_life_std_label = QLabel("Long Life Standard (E24): -")
        self.long_life_std_label.setFont(font_bold)
        palette_long = self.long_life_std_label.palette()
        palette_long.setColor(QPalette.WindowText, QColor(0, 120, 0)) 
        self.long_life_std_label.setPalette(palette_long)
        right_layout.addWidget(self.long_life_std_label)

        info_text = QLabel("Calculated resistance is based on the formula for maximum brightness.")
        info_text.setWordWrap(True)
        info_text.setStyleSheet("font-size: 10px; color: #555;")
        right_layout.addWidget(info_text)

        self.calc_button = QPushButton("Calculate")
        self.apply_button_style(self.calc_button)
        self.calc_button.clicked.connect(self.calculate_series)
        right_layout.addWidget(self.calc_button)

        layout.addLayout(right_layout)
        self.series_tab.setLayout(layout)

    def setup_parallel_tab(self, image_path):
        layout = QHBoxLayout()
        
        # Left Panel - Image
        image_label = QLabel()
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            image_label.setPixmap(pixmap.scaled(200, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            image_label.setText("Parallel Image\nnot found")
        layout.addWidget(image_label)

        # Right Panel - Controls
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(10, 5, 10, 5)
        right_layout.setSpacing(2)

        # Formula Label
        p_formula_label = QLabel("Formula: R = (Vs - Vf) / (If * count)")
        p_formula_label.setStyleSheet("color: #00008B; font-weight: bold; margin-bottom: 5px;")
        right_layout.addWidget(p_formula_label)

        right_layout.addWidget(QLabel("Source Voltage (Vs) [Volt]:"))
        self.p_vs_input = QLineEdit()
        right_layout.addWidget(self.p_vs_input)

        right_layout.addWidget(QLabel("LED Forward Voltage (Vf) [Volt]:"))
        self.p_vf_input = QLineEdit()
        right_layout.addWidget(self.p_vf_input)

        right_layout.addWidget(QLabel("Number of LEDs in Parallel:"))
        self.p_led_count_input = QLineEdit("1")
        right_layout.addWidget(self.p_led_count_input)

        right_layout.addWidget(QLabel("Single LED Current (If) [mA]:"))
        self.p_if_input = QLineEdit()
        right_layout.addWidget(self.p_if_input)

        font_bold = QFont()
        font_bold.setBold(True)

        self.p_calc_res_label = QLabel("Calculated Resistance: -")
        right_layout.addWidget(self.p_calc_res_label)
        
        self.p_std_res_label = QLabel("Suggested Standard (E24): -")
        self.p_std_res_label.setFont(font_bold)
        right_layout.addWidget(self.p_std_res_label)

        self.p_pwr_res_label = QLabel("Resistor Power Dissipation: -")
        self.p_pwr_res_label.setFont(font_bold)
        right_layout.addWidget(self.p_pwr_res_label)

        self.p_long_life_calc_label = QLabel("Long Life Calculated: -")
        right_layout.addWidget(self.p_long_life_calc_label)
        
        self.p_long_life_std_label = QLabel("Long Life Standard (E24): -")
        self.p_long_life_std_label.setFont(font_bold)
        palette_long = self.p_long_life_std_label.palette()
        palette_long.setColor(QPalette.WindowText, QColor(0, 120, 0)) 
        self.p_long_life_std_label.setPalette(palette_long)
        right_layout.addWidget(self.p_long_life_std_label)

        info_text = QLabel("In parallel, total current is (If * count). Vf remains same.")
        info_text.setWordWrap(True)
        info_text.setStyleSheet("font-size: 10px; color: #555;")
        right_layout.addWidget(info_text)

        self.p_calc_button = QPushButton("Calculate")
        self.apply_button_style(self.p_calc_button)
        self.p_calc_button.clicked.connect(self.calculate_parallel)
        right_layout.addWidget(self.p_calc_button)

        layout.addLayout(right_layout)
        self.parallel_tab.setLayout(layout)

    def apply_button_style(self, button):
        font_bold = QFont()
        font_bold.setBold(True)
        button.setAutoFillBackground(True)
        palette = button.palette()
        palette.setColor(QPalette.Button, QColor(139, 0, 0)) 
        palette.setColor(QPalette.ButtonText, Qt.white)      
        button.setPalette(palette)
        button.setFont(font_bold)

    def parse_float(self, text):
        return float(text.replace(',', '.'))

    def format_resistance(self, value):
        if value >= 1000000:
            return f"{value/1000000:.2f} MΩ"
        elif value >= 1000:
            return f"{value/1000:.2f} kΩ"
        else:
            return f"{value:.2f} Ω"

    def find_nearest_standard_e24(self, value):
        if value <= 0: return 0
        e24_base = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 
                    3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]
        exponent = math.floor(math.log10(value))
        multiplier = 10 ** exponent
        base_value = value / multiplier
        potential_bases = e24_base + [10.0]
        nearest_base = min(potential_bases, key=lambda x: abs(x - base_value))
        return round(nearest_base * multiplier, 2)

    def calculate_series(self):
        try:
            vs = self.parse_float(self.vs_input.text())
            vf = self.parse_float(self.vf_input.text())
            count = int(self.led_count_input.text())
            if_ma = self.parse_float(self.if_input.text())
            
            total_vf = vf * count
            if vs <= total_vf:
                QMessageBox.warning(self, "Input Error", "Source voltage must be greater than total LED voltage.")
                return
            
            if_a = if_ma / 1000
            res_val = (vs - total_vf) / if_a
            pwr_val = (vs - total_vf) * if_a
            
            std_val = self.find_nearest_standard_e24(res_val)
            long_res_val = res_val * 2
            long_std_val = self.find_nearest_standard_e24(long_res_val)
            
            self.calc_res_label.setText(f"Calculated Resistance: {self.format_resistance(res_val)}")
            self.std_res_label.setText(f"Suggested Standard (E24): {self.format_resistance(std_val)}")
            self.pwr_res_label.setText(f"Resistor Power Dissipation: {pwr_val:.3f} W")
            self.long_life_calc_label.setText(f"Long Life Calculated: {self.format_resistance(long_res_val)}")
            self.long_life_std_label.setText(f"Long Life Standard (E24): {self.format_resistance(long_std_val)}")
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please enter valid numerical values.")

    def calculate_parallel(self):
        try:
            vs = self.parse_float(self.p_vs_input.text())
            vf = self.parse_float(self.p_vf_input.text())
            count = int(self.p_led_count_input.text())
            if_ma = self.parse_float(self.p_if_input.text())
            
            if vs <= vf:
                QMessageBox.warning(self, "Input Error", "Source voltage must be greater than LED voltage.")
                return
            
            total_if_a = (if_ma * count) / 1000
            res_val = (vs - vf) / total_if_a
            pwr_val = (vs - vf) * total_if_a
            
            std_val = self.find_nearest_standard_e24(res_val)
            long_res_val = res_val * 2
            long_std_val = self.find_nearest_standard_e24(long_res_val)
            
            self.p_calc_res_label.setText(f"Calculated Resistance: {self.format_resistance(res_val)}")
            self.p_std_res_label.setText(f"Suggested Standard (E24): {self.format_resistance(std_val)}")
            self.p_pwr_res_label.setText(f"Resistor Power Dissipation: {pwr_val:.3f} W")
            self.p_long_life_calc_label.setText(f"Long Life Calculated: {self.format_resistance(long_res_val)}")
            self.p_long_life_std_label.setText(f"Long Life Standard (E24): {self.format_resistance(long_std_val)}")
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please enter valid numerical values.")
        except ZeroDivisionError:
            QMessageBox.critical(self, "Input Error", "Total current cannot be zero.")

    def show_about(self):
        about_text = (
            "<h3>About LED Resistor Calculator</h3><hr>"
            "<b>Version:</b> 1.4<br>"
            "<b>License:</b> GNU GPLv3<br>"
            "<b>UI:</b> Python3-PyQt5<br>"
            "<b>Developer:</b> A. Serhat KILIÇOĞLU (shampuan)<br>"
            "<b>Github:</b> <a href='http://www.github.com/shampuan'>www.github.com/shampuan</a><hr>"
            "This program calculates the resistor value and power rating required to run LEDs safely.<br><br>"
            "<i>This program comes with no warranty.</i><hr>"
            "Copyright: (C) 2026 - A. Serhat KILIÇOĞLU"
        )
        
        msg = QMessageBox(self)
        msg.setWindowTitle("About")
        msg.setTextFormat(Qt.RichText)
        msg.setText(about_text)
        pixmap = QPixmap(self.app_icon_path)
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