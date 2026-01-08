#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox, 
                             QDesktopWidget)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

# GNOME/Wayland ortamında stabilite için
os.environ["QT_QPA_PLATFORM"] = "xcb"

class FiveFiveFiveCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def get_resource_path(self, relative_path):
        """icons klasöründeki dosyalara tam yolu döndürür."""
        base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, "icons", relative_path)

    def parse_value(self, value_str):
        """k, M, n, u gibi birimleri sayısal değerlere dönüştürür."""
        if not value_str or not value_str.strip():
            return None
        
        value_str = value_str.replace(',', '.').strip().lower()
        
        multipliers = {
            'k': 1e3,
            'm': 1e6,
            'u': 1e-6,
            'n': 1e-9,
            'p': 1e-12,
        }

        match = re.match(r"([0-9\.]+)\s*([a-z]*)", value_str)
        if match:
            try:
                num_part = float(match.group(1))
                suffix = match.group(2)
                if suffix and suffix[0] in multipliers:
                    return num_part * multipliers[suffix[0]]
                return num_part
            except ValueError:
                return None
        return None

    def format_frequency(self, freq_hz):
        """Frekans 1000'i geçtiğinde kHz cinsinden formatlar."""
        if freq_hz >= 1000:
            return f"{freq_hz / 1000:.2f} kHz"
        return f"{freq_hz:.2f} Hz"

    def initUI(self):
        self.setWindowTitle('555 Calculator')
        self.setWindowIcon(QIcon(self.get_resource_path('555.png')))
        self.setFixedSize(420, 580)

        main_layout = QVBoxLayout()

        # Üst Kısım: Devre Şeması
        self.schema_label = QLabel(self)
        pixmap = QPixmap(self.get_resource_path('555calc.png'))
        if not pixmap.isNull():
            self.schema_label.setPixmap(pixmap.scaled(400, 220, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.schema_label.setText("Circuit Schema (555calc.png) not found.")
        self.schema_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.schema_label)

        # Giriş Alanları
        input_layout = QVBoxLayout()
        
        input_layout.addWidget(QLabel("Resistor R1 (Ω):"))
        self.r1_input = QLineEdit()
        self.r1_input.setPlaceholderText("e.g. 1k, 10k")
        input_layout.addWidget(self.r1_input)

        input_layout.addWidget(QLabel("Resistor R2 (Ω):"))
        self.r2_input = QLineEdit()
        self.r2_input.setPlaceholderText("e.g. 470, 2.2k")
        input_layout.addWidget(self.r2_input)

        input_layout.addWidget(QLabel("Capacitor C1:"))
        self.c1_input = QLineEdit()
        self.c1_input.setPlaceholderText("e.g. 10u, 100n")
        input_layout.addWidget(self.c1_input)

        input_layout.addWidget(QLabel("Frequency:"))
        self.freq_input = QLineEdit()
        self.freq_input.setPlaceholderText("Result or input frequency")
        input_layout.addWidget(self.freq_input)

        main_layout.addLayout(input_layout)

        # Calculate Butonu
        self.calc_btn = QPushButton("Calculate")
        self.calc_btn.setStyleSheet("background-color: darkgreen; color: white; font-weight: bold;")
        self.calc_btn.setMinimumHeight(40)
        self.calc_btn.clicked.connect(self.calculate_555)
        main_layout.addWidget(self.calc_btn)

        # About Butonu
        self.about_btn = QPushButton("About 555 Calculator")
        self.about_btn.clicked.connect(self.show_about)
        main_layout.addWidget(self.about_btn)

        self.setLayout(main_layout)
        self.center()

    def keyPressEvent(self, event):
        """Herhangi bir inputtayken Enter'a basıldığında hesaplama yap."""
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.calculate_555()
        else:
            super().keyPressEvent(event)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def calculate_555(self):
        try:
            r1_text = self.r1_input.text().strip()
            r2_text = self.r2_input.text().strip()
            c1_text = self.c1_input.text().strip()
            freq_text = self.freq_input.text().strip()

            r1 = self.parse_value(r1_text)
            r2 = self.parse_value(r2_text)
            c1 = self.parse_value(c1_text)
            freq = self.parse_value(freq_text)

            # Boş olan alanı bulma kontrolü
            if r1 is not None and r2 is not None and c1 is not None and not freq_text:
                res = 1.44 / ((r1 + 2 * r2) * c1)
                self.freq_input.setText(self.format_frequency(res))
            
            elif r1 is not None and r2 is not None and freq is not None and not c1_text:
                res = 1.44 / ((r1 + 2 * r2) * freq)
                self.c1_input.setText(f"{res:.10f}")
            
            elif r1 is not None and c1 is not None and freq is not None and not r2_text:
                res = ((1.44 / (freq * c1)) - r1) / 2
                self.r2_input.setText(f"{res:.2f}")
                
            elif r2 is not None and c1 is not None and freq is not None and not r1_text:
                res = (1.44 / (freq * c1)) - (2 * r2)
                self.r1_input.setText(f"{res:.2f}")
            
            else:
                QMessageBox.warning(self, "Input Error", "Please leave exactly one field empty to calculate it.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def show_about(self):
        about_msg = QMessageBox(self)
        about_msg.setWindowTitle("About 555 Calculator")
        
        icon_pix = QPixmap(self.get_resource_path('555.png'))
        if not icon_pix.isNull():
            about_msg.setIconPixmap(icon_pix.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        about_text = (
            "<center><h2>555 Calculator</h2></center><br>"
            "Version: 1.0.0<br>"
            "License: GNU GPLv3<br>"
            "UI: Python3-PyQt5<br>"
            "Developer: A. Serhat KILIÇOĞLU (shampuan)<br>"
            "Github: <a href='https://www.github.com/shampuan'>www.github.com/shampuan</a><br><br>"
            "This program calculates values for a 555 timer circuit.<br><br>"
            "This program comes with ABSOLUTELY NO WARRANTY.<br><br>"
            "Copyright © 2026 - A. Serhat KILIÇOĞLU"
        )
        
        about_msg.setTextFormat(Qt.RichText)
        about_msg.setText(about_text)
        about_msg.setStandardButtons(QMessageBox.Ok)
        about_msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FiveFiveFiveCalculator()
    ex.show()
    sys.exit(app.exec_())