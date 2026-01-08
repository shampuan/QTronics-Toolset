#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import math
import re

# Environment variable to ensure Qt5 works correctly on GNOME
os.environ["QT_QPA_PLATFORM"] = "xcb"

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox, 
                             QComboBox, QGroupBox, QGridLayout, QTabWidget)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

class FilterCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.icons_dir = os.path.join(self.script_dir, "icons")
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Active-Passive Filter Calculator")
        icon_path = os.path.join(self.icons_dir, "a-cfilter.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Pencere boyutunu sabitle (Active modundaki genişlemeyi kapsayacak şekilde)
        # Genişlik: 550, Yükseklik: 680 (Sabit ve tam ekran yapılamaz)
        self.setFixedSize(550, 680)

        main_layout = QVBoxLayout()
        self.tabs = QTabWidget()
        
        self.tab_lp = self.create_filter_tab("Low Pass Filter", "lowpass.png", "lowopamp.png")
        self.tab_hp = self.create_filter_tab("High Pass Filter", "highpass.png", "highopamp.png")
        
        self.tabs.addTab(self.tab_lp, "Low Pass")
        self.tabs.addTab(self.tab_hp, "High Pass")
        
        main_layout.addWidget(self.tabs)

        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.show_about)
        main_layout.addWidget(self.about_button)

        self.setLayout(main_layout)

    def parse_value(self, text):
        if not text.strip(): return None
        val_str = text.strip().replace(',', '.').lower()
        match = re.match(r"([0-9\.]+)\s*([a-z]*)", val_str)
        if not match:
            return None
            
        number = float(match.group(1))
        suffix = match.group(2)

        multipliers = {
            'm': 1e6, 'k': 1e3,
            'u': 1e-6, 'n': 1e-9, 'p': 1e-12,
            'uf': 1e-6, 'nf': 1e-9, 'pf': 1e-12,
            'khz': 1e3, 'mhz': 1e6
        }

        for s, mult in multipliers.items():
            if suffix.startswith(s):
                return number * mult
                
        return number

    def create_filter_tab(self, title, passive_img, active_img):
        tab = QWidget()
        layout = QVBoxLayout()

        img_label = QLabel()
        img_label.setAlignment(Qt.AlignCenter)
        img_label.setMinimumHeight(250) # Resim alanı için yer ayır
        layout.addWidget(img_label)

        def update_image(is_active):
            img_name = active_img if is_active else passive_img
            img_path = os.path.join(self.icons_dir, img_name)
            if os.path.exists(img_path):
                pixmap = QPixmap(img_path)
                img_label.setPixmap(pixmap.scaledToWidth(500, Qt.SmoothTransformation))
            else:
                img_label.setText(f"{img_name} not found")

        type_combo = QComboBox()
        type_combo.addItems(["Passive (RC)", "Active (Op-Amp)"])
        layout.addWidget(QLabel(f"<b>{title} Type:</b>"))
        layout.addWidget(type_combo)

        group = QGroupBox("Parameters (Supports suffixes like k, M, n, u)")
        grid = QGridLayout()
        
        inputs = {
            'r': QLineEdit(),
            'c': QLineEdit(),
            'rf': QLineEdit(),
            'rin': QLineEdit(),
            'res_fc': QLabel('Cut-off Frequency (fc): <span style="color: red;">-</span>'),
            'res_gain': QLabel('Voltage Gain (Av): <span style="color: red;">-</span>')
        }
        
        inputs['r'].setPlaceholderText("e.g. 10k or 4700")
        inputs['c'].setPlaceholderText("e.g. 100n or 0.1u")

        grid.addWidget(QLabel("Resistor (R):"), 0, 0)
        grid.addWidget(inputs['r'], 0, 1)
        grid.addWidget(QLabel("Capacitor (C):"), 1, 0)
        grid.addWidget(inputs['c'], 1, 1)
        
        lbl_rf = QLabel("Feedback Res. (Rf):")
        lbl_rin = QLabel("Input Res. (Rin):")
        grid.addWidget(lbl_rf, 2, 0)
        grid.addWidget(inputs['rf'], 2, 1)
        grid.addWidget(lbl_rin, 3, 0)
        grid.addWidget(inputs['rin'], 3, 1)
        
        group.setLayout(grid)
        layout.addWidget(group)

        for key in ['res_fc', 'res_gain']:
            inputs[key].setStyleSheet("font-weight: bold; color: black;")
            layout.addWidget(inputs[key])

        btn = QPushButton("Calculate")
        btn.setFixedHeight(35)
        btn.setStyleSheet("background-color: darkgreen; color: white; font-weight: bold;")
        btn.clicked.connect(lambda: self.calculate_logic(inputs, type_combo.currentText()))
        layout.addWidget(btn)

        def toggle():
            is_active = "Active" in type_combo.currentText()
            # Giriş alanlarını göster/gizle
            lbl_rf.setVisible(is_active)
            inputs['rf'].setVisible(is_active)
            lbl_rin.setVisible(is_active)
            inputs['rin'].setVisible(is_active)
            # Resmi güncelle
            update_image(is_active)
        
        type_combo.currentIndexChanged.connect(toggle)
        toggle()

        tab.setLayout(layout)
        return tab

    def calculate_logic(self, inputs, f_type):
        try:
            r = self.parse_value(inputs['r'].text())
            c = self.parse_value(inputs['c'].text())
            if r is None or c is None: raise ValueError
            
            fc = 1 / (2 * math.pi * r * c)
            
            if fc >= 1e6:
                fc_text = f"{fc/1e6:.2f} MHz"
            elif fc >= 1e3:
                fc_text = f"{fc/1e3:.2f} kHz"
            else:
                fc_text = f"{fc:.2f} Hz"
                
            inputs['res_fc'].setText(f'Cut-off Frequency (fc): <span style="color: red;">{fc_text}</span>')

            if "Active" in f_type:
                rf = self.parse_value(inputs['rf'].text())
                rin = self.parse_value(inputs['rin'].text())
                if rf is not None and rin is not None:
                    av = 1 + (rf / rin)
                    db = 20 * math.log10(av) if av > 0 else 0
                    inputs['res_gain'].setText(f'Voltage Gain (Av): <span style="color: red;">{av:.2f} ({db:.2f} dB)</span>')
                else:
                    inputs['res_gain'].setText('Voltage Gain (Av): <span style="color: red;">Missing Rf/Rin</span>')
            else:
                inputs['res_gain'].setText('Voltage Gain (Av): <span style="color: red;">Passive (No Gain)</span>')
        except:
            QMessageBox.critical(self, "Error", "Please enter valid values (e.g. 10k, 100n, 4.7uF).")

    def show_about(self):
        about_box = QMessageBox(self)
        about_box.setWindowTitle("About Filter Calculator")
        icon_path = os.path.join(self.icons_dir, "a-cfilter.png")
        if os.path.exists(icon_path):
            about_box.setWindowIcon(QIcon(icon_path))
            about_box.setIconPixmap(QPixmap(icon_path).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        about_text = f"""
        <div style="text-align: left;">
            <h3>Active-Passive Filter Calculator</h3>
            <br>
            <b>Version:</b> 1.0.0<br>
            <b>License:</b> GPLv3<br>
            <b>UI:</b> PyQt5<br>
            <b>Developer:</b> A. Serhat KILIÇOĞLU (shampuan)<br>
            <b>Github:</b> <a href="http://www.github.com/shampuan">www.github.com/shampuan</a>
            <hr>
            <br>
            This application is designed to calculate the cut-off frequencies and gains of active and passive filter circuits.
            Supports unit suffixes (k, M, n, u, p) for easier calculation.<br><br>
            This program comes with absolutely no warranty.<br><br>
            Copyright © - 2026 - A. Serhat KILIÇOĞLU
        </div>
        """
        about_box.setText(about_text)
        about_box.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = FilterCalculator()
    calc.show()
    sys.exit(app.exec_())
