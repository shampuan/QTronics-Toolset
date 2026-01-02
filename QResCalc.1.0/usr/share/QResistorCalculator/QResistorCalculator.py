#!/usr/bin/env python3

import sys
import os

# Gnome environment fix
os.environ["QT_QPA_PLATFORM"] = "xcb"

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QComboBox, QPushButton, QLabel, QRadioButton, 
                             QButtonGroup, QDialog, QTabWidget, QLineEdit)
from PyQt5.QtGui import QPixmap, QPainter, QColor, QIcon
from PyQt5.QtCore import Qt

class AboutDialog(QDialog):
    def __init__(self, parent=None, icon_path=None):
        super().__init__(parent)
        self.setWindowTitle("About QResistorCalculator")
        # Pencere boyutu sabitlendi
        self.setFixedSize(380, 420)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        if icon_path and os.path.exists(icon_path):
            icon_label = QLabel()
            pixmap = QPixmap(icon_path).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(pixmap)
            icon_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(icon_label)
        
        text_label = QLabel(
            "<b>About QResistorCalculator:</b><br><br>"
            "License: GNU GPLv3<br>"
            "Version: 1.0.0<br>"
            "UI: PyQt5<br>"
            "Programming language: Python3<br>"
            "Developer: A. Serhat KILIÇOĞLU (shampuan)<br>"
            "Github: <a href='https://www.github.com/shampuan' style='color: #0000ff;'>www.github.com/shampuan</a><br><br>"
            "This is a simple resistor color code calculator.<br><br>"
            "This program comes with ABSOLUTELY NO WARRANTY.<br><br>"
            "Copyright: © 2026 - A. Serhat KILIÇOĞLU"
        )
        text_label.setOpenExternalLinks(True)
        text_label.setWordWrap(True)
        text_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(text_label)
        
        layout.addStretch()
        
        close_btn = QPushButton("OK")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)

class ResistorCalculator(QWidget):
    def __init__(self):
        super().__init__()
        
        # Dinamik dizin belirleme: Scriptin bulunduğu dizini baz alır
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.icons_path = os.path.join(base_dir, "colors")
        self.main_icon_path = os.path.join(self.icons_path, "qresistorcalculator.png")
        
        self.colors_data = [
            ("Black", 0, 1, None, "#000000"),
            ("Brown", 1, 10, 1, "#8B4513"),
            ("Red", 2, 100, 2, "#FF0000"),
            ("Orange", 3, 1000, None, "#FFA500"),
            ("Yellow", 4, 10000, None, "#FFFF00"),
            ("Green", 5, 100000, 0.5, "#008000"),
            ("Blue", 6, 1000000, 0.25, "#0000FF"),
            ("Violet", 7, 10000000, 0.1, "#EE82EE"),
            ("Grey", 8, None, 0.05, "#808080"),
            ("White", 9, None, None, "#FFFFFF"),
            ("Gold", None, 0.1, 5, "#FFD700"),
            ("Silver", None, 0.01, 10, "#C0C0C0")
        ]
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle("QResistorCalculator")
        # Genişlik %10 azaltıldı (495px), Yükseklik azaltıldı (380px)
        self.setFixedSize(495, 380)
        
        if os.path.exists(self.main_icon_path):
            self.setWindowIcon(QIcon(self.main_icon_path))

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(15, 10, 15, 10)
        
        # Radio Buttons
        self.radio_layout = QHBoxLayout()
        self.radio_group = QButtonGroup(self)
        self.radio_4band = QRadioButton("4-colors")
        self.radio_5band = QRadioButton("5-colors")
        self.radio_4band.setChecked(True)
        self.radio_group.addButton(self.radio_4band)
        self.radio_group.addButton(self.radio_5band)
        self.radio_layout.addStretch()
        self.radio_layout.addWidget(self.radio_4band)
        self.radio_layout.addSpacing(30)
        self.radio_layout.addWidget(self.radio_5band)
        self.radio_layout.addStretch()
        self.main_layout.addLayout(self.radio_layout)
        
        # Resistor Display
        self.resistor_display = QLabel()
        self.resistor_display.setFixedSize(229, 76)
        display_container = QHBoxLayout()
        display_container.addStretch()
        display_container.addWidget(self.resistor_display)
        display_container.addStretch()
        self.main_layout.addLayout(display_container)

        # Tabs
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab1, "Colors to Value")
        self.tabs.addTab(self.tab2, "Value to Colors")
        
        self.setup_tab1()
        self.setup_tab2()
        self.main_layout.addWidget(self.tabs)

        # Footer
        self.about_button = QPushButton("About")
        self.about_button.setFixedWidth(80)
        self.about_button.clicked.connect(self.show_about)
        self.main_layout.addWidget(self.about_button, alignment=Qt.AlignRight)

        self.setLayout(self.main_layout)

        # Signals for Resetting
        self.radio_4band.toggled.connect(self.reset_all)
        self.tabs.currentChanged.connect(self.reset_all)
        
        self.reset_all()

    def setup_tab1(self):
        layout = QVBoxLayout()
        self.result_label = QLabel("Please make a selection")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 5px;")
        layout.addWidget(self.result_label)

        self.combo_container = QHBoxLayout()
        self.combos = []
        labels = ["Band 1", "Band 2", "Band 3", "Multiplier", "Tolerance"]
        for i in range(5):
            v_box = QVBoxLayout()
            lbl = QLabel(labels[i])
            lbl.setAlignment(Qt.AlignCenter)
            combo = QComboBox()
            combo.addItem("Select")
            for name, val, mult, tol, hex_code in self.colors_data:
                if i < 3 and val is None: continue
                if i == 3 and mult is None: continue
                if i == 4 and tol is None: continue
                combo.addItem(name)
                combo.setItemData(combo.count()-1, QColor(hex_code), Qt.DecorationRole)
            combo.currentIndexChanged.connect(self.update_image_from_combos)
            self.combos.append(combo)
            v_box.addWidget(lbl)
            v_box.addWidget(combo)
            self.combo_container.addLayout(v_box)
        layout.addLayout(self.combo_container)
        
        calc_btn = QPushButton("Calculate")
        calc_btn.clicked.connect(self.calculate_from_colors)
        layout.addWidget(calc_btn)
        self.tab1.setLayout(layout)

    def setup_tab2(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        instr = QLabel("Enter value (e.g. 10k, 220, 0.22R, 1M):")
        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("e.g. 4.7k")
        
        self.tol_combo_tab2 = QComboBox()
        for name, val, mult, tol, hex_code in self.colors_data:
            if tol is not None:
                self.tol_combo_tab2.addItem(name)
                self.tol_combo_tab2.setItemData(self.tol_combo_tab2.count()-1, QColor(hex_code), Qt.DecorationRole)
        
        convert_btn = QPushButton("Convert to Colors")
        convert_btn.clicked.connect(self.calculate_from_value)
        
        layout.addWidget(instr)
        layout.addWidget(self.value_input)
        layout.addWidget(QLabel("Select Tolerance:"))
        layout.addWidget(self.tol_combo_tab2)
        layout.addWidget(convert_btn)
        layout.addStretch()
        self.tab2.setLayout(layout)

    def reset_all(self):
        """Her şeyi başlangıç durumuna getirir."""
        # Comboboxları sıfırla
        for combo in self.combos:
            combo.blockSignals(True)
            combo.setCurrentIndex(0)
            combo.blockSignals(False)
        
        # 4 bant modunda 3. bant gizleme ayarı
        is_4 = self.radio_4band.isChecked()
        self.combos[2].setVisible(not is_4)
        self.combo_container.itemAt(2).layout().itemAt(0).widget().setVisible(not is_4)
        
        # Tab 2 girdi alanını sıfırla
        self.value_input.clear()
        
        # Sonuç yazısını sıfırla
        self.result_label.setText("Please make a selection")
        
        # Görseli sıfırla (sadece baz direnç resmini çiz)
        self.draw_resistor([])

    def get_pixmap(self, name):
        path = os.path.join(self.icons_path, f"{name}.png")
        if os.path.exists(path): return QPixmap(path)
        if "gold" in name:
            alt = os.path.join(self.icons_path, name.replace("gold", "golden") + ".png")
            if os.path.exists(alt): return QPixmap(alt)
        return None

    def draw_resistor(self, color_names):
        is_4 = self.radio_4band.isChecked()
        base = "4colorresistor" if is_4 else "5colorresistor"
        pix = self.get_pixmap(base)
        if not pix: return

        canvas = QPixmap(pix.size())
        canvas.fill(Qt.transparent)
        painter = QPainter(canvas)
        painter.drawPixmap(0, 0, pix)

        if is_4:
            prefixes = [("1", 0), ("2", 1), ("3", 2), ("T", 3)]
        else:
            prefixes = [("1", 0), ("2", 1), ("3", 2), ("4", 3), ("T", 4)]
        
        for pref, idx in prefixes:
            if idx < len(color_names) and color_names[idx]:
                layer = self.get_pixmap(f"{pref}{color_names[idx].lower()}")
                if layer: painter.drawPixmap(0, 0, layer)

        refl = self.get_pixmap("reflect")
        if refl: painter.drawPixmap(0, 0, refl)
        painter.end()
        self.resistor_display.setPixmap(canvas)

    def update_image_from_combos(self):
        is_4 = self.radio_4band.isChecked()
        indices = [0, 1, 3, 4] if is_4 else [0, 1, 2, 3, 4]
        selected = []
        for i in indices:
            t = self.combos[i].currentText()
            selected.append(t if t != "Select" else None)
        self.draw_resistor(selected)

    def calculate_from_colors(self):
        is_4 = self.radio_4band.isChecked()
        indices = [0, 1, 3, 4] if is_4 else [0, 1, 2, 3, 4]
        if any(self.combos[i].currentText() == "Select" for i in indices):
            self.result_label.setText("Missing selection!")
            return
        
        d = [next((x for x in self.colors_data if x[0] == self.combos[i].currentText()), None) for i in range(5)]
        try:
            if is_4:
                val = (d[0][1] * 10 + d[1][1]) * d[3][2]
                tol = d[4][3]
            else:
                val = (d[0][1] * 100 + d[1][1] * 10 + d[2][1]) * d[3][2]
                tol = d[4][3]
            
            if val >= 1000000: res = f"{val/1000000:g} MΩ"
            elif val >= 1000: res = f"{val/1000:g} kΩ"
            else: res = f"{val:g} Ω"
            self.result_label.setText(f"{res} ±{tol}%")
        except: self.result_label.setText("Error!")

    def calculate_from_value(self):
        raw = self.value_input.text().upper().replace(" ", "").replace(",", ".")
        if not raw: return
        try:
            mult_map = {"R": 1, "K": 1000, "M": 1000000}
            unit = 1
            for char, m in mult_map.items():
                if char in raw:
                    unit = m
                    raw = raw.replace(char, "")
                    break
            
            num = float(raw) * unit
            is_4 = self.radio_4band.isChecked()
            
            temp = num
            exp = 0
            if temp > 0:
                while temp >= (100 if is_4 else 1000):
                    temp /= 10
                    exp += 1
                while temp < (10 if is_4 else 100):
                    temp *= 10
                    exp -= 1
            
            digits = str(int(round(temp, 0)))
            res_colors = [self.colors_data[int(d)][0] for d in digits]
            
            target_mult = 10**exp
            m_color = next(c[0] for c in self.colors_data if c[2] == target_mult)
            res_colors.append(m_color)
            res_colors.append(self.tol_combo_tab2.currentText())
            
            self.draw_resistor(res_colors)
        except:
            self.result_label.setText("Invalid format!")

    def show_about(self):
        AboutDialog(self, self.main_icon_path).exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ResistorCalculator()
    ex.show()
    sys.exit(app.exec_())
