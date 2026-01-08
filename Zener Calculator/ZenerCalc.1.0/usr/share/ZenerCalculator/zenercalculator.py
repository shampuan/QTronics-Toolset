#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# GNOME'da Qt5'in düzgün çalışmasını sağlayan ortam değişkeni
os.environ["QT_QPA_PLATFORM"] = "xcb"

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox, 
                             QFrame)
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt

class ZenerCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Yol tanımlamaları
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.icons_dir = os.path.join(self.base_dir, "icons")
        
        # Pencere Ayarları
        self.setWindowTitle("Zener Calculator")
        self.setWindowIcon(QIcon(os.path.join(self.icons_dir, "zener.png")))
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        # Üst Resim (Devre Şeması)
        self.schema_label = QLabel()
        pixmap = QPixmap(os.path.join(self.icons_dir, "zenercalc.png"))
        if not pixmap.isNull():
            self.schema_label.setPixmap(pixmap.scaledToWidth(380, Qt.SmoothTransformation))
            self.schema_label.setAlignment(Qt.AlignCenter)
        else:
            self.schema_label.setText("Circuit Schema (zenercalc.png not found)")
        layout.addWidget(self.schema_label)

        # Giriş Alanları
        input_layout = QVBoxLayout()
        
        self.inputs = {}
        fields = [
            ("Input Voltage (Vi) [V]:", "vi"),
            ("Max Input Voltage (Vimax):", "vimax"),
            ("Zener Voltage (Vz) [V]:", "vz"),
            ("Load Current (Il) [mA]:", "il")
        ]

        for label_text, key in fields:
            h_layout = QHBoxLayout()
            lbl = QLabel(label_text)
            lbl.setFixedWidth(160)
            self.inputs[key] = QLineEdit()
            if key == "vimax":
                self.inputs[key].setPlaceholderText("Optional (for ripple)")
            h_layout.addWidget(lbl)
            h_layout.addWidget(self.inputs[key])
            input_layout.addLayout(h_layout)

        layout.addLayout(input_layout)

        # Sonuç Alanları (Yan başlıklar siyah, değerler kırmızı)
        self.res_r = QLabel('Resistor (R): <span style="color: red;">-</span>')
        self.res_pr = QLabel('Resistor Power (Pr): <span style="color: red;">-</span>')
        self.res_pz = QLabel('Zener Power (Pz): <span style="color: red;">-</span>')
        
        for res_lbl in [self.res_r, self.res_pr, self.res_pz]:
            res_lbl.setStyleSheet("font-weight: bold; color: black;")
            layout.addWidget(res_lbl)

        # Hesapla Butonu
        self.calc_button = QPushButton("Calculate")
        self.calc_button.setFixedHeight(40)
        self.calc_button.setStyleSheet("background-color: darkgreen; color: white; font-weight: bold;")
        self.calc_button.clicked.connect(self.calculate_zener)
        layout.addWidget(self.calc_button)

        # Hakkında Butonu
        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.show_about)
        layout.addWidget(self.about_button)

        self.setLayout(layout)

    def parse_float(self, text):
        """Virgül veya nokta kullanımını destekleyen sayı dönüştürücü."""
        if not text.strip():
            return None
        return float(text.replace(',', '.'))

    def calculate_zener(self):
        try:
            vi = self.parse_float(self.inputs["vi"].text())
            vz = self.parse_float(self.inputs["vz"].text())
            il_input = self.parse_float(self.inputs["il"].text())
            
            # Vimax kontrolü
            vimax = self.parse_float(self.inputs["vimax"].text())
            if vimax is None:
                vimax = vi

            if vi is None or vz is None or il_input is None:
                raise ValueError("Missing values")

            if vi <= vz or vimax < vi:
                QMessageBox.warning(self, "Error", "Input voltage must be greater than Zener voltage!")
                return

            il = il_input / 1000  # mA to A
            
            # Iz_min (Diz akımı emniyeti için 5mA varsayımı)
            iz_min = 0.005 
            itot = il + iz_min
            
            # Direnç hesaplama (Vi'ye göre)
            r_val = (vi - vz) / itot
            
            # Direnç gücü (Vimax'e göre en kötü durum)
            pr_val = (vimax - vz)**2 / r_val
            
            # Zener gücü (Yük bağlı değilken ve Vimax durumunda en yüksek akım geçer)
            iz_max = (vimax - vz) / r_val
            pz_val = vz * iz_max

            self.res_r.setText(f'Resistor (R): <span style="color: red;">{r_val:.2f} Ohm</span>')
            self.res_pr.setText(f'Resistor Power (Pr): <span style="color: red;">{pr_val:.2f} W</span>')
            self.res_pz.setText(f'Zener Power (Pz): <span style="color: red;">{pz_val:.2f} W</span>')

        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter valid numerical values (use . or , as decimal separator).")

    def show_about(self):
        about_box = QMessageBox(self)
        about_box.setWindowTitle("About Zener Calculator")
        about_box.setWindowIcon(QIcon(os.path.join(self.icons_dir, "zener.png")))
        
        about_text = f"""
        <div style="text-align: left;">
            <h3>Zener Calculator</h3>
            <hr>
            <b>Version:</b> 1.0.0<br>
            <b>License:</b> GNU GPLv3<br>
            <b>UI:</b> Python3 PyQt5<br>
            <b>Developer:</b> A. Serhat KILIÇOĞLU (shampuan)<br>
            <b>Github:</b> <a href="http://www.github.com/shampuan">www.github.com/shampuan</a>
            <hr>
            This program performs calculations to ensure you choose the correct values when working with zener diodes.<br><br>
            This program comes with NO WARRANTY.<br><br>
            Copyright © - 2026 - A. Serhat KILIÇOĞLU
        </div>
        """
        about_box.setText(about_text)
        about_box.setIconPixmap(QIcon(os.path.join(self.icons_dir, "zener.png")).pixmap(64, 64))
        about_box.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = ZenerCalculator()
    calc.show()
    sys.exit(app.exec_())
