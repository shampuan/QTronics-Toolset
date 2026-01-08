#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# GNOME ortamında Qt uygulamalarının platform uyumsuzluğu nedeniyle 
# açılmamasını engellemek için kullanılan kritik ortam değişkeni:
os.environ["QT_QPA_PLATFORM"] = "xcb"

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox, QDialog, QFrame)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

class AboutDialog(QDialog):
    def __init__(self, icon_path):
        super().__init__()
        self.setWindowTitle("About Voltage Divider")
        self.setFixedWidth(420)
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.initUI(icon_path)

    def initUI(self, icon_path):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(25, 20, 25, 20)

        # Program İkonu
        icon_label = QLabel()
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            icon_label.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        # Başlık
        title = QLabel("Voltage Divider Calculator")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Ayırıcı Çizgi
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line1)

        # Bilgiler
        v_lbl = QLabel("<b>Version:</b> 1.0.0")
        layout.addWidget(v_lbl)
        
        l_lbl = QLabel("<b>License:</b> GNU GPLv3")
        layout.addWidget(l_lbl)
        
        u_lbl = QLabel("<b>UI:</b> Python3 PyQt5")
        layout.addWidget(u_lbl)
        
        d_lbl = QLabel("<b>Developer:</b> A. Serhat KILIÇOĞLU (shampuan)")
        layout.addWidget(d_lbl)
        
        github_lbl = QLabel('<b>Github:</b> <a href="https://www.github.com/shampuan" style="color: #3498db; text-decoration: none;">www.github.com/shampuan</a>')
        github_lbl.setOpenExternalLinks(True)
        layout.addWidget(github_lbl)

        # Ayırıcı Çizgi
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line2)

        # Açıklama
        desc_label = QLabel("This is a simple calculator that makes it easy to create a voltage divider to obtain reference voltages with resistors easily.")
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(desc_label)

        # Garanti Reddi
        warranty_label = QLabel("This program comes with ABSOLUTELY NO WARRANTY.")
        warranty_label.setStyleSheet("font-style: italic; color: #555; font-size: 11px;")
        warranty_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(warranty_label)

        # Telif Hakkı
        copyright_label = QLabel("© 2026 - A. Serhat KILIÇOĞLU")
        copyright_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(copyright_label)

        # Tamam Butonu
        ok_btn = QPushButton("OK")
        ok_btn.setFixedWidth(100)
        ok_btn.clicked.connect(self.accept)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(ok_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.adjustSize()

class VoltageDividerCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.icons_dir = os.path.join(base_path, "icons")
        
        self.icon_file = os.path.join(self.icons_dir, "divider.png")
        image_file = os.path.join(self.icons_dir, "voltagedivider.png")

        self.setWindowTitle('Voltage Divider Calculator')
        self.setWindowIcon(QIcon(self.icon_file))
        
        layout = QVBoxLayout()

        # Devre Şeması Görseli
        self.img_label = QLabel(self)
        if os.path.exists(image_file):
            pixmap = QPixmap(image_file)
            self.img_label.setPixmap(pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.img_label.setAlignment(Qt.AlignCenter)
        else:
            self.img_label.setText("Circuit diagram (voltagedivider.png) not found.")
        
        layout.addWidget(self.img_label)

        # Giriş Alanları
        self.inputs = {}
        fields = [
            ('Input Voltage (Vi):', 'Vi'),
            ('Resistor 1 (R1):', 'R1'),
            ('Resistor 2 (R2):', 'R2'),
            ('Output Voltage (Vo):', 'Vo')
        ]

        for label_text, key in fields:
            h_layout = QHBoxLayout()
            lbl = QLabel(label_text)
            edit = QLineEdit()
            edit.setPlaceholderText(f"e.g. 1.5k or 1500")
            h_layout.addWidget(lbl)
            h_layout.addWidget(edit)
            self.inputs[key] = edit
            layout.addLayout(h_layout)

        # Hesaplama Butonu (Koyu Yeşil Arkaplan, Kalın Beyaz Yazı)
        self.calc_btn = QPushButton('Calculate Missing Value')
        self.calc_btn.setStyleSheet("background-color: darkgreen; color: white; font-weight: bold;")
        self.calc_btn.clicked.connect(self.calculate)
        layout.addWidget(self.calc_btn)

        self.clear_btn = QPushButton('Clear All')
        self.clear_btn.clicked.connect(self.clear_fields)
        layout.addWidget(self.clear_btn)

        self.about_btn = QPushButton('About')
        self.about_btn.clicked.connect(self.show_about)
        layout.addWidget(self.about_btn)

        self.setLayout(layout)
        self.setMinimumWidth(450)

    def parse_value(self, text):
        if not text:
            return None
        text = text.lower().replace(',', '.').strip()
        multipliers = {'k': 1000, 'm': 1000000}
        
        unit = text[-1]
        if unit in multipliers:
            try:
                return float(text[:-1]) * multipliers[unit]
            except ValueError:
                return None
        else:
            try:
                return float(text)
            except ValueError:
                return None

    def format_result(self, value):
        if value == int(value):
            return str(int(value))
        return f"{value:.2f}"

    def clear_fields(self):
        for edit in self.inputs.values():
            edit.clear()

    def show_about(self):
        dlg = AboutDialog(self.icon_file)
        dlg.exec_()

    def calculate(self):
        try:
            vi = self.parse_value(self.inputs['Vi'].text())
            r1 = self.parse_value(self.inputs['R1'].text())
            r2 = self.parse_value(self.inputs['R2'].text())
            vo = self.parse_value(self.inputs['Vo'].text())

            if all(v is not None for v in [vi, r1, r2]) and vo is None:
                res = vi * (r2 / (r1 + r2))
                self.inputs['Vo'].setText(self.format_result(res))
            elif all(v is not None for v in [vi, r1, vo]) and r2 is None:
                if (vi - vo) == 0: raise ZeroDivisionError
                res = (vo * r1) / (vi - vo)
                self.inputs['R2'].setText(self.format_result(res))
            elif all(v is not None for v in [vi, r2, vo]) and r1 is None:
                if vo == 0: raise ZeroDivisionError
                res = (r2 * (vi - vo)) / vo
                self.inputs['R1'].setText(self.format_result(res))
            elif all(v is not None for v in [r1, r2, vo]) and vi is None:
                res = vo * (r1 + r2) / r2
                self.inputs['Vi'].setText(self.format_result(res))
            else:
                QMessageBox.warning(self, "Input Error", "Please fill in exactly 3 values to calculate the 4th.")
        except ZeroDivisionError:
            QMessageBox.critical(self, "Calculation Error", "Division by zero! Check your values.")
        except Exception:
            QMessageBox.critical(self, "Error", "Please enter valid numeric values (e.g., 10k, 1.5k, 1500).")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VoltageDividerCalculator()
    ex.show()
    sys.exit(app.exec_())