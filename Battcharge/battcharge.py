#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

os.environ["QT_QPA_PLATFORM"] = "xcb"

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt5.QtGui import QPixmap, QIcon, QFont, QPalette, QColor
from PyQt5.QtCore import Qt

class BatteryChargeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def get_resource_path(self, relative_path):
        base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, "icons", relative_path)

    def initUI(self):
        # Pencere Ayarları - Sabit Yükseklik Korundu
        self.setWindowTitle('Battery Charge Calculator')
        self.setFixedSize(480, 600) 
        
        icon_path = self.get_resource_path('battcharge.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(8)

        # Üst Resim
        header_img = QLabel()
        img_path = self.get_resource_path('battcharge2.png')
        if os.path.exists(img_path):
            pixmap = QPixmap(img_path)
            header_img.setPixmap(pixmap.scaled(480, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        header_img.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_img)

        # Giriş Alanları
        self.vs_input = self.create_input_row(main_layout, "Source Voltage (Vs) [V]:")
        self.icharge_rate_input = self.create_input_row(main_layout, "Charge Rate (1/n):")
        self.vmax_input = self.create_input_row(main_layout, "Battery Max Voltage (Vmax) [V]:")
        self.cbatt_input = self.create_input_row(main_layout, "Battery Capacity (Cbatt) [Ah]:")

        # Calculate Butonu - QPalette Yeşil
        self.calc_btn = QPushButton("Calculate")
        btn_font = self.calc_btn.font()
        btn_font.setBold(True)
        self.calc_btn.setFont(btn_font)
        
        palette = self.calc_btn.palette()
        palette.setColor(QPalette.Button, QColor("darkgreen"))
        palette.setColor(QPalette.ButtonText, QColor("white"))
        self.calc_btn.setPalette(palette)
        self.calc_btn.setAutoFillBackground(True) 
        
        self.calc_btn.clicked.connect(self.calculate)
        main_layout.addWidget(self.calc_btn)

        # Sonuç ve Uyarı Ekranı
        self.result_label = QLabel("Waiting for calculation...\n\nNote: Charge rate should be between 4 and 10 for healthy charging.")
        self.result_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.result_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.result_label.setWordWrap(True)
        self.result_label.setFixedHeight(200) # Uyarılar için alan genişletildi
        self.result_label.setMargin(12)
        self.result_label.setTextFormat(Qt.RichText)
        main_layout.addWidget(self.result_label)

        # Hakkında Butonu
        self.about_btn = QPushButton("About")
        self.about_btn.clicked.connect(self.show_about)
        main_layout.addWidget(self.about_btn)

        self.setLayout(main_layout)

    def create_input_row(self, layout, label_text):
        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(0, 0, 0, 0)
        lbl = QLabel(label_text)
        lbl.setFixedWidth(220)
        txt = QLineEdit()
        txt.setAlignment(Qt.AlignLeft) 
        row_layout.addWidget(lbl)
        row_layout.addWidget(txt)
        layout.addWidget(row_widget)
        return txt

    def clean_input(self, text):
        return float(text.replace(',', '.'))

    def calculate(self):
        try:
            vs = self.clean_input(self.vs_input.text())
            rate = self.clean_input(self.icharge_rate_input.text())
            vmax = self.clean_input(self.vmax_input.text())
            cbatt = self.clean_input(self.cbatt_input.text())

            # Temel Hesaplamalar
            icharge = cbatt / rate
            r1 = (vs - vmax) / icharge
            pr1 = (vs - vmax) * icharge

            # LED Direnci (R2) - Tabloya göre tam 166.67 Ohm (18V için)
            # Formül: (Vs - 2.5) / 0.093
            r_led = (vs - 2.5) / 0.093

            # Tampon Şarj (Trickle) - Tablo notu: Kapasite / 200
            i_trickle = cbatt / 200 
            r1_trickle = (vs - vmax) / i_trickle
            pr1_trickle = (vs - vmax) * i_trickle

            fast_charge_tag = ""
            if rate < 10:
                fast_charge_tag = " <font color='red'>(Quick Charge)</font>"

            # Tablodan alınan uyarı notları
            notes = (
                "<br><small>"
                "- Charge rate is recommended between 4 and 10.<br>"
                "- Trickle charge starts when battery reaches max voltage.<br>"
                "<font color='red'>- Lithium batteries should never be trickle charged!</font><br>"
                "- Please check resistor power ratings (Watt) for safety.</small>"
            )
            res_text = (
                f"<b>Charge Current:</b> {icharge:.3f} A{fast_charge_tag}<br>"
                f"<b>Main Resistor (R1):</b> {r1:.2f} Ohm<br>"
                f"<b>Main Resistor Power (Pr1):</b> {pr1:.2f} Watt<br>"
                f"<b>LED Resistor (RLED):</b> {r_led:.2f} Ohm<br>"
                f"-------------------------------------------<br>"
                f"<b>Trickle Charge Current:</b> {i_trickle:.3f} A<br>"
                f"<b>Trickle Resistor (R1_t):</b> {r1_trickle:.2f} Ohm<br>"
                f"<b>Trickle Resistor Power (Pr1_t):</b> {pr1_trickle:.2f} Watt"
                f"{notes}"
            )
            self.result_label.setText(res_text)

        except (ValueError, ZeroDivisionError):
            QMessageBox.critical(self, "Error", "Invalid inputs! Please use numbers.")

    def show_about(self):
        about_box = QMessageBox(self)
        about_box.setWindowTitle("About Battery Charge Calculator")
        icon_path = self.get_resource_path('battcharge.png')
        if os.path.exists(icon_path):
            about_box.setIconPixmap(QIcon(icon_path).pixmap(64, 64))

        about_text = (
            "<b>Battery Charge Calculator</b><br><br>"
            "<b>Version:</b> 1.0.0<br>"
            "<b>License:</b> GNU GPLv3<br>"
            "<b>UI:</b> Python PyQt5<br>"
            "<b>Developer:</b> A. Serhat KILIÇOĞLU (shampuan)<br>"
            "<b>Github:</b> <a href='https://www.github.com/shampuan'>www.github.com/shampuan</a><br><br>"
            "This application calculates essential parameters like resistor values "
            "and power ratings for charging circuits.<br><br>"
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
