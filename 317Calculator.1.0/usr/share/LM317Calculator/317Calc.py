#!/usr/bin/env python3

import sys
import os

# GNOME ve Wayland ortamlarında Qt5'in ölçekleme/tema sorunlarını gidermek için
os.environ["QT_QPA_PLATFORM"] = "xcb"

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QGroupBox, QGridLayout, QMessageBox)
from PyQt5.QtGui import QPixmap, QDesktopServices, QIcon
from PyQt5.QtCore import Qt, QUrl

class LM317Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.activate_vo_mode()

    def initUI(self):
        self.setWindowTitle('LM317 Calculator')
        self.setFixedWidth(560) 
        
        # --- Paths ---
        base_path = os.path.dirname(os.path.abspath(__file__))
        icons_path = os.path.join(base_path, "icons")
        icon_file = os.path.join(icons_path, "317.png")
        scheme_path = os.path.join(icons_path, "317_scheme.png")
        principle_path = os.path.join(icons_path, "317_principle.png")

        # Set Window Icon
        if os.path.exists(icon_file):
            self.setWindowIcon(QIcon(icon_file))
        
        main_layout = QVBoxLayout()

        # --- Images ---
        image_layout = QHBoxLayout()
        self.lbl_scheme = QLabel()
        pix_scheme = QPixmap(scheme_path)
        if not pix_scheme.isNull():
            self.lbl_scheme.setPixmap(pix_scheme.scaled(240, 220, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        self.lbl_principle = QLabel()
        pix_principle = QPixmap(principle_path)
        if not pix_principle.isNull():
            self.lbl_principle.setPixmap(pix_principle.scaled(240, 220, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        image_layout.addWidget(self.lbl_scheme)
        image_layout.addWidget(self.lbl_principle)
        main_layout.addLayout(image_layout)

        # --- Parameters ---
        input_group = QGroupBox("Calculation Parameters")
        self.grid_layout = QGridLayout()

        self.grid_layout.addWidget(QLabel("Input Voltage (Vi):"), 0, 0)
        self.input_vi = QLineEdit()
        self.input_vi.setPlaceholderText("Enter source voltage")
        self.grid_layout.addWidget(self.input_vi, 0, 1)

        self.grid_layout.addWidget(QLabel("R1 Resistor (Ohm):"), 1, 0)
        self.input_r1 = QLineEdit()
        self.input_r1.setText("240")
        self.grid_layout.addWidget(self.input_r1, 1, 1)

        self.label_r2_title = QLabel("R2 Resistor (Ohm):")
        self.input_r2 = QLineEdit()
        self.result_r2 = QLabel("-")
        self.result_r2.setStyleSheet("color: red; font-weight: bold; font-size: 13px;")
        self.grid_layout.addWidget(self.label_r2_title, 2, 0)
        self.grid_layout.addWidget(self.input_r2, 2, 1)
        self.grid_layout.addWidget(self.result_r2, 2, 1)

        self.label_vo_title = QLabel("Output Voltage (Vo):")
        self.input_vo = QLineEdit()
        self.result_vo = QLabel("-")
        self.result_vo.setStyleSheet("color: red; font-weight: bold; font-size: 13px;")
        self.grid_layout.addWidget(self.label_vo_title, 3, 0)
        self.grid_layout.addWidget(self.input_vo, 3, 1)
        self.grid_layout.addWidget(self.result_vo, 3, 1)

        input_group.setLayout(self.grid_layout)
        main_layout.addWidget(input_group)

        # --- Action Buttons ---
        btn_layout = QHBoxLayout()
        self.btn_calc_vo = QPushButton("Calculate Vo")
        self.btn_calc_r2 = QPushButton("Calculate R2")
        
        # Applying colors while keeping native look
        self.btn_calc_vo.setStyleSheet("background-color: #369934; color: white; font-weight: bold;")
        self.btn_calc_r2.setStyleSheet("background-color: #528cb3; color: white; font-weight: bold;")
        
        self.btn_calc_vo.clicked.connect(self.activate_vo_mode)
        self.btn_calc_r2.clicked.connect(self.activate_r2_mode)
        
        btn_layout.addWidget(self.btn_calc_vo)
        btn_layout.addWidget(self.btn_calc_r2)
        main_layout.addLayout(btn_layout)

        # --- Bottom Buttons ---
        bottom_btn_layout = QHBoxLayout()
        self.btn_about = QPushButton("About")
        self.btn_datasheet = QPushButton("Open Datasheet")
        
        self.btn_about.clicked.connect(self.show_about)
        self.btn_datasheet.clicked.connect(self.open_pdf)
        
        bottom_btn_layout.addWidget(self.btn_about)
        bottom_btn_layout.addWidget(self.btn_datasheet)
        main_layout.addLayout(bottom_btn_layout)

        self.lbl_info = QLabel("")
        self.lbl_info.setAlignment(Qt.AlignCenter)
        self.lbl_info.setStyleSheet("color: #d35400;")
        main_layout.addWidget(self.lbl_info)

        self.setLayout(main_layout)

    def activate_vo_mode(self):
        self.current_mode = "vo"
        self.input_r2.setVisible(True)
        self.result_r2.setVisible(False)
        self.input_vo.setVisible(False)
        self.result_vo.setVisible(True)
        self.calculate()

    def activate_r2_mode(self):
        self.current_mode = "r2"
        self.input_vo.setVisible(True)
        self.result_vo.setVisible(False)
        self.input_r2.setVisible(False)
        self.result_r2.setVisible(True)
        self.calculate()

    def show_about(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_path, "icons", "317.png")
        
        about_text = (
            "<b>About LM317 Calculator</b><br><br>"
            "Version: 1.0.0<br>"
            "License: GNU GPLv3<br>"
            "UI: Python3 PyQt5<br>"
            "Developer: A. Serhat KILIÇOĞLU (shampuan)<br>"
            "Github: <a href='https://www.github.com/shampuan'>www.github.com/shampuan</a><br><br>"
            "Simple LM317 calculator. This program comes with ABSOLUTELY NO WARRANTY.<br><br>"
            "Copyright © 2026 - A. Serhat KILIÇOĞLU"
        )
        msg = QMessageBox(self)
        msg.setWindowTitle("About")
        msg.setTextFormat(Qt.RichText)
        msg.setText(about_text)
        
        if os.path.exists(icon_path):
            pix = QPixmap(icon_path).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            msg.setIconPixmap(pix)
            
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def open_pdf(self):
        pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "LM317.pdf")
        if os.path.exists(pdf_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(pdf_path))
        else:
            QMessageBox.warning(self, "Error", "LM317.pdf not found!")

    def calculate(self):
        self.lbl_info.setText("")
        try:
            vi_text = self.input_vi.text()
            r1_text = self.input_r1.text()
            if not vi_text or not r1_text: return
            
            vi = float(vi_text)
            r1 = float(r1_text)

            if self.current_mode == "vo":
                r2_text = self.input_r2.text()
                if r2_text:
                    r2 = float(r2_text)
                    vo = 1.25 * (1 + (r2 / r1))
                    if vo > (vi - 1.5):
                        self.result_vo.setText("Error (Low Vi)")
                        self.lbl_info.setText(f"Vi ({vi}V) is insufficient for {vo:.2f}V output!")
                    else:
                        self.result_vo.setText(f"{vo:.2f} V")
            
            elif self.current_mode == "r2":
                vo_text = self.input_vo.text()
                if vo_text:
                    vo = float(vo_text)
                    if vo > (vi - 1.5):
                        self.result_r2.setText("Invalid Case")
                        self.lbl_info.setText(f"Low Vi for {vo}V output!")
                    elif vo < 1.25:
                        self.result_r2.setText("Error")
                        self.lbl_info.setText("Min output is 1.25V.")
                    else:
                        r2 = r1 * ((vo / 1.25) - 1)
                        self.result_r2.setText(f"{r2:.1f} Ohm")
        except:
            pass

    def keyReleaseEvent(self, event):
        self.calculate()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LM317Calculator()
    ex.show()
    sys.exit(app.exec_())
