#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import numpy as np
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QFrame, QSlider, 
                             QComboBox, QCheckBox, QSpacerItem, QSizePolicy, QMessageBox)
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPainterPath, QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer, QIODevice, QRect

# GNOME xcb/wayland compatibility fix
os.environ["QT_QPA_PLATFORM"] = "xcb"

class AudioGenerator(QIODevice):
    def __init__(self, format, parent=None):
        super().__init__(parent)
        self.format = format
        self.phase = 0
        self.frequency = 440
        self.amp_pos = 0.05
        self.amp_neg = 0.05
        self.is_asymmetric = False
        self.wave_type = "Sine"
        self.duty_cycle = 0.5
        self.rectification = "Full"
        self.sample_rate = format.sampleRate()

    def start(self):
        self.open(QIODevice.ReadOnly)

    def stop(self):
        self.close()

    def readData(self, maxlen):
        samples = maxlen // (self.format.sampleSize() // 8)
        if samples <= 0: return b""
            
        t = np.arange(samples) + self.phase
        self.phase += samples
        v = t * 2 * np.pi * self.frequency / self.sample_rate
        
        if self.wave_type == "Sine":
            y = np.sin(v)
        elif self.wave_type == "Square":
            y = np.where(np.mod(v, 2 * np.pi) < 2 * np.pi * self.duty_cycle, 1, -1)
        elif self.wave_type == "Triangle":
            y = 2 * np.abs(2 * (v / (2 * np.pi) - np.floor(v / (2 * np.pi) + 0.5))) - 1
        
        if self.rectification == "Half":
            y = np.maximum(0, y)

        if self.is_asymmetric:
            y = np.where(y >= 0, y * self.amp_pos, y * self.amp_neg)
        else:
            y = y * self.amp_pos

        y = (y * 32767).astype(np.int16)
        return y.tobytes()

class RulerSlider(QWidget):
    def __init__(self, label_text, min_val, max_val, default_val, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.label = QLabel(label_text)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(min_val, max_val)
        self.slider.setValue(default_val)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.slider)
        self.setFixedHeight(42)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(QColor(100, 100, 100), 1))
        slider_rect = self.slider.geometry()
        x_start, x_end = slider_rect.left() + 10, slider_rect.right() - 10
        y_pos, width = slider_rect.bottom() - 3, x_end - x_start
        for i in range(11):
            curr_x = int(x_start + (width * (i / 10)))
            h = 6 if i % 5 == 0 else 3
            painter.drawLine(curr_x, y_pos, curr_x, y_pos + h)

class WavePreview(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #002b00; border: 2px solid #001a00; border-radius: 4px;")
        self.params = {}
        self.is_frozen = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(30)
        self.offset = 0

    def update_params(self, params):
        self.params = params

    def paintEvent(self, event):
        if not self.params: return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        mid_y = h / 2

        grid_pen = QPen(QColor(0, 80, 0), 1, Qt.DotLine)
        painter.setPen(grid_pen)
        for i in range(1, 10): painter.drawLine(0, int(h*i/10), w, int(h*i/10))
        for i in range(1, 12): painter.drawLine(int(w*i/12), 0, int(w*i/12), h)

        painter.setPen(QPen(QColor(57, 255, 20, 100), 1.5))
        painter.drawLine(0, int(mid_y), w, int(mid_y))

        if not self.is_frozen: self.offset += 0.2

        # Zaman bazlı ölçeklendirme (Timebase)
        # Sürgü değeri 1 (geniş) ile 100 (sıkışık) arası değişiyor
        time_factor = self.params.get('timebase', 50) / 10.0
        freq = max(1, self.params.get('freq', 440))
        freq_scale = (freq / 100.0) * time_factor

        def draw_wave(color, amp_p, amp_n, is_asym, offset_val):
            path = QPainterPath()
            path.moveTo(0, mid_y)
            scale_p = (h / 2.3) * np.sqrt(max(0.001, amp_p))
            scale_n = (h / 2.3) * np.sqrt(max(0.001, amp_n))
            for x in range(w):
                v = (x / 50) * freq_scale + offset_val
                if self.params['w_type'] == "Sine": val = np.sin(v)
                elif self.params['w_type'] == "Square": val = 1 if (v % (2*np.pi)) < (2*np.pi*self.params['duty']) else -1
                else: val = 2 * np.abs(2 * (v / (2*np.pi) - np.floor(v / (2*np.pi) + 0.5))) - 1
                if self.params['rect'] == "Half": val = max(0, val)
                s = scale_p if val >= 0 else (scale_n if is_asym else scale_p)
                path.lineTo(x, mid_y - (val * s))
            painter.setPen(QPen(color, 2))
            painter.drawPath(path)

        if self.params.get('dual_trace'):
            draw_wave(QColor(0, 150, 255, 100), 0.05, 0.05, False, self.offset)
        draw_wave(QColor(57, 255, 20), self.params['amp_p'], self.params['amp_n'], self.params['is_asym'], self.offset)

        painter.setPen(QColor(200, 255, 200))
        painter.setFont(QFont("Monospace", 9))
        status = "FROZEN" if self.is_frozen else "RUNNING"
        painter.drawText(10, 20, f"[{status}] {self.params['w_type']} | {self.params['freq']} Hz")

class SignalGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.is_playing = False
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.icon_path = os.path.join(base_dir, "icons", "singen.png")
        
        self.init_audio()
        self.init_ui()

    def init_audio(self):
        from PyQt5.QtMultimedia import QAudioFormat, QAudioOutput
        fmt = QAudioFormat()
        fmt.setSampleRate(44100); fmt.setChannelCount(1); fmt.setSampleSize(16)
        fmt.setCodec("audio/pcm"); fmt.setByteOrder(QAudioFormat.LittleEndian); fmt.setSampleType(QAudioFormat.SignedInt)
        self.audio_output = QAudioOutput(fmt, self)
        self.generator = AudioGenerator(fmt, self)

    def init_ui(self):
        self.setWindowTitle("QSignal Generator")
        self.setFixedSize(520, 610)
        
        if os.path.exists(self.icon_path):
            self.setWindowIcon(QIcon(self.icon_path))

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 10, 15, 15)
        main_layout.setSpacing(0)

        # PREVIEW
        self.preview_area = WavePreview(self)
        self.preview_area.setMinimumHeight(240)
        main_layout.addWidget(self.preview_area)
        main_layout.addSpacing(5)

        # TOOLBAR
        tbar = QHBoxLayout()
        tbar.setSpacing(20)
        self.freeze_btn = QPushButton("Freeze Screen"); self.freeze_btn.setCheckable(True)
        self.freeze_btn.setFixedHeight(28)
        self.freeze_btn.clicked.connect(self.toggle_freeze)
        self.dual_check = QCheckBox("Dual Trace (Ref)"); self.dual_check.stateChanged.connect(self.sync_parameters)
        self.asym_check = QCheckBox("Asymmetric Amp"); self.asym_check.stateChanged.connect(self.sync_parameters)
        tbar.addWidget(self.freeze_btn); tbar.addWidget(self.dual_check); tbar.addWidget(self.asym_check)
        main_layout.addLayout(tbar)
        main_layout.addSpacing(5)

        # FREQUENCY & TIMEBASE
        h_freq = QHBoxLayout()
        v_freq = QVBoxLayout(); v_freq.setSpacing(0)
        v_freq.addWidget(QLabel("Frequency (Hz):"))
        self.freq_input = QLineEdit("440"); self.freq_input.textChanged.connect(self.sync_parameters)
        v_freq.addWidget(self.freq_input)
        
        v_time = QVBoxLayout(); v_time.setSpacing(0)
        self.time_label = QLabel("Timebase (Zoom):")
        v_time.addWidget(self.time_label)
        self.time_slider = QSlider(Qt.Horizontal)
        self.time_slider.setRange(1, 100); self.time_slider.setValue(10) # Başlangıçta makul bir zoom
        self.time_slider.valueChanged.connect(self.sync_parameters)
        v_time.addWidget(self.time_slider)
        
        h_freq.addLayout(v_freq, 2); h_freq.addLayout(v_time, 3)
        main_layout.addLayout(h_freq)
        main_layout.addSpacing(5)

        # WAVE & RECT
        h1 = QHBoxLayout()
        v_box1 = QVBoxLayout(); v_box1.setSpacing(0)
        v_box1.addWidget(QLabel("Waveform:"))
        self.wave_combo = QComboBox(); self.wave_combo.addItems(["Sine", "Square", "Triangle"])
        self.wave_combo.currentTextChanged.connect(self.sync_parameters)
        v_box1.addWidget(self.wave_combo)
        
        v_box2 = QVBoxLayout(); v_box2.setSpacing(0)
        v_box2.addWidget(QLabel("Rectification:"))
        self.rect_combo = QComboBox(); self.rect_combo.addItems(["Full", "Half"])
        self.rect_combo.currentTextChanged.connect(self.sync_parameters)
        v_box2.addWidget(self.rect_combo)
        
        h1.addLayout(v_box1); h1.addLayout(v_box2)
        main_layout.addLayout(h1)
        main_layout.addSpacing(5)

        # AMPLITUDES
        self.amp_p_widget = RulerSlider("Amplitude (5%) - Be careful!", 0, 100, 5)
        self.amp_p_widget.slider.valueChanged.connect(self.sync_parameters)
        main_layout.addWidget(self.amp_p_widget)

        self.amp_n_widget = RulerSlider("Negative Amplitude (5%) - Be Careful!", 0, 100, 5)
        self.amp_n_widget.slider.valueChanged.connect(self.sync_parameters)
        self.amp_n_widget.setVisible(False)
        main_layout.addWidget(self.amp_n_widget)

        # DUTY CYCLE
        self.duty_widget = RulerSlider("Duty Cycle (50%):", 1, 99, 50)
        self.duty_widget.slider.valueChanged.connect(self.sync_parameters)
        main_layout.addWidget(self.duty_widget)

        main_layout.addStretch(1)

        # START / STOP BUTTON
        self.toggle_button = QPushButton("START AUDIO")
        self.toggle_button.setFixedHeight(40); self.toggle_button.setStyleSheet("background-color: darkgreen; color: white; font-weight: bold; font-size: 14px;")
        self.toggle_button.clicked.connect(self.toggle_playback)
        main_layout.addWidget(self.toggle_button)
        
        main_layout.addSpacing(5)

        # ABOUT BUTTON
        self.about_btn = QPushButton("About")
        self.about_btn.setFixedHeight(30)
        self.about_btn.clicked.connect(self.show_about)
        main_layout.addWidget(self.about_btn)

        self.setLayout(main_layout); self.sync_parameters()

    def show_about(self):
        about_box = QMessageBox(self)
        about_box.setWindowTitle("About QSignal Generator")
        
        if os.path.exists(self.icon_path):
            pixmap = QPixmap(self.icon_path).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            about_box.setIconPixmap(pixmap)
            
        about_text = (
            "<h3>QSignal Generator</h3>"
            "<b>Version:</b> 1.0.0<br>"
            "<b>License:</b> GNU GPLv3<br>"
            "<b>UI:</b> Python3-PyQt5<br>"
            "<b>Developer:</b> A. Serhat KILIÇOĞLU<br>"
            "<b>Github:</b> <a href='https://www.github.com/shampuan'>www.github.com/shampuan</a><br><br>"
            "This program is a real-time signal generator with adjustable frequency, timebase, and asymmetric amplitude controls.<br><br>"
            "This program comes with ABSOLUTELY NO WARRANTY.<br><br>"
            "Copyright © 2026 - A. Serhat KILIÇOĞLU"
        )
        about_box.setTextFormat(Qt.RichText)
        about_box.setText(about_text)
        about_box.setStandardButtons(QMessageBox.Ok)
        about_box.exec_()

    def toggle_freeze(self):
        self.preview_area.is_frozen = self.freeze_btn.isChecked()
        self.freeze_btn.setText("Run Screen" if self.preview_area.is_frozen else "Freeze Screen")

    def sync_parameters(self):
        asym = self.asym_check.isChecked()
        self.amp_n_widget.setVisible(asym)
        try: freq = float(self.freq_input.text().replace(',', '.'))
        except: freq = 0
        
        params = {
            'freq': freq, 'w_type': self.wave_combo.currentText(),
            'rect': self.rect_combo.currentText(), 'amp_p': self.amp_p_widget.slider.value()/100.0,
            'amp_n': self.amp_n_widget.slider.value()/100.0, 'is_asym': asym,
            'duty': self.duty_widget.slider.value()/100.0, 'dual_trace': self.dual_check.isChecked(),
            'timebase': self.time_slider.value()
        }
        
        self.amp_p_widget.label.setText(f"{'Positive ' if asym else ''}Amplitude ({self.amp_p_widget.slider.value()}%) - Be careful!")
        self.amp_n_widget.label.setText(f"Negative Amplitude ({self.amp_n_widget.slider.value()}%) - Be careful!")
        self.duty_widget.label.setText(f"Duty Cycle ({self.duty_widget.slider.value()}%):")
        self.time_label.setText(f"Timebase (Zoom: {self.time_slider.value()}):")
        
        self.generator.frequency = params['freq']
        self.generator.wave_type = params['w_type']
        self.generator.amp_pos = params['amp_p']; self.generator.amp_neg = params['amp_n']
        self.generator.is_asymmetric = params['is_asym']; self.generator.duty_cycle = params['duty']
        self.generator.rectification = params['rect']
        self.preview_area.update_params(params)

    def toggle_playback(self):
        if not self.is_playing:
            self.generator.start(); self.audio_output.start(self.generator)
            self.toggle_button.setText("STOP AUDIO"); self.toggle_button.setStyleSheet("background-color: #8b0000; color: white; font-weight: bold; font-size: 14px;")
            self.is_playing = True
        else:
            self.audio_output.stop(); self.generator.stop()
            self.toggle_button.setText("START AUDIO"); self.toggle_button.setStyleSheet("background-color: darkgreen; color: white; font-weight: bold; font-size: 14px;")
            self.is_playing = False

if __name__ == "__main__":
    app = QApplication(sys.argv); window = SignalGenerator(); window.show(); sys.exit(app.exec_())