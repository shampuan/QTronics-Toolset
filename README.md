# QTronics-Toolset
It includes tools for performing electronic calculations.

<div align="center">

<img src="ScreenShots/logo.png" alt="QTronics ToolSet logo" width="96" height="96">

# QTronics ToolSet

**A free, open-source electronics calculator suite for Linux**

Ohm's Law · Resistor Networks · Filters · Regulators · Signal Generation · Unit Conversion — all in one lightweight desktop app.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux-informational)](#-installation)
[![Made with Python](https://img.shields.io/badge/made%20with-Python-3776AB?logo=python&logoColor=white)](#)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-41CD52?logo=qt&logoColor=white)](#)
[![Pardus](https://img.shields.io/badge/tested%20on-Pardus%20Linux-D71920)](#)

[SourceForge](https://sourceforge.net/projects/qtronics-toolset/) · [Report a Bug](https://github.com/shampuan/QTronics-Toolset/issues) · [Request a Feature](https://github.com/shampuan/QTronics-Toolset/issues)

</div>

---

## About

**QTronics ToolSet** is a modular, offline electronics calculator built for hobbyists, students, and engineers who work on Linux. Instead of juggling a dozen browser tabs for Ohm's law, LED resistor sizing, filter design, or voltage regulator math, QTronics ToolSet keeps every calculation in one native, distraction-free desktop application.

It was built out of a simple frustration: most electronics calculator tools online are ad-heavy, require an internet connection, or simply don't exist as native Linux apps. QTronics ToolSet fixes that with a single, self-contained toolbox — no browser, no ads, no telemetry.

- 🐧 **Linux-first** — built and tested on Pardus Linux (Debian-based), works across most modern distros
- 📴 **Fully offline** — no internet connection required, no data leaves your machine
- 🧩 **Modular** — 50+ independent calculation tools behind one launcher
- 🪶 **Lightweight** — pure Python + PyQt6, minimal dependencies
- 🔓 **Free & open source** — GPL-3.0 licensed, forever

---

## 📸 Screenshots

<div align="center">
<img src="ScreenShots/main-window.png" alt="QTronics ToolSet main window" width="700">
</div>

<details>
<summary><strong>More screenshots</strong></summary>

<br>

| Ohm's Law Calculator | Resistor Color Decoder | Filter Designer |
|:---:|:---:|:---:|
| <img src="ScreenShots/ohms-law.png" width="260"> | <img src="ScreenShots/resistor-color.png" width="260"> | <img src="ScreenShots/filter.png" width="260"> |

</details>

---

## ✨ Features

QTronics ToolSet groups electronics calculations into focused, single-purpose tools. Every tool opens in its own compact window so you only see what you need.

<details open>
<summary><strong>🔢 Fundamentals & Resistor Networks</strong></summary>

| Tool | Description |
|---|---|
| Ohm's Law | Solve for V, I, or R instantly |
| Kirchhoff's Laws | Current/voltage law reference & solver |
| Parallel Resistor | Combined resistance for parallel networks |
| Voltage Divider | Two-resistor divider output calculation |
| Wheatstone Bridge | Bridge balance and unknown resistance solver |
| Resistor Color Code | Band color ↔ resistance value decoder |
| Standard Resistor | Nearest E-series (E12/E24/E96) value finder |
| Base Resistor | BJT base resistor sizing |

</details>

<details>
<summary><strong>⚡ Components & Passive Networks</strong></summary>

| Tool | Description |
|---|---|
| Zener Diode | Zener regulator resistor sizing |
| LED Resistor | Series resistor for single/multiple LEDs |
| Capacitor | Capacitance, charge, and energy calculations |
| Capacitive Reactance | Xc at a given frequency |
| Inductor | Inductance and reactance calculations |
| Transformer / Transformer VA | Turns ratio, VA rating, secondary current |
| R-C Time | RC charge/discharge time constant |
| Toroid Core | Turns count for a target inductance |
| SMD Code | SMD resistor marking decoder |

</details>

<details>
<summary><strong>🔋 Power, Regulation & Charging</strong></summary>

| Tool | Description |
|---|---|
| LED from HV | Driving an LED directly from mains/high voltage |
| Charge from HV | HV-derived low-current charging calculations |
| Transformerless PSU | Capacitive dropper power supply design |
| 78XX Heat | Linear regulator heat dissipation |
| LM317 Regulator | Output voltage / resistor divider design |
| Current Limit | Current-limiting resistor design |
| Transistor Regulator | Discrete transistor-based regulation |
| Current Mirror | Bias and output current calculations |
| Battery Charge / 3XX Battery Charger | Charging current & time estimation |
| Cbatt Time | Capacitor-based battery runtime estimate |
| Heatsink Calc | Thermal resistance & heatsink sizing |

</details>

<details>
<summary><strong>📶 Signal, Analog & Digital Design</strong></summary>

| Tool | Description |
|---|---|
| NE555 | Astable/monostable timing calculator |
| TL431 | Precision reference divider design |
| BJT Saturation | Saturation region check for switching transistors |
| MOSFET | Gate resistor & switching parameter helper |
| Hi-Lo Pass | RC high-pass / low-pass corner frequency |
| OPAMP | Common op-amp gain configurations |
| Schmitt-Trigger | Threshold design for hysteresis circuits |
| Signal Generator | Waveform frequency/period reference tool |
| Darlington/Sziklai | Compound transistor pair gain |
| Ladder DAC | R-2R ladder output calculation |
| Long Tailed Pair | Differential pair biasing |
| Buck-Boost | Switching converter component sizing |
| Logic Gates | Truth table reference for common gates |
| Flip-Flop | Sequential logic reference |
| Electronic Filter | Passive filter design helper |
| 7 Segment | Segment/pin mapping reference |

</details>

<details>
<summary><strong>📏 RF, Layout & Unit Conversion</strong></summary>

| Tool | Description |
|---|---|
| Antenna Length | Quarter/half-wave antenna length by frequency |
| Trace Size | PCB copper trace width for target current |
| Cable Diameter | Wire gauge sizing for current/length |
| Decibel Converter | dB ↔ ratio/power conversions |
| Unit Converter | General electronics unit conversions |

</details>

---

## 📥 Installation

QTronics ToolSet is distributed as a `.deb` package for Debian-based distributions (Pardus, Debian, Ubuntu, and derivatives), and via SourceForge for broader access.

### Option 1 — Download the `.deb` package (recommended)

[![Download QTronics ToolSet](https://img.shields.io/sourceforge/dm/qtronics-toolset.svg)](https://sourceforge.net/projects/qtronics-toolset/files/latest/download)

```bash
# Download the latest .deb from the Releases page or SourceForge, then:
sudo dpkg -i QTronicsTool*.deb
sudo apt-get install -f   # resolves any missing dependencies
```

### Option 2 — Run from source

<details>
<summary><strong>Show source installation steps</strong></summary>

```bash
git clone https://github.com/shampuan/QTronics-Toolset.git
cd QTronics-Toolset

# Install PyQt6 if not already present
pip install PyQt6 --break-system-packages

python3 qtronics_toolset.py
```

</details>

### Uninstall

```bash
sudo apt remove qtronics-toolset
```

---

## 🖥️ Requirements

| Requirement | Version |
|---|---|
| OS | Debian-based Linux (Pardus, Debian, Ubuntu, etc.) |
| Python | 3.x |
| GUI Toolkit | PyQt6 |
| Disk space | < 20 MB |

---

## 🗺️ Roadmap

- [ ] Additional filter topologies (active filters)
- [ ] Dark/light theme toggle independent of system theme
- [ ] More unit categories in the general converter
- [ ] Translations beyond Turkish/English

Have an idea for a tool that's missing? [Open an issue](https://github.com/shampuan/QTronics-Toolset/issues) — module suggestions are welcome.

---

## 🤝 Contributing

Contributions, bug reports, and tool suggestions are welcome.

1. Fork the repository
2. Create a branch (`git checkout -b feature/new-tool`)
3. Commit your changes
4. Open a pull request describing the tool or fix

Since the project is composed of independent calculator modules, small, focused pull requests (one tool per PR) are the easiest to review.

---

## 📄 License

QTronics ToolSet is released under the **GNU General Public License v3.0**. See [LICENSE](LICENSE) for the full text.

---

## 👤 Author

**A. Serhat KILIÇOĞLU**
GitHub: [@shampuan](https://github.com/shampuan)

<div align="center">

If QTronics ToolSet saved you a trip to a browser calculator, consider starring the repo — it helps other Linux users find the project.

</div>

<a href="https://sourceforge.net/projects/qtronics-toolset/files/latest/download"><img alt="Download QTronics ToolSet" src="https://img.shields.io/sourceforge/dm/qtronics-toolset.svg" ></a>

<a href="https://sourceforge.net/projects/qtronics-toolset/files/latest/download"><img alt="Download QTronics ToolSet" src="https://a.fsdn.com/con/app/sf-download-button" width=276 height=48 srcset="https://a.fsdn.com/con/app/sf-download-button?button_size=2x 2x"></a>


<img width="740" height="674" alt="Ekran görüntüsü_2026-01-24_02-27-55" src="https://github.com/user-attachments/assets/41727086-6b70-4a35-aa5f-edf7a4ca0034" />


<img width="460" height="554" alt="Ekran görüntüsü_2026-01-24_18-36-06" src="https://github.com/user-attachments/assets/51690727-30c2-42ab-b52b-54e621a09a29" />
<img width="510" height="584" alt="Ekran görüntüsü_2026-01-24_18-35-58" src="https://github.com/user-attachments/assets/33496bdf-d6b7-4790-a612-777b63765f32" />
<img width="490" height="559" alt="Ekran görüntüsü_2026-01-24_18-35-50" src="https://github.com/user-attachments/assets/22d9e02c-19fa-4b5a-ba17-534ba5f01c48" />
<img width="460" height="614" alt="Ekran görüntüsü_2026-01-24_18-35-40" src="https://github.com/user-attachments/assets/07a68380-d6ac-4ac6-a3aa-93a721a90305" />
<img width="560" height="684" alt="Ekran görüntüsü_2026-01-24_18-35-22" src="https://github.com/user-attachments/assets/4d2d75df-f048-4903-9f4c-c29af2050a16" />
<img width="490" height="674" alt="Ekran görüntüsü_2026-01-24_18-35-12" src="https://github.com/user-attachments/assets/528f4148-becb-4848-906b-c8b09b68c737" />
<img width="510" height="604" alt="Ekran görüntüsü_2026-01-24_18-34-55" src="https://github.com/user-attachments/assets/63fab4a1-7f9e-4ad7-a61d-25eae891cd9a" />
<img width="530" height="644" alt="Ekran görüntüsü_2026-01-24_18-34-32" src="https://github.com/user-attachments/assets/4e924771-2cf6-4fc0-aa00-b00a41e9f5cb" />
<img width="570" height="674" alt="Ekran görüntüsü_2026-01-24_18-34-24" src="https://github.com/user-attachments/assets/2ce06546-3f21-4516-a5ea-deeb9d63bd4a" />
<img width="460" height="534" alt="Ekran görüntüsü_2026-01-24_18-34-04" src="https://github.com/user-attachments/assets/f5af746f-9425-47be-9d8f-8654bcf1eacc" />
<img width="530" height="784" alt="Ekran görüntüsü_2026-01-24_18-33-54" src="https://github.com/user-attachments/assets/cae57b12-63a6-40d3-b794-2660891d6f3a" />
<img width="460" height="544" alt="Ekran görüntüsü_2026-01-24_18-33-36" src="https://github.com/user-attachments/assets/cd8a4333-a66a-48e5-b02f-b7b266b8b240" />
<img width="460" height="535" alt="Ekran görüntüsü_2026-01-24_18-33-26" src="https://github.com/user-attachments/assets/f35b479f-f2a6-428c-871c-946c7fb3d17b" />
<img width="460" height="634" alt="Ekran görüntüsü_2026-01-24_18-33-18" src="https://github.com/user-attachments/assets/5a09a223-a349-4d16-9a71-93927567bcc5" />
<img width="490" height="634" alt="Ekran görüntüsü_2026-01-24_18-33-10" src="https://github.com/user-attachments/assets/e4ddc498-10a7-49ac-9a51-b3469d07bbb3" />
<img width="460" height="594" alt="Ekran görüntüsü_2026-01-24_18-33-01" src="https://github.com/user-attachments/assets/7c3b7d4e-6959-488f-8d3e-c896e60535cd" />
<img width="560" height="784" alt="Ekran görüntüsü_2026-01-24_18-32-51" src="https://github.com/user-attachments/assets/3d94296a-dc3b-427f-8b4e-72f339b612a4" />
<img width="610" height="598" alt="Ekran görüntüsü_2026-01-24_18-32-33" src="https://github.com/user-attachments/assets/cdaaf219-1568-4f1d-8707-2c4926e2bdda" />
<img width="570" height="503" alt="Ekran görüntüsü_2026-01-24_18-32-24" src="https://github.com/user-attachments/assets/ab437b9e-24de-4337-9998-93b4e6b7b717" />
<img width="515" height="572" alt="Ekran görüntüsü_2026-01-24_18-32-16" src="https://github.com/user-attachments/assets/369fb49f-0c66-4b42-8577-96d851baaef1" />
<img width="430" height="534" alt="Ekran görüntüsü_2026-01-24_18-32-06" src="https://github.com/user-attachments/assets/d63dc30c-c2cb-4f6b-8452-7b0aaaa7b36d" />
<img width="430" height="624" alt="Ekran görüntüsü_2026-01-24_18-31-54" src="https://github.com/user-attachments/assets/c9703834-587f-441c-9102-29bf5d9b505c" />
<img width="460" height="434" alt="Ekran görüntüsü_2026-01-24_18-31-47" src="https://github.com/user-attachments/assets/25745374-8a14-4cc4-b006-832f5ddb4d62" />
<img width="610" height="614" alt="Ekran görüntüsü_2026-01-24_18-31-38" src="https://github.com/user-attachments/assets/3defe419-d986-4cee-83b9-8838b16af824" />
<img width="430" height="612" alt="Ekran görüntüsü_2026-01-24_18-31-14" src="https://github.com/user-attachments/assets/5a274265-e316-4bef-b6e0-f493400b2bce" />
<img width="550" height="606" alt="Ekran görüntüsü_2026-01-24_18-31-02" src="https://github.com/user-attachments/assets/c02b596f-dfef-4504-b50d-e6e0f2d5d5dd" />
<img width="430" height="494" alt="Ekran görüntüsü_2026-01-24_18-30-06" src="https://github.com/user-attachments/assets/c65a1ebb-c19f-4010-bcd2-381f5478d859" />
<img width="490" height="514" alt="Ekran görüntüsü_2026-01-24_18-29-57" src="https://github.com/user-attachments/assets/cb9762dc-61d1-46a8-9dc8-89b0372db82d" />
<img width="560" height="614" alt="Ekran görüntüsü_2026-01-24_18-29-47" src="https://github.com/user-attachments/assets/8d39d6a1-4dff-44d7-a86a-a1d987dea9cc" />
<img width="590" height="684" alt="Ekran görüntüsü_2026-01-24_18-29-36" src="https://github.com/user-attachments/assets/72f2adcd-ec12-4101-9222-7e7903ec3397" />
<img width="460" height="414" alt="Ekran görüntüsü_2026-01-24_18-29-21" src="https://github.com/user-attachments/assets/836bed1c-fbbf-4f9c-a4b1-dab00bef47c5" />
<img width="560" height="614" alt="Ekran görüntüsü_2026-01-24_18-29-13" src="https://github.com/user-attachments/assets/4093c4a3-c949-49cb-aba5-5c15cc3c0206" />
<img width="560" height="614" alt="Ekran görüntüsü_2026-01-24_18-29-07" src="https://github.com/user-attachments/assets/ccbd8d2c-abba-4da8-992c-de4396bd85f9" />
<img width="412" height="586" alt="Ekran görüntüsü_2026-01-24_18-28-52" src="https://github.com/user-attachments/assets/fd607071-4447-4c79-ab75-081ddf229e08" />
<img width="460" height="534" alt="Ekran görüntüsü_2026-01-24_18-28-39" src="https://github.com/user-attachments/assets/bc7df00d-c0bd-4ab4-8a28-8d1fd8f8cdfa" />
<img width="460" height="494" alt="Ekran görüntüsü_2026-01-24_18-28-24" src="https://github.com/user-attachments/assets/2dc76cdc-e0aa-489e-9235-ad6b2994340a" />
<img width="490" height="564" alt="Ekran görüntüsü_2026-01-24_18-28-16" src="https://github.com/user-attachments/assets/f58de581-3a2c-4b58-93a7-b644f92f2ed0" />
<img width="440" height="594" alt="Ekran görüntüsü_2026-01-24_18-28-05" src="https://github.com/user-attachments/assets/25c04569-2533-4fa9-aad1-b55688cb706f" />
<img width="462" height="561" alt="Ekran görüntüsü_2026-01-24_03-19-15" src="https://github.com/user-attachments/assets/47bbf283-7ed8-435e-b94c-166610dc9328" />
<img width="510" height="584" alt="Ekran görüntüsü_2026-01-24_03-18-36" src="https://github.com/user-attachments/assets/e30d08d8-0f89-4d9c-892b-af5e5381fad4" />
<img width="528" height="676" alt="Ekran görüntüsü_2026-01-24_02-31-40" src="https://github.com/user-attachments/assets/6417184c-b588-4df5-950a-7383a9dda2e3" />
<img width="530" height="514" alt="Ekran görüntüsü_2026-01-24_02-30-47" src="https://github.com/user-attachments/assets/13a2c323-9954-4948-b1c1-8e7f5a740f93" />
<img width="460" height="510" alt="Ekran görüntüsü_2026-01-24_02-30-09" src="https://github.com/user-attachments/assets/054e7799-a514-4fa0-8777-96b148fea440" />
<img width="510" height="564" alt="Ekran görüntüsü_2026-01-24_02-29-34" src="https://github.com/user-attachments/assets/3f35d288-230c-4f07-bcb6-38c3503021a9" />
<img width="510" height="634" alt="Ekran görüntüsü_2026-01-24_02-29-19" src="https://github.com/user-attachments/assets/d3127b10-10ac-4431-8a13-2f779fc55f80" />
<img width="505" height="414" alt="Ekran görüntüsü_2026-01-24_02-28-40" src="https://github.com/user-attachments/assets/5a9577c3-4e6c-4c9a-afd1-b1d8e7b3df02" />
<img width="460" height="644" alt="Ekran görüntüsü_2026-01-24_02-28-12" src="https://github.com/user-attachments/assets/86f71c5c-f111-4cf9-b024-72b98a8cdcab" />
