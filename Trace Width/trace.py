#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import math
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QFrame, QMessageBox)
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QRect

# GNOME xcb/wayland compatibility fix
os.environ["QT_QPA_PLATFORM"] = "xcb"

class PCBTraceCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.trace_width_mm = 0.0
        self.trace_length_mm = 0.0
        
        # Icon Path Configuration
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.icon_path = os.path.join(self.base_path, "icons", "trace.png")
        
        if os.path.exists(self.icon_path):
            self.setWindowIcon(QIcon(self.icon_path))
            
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PCB Trace Width Calculator")
        # Pencere yüksekliğini boşlukları azalttığımız için düşürdük
        self.setFixedSize(480, 510) 

        self.main_layout = QVBoxLayout()
        # Ana layout boşluklarını sıfırlıyoruz
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(15, 10, 15, 10)

        # --- PREVIEW AREA ---
        self.preview_area = PreviewFrame(self)
        self.preview_area.setMinimumHeight(180)
        self.main_layout.addWidget(self.preview_area)

        # Çizim alanı ile sonuçlar arasındaki boşluk
        self.main_layout.addSpacing(10)

        # --- RESULT LABELS ---
        # Recommended Width Row
        width_row = QHBoxLayout()
        self.result_title = QLabel("Recommended Width: ")
        self.result_title.setStyleSheet("font-weight: bold; color: black;")
        self.result_value = QLabel("- mm")
        self.result_value.setStyleSheet("font-weight: bold; color: red;")
        width_row.addWidget(self.result_title)
        width_row.addWidget(self.result_value)
        width_row.addStretch()
        self.main_layout.addLayout(width_row)

        # Extra Info Row (Resistance, Drop, Loss)
        self.extra_info = QLabel("Res: - Ω | Drop: - V | Loss: - W")
        self.extra_info.setStyleSheet("font-size: 11px; color: #444;")
        self.main_layout.addWidget(self.extra_info)

        # Sonuçlar ile giriş alanları arasındaki boşluk
        self.main_layout.addSpacing(10)

        # --- INPUT FIELDS ---
        # Giriş alanlarını birbirine yaklaştırıyoruz
        self.current_input = self.create_input_pair("Current (Amps):", "1.0")
        self.temp_input = self.create_input_pair("Temperature Rise (°C):", "10")
        self.copper_input = self.create_input_pair("Copper Weight (oz/ft²):", "1.0")
        self.length_input = self.create_input_pair("Trace Length (mm):", "50")

        self.main_layout.addSpacing(10)

        # --- BUTTONS ---
        self.calc_button = QPushButton("Calculate")
        self.calc_button.setFixedHeight(40)
        self.calc_button.setStyleSheet("background-color: darkgreen; color: white; font-weight: bold;")
        self.calc_button.clicked.connect(self.calculate_trace)
        self.main_layout.addWidget(self.calc_button)

        self.main_layout.addSpacing(5)

        self.about_button = QPushButton("About")
        self.about_button.setFixedHeight(28)
        self.about_button.clicked.connect(self.show_about)
        self.main_layout.addWidget(self.about_button)

        # En alttaki boşluğu önlemek için yukarı yaslıyoruz
        self.main_layout.addStretch()
        self.setLayout(self.main_layout)

    def create_input_pair(self, label_text, default_val):
        lbl = QLabel(label_text)
        self.main_layout.addWidget(lbl)
        
        line_edit = QLineEdit(default_val)
        line_edit.returnPressed.connect(self.calculate_trace)
        self.main_layout.addWidget(line_edit)
        
        # Her kutucuktan sonraki küçük boşluk
        self.main_layout.addSpacing(4)
        return line_edit

    def calculate_trace(self):
        try:
            I = float(self.current_input.text().replace(',', '.'))
            dT = float(self.temp_input.text().replace(',', '.'))
            oz = float(self.copper_input.text().replace(',', '.'))
            L_mm = float(self.length_input.text().replace(',', '.'))

            k, b, c = 0.048, 0.44, 0.725
            area_mils2 = math.pow((I / (k * math.pow(dT, b))), (1/c))
            thickness_mils = oz * 1.37
            width_mils = area_mils2 / thickness_mils
            self.trace_width_mm = width_mils * 0.0254
            
            thickness_mm = thickness_mils * 0.0254
            area_m2 = (self.trace_width_mm / 1000.0) * (thickness_mm / 1000.0)
            length_m = L_mm / 1000.0
            resistivity_copper = 1.724e-8
            
            resistance = resistivity_copper * (length_m / area_m2)
            voltage_drop = I * resistance
            power_loss = (I ** 2) * resistance

            self.result_value.setText(f"{self.trace_width_mm:.4f} mm")
            self.extra_info.setText(
                f"Res: {resistance:.4f} Ω | "
                f"Drop: {voltage_drop:.4f} V | "
                f"Loss: {power_loss:.4f} W"
            )
            self.preview_area.update_dimensions(self.trace_width_mm, L_mm)

        except Exception:
            self.result_value.setText("Invalid Input")

    def show_about(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("About PCB Trace Width Calculator")
        if os.path.exists(self.icon_path):
            pixmap = QPixmap(self.icon_path)
            msg.setIconPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            msg.setIcon(QMessageBox.Information)
        
        about_content = (
            f"<b>PCB Trace Width Calculator</b><br><br>"
            f"<b>Version:</b> 1.0.0<br>"
            f"<b>License:</b> GNU GPLv3<br>"
            f"<b>UI:</b> Python3-PyQt5<br>"
            f"<b>Developer:</b> A. Serhat KILIÇOĞLU (shampuan)<br>"
            f"<b>Github:</b> <a href='https://www.github.com/shampuan'>www.github.com/shampuan</a><br><br>"
            f"This application calculates the minimum required PCB trace width "
            f"according to IPC-2221 standards and estimates power-related losses.<br><br>"
            f"<i>This program comes with ABSOLUTELY NO WARRANTY.</i><br><br>"
            f"Copyright © 2026 - A. Serhat KILIÇOĞLU"
        )
        msg.setText(about_content)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

class PreviewFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.w_mm = 0.0
        self.l_mm = 50.0
        self.setStyleSheet("background-color: #004d00; border: 2px solid #002d00; border-radius: 4px;")

    def update_dimensions(self, w, l):
        self.w_mm = w
        self.l_mm = l
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.contentsRect()
        center_x, center_y = rect.center().x(), rect.center().y()
        
        # Statik boyutlar
        fixed_w, fixed_h = 220, 35
        trace_rect = QRect(int(center_x - fixed_w/2), int(center_y - fixed_h/2), fixed_w, fixed_h)
        
        painter.fillRect(trace_rect, QColor(57, 255, 20))
        painter.setPen(QPen(QColor(240, 240, 240), 1.2))
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        
        # X Ölçüsü
        start_x, end_x, y_line = trace_rect.left(), trace_rect.right(), trace_rect.top() - 30
        painter.drawLine(start_x, y_line - 5, start_x, y_line + 5)
        painter.drawLine(end_x, y_line - 5, end_x, y_line + 5)
        painter.drawLine(start_x, y_line, end_x, y_line)
        painter.drawText(QRect(start_x, y_line - 22, fixed_w, 20), Qt.AlignCenter, f"{self.l_mm} mm")

        # Y Ölçüsü
        x_line, start_y, end_y = trace_rect.right() + 25, trace_rect.top(), trace_rect.bottom()
        painter.drawLine(x_line - 5, start_y, x_line + 5, start_y)
        painter.drawLine(x_line - 5, end_y, x_line + 5, end_y)
        painter.drawLine(x_line, start_y, x_line, end_y)
        painter.drawText(x_line + 10, center_y + 5, f"{self.w_mm:.2f} mm")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PCBTraceCalculator()
    window.show()
    sys.exit(app.exec_())