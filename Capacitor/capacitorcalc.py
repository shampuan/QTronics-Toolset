#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# GNOME'da Qt5'in düzgün çalışmasını sağlayan ortam değişkeni
os.environ["QT_QPA_PLATFORM"] = "xcb"

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox, 
                             QGroupBox, QGridLayout)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

class CapacitorCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Yolu en garanti yöntemle (realpath) alıyoruz
        # Bu yöntem, script başka bir klasörden çağrılsa bile dosyanın kendi konumunu bulur.
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.icons_dir = os.path.join(self.script_dir, "icons")
        self.icon_path = os.path.join(self.icons_dir, "cap.png")
        
        # Pencere Ayarları
        self.setWindowTitle("Capacitor Code Converter")
        if os.path.exists(self.icon_path):
            self.setWindowIcon(QIcon(self.icon_path))
        
        self.setMinimumWidth(450)

        layout = QVBoxLayout()

        # Üst Amblem (cap.png)
        self.logo_label = QLabel()
        if os.path.exists(self.icon_path):
            pixmap = QPixmap(self.icon_path)
            self.logo_label.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.logo_label.setAlignment(Qt.AlignCenter)
        else:
            # Hata ayıklama için dosyanın arandığı tam yolu ekrana yazdırıyoruz (Geliştirme aşaması için)
            self.logo_label.setText(f"Icon not found at:\n{self.icon_path}")
            self.logo_label.setAlignment(Qt.AlignCenter)
            self.logo_label.setStyleSheet("color: gray; font-size: 10px;")
            
        layout.addWidget(self.logo_label)

        # --- BÖLÜM 1: Seramik Kondansatör Kod Çözücü ---
        ceramic_group = QGroupBox("Ceramic Capacitor Code (e.g., 104J, 222K)")
        ceramic_layout = QGridLayout()

        ceramic_layout.addWidget(QLabel("Enter Code:"), 0, 0)
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("e.g. 104J")
        ceramic_layout.addWidget(self.code_input, 0, 1)

        self.res_ceramic = QLabel('Result: <span style="color: red;">-</span>')
        self.res_ceramic.setStyleSheet("font-weight: bold; color: black;")
        ceramic_layout.addWidget(self.res_ceramic, 1, 0, 1, 2)

        ceramic_group.setLayout(ceramic_layout)
        layout.addWidget(ceramic_group)

        # --- BÖLÜM 2: Birim Dönüştürücü (Elektrolitik & Genel) ---
        unit_group = QGroupBox("Unit Converter (uF / nF / pF)")
        unit_layout = QGridLayout()

        unit_layout.addWidget(QLabel("Value:"), 0, 0)
        self.val_input = QLineEdit()
        self.val_input.setPlaceholderText("e.g. 0.047")
        unit_layout.addWidget(self.val_input, 0, 1)

        unit_layout.addWidget(QLabel("From Unit:"), 1, 0)
        self.unit_from = QLineEdit()
        self.unit_from.setPlaceholderText("uF, nF or pF")
        unit_layout.addWidget(self.unit_from, 1, 1)

        self.res_unit = QLabel('Converted: <span style="color: red;">-</span>')
        self.res_unit.setStyleSheet("font-weight: bold; color: black;")
        unit_layout.addWidget(self.res_unit, 2, 0, 1, 2)

        unit_group.setLayout(unit_layout)
        layout.addWidget(unit_group)

        # Hesapla Butonu
        self.calc_button = QPushButton("Calculate / Convert")
        self.calc_button.setFixedHeight(40)
        self.calc_button.setStyleSheet("background-color: darkgreen; color: white; font-weight: bold;")
        self.calc_button.clicked.connect(self.perform_calculations)
        layout.addWidget(self.calc_button)

        # Hakkında Butonu
        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.show_about)
        layout.addWidget(self.about_button)

        self.setLayout(layout)

    def parse_float(self, text):
        if not text.strip(): return None
        return float(text.replace(',', '.'))

    def perform_calculations(self):
        code_text = self.code_input.text().strip().upper()
        if code_text:
            self.solve_ceramic(code_text)

        val_text = self.val_input.text().strip()
        unit_text = self.unit_from.text().strip().lower()
        if val_text and unit_text:
            self.convert_units(val_text, unit_text)

    def solve_ceramic(self, code):
        try:
            tolerance_map = {'J': '±5%', 'K': '±10%', 'M': '±20%', 'F': '±1%', 'G': '±2%'}
            tol = ""
            if code[-1].isalpha():
                tol = tolerance_map.get(code[-1], "Unknown")
                num_part = code[:-1]
            else:
                num_part = code

            if len(num_part) >= 3:
                base = int(num_part[:2])
                exp = int(num_part[2:])
                pf_val = base * (10 ** exp)
            else:
                pf_val = int(num_part)

            nf_val = pf_val / 1000
            uf_val = nf_val / 1000

            result_str = f"{pf_val} pF | {nf_val} nF | {uf_val:.6f} uF"
            if tol: result_str += f" (Tol: {tol})"
            
            self.res_ceramic.setText(f'Result: <span style="color: red;">{result_str}</span>')
        except:
            self.res_ceramic.setText('Result: <span style="color: red;">Invalid Code</span>')

    def convert_units(self, val_str, unit):
        try:
            val = self.parse_float(val_str)
            if val is None: return
            
            if unit == "uf":
                nf, pf = val * 1000, val * 1000000
            elif unit == "nf":
                uf, pf = val / 1000, val * 1000
            elif unit == "pf":
                uf, nf = val / 1000000, val / 1000
            else:
                self.res_unit.setText('Converted: <span style="color: red;">Unknown Unit</span>')
                return

            if unit == "uf": res = f"{nf} nF / {pf} pF"
            elif unit == "nf": res = f"{uf:.6f} uF / {pf} pF"
            else: res = f"{uf:.9f} uF / {nf:.6f} nF"

            self.res_unit.setText(f'Converted: <span style="color: red;">{res}</span>')
        except:
            self.res_unit.setText('Converted: <span style="color: red;">Error</span>')

    def show_about(self):
        about_box = QMessageBox(self)
        about_box.setWindowTitle("About Capacitor Converter")
        if os.path.exists(self.icon_path):
            about_box.setWindowIcon(QIcon(self.icon_path))
            about_box.setIconPixmap(QPixmap(self.icon_path).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        about_text = f"""
        <div style="text-align: left;">
            <h3>Capacitor Converter</h3>
            <hr>
            <b>Version:</b> 1.0.0<br>
            <b>License:</b> GNU GPLv3<br>
            <b>Developer:</b> A. Serhat KILIÇOĞLU (shampuan)<br>
            <b>Github:</b> <a href="http://www.github.com/shampuan">www.github.com/shampuan</a>
            <hr>
            Decodes ceramic capacitor codes and converts between uF, nF, and pF.<br><br>
            Copyright © - 2026 - A. Serhat KILIÇOĞLU
        </div>
        """
        about_box.setText(about_text)
        about_box.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = CapacitorCalculator()
    calc.show()
    sys.exit(app.exec_())
