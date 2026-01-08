#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

os.environ["QT_QPA_PLATFORM"] = "xcb"


from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtGui import QIcon, QPixmap, QDoubleValidator
from PyQt5.QtCore import Qt

class BatteryChargeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Pencere Ayarları
        self.setWindowTitle('Battery Charge Time Calculator')
        # Pencere yüksekliği talimatın üzerine azaltıldı
        self.setFixedWidth(450)
        
        # Dosya yolları
        base_path = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_path, 'icons', 'battcalc.png')
        formula_path = os.path.join(base_path, 'icons', 'battcalc2.png')
        
        # İkon Ayarı
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        layout = QVBoxLayout()

        # Üst Resim (battcalc2.png)
        self.header_label = QLabel()
        if os.path.exists(formula_path):
            pixmap = QPixmap(formula_path)
            self.header_label.setPixmap(pixmap.scaledToWidth(400, Qt.SmoothTransformation))
            self.header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.header_label)

        # Giriş Alanları
        form_layout = QVBoxLayout()

        form_layout.addWidget(QLabel("Source Voltage (Vs) [V]:"))
        self.input_vs = QLineEdit()
        self.input_vs.setValidator(QDoubleValidator(0.0, 1000.0, 2))
        form_layout.addWidget(self.input_vs)

        form_layout.addWidget(QLabel("Charge Current (Icharge) [A]:"))
        self.input_icharge = QLineEdit()
        self.input_icharge.setValidator(QDoubleValidator(0.0, 1000.0, 2))
        form_layout.addWidget(self.input_icharge)

        # Talimat üzerine: "Battery Full Voltage (Vfull)" olarak güncellendi
        form_layout.addWidget(QLabel("Battery Full Voltage (Vfull) [V]:"))
        self.input_vfull = QLineEdit()
        self.input_vfull.setValidator(QDoubleValidator(0.0, 1000.0, 2))
        form_layout.addWidget(self.input_vfull)

        form_layout.addWidget(QLabel("Battery Capacity (Cbatt) [Ah]:"))
        self.input_cbatt = QLineEdit()
        self.input_cbatt.setValidator(QDoubleValidator(0.0, 10000.0, 2))
        form_layout.addWidget(self.input_cbatt)

        form_layout.addWidget(QLabel("Efficiency (η) [%]:"))
        self.input_efficiency = QLineEdit()
        self.input_efficiency.setText("85")
        self.input_efficiency.setValidator(QDoubleValidator(1.0, 100.0, 2))
        form_layout.addWidget(self.input_efficiency)

        layout.addLayout(form_layout)

        # Sonuç Alanı - "Result:" siyah, değer kırmızı
        self.result_container = QLabel()
        self.result_container.setAlignment(Qt.AlignCenter)
        self.update_result_text("00:00")
        layout.addWidget(self.result_container)

        # Butonlar - Alt alta dizildi
        self.calc_button = QPushButton("Calculate")
        # Koyu yeşil üzerine beyaz bold yazı (Qt Palette/StyleSheet mantığıyla)
        self.calc_button.setStyleSheet("background-color: darkgreen; color: white; font-weight: bold;")
        self.calc_button.clicked.connect(self.calculate_time)
        
        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.show_about)
        
        layout.addWidget(self.calc_button)
        layout.addWidget(self.about_button)

        self.setLayout(layout)
        # İçerik yerleşince yüksekliği otomatik ayarla (fazla boşluğu alır)
        self.adjustSize()

    def update_result_text(self, time_val):
        # Rich Text kullanarak Result kelimesini siyah, süreyi kırmızı yaptık
        self.result_container.setText(
            f"<span style='color: black; font-weight: bold; font-size: 16px;'>Result: </span>"
            f"<span style='color: red; font-weight: bold; font-size: 16px;'>{time_val}</span>"
        )

    def calculate_time(self):
        try:
            vs = float(self.input_vs.text().replace(',', '.'))
            icharge = float(self.input_icharge.text().replace(',', '.'))
            vfull = float(self.input_vfull.text().replace(',', '.'))
            cbatt = float(self.input_cbatt.text().replace(',', '.'))
            efficiency = float(self.input_efficiency.text().replace(',', '.')) / 100.0

            if vs <= 0 or icharge <= 0 or vfull <= 0 or cbatt <= 0 or efficiency <= 0:
                raise ValueError()

            # T = (Cbatt * Vfull) / (Vs * Icharge * n)
            total_hours = (cbatt * vfull) / (vs * icharge * efficiency)
            
            hours = int(total_hours)
            minutes = int((total_hours - hours) * 60)

            self.update_result_text(f"{hours:02d}:{minutes:02d}")

        except (ValueError, ZeroDivisionError):
            QMessageBox.warning(self, "Input Error", "Please enter valid numeric values greater than zero.")

    def show_about(self):
        about_box = QMessageBox(self)
        about_box.setWindowTitle("About Battery Charge Time Calculator")
        
        base_path = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_path, 'icons', 'battcalc.png')
        
        if os.path.exists(icon_path):
            about_box.setIconPixmap(QIcon(icon_path).pixmap(64, 64))

        about_text = (
            "<b>Battery Charge Time Calculator</b><br><br>"
            "<b>Version:</b> 1.0.0<br>"
            "<b>License:</b> GNU GPLv3<br>"
            "<b>UI:</b> Python PyQt5<br>"
            "<b>Developer:</b> A. Serhat KILIÇOĞLU (shampuan)<br>"
            "<b>Github:</b> <a href='http://www.github.com/shampuan'>www.github.com/shampuan</a><br><br>"
            "This application calculates the estimated charging time of batteries "
            "based on source voltage, charge current, battery full voltage, and efficiency losses.<br><br>"
            "This program comes with ABSOLUTELY NO WARRANTY.<br><br>"
            "Copyright © 2026 - A. Serhat KILIÇOĞLU"
        )
        
        about_box.setTextFormat(Qt.RichText)
        about_box.setText(about_text)
        about_box.setStandardButtons(QMessageBox.Ok)
        about_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BatteryChargeCalculator()
    ex.show()
    sys.exit(app.exec_())
