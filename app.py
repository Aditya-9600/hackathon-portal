import streamlit as st
import streamlit.components.v1 as components
import qrcode
import requests
from io import BytesIO
import urllib.parse
import uuid
import datetime
import os

# ==============================================================================
# 1. PAGE CONFIGURATION & SIH THEME STYLING
# ==============================================================================
st.set_page_config(
    page_title="WCE Hackathon 2026 | SIH Theme",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session State for Navigation
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_ps' not in st.session_state:
    st.session_state.selected_ps = None

def navigate_to(page_name, ps_title=None):
    st.session_state.page = page_name
    if ps_title:
        st.session_state.selected_ps = ps_title

# SIH-Inspired CSS (Deep Navy, Pure White, and Saffron/Orange Accents)
st.markdown("""
<style>
    /* Global Background */
    .stApp {
        background-color: #F4F6F9 !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    .stApp p, .stApp span, .stApp label, .stApp div, .stApp h3, .stApp h4 { 
        color: #1E293B; 
    }

    /* SIH Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #05234A 0%, #0A3D85 100%);
        border-radius: 12px;
        padding: 3rem 4rem;
        margin-bottom: 2.5rem;
        box-shadow: 0 12px 35px -10px rgba(5, 35, 74, 0.4);
        border-bottom: 8px solid #FF7A00; /* SIH Saffron/Orange */
        position: relative;
        overflow: hidden;
    }
    
    /* Subtle background pattern for hero */
    .hero-banner::after {
        content: '';
        position: absolute;
        top: 0; right: 0; bottom: 0; left: 0;
        background-image: radial-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px);
        background-size: 20px 20px;
        opacity: 0.5;
        pointer-events: none;
    }

    .hero-banner h1, .hero-banner p, .hero-banner div {
        color: #FFFFFF !important;
        position: relative;
        z-index: 2;
    }
    .inst-tag {
        display: inline-block;
        background: #FF7A00;
        color: #FFFFFF !important;
        padding: 6px 18px;
        border-radius: 4px;
        font-size: 0.9rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 10px rgba(255, 122, 0, 0.4);
    }
    .hero-title {
        font-size: 3rem; font-weight: 900; line-height: 1.2; margin: 0; letter-spacing: -0.5px;
    }
    .hero-sub {
        font-size: 1.25rem; opacity: 0.95; margin-top: 1rem; font-weight: 400; max-width: 800px;
    }
    
    /* Problem Statement Expanders (SIH Table style) */
    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 1rem !important;
        overflow: hidden;
    }
    [data-testid="stExpander"] summary {
        background-color: #FFFFFF !important;
        padding: 1rem !important;
        font-weight: 700 !important;
        color: #05234A !important;
    }
    [data-testid="stExpander"] summary:hover {
        background-color: #F8FAFC !important;
    }
    
    /* Badges */
    .badge-hw {
        background-color: #E6F4EA; color: #137333; padding: 5px 14px;
        border-radius: 4px; font-weight: 700; font-size: 0.85rem; border: 1px solid #CEEAD6;
    }
    .badge-sw {
        background-color: #E8F0FE; color: #1967D2; padding: 5px 14px;
        border-radius: 4px; font-weight: 700; font-size: 0.85rem; border: 1px solid #D2E3FC;
    }
    
    /* Secondary/Back Buttons */
    .stButton>button {
        border-radius: 6px; font-weight: 600; padding: 0.6rem 1.5rem;
        border: 1px solid #CBD5E1; color: #334155; transition: all 0.2s;
    }
    
    /* Primary "Register Now" SIH Buttons */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #FF7A00 0%, #E65C00 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 6px;
        font-weight: 700;
        font-size: 1.05rem;
        padding: 0.75rem 2rem;
        box-shadow: 0 6px 15px rgba(255, 122, 0, 0.3) !important;
        width: 100%;
        margin-top: 1rem;
    }
    .stButton>button[kind="primary"]:hover {
        background: linear-gradient(135deg, #E65C00 0%, #CC5200 100%) !important;
        box-shadow: 0 8px 20px rgba(255, 122, 0, 0.4) !important;
        transform: translateY(-1px);
    }

    /* Inputs & Form Elements */
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {
        background-color: #FFFFFF !important; border: 1px solid #CBD5E1 !important;
        border-radius: 6px !important; color: #0F172A !important; padding: 0.6rem !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #05234A !important; box-shadow: 0 0 0 2px rgba(5, 35, 74, 0.15) !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. OFFICIAL DATABASE (ALL 69 STATEMENTS, NO PRICING)
# ==============================================================================
PROBLEM_STATEMENTS = [
    # DOMAIN 01: Smart Cities & Urbanization
    {"id": 1, "domain": "Smart Cities & Urbanization", "title": "Smart Street Environment & Noise Monitoring", "category": "HARDWARE",
     "desc": "Develop an IoT-based system that dynamically controls streetlight brightness based on real-time pedestrian/vehicle activity while continuously monitoring urban noise levels.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "MAX9814 Electret Microphone with Auto Gain Control (Qty: 1)", "HC-SR501 PIR Motion Sensor Module (Qty: 1)", "LDR Photoresistor Module (Qty: 1)", "12V 5W High-Power LED Module (Qty: 1)", "RC522 RFID Module (Qty: 1)", "12V 3A SMPS Enclosed Industrial Unit (Qty: 1)", "LM2596 DC-DC Step-Down Buck Module (Qty: 1)", "IRF520 MOSFET Driver IC (Qty: 1)", "830-Tie Point Breadboard (Qty: 1)", "10µF Filter Capacitors, Jumper Wires, Terminals (Qty: 1)"]},
    {"id": 2, "domain": "Smart Cities & Urbanization", "title": "Urban Flood Monitoring & Early Warning", "category": "HARDWARE",
     "desc": "Develop a waterproof monitoring system that detects rapidly rising water levels in urban drains and underpasses and provides early warnings.",
     "components": ["ESP32-WROOM-32U (External Antenna) (Qty: 1)", "JSN-SR04T Waterproof Ultrasonic Level Sensor Module (Qty: 1)", "RC522 RFID Module (Qty: 1)", "High-Decibel 12V Outdoor Siren Module (Qty: 1)", "12V 3A Weatherproof Industrial SMPS Supply (Qty: 1)", "LM2596 DC-DC Step-Down Buck Module (Qty: 1)", "PC817 Optocoupler IC (Qty: 1)", "TIP122 Darlington Transistor IC (Qty: 1)", "400-Tie Point Breadboard & IP65 Enclosure (Qty: 1)", "Cable Glands, 1N4007 Diodes, Jumper Wires (Qty: 1)"]},
    {"id": 3, "domain": "Smart Cities & Urbanization", "title": "Urban Underground Water Leak Detection", "category": "HARDWARE",
     "desc": "Develop a system that detects and helps locate underground water-pipe leaks using flow, pressure, and acoustic sensing without excavation.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "Piezo Electric Acoustic Contact Sensor + LM358 Pre-Amp (Qty: 1)", "YF-S201 Hall-Effect Water Flow Sensor (Qty: 2)", "RC522 RFID Module (Qty: 1)", "12V 2A SMPS Power Supply (Qty: 1)", "LM2596 DC-DC Step-Down Buck Module (Qty: 1)", "74HC14 Schmitt Trigger IC (Qty: 1)", "830-Tie Point Breadboard (Qty: 1)", "Jumper Wires, 10kΩ Pull-up Resistors, Filter Caps (Qty: 1)"]},
    {"id": 4, "domain": "Smart Cities & Urbanization", "title": "Underground Sewage Gas Safety", "category": "HARDWARE",
     "desc": "Develop a low-power system that continuously monitors toxic and combustible gases in underground sewage systems and provides warnings.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "MQ-136 Hydrogen Sulfide (H2S) Gas Sensor Module (Qty: 1)", "MQ-4 Methane / Combustible Gas Sensor Module (Qty: 1)", "12V 1A DC Exhaust Blower Fan + 1-Channel Relay (Qty: 1)", "RC522 RFID Module (Qty: 1)", "12V 5A Industrial Metal SMPS Unit (Qty: 1)", "LM2596S DC-DC Step-Down Buck Module (Qty: 1)", "PC817 Optocoupler IC (Qty: 1)", "830-Tie Point Breadboard (Qty: 1)", "High-Decibel Buzzer, Jumper Wires, Status LEDs (Qty: 1)"]},
    {"id": 5, "domain": "Smart Cities & Urbanization", "title": "Dynamic Digital Traffic Signage", "category": "HARDWARE",
     "desc": "Develop a connected digital signage system that receives real-time traffic data and automatically displays alternative routes or detour instructions.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "MAX7219 4-in-1 Dot Matrix LED Display Module (32x8) (Qty: 2)", "DS3231 High-Precision Real Time Clock IC Module (Qty: 1)", "RC522 RFID Module (Qty: 1)", "5V 4A SMPS Enclosed Industrial Supply (Qty: 1)", "74HC595 Shift Register IC (Qty: 1)", "830-Tie Point Breadboard (Qty: 1)", "Jumper Wires, 10µF Smoothing Capacitors, Resistors (Qty: 1)"]},
    {"id": 6, "domain": "Smart Cities & Urbanization", "title": "Smart Waste Management", "category": "HARDWARE",
     "desc": "Develop an IoT-based waste management system that monitors garbage-bin fill levels, detects overflow conditions, and sends alerts.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "HC-SR04 Ultrasonic Distance Sensor Modules (Qty: 2)", "SW-520D Roller Ball Tilt / Overflow Sensor Module (Qty: 1)", "RC522 RFID Module (Qty: 1)", "SG90 9g Micro Servo Motor (Qty: 1)", "5V 2A SMPS Power Supply Adapter (Qty: 1)", "AMS1117-3.3V LDO IC (Qty: 2)", "400-Tie Point Breadboard (Qty: 1)", "Jumper Wires, Status LEDs, 10kΩ Pull-up Resistors (Qty: 1)"]},
    {"id": 7, "domain": "Smart Cities & Urbanization", "title": "AI-Powered Traffic Flow Optimization", "category": "SOFTWARE",
     "desc": "Develop a centralized software platform that ingests real-time transit and ride-sharing GPS data to dynamically adjust traffic light timings.",
     "components": []},
    {"id": 8, "domain": "Smart Cities & Urbanization", "title": "Civic Issue Crowdsourcing & Triage", "category": "SOFTWARE",
     "desc": "Develop a web/mobile application that allows citizens to report civic issues with geotagged photos, using AI to route to municipal departments.",
     "components": []},

    # DOMAIN 02: Healthcare & Medical Technology
    {"id": 9, "domain": "Healthcare & Medical Technology", "title": "Elderly Care & Assistive Technology", "category": "HARDWARE",
     "desc": "Develop a wearable system that detects accidental falls in elderly individuals, provides medication reminders, and sends SOS alerts with GPS location.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "MPU-6050 6-Axis Accelerometer/Gyro Module (Qty: 1)", "NEO-6M GPS Module with Ceramic Antenna (Qty: 1)", "SIM800L GPRS/GSM Module (Qty: 1)", "DS3231 High-Precision RTC IC Module (Qty: 1)", "3V Coin Flat Vibration Motor (Qty: 1)", "TP4056 1A Li-Ion Battery Charger IC Module (Qty: 1)", "3.7V 1200mAh Li-Po Rechargeable Battery (Qty: 1)", "5V 2A SMPS Module (Qty: 1)", "2N2222 NPN Transistor (Qty: 2)", "AMS1117-3.3V LDO Voltage Regulator IC (Qty: 2)", "Mini 170-Tie Point Breadboard (Qty: 1)", "Tactile SOS Push Button, 1N4148 Diodes, Resistors & Caps (Qty: 1)"]},
    {"id": 10, "domain": "Healthcare & Medical Technology", "title": "Hospital Patient Safety & Monitoring", "category": "HARDWARE",
     "desc": "Develop a smart monitoring system that continuously detects the remaining level of an IV fluid bag and automatically alerts nursing staff.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "1kg Straight Bar Load Cell + HX711 24-bit ADC Module (Qty: 1)", "16x2 Character LCD with PCF8574 I2C Backpack (Qty: 1)", "5V Loud Active Buzzer + Ultra-bright Red LED (Qty: 1)", "12V 2A SMPS (Qty: 1)", "LM2596S DC-DC Step-Down Buck Converter Module (Qty: 1)", "HX711 24-Bit ADC IC Spare (Qty: 1)", "PC817 Optocoupler IC (Qty: 2)", "830-Tie Point Breadboard (Qty: 1)", "1N4007 Diodes, Resistor Pack, JST Cables, Jumpers (Qty: 1)"]},
    {"id": 11, "domain": "Healthcare & Medical Technology", "title": "Blood Bank & Medical Inventory Management", "category": "HARDWARE",
     "desc": "Develop an IoT-based system that continuously monitors blood storage temperature and tracks blood bag inventory/expiry information.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "RC522 13.56 MHz RFID Reader Module (Qty: 1)", "13.56MHz Mifare Classic 1K RFID Adhesive Tags/Cards (Qty: 10)", "DS18B20 Waterproof Stainless Steel Digital Probe (Qty: 2)", "20x4 Character LCD with I2C Interface Adapter (Qty: 1)", "12V 3A SMPS (Qty: 1)", "LM2596 DC-DC Buck Module (Qty: 1)", "DS18B20 1-Wire IC (Qty: 1)", "74HC4050 Hex Buffer IC (Qty: 1)", "BC547 NPN BJT IC (Qty: 2)", "830-Tie Point Breadboard (Qty: 1)", "Pull-Up Resistors, Filter Caps, Piezo Alarm Buzzer, Jumpers (Qty: 1)"]},
    {"id": 12, "domain": "Healthcare & Medical Technology", "title": "Neonatal & Maternal Healthcare", "category": "HARDWARE",
     "desc": "Develop a smart incubator monitoring and control system that maintains stable temperature and humidity for premature babies.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "SHT31 High-Accuracy I2C Temp & Humidity Sensor (Qty: 1)", "DS18B20 Waterproof Skin-Surface Probe (Qty: 1)", "12V 50W PTC Ceramic Insulated Air Heating Element (Qty: 1)", "12V Brushless DC Blower Fan (Qty: 1)", "5V/12V Ultrasonic Mist Maker Disk (Qty: 1)", "IRF520/AOD4184 MOSFET Driver Module (Qty: 2)", "12V 10A 120W SMPS (Qty: 1)", "LM2596 Step-Down Buck Converter (Qty: 2)", "AMS1117-3.3V LDO IC (Qty: 2)", "PC817 Optocoupler IC (Qty: 2)", "1N4007 Flyback Diodes, Barrier Screw Terminals, 830 Breadboard (Qty: 1)"]},
    {"id": 13, "domain": "Healthcare & Medical Technology", "title": "Preventive Healthcare & Wellness", "category": "HARDWARE",
     "desc": "Develop a smart bottle that automatically measures water intake, monitors hydration patterns, and provides personalized reminders.",
     "components": ["ESP32-C3 SuperMini RISC-V Dev Board (Qty: 1)", "Non-Contact Capacitive Liquid Level Sensor (Qty: 1)", "RC522 13.56MHz RFID Reader Module (Qty: 1)", "0.42-inch OLED I2C Display Module (Qty: 1)", "5V 2A SMPS Wall Charger Adapter (Qty: 1)", "TP4056 Battery Charger IC + 1000mAh LiPo (Qty: 1)", "AMS1117-3.3V LDO IC (Qty: 2)", "3V Coin Flat Vibration Motor (Qty: 1)", "Mini 170-Tie Point Breadboard, Resistors, Caps, Pushbutton, Jumpers (Qty: 1)"]},
    {"id": 14, "domain": "Healthcare & Medical Technology", "title": "AI-Based Disease Detection & Medical Diagnostics", "category": "HARDWARE",
     "desc": "Develop a low-cost digital microscopy system that captures blood-smear images and uses computer vision to highlight malaria/dengue cells.",
     "components": ["ESP32-S3-WROOM-1 DevKit (16MB Flash, 8MB PSRAM) (Qty: 1)", "OV5640 5MP Camera Module with AF Lens (Qty: 1)", "Precision Adjustable LED Spotlight Condenser (Qty: 1)", "RC522 RFID Module (Qty: 1)", "NEMA 17 Stepper Motor (Qty: 1)", "12V 3A Enclosed SMPS Power Supply (Qty: 1)", "LM2596 DC-DC Step-Down Buck Converter (Qty: 1)", "A4988 Stepper Motor Driver IC Board (Qty: 1)", "AMS1117-3.3V LDO IC (Qty: 2)", "830-Tie Point Breadboard, Zero PCB, Limit Switches, Jumpers (Qty: 1)"]},
    {"id": 15, "domain": "Healthcare & Medical Technology", "title": "Digital Healthcare & Organ Transplant Management", "category": "SOFTWARE",
     "desc": "Develop a secure platform that enables hospitals to efficiently match organ donors with eligible recipients based on compatibility factors.",
     "components": []},
    {"id": 16, "domain": "Healthcare & Medical Technology", "title": "Predictive Hospital Bed Management", "category": "SOFTWARE",
     "desc": "Develop a software solution integrating with EHR to forecast patient admission rates and discharge times using machine learning.",
     "components": []},

    # DOMAIN 03: Electric Vehicles (EV) & Mobility
    {"id": 17, "domain": "Electric Vehicles (EV) & Mobility", "title": "EV Battery Safety & Thermal Runaway", "category": "HARDWARE",
     "desc": "Develop a low-cost battery monitoring system that detects early signs of thermal runaway at the cell level and isolates the affected module.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "NTC 10k Precision Thermistors (Pack of 5 Cell Probes) (Qty: 1)", "MQ-2 Flammable Gas / Venting Smoke Sensor Module (Qty: 1)", "4-Channel 5V Optocoupled Relay Module (Qty: 1)", "RC522 RFID Module (Qty: 1)", "12V 10A 120W Industrial SMPS (Qty: 1)", "LM393 Dual Comparator IC (Qty: 2)", "LM2596S DC-DC Step-Down Buck Module (Qty: 1)", "830-Tie Point Breadboard, High-Decibel Siren, 10kΩ Resistors, Harness (Qty: 1)"]},
    {"id": 18, "domain": "Electric Vehicles (EV) & Mobility", "title": "EV Motor Fault Detection & Predictive Maintenance", "category": "HARDWARE",
     "desc": "Develop a sensorless motor-monitoring system analyzing three-phase current signals to detect developing inter-turn winding faults.",
     "components": ["ESP32-WROOM-32 (Fast ADC & FFT) (Qty: 1)", "ACS712 30A Current Sensor Modules (Qty: 3)", "LM358 Operational Amplifier Signal Conditioning ICs (Qty: 2)", "RC522 RFID Module (Qty: 1)", "12V 5A Bench Industrial SMPS Unit (Qty: 1)", "LM2596 DC-DC Step-Down Buck Module (Qty: 1)", "0.96-inch I2C OLED Display Module (Qty: 1)", "Small 3-Phase BLDC Motor + ESC (Qty: 1)", "830 Breadboard, Shielded Hookup Wire, Filter Caps, Jumpers (Qty: 1)"]},
    {"id": 19, "domain": "Electric Vehicles (EV) & Mobility", "title": "EV Charging Infrastructure Monitoring", "category": "HARDWARE",
     "desc": "Develop a retrofit device that independently verifies whether an EV charging station is delivering power and logs genuine charging events.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "PZEM-004T V3.0 AC Multi-Function Energy Meter Module (Qty: 1)", "SCT-013-000 100A Current Transformer Clamp (Qty: 1)", "RC522 13.56MHz RFID Reader (Qty: 1)", "12V 2A Enclosed Industrial SMPS Unit (Qty: 1)", "LM2596 DC-DC Step-Down Buck Module (Qty: 1)", "0.96-inch I2C OLED Display Screen (Qty: 1)", "5V 2A USB Dummy Load Resistor (Qty: 1)", "830-Tie Point Breadboard, Terminal Blocks, 14AWG Wire, Jumpers (Qty: 1)"]},
    {"id": 20, "domain": "Electric Vehicles (EV) & Mobility", "title": "Regenerative Braking & Energy Recovery", "category": "HARDWARE",
     "desc": "Develop an intelligent regenerative-braking controller that dynamically manages regen levels based on motor status and battery state.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "ACS712 30A Bidirectional Current Sensor Module (Qty: 1)", "IRFB3077 High Current N-MOSFET (Qty: 2)", "TC4427/IR2104 High-Speed MOSFET Gate Driver IC (Qty: 1)", "RC522 RFID Module (Qty: 1)", "12V 10A 120W Industrial SMPS (Qty: 1)", "LM2596S DC-DC Step-Down Buck Module (Qty: 1)", "PC817 Optocoupler IC (Qty: 2)", "830 Breadboard, Power Resistors, 1000µF Filter Caps, 14AWG Wire (Qty: 1)"]},
    {"id": 21, "domain": "Electric Vehicles (EV) & Mobility", "title": "EV Traction Control & Vehicle Stability", "category": "HARDWARE",
     "desc": "Develop an intelligent traction-control system that detects excessive wheel slip and dynamically adjusts motor torque.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "LM393 Optical Wheel Speed Sensor Modules (Dual Encoders) (Qty: 2)", "L298N Dual H-Bridge Motor Driver Module (Qty: 1)", "Dual TT DC Geared Motors with Encoder Disks (Qty: 2)", "RC522 RFID Module (Qty: 1)", "12V 5A Bench Industrial SMPS Unit (Qty: 1)", "LM2596 DC-DC Step-Down Buck Module (Qty: 1)", "74HC14 Hex Inverting Schmitt Trigger IC (Qty: 1)", "830 Breadboard, Jumpers, 100nF Ceramic Capacitors, Status LEDs (Qty: 1)"]},
    {"id": 22, "domain": "Electric Vehicles (EV) & Mobility", "title": "EV Structural Health & Predictive Maintenance", "category": "HARDWARE",
     "desc": "Develop an accelerometer-based system for detecting structural fatigue in an EV battery mounting system by analyzing resonant frequency.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "ADXL345 3-Axis Digital High-g Accelerometer (Qty: 1)", "SW-420 High Sensitivity Shock/Vibration Sensor (Qty: 1)", "RC522 RFID Module (Qty: 1)", "0.96-inch I2C OLED Display Module (Qty: 1)", "12V 2A SMPS Power Supply (Qty: 1)", "LM2596 DC-DC Step-Down Buck Module (Qty: 1)", "LM393 Dual Comparator IC (Qty: 1)", "830-Tie Point Breadboard, Jumpers, Status LEDs, 10kΩ Resistors (Qty: 1)"]},
    {"id": 23, "domain": "Electric Vehicles (EV) & Mobility", "title": "Smart EV Fleet Routing & Charging", "category": "SOFTWARE",
     "desc": "Develop a cloud-based software platform for commercial EV fleets calculating optimal delivery routes factoring in SOC and charging stations.",
     "components": []},
    {"id": 24, "domain": "Electric Vehicles (EV) & Mobility", "title": "EV Battery Degradation Analytics", "category": "SOFTWARE",
     "desc": "Develop a machine learning application analyzing historical charging/usage data to predict long-term battery degradation and advise charging habits.",
     "components": []},

    # DOMAIN 04: Education & Academic Learning
    {"id": 25, "domain": "Education & Academic Learning", "title": "Multilingual Academic Learning Support", "category": "SOFTWARE",
     "desc": "Develop a multilingual academic platform that accepts questions in Marathi, Hindi, or English and provides clear explanations suited to student levels.",
     "components": []},
    {"id": 26, "domain": "Education & Academic Learning", "title": "Personalized Educational Resource Recommendation", "category": "SOFTWARE",
     "desc": "Develop an adaptive system analyzing student interactions (quiz time, retry behavior) to identify learning gaps and recommend personalized resources.",
     "components": []},
    {"id": 27, "domain": "Education & Academic Learning", "title": "Interactive AI-Powered Quantum Learning", "category": "SOFTWARE",
     "desc": "Develop an interactive educational platform enabling students to design quantum circuits, visualize quantum states, and receive AI-based optimization guidance.",
     "components": []},
    {"id": 28, "domain": "Education & Academic Learning", "title": "Academic–Industry Collaboration Platform", "category": "SOFTWARE",
     "desc": "Develop a platform connecting universities and industries to initiate and manage industrial visits, projects, internships, and research partnerships.",
     "components": []},
    {"id": 29, "domain": "Education & Academic Learning", "title": "Smart Handwriting Posture & Grip Assistant", "category": "HARDWARE",
     "desc": "Develop a smart pen or wearable that detects incorrect writing posture or pencil grip in real time and provides child-friendly tactile feedback.",
     "components": ["ESP32-C3 SuperMini RISC-V Dev Board (Qty: 1)", "Square/Round Force Sensing Resistor (FSR402) (Qty: 2)", "MPU-6050 6-Axis Motion Sensor Module (Qty: 1)", "Miniature 3V Coin Vibration Motor (Qty: 1)", "RC522 RFID Module (Qty: 1)", "TP4056 LiPo Charger IC Board + 3.7V 300mAh LiPo Cell (Qty: 1)", "5V 1A SMPS Charging Dock Power Supply (Qty: 1)", "2N2222 NPN Transistor IC (Qty: 1)", "Mini 170 Breadboard, 10kΩ Resistors, 1N4148 Diode, Flexible Wire (Qty: 1)"]},
    {"id": 30, "domain": "Education & Academic Learning", "title": "Visual Pronunciation Learning Device", "category": "HARDWARE",
     "desc": "Develop a standalone device that uses microphone input and a small display to provide visual mouth-shape feedback to improve pronunciation.",
     "components": ["ESP32-S3 DevKit (DSP Audio Frequency Classifier) (Qty: 1)", "MAX9814 Electret Microphone with Auto Gain Control (Qty: 1)", "1.8-inch SPI ST7735 Full-Color TFT Display Module (Qty: 1)", "RC522 RFID Module (Qty: 1)", "5V 2A Low-Noise SMPS Power Adapter (Qty: 1)", "AMS1117-3.3V LDO IC (Qty: 2)", "830-Tie Point Breadboard, Audio Filter Capacitors, 10kΩ Resistors, Jumpers (Qty: 1)"]},
    {"id": 31, "domain": "Education & Academic Learning", "title": "AI-Driven Academic Integrity Detector", "category": "SOFTWARE",
     "desc": "Develop a natural language processing software tool that analyzes student submissions to differentiate human writing, plagiarized text, and AI text.",
     "components": []},

    # DOMAIN 05: Renewable Energy & Power Systems
    {"id": 32, "domain": "Renewable Energy & Power Systems", "title": "Solar Energy & Battery Management", "category": "HARDWARE",
     "desc": "Develop an energy-management controller that monitors solar generation and load demand, intelligently scheduling battery cycles.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "6V 3W Mini Solar Panel (Qty: 1)", "ACS712 30A Current Sensor Modules (Qty: 2)", "Voltage Detection Divider Sensor Modules (0-25V) (Qty: 2)", "IRF3205 N-MOSFET High Current Switch Modules (Qty: 2)", "RC522 RFID Module (Qty: 1)", "12V 10A Industrial Metal SMPS Unit (Qty: 1)", "LM2596S Step-Down Converter Module (Qty: 1)", "IR2104 Half-Bridge Gate Driver IC (Qty: 2)", "830 Breadboard, Power Terminals, 1000µF Filter Caps, Shunts, 14AWG Wire (Qty: 1)"]},
    {"id": 33, "domain": "Renewable Energy & Power Systems", "title": "Power Quality & Harmonic Management", "category": "HARDWARE",
     "desc": "Develop a real-time power-quality monitoring system detecting harmonic distortions and evaluating the impact of active compensation.",
     "components": ["ESP32-WROOM-32 (Fast FFT Processing) (Qty: 1)", "ZMPT101B Active Single-Phase AC Voltage Transformer (Qty: 1)", "SCT-013-000 100A Non-Invasive AC Current Clamp (Qty: 1)", "RC522 RFID Module (Qty: 1)", "12V 2A SMPS Power Supply (Qty: 1)", "LM2596 DC-DC Buck Module (Qty: 1)", "LM358 Dual Op-Amp Signal Clamping IC (Qty: 2)", "AC/DC Non-Linear Load Simulator (Qty: 1)", "830 Breadboard, 10kΩ Bias Resistors, 10µF Tantalum Caps, Jumpers (Qty: 1)"]},
    {"id": 34, "domain": "Renewable Energy & Power Systems", "title": "Solar Microgrid & Black-Start", "category": "HARDWARE",
     "desc": "Develop a black-start controller that safely restores a renewable-energy microgrid after a complete blackout by sequencing loads.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "6V 3W Mini Solar Panel (Qty: 1)", "ZMPT101B AC Voltage Sensor Module (Qty: 1)", "ACS712 20A Hall Current Sensor Modules (Qty: 2)", "4-Channel 5V Relay Module (Qty: 1)", "RC522 RFID Module (Qty: 1)", "12V 5A 60W Industrial SMPS Power Supply (Qty: 1)", "LM2596S DC-DC Buck Module (Qty: 1)", "ULN2803A Darlington Transistor Array IC (Qty: 1)", "PC817 Optocoupler IC (Qty: 4)", "830 Breadboard, 1N4007 Diodes, AC Snubber Caps, Industrial Terminals (Qty: 1)"]},
    {"id": 35, "domain": "Renewable Energy & Power Systems", "title": "Electric Vehicles & Vehicle-to-Grid (V2G) Tech", "category": "HARDWARE",
     "desc": "Develop a smart V2G controller that coordinates EV power feed back into the grid based on peak demand while maintaining minimum battery availability.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "ACS712 30A Bidirectional Current Sensor (Qty: 2)", "MCP2515 CAN Bus Controller SPI Module + TJA1050 IC (Qty: 1)", "RC522 13.56MHz RFID Reader (Qty: 1)", "12V 10A 120W SMPS Industrial Unit (Qty: 1)", "IRF3205 N-Channel MOSFET Power Switch Modules (Qty: 2)", "LM393 Dual Voltage Comparator IC (Qty: 1)", "LM2596S DC-DC Step Down Buck Module (Qty: 1)", "830 Breadboard, Power Terminals, 1000µF Filter Caps, Shunts, 14AWG Wire (Qty: 1)"]},
    {"id": 36, "domain": "Renewable Energy & Power Systems", "title": "Urban Renewable Energy", "category": "HARDWARE",
     "desc": "Develop a small-scale energy harvesting system capturing low-level wind or footfall kinetic energy and converting it into electrical storage.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "Piezoelectric Vibration Transducer Discs (Pack of 5) (Qty: 1)", "Mini 3-Phase AC Wind Dynamo Generator Motor (Qty: 1)", "2.7V 10F Supercapacitor (Qty: 2)", "LTC3588 Energy Harvesting Power Supply IC Module (Qty: 1)", "RC522 RFID Module (Qty: 1)", "5V 2A SMPS Power Supply (Qty: 1)", "1N5819 Schottky Diode Bridge Rectifier IC Array (Qty: 4)", "400 Breadboard, Zener Diodes, Jumpers, Storage Caps (Qty: 1)"]},
    {"id": 37, "domain": "Renewable Energy & Power Systems", "title": "Railway Energy Harvesting", "category": "HARDWARE",
     "desc": "Develop a vibration-energy harvesting system capturing mechanical track vibrations from train transit for self-powered track monitors.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "Piezoelectric Ceramic Energy Harvester Module (Qty: 1)", "INA219 I2C Micro-Power Monitoring Module (Qty: 1)", "SW-420 High Sensitivity Vibration Sensor Module (Qty: 1)", "RC522 RFID Module (Qty: 1)", "12V 2A Enclosed SMPS Unit (Qty: 1)", "LM2596 DC-DC Buck Module (Qty: 1)", "DB107 Full Wave Diode Bridge Rectifier IC (Qty: 1)", "830 Breadboard, Supercapacitors (5V), 10k Resistors, Jumpers (Qty: 1)"]},
    {"id": 38, "domain": "Renewable Energy & Power Systems", "title": "Community Microgrid & Energy Sharing", "category": "HARDWARE",
     "desc": "Develop an intelligent microgrid controller that manages distributed renewable assets and balances islanded microgrid clusters.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "PZEM-004T Multi-Function AC Power Meter (Qty: 1)", "2-Channel 5V Optocoupled Relay Module (30A) (Qty: 1)", "RC522 RFID Module (Qty: 1)", "12V 5A 60W SMPS Power Supply (Qty: 1)", "16x2 I2C Character LCD Display (Qty: 1)", "LM2596 DC-DC Step-Down Buck Module (Qty: 1)", "PC817 Optocoupler IC (Qty: 2)", "830 Breadboard, Power Terminals, 16AWG Wiring, Snubber Caps (Qty: 1)"]},
    {"id": 39, "domain": "Renewable Energy & Power Systems", "title": "Wind Energy & Predictive Maintenance", "category": "HARDWARE",
     "desc": "Develop a wind-turbine condition monitoring unit tracking vibration, bearing temperature, RPM, and power output to predict failures.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "ADXL345 3-Axis Digital Accelerometer (Qty: 1)", "LM393 Optical IR Speed/RPM Sensor Module (Qty: 1)", "DS18B20 Waterproof Temperature Sensor Probe (Qty: 1)", "12V DC Motor (Turbine Drive Sim) (Qty: 1)", "RC522 RFID Module (Qty: 1)", "12V 3A SMPS Power Supply Unit (Qty: 1)", "LM2596 DC-DC Buck Module (Qty: 1)", "74HC14 Schmitt Trigger IC (Qty: 1)", "830 Breadboard, Jumpers, 4.7k Pull-up Resistors, Status LEDs (Qty: 1)"]},
    {"id": 40, "domain": "Renewable Energy & Power Systems", "title": "Regenerative Energy Recovery", "category": "HARDWARE",
     "desc": "Develop a scaled regenerative braking system capturing energy from descending elevators and safely storing or dumping excess power.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "12V High-Torque DC Motor/Generator (Qty: 1)", "INA219 Bidirectional Voltage & Current I2C Module (Qty: 1)", "Supercapacitor Bank (5.4V 5F Series/Parallel) (Qty: 2)", "IRFB3077/IRF3205 N-MOSFET (Qty: 2)", "RC522 13.56MHz RFID Module (Qty: 1)", "12V 5A Industrial Enclosed SMPS Unit (Qty: 1)", "LM2596S DC-DC Step-Down Buck Converter Module (Qty: 1)", "TC4427/IR2104 Dual Gate Driver IC (Qty: 1)", "PC817 Optocoupler IC (Qty: 2)", "1N5822 3A Schottky Flyback Diodes (Qty: 4)", "Ceramic Power Dump Resistors (10Ω 10W), 830 Breadboard, Terminals (Qty: 1)"]},
    {"id": 41, "domain": "Renewable Energy & Power Systems", "title": "Solar PV Predictive Maintenance & Soiling", "category": "HARDWARE",
     "desc": "Develop a low-cost PV monitoring device comparing expected irradiance with actual output to identify persistent soiling and dust buildup.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "6V 3W Mini Solar Panel (Qty: 1)", "BH1750 Digital Ambient Light / Lux Sensor (I2C) (Qty: 1)", "INA219 High-Side DC Voltage & Current Sensor Module (Qty: 1)", "DS18B20 Waterproof Digital Temperature Probe (Qty: 1)", "RC522 RFID Module (Qty: 1)", "12V 2A Enclosed SMPS Power Supply (Qty: 1)", "LM2596S DC-DC Step-Down Buck Module (Qty: 1)", "LM358 Dual Op-Amp IC (Qty: 1)", "AMS1117-3.3V LDO IC (Qty: 2)", "830 Breadboard, 4.7kΩ Pull-Up Resistors, 100nF Filter Caps, Jumpers (Qty: 1)"]},
    {"id": 42, "domain": "Renewable Energy & Power Systems", "title": "Solar Farm Yield Forecasting", "category": "SOFTWARE",
     "desc": "Develop a software system integrating meteorological satellite feeds to predict hour-ahead solar power generation for transmission grid stability.",
     "components": []},
    {"id": 43, "domain": "Renewable Energy & Power Systems", "title": "Microgrid Load Balancing Algorithm", "category": "SOFTWARE",
     "desc": "Develop an autonomous software engine that dynamically redistributes renewable power among peer-to-peer consumers to avoid localized blackouts.",
     "components": []},

    # DOMAIN 06: Aerospace, Aviation & Space Tech
    {"id": 44, "domain": "Aerospace, Aviation & Space Tech", "title": "UAV Safety & Autonomous Landing", "category": "HARDWARE",
     "desc": "Develop an autonomous emergency landing unit for drones that detects in-flight propulsion failure and guides descent to a safe landing zone.",
     "components": ["ESP32-S3-DevKitC-1 (Qty: 1)", "MPU-6050 6-DOF IMU Accelerometer Module (Qty: 1)", "BMP280 High-Precision Barometric Pressure Sensor (Qty: 1)", "MG996R High-Torque Metal Gear Servo Motor (Qty: 1)", "RC522 RFID Module (Qty: 1)", "12V 5A Bench SMPS (Qty: 1)", "TP4056 Module + 3.7V 800mAh High-Discharge LiPo (Qty: 1)", "PC817 Optocoupler IC (Qty: 2)", "Mini 170 Breadboard, 5V Active Buzzer, High-Bright LED, Jumpers (Qty: 1)"]},
    {"id": 45, "domain": "Aerospace, Aviation & Space Tech", "title": "Autonomous Navigation & Collision Avoidance", "category": "HARDWARE",
     "desc": "Develop an obstacle detection and path replanning module enabling UAVs to detect powerlines and obstacles in real time.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "VL53L0X Time-of-Flight Laser Distance Sensors (Qty: 3)", "HC-SR04 Ultrasonic Distance Sensor Modules (Qty: 2)", "RC522 RFID Module (Qty: 1)", "12V 5A Bench SMPS (Qty: 1)", "LM2596 DC-DC Step-Down Buck Converter (Qty: 1)", "74HC14 Hex Inverting Schmitt Trigger IC (Qty: 1)", "Bidirectional Logic Level Converter (Qty: 3)", "830 Breadboard, 4.7k Pullup Resistors, 10µF Caps, Jumpers (Qty: 1)"]},
    {"id": 46, "domain": "Aerospace, Aviation & Space Tech", "title": "Energy-Efficient UAV Operations", "category": "HARDWARE",
     "desc": "Develop an energy-aware UAV mission computer that recalculates flight paths dynamically based on instantaneous battery discharge and headwind.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "INA219 High-Side I2C Current Sensor (Qty: 2)", "RC522 RFID Module (Qty: 1)", "12V 5A Industrial Bench SMPS Unit (Qty: 1)", "LM2596 DC-DC Buck Converter Module (Qty: 1)", "0.96-inch OLED I2C Display Module (Qty: 1)", "AMS1117-3.3V LDO IC (Qty: 2)", "830 Breadboard, Power Shunt Resistors, Filter Caps, Jumpers (Qty: 1)"]},
    {"id": 47, "domain": "Aerospace, Aviation & Space Tech", "title": "Aircraft Electrical Systems & Fault Management", "category": "HARDWARE",
     "desc": "Develop a multi-bus electrical fault isolation system that disconnects shorted avionics lines and reroutes power via alternate buses.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "ACS712 20A Hall-Effect Current Sensor Modules (Qty: 3)", "ZMPT101B Active AC/DC Voltage Sensor Modules (Qty: 3)", "4-Channel 5V Relay Isolation Module (Qty: 1)", "RC522 RFID Module (Qty: 1)", "12V 10A 120W SMPS Power Supply (Qty: 1)", "ULN2803A Darlington Transistor Driver IC (Qty: 1)", "LM358 Dual Op-Amp ICs (Qty: 2)", "LM2596S Buck Module (Qty: 1)", "830 Breadboard & Terminal Blocks (Qty: 1)"]},
    {"id": 48, "domain": "Aerospace, Aviation & Space Tech", "title": "Autonomous Search & Rescue", "category": "HARDWARE",
     "desc": "Develop a compact drone payload that scans disaster zones, detects human presence using thermal signatures, and beacons GPS coordinates.",
     "components": ["ESP32-S3-WROOM-1 DevKit with OV2640 Camera (Qty: 1)", "NEO-6M GPS Module with Active Antenna (Qty: 1)", "RC522 RFID Module (Qty: 1)", "12V 3A SMPS Power Supply (Qty: 1)", "LM2596 DC-DC Step-Down Buck Module (Qty: 1)", "High-Decibel 5V Alarm Siren + Ultra-Bright 3W LED (Qty: 1)", "TIP122 Darlington Transistor IC (Qty: 1)", "Mini Solderless Breadboard, 10kΩ Resistors, 1N4007 Diodes, Jumpers (Qty: 1)"]},
    {"id": 49, "domain": "Aerospace, Aviation & Space Tech", "title": "Spacecraft Power Management", "category": "HARDWARE",
     "desc": "Develop a fault-tolerant satellite EPS module prioritizing onboard instrument power and shedding non-critical payload during eclipse periods.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "INA226 I2C High-Accuracy Power Monitor IC Boards (Qty: 3)", "IRF540N N-Channel Power MOSFET Switch Modules (Qty: 4)", "RC522 RFID Module (Qty: 1)", "12V 10A 120W SMPS Power Supply Unit (Qty: 1)", "LM2596S Adjustable Buck Converter Module (Qty: 2)", "LM358 Dual Op-Amp IC (Qty: 2)", "PC817 Optocoupler IC (Qty: 4)", "830 Breadboard, Power Terminals, 16AWG Wiring, 10kΩ Pull-downs (Qty: 1)"]},
    {"id": 50, "domain": "Aerospace, Aviation & Space Tech", "title": "Space Safety & Debris Collision Avoidance", "category": "SOFTWARE",
     "desc": "Develop an orbital mechanics simulator that ingests TLE space debris data, predicts conjunction risks, and computes fuel-optimal thruster burns.",
     "components": []},
    {"id": 51, "domain": "Aerospace, Aviation & Space Tech", "title": "UAV Fleet Traffic Management (UTM)", "category": "SOFTWARE",
     "desc": "Develop a centralized airspace coordinator managing commercial delivery drone corridors, adhering to geofenced no-fly zones.",
     "components": []},
    {"id": 52, "domain": "Aerospace, Aviation & Space Tech", "title": "Satellite Telemetry Anomaly Detection", "category": "SOFTWARE",
     "desc": "Develop an AI/ML time-series engine that parses multi-channel satellite housekeeping telemetry to uncover subtle degradation patterns.",
     "components": []},

    # DOMAIN 07: Cybersecurity & Digital Forensics
    {"id": 53, "domain": "Cybersecurity & Digital Forensics", "title": "Wireless Network Security", "category": "HARDWARE",
     "desc": "Develop an edge intrusion monitor that detects 802.11 deauthentication attacks, rogue Wi-Fi clones, and maintains an offline alert log.",
     "components": ["ESP32-WROOM-32U DevKit + 2.4GHz Antenna (Qty: 1)", "5V 2A SMPS Wall Power Adapter (Qty: 1)", "0.96-inch I2C OLED Display (SSD1306) (Qty: 1)", "5V Active Piezo Buzzer (Qty: 1)", "MicroSD Card Adapter Module (SPI) + 16GB Card (Qty: 1)", "AMS1117-3.3V LDO Voltage Regulator IC (Qty: 2)", "830-Tie Point Breadboard, 10kΩ/330Ω Resistors, Decoupling Caps, LEDs, Jumpers (Qty: 1)"]},
    {"id": 54, "domain": "Cybersecurity & Digital Forensics", "title": "USB Security & Hardware-Based Cybersecurity", "category": "HARDWARE",
     "desc": "Develop an inline hardware security device that screens incoming USB endpoints, dropping rogue Human Interface Device (HID) keystroke injection.",
     "components": ["ESP32-S3-DevKitC-1 (Dual Type-C) (Qty: 1)", "MAX3421E USB Host Controller IC Module (Qty: 1)", "RC522 RFID Module (Qty: 1)", "5V 2A Low-Noise SMPS Power Adapter (Qty: 1)", "TPD4E001 ESD Protection Diode Array IC (Qty: 2)", "0.96-inch OLED Display (Qty: 1)", "5V Active Piezo Buzzer (Qty: 1)", "830 Breadboard, USB Breakouts, 22Ω Resistors, Jumpers (Qty: 1)"]},
    {"id": 55, "domain": "Cybersecurity & Digital Forensics", "title": "Digital Forensics & Evidence Analysis", "category": "SOFTWARE",
     "desc": "Develop an automated digital forensic tool parsing file system metadata, generating cryptographic SHA-256 hashes, and building forensic timelines.",
     "components": []},
    {"id": 56, "domain": "Cybersecurity & Digital Forensics", "title": "Forensic Evidence Protection (Write-Blocker)", "category": "HARDWARE",
     "desc": "Develop an inline forensic write-blocker intercepting SD/USB mass storage commands, allowing investigators read-only analysis without contamination.",
     "components": ["ESP32-S3-DevKitC-1 (Dual Type-C) (Qty: 1)", "MAX3421E USB Host Controller Module (Qty: 1)", "RC522 13.56MHz RFID Module (Qty: 1)", "12V 3A SMPS Dual-Rail Power Supply (Qty: 1)", "LM2596S DC-DC Step-Down Buck Converter (Qty: 1)", "TPS2051 Current-Limited Power Distribution Switch IC (Qty: 2)", "16x2 I2C LCD Display + Active Buzzer (Qty: 1)", "830 Breadboard, Shunt Resistors, Status LEDs, Jumpers (Qty: 1)"]},
    {"id": 57, "domain": "Cybersecurity & Digital Forensics", "title": "Cyber Incident Response & Digital Evidence", "category": "SOFTWARE",
     "desc": "Develop an evidence repository establishing tamper-evident chains of custody using Merkle trees and cryptographic verification.",
     "components": []},
    {"id": 58, "domain": "Cybersecurity & Digital Forensics", "title": "Secure Digital Forensics & Field Investigation", "category": "HARDWARE",
     "desc": "Develop a portable, biometric/RFID access-controlled storage imager that logs session operators and detects physical chassis tampering.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "12V Micro Solenoid Electronic Cabinet Lock (Qty: 1)", "RC522 RFID Module (Qty: 1)", "SW-420 Vibration / Tamper Tilt Sensor Module (Qty: 1)", "12V 3A SMPS Enclosed Industrial Unit (Qty: 1)", "LM2596 DC-DC Buck Converter (Qty: 1)", "ULN2003 Driver IC (Qty: 1)", "1N4007 Flyback Diodes (Qty: 4)", "830 Breadboard, Magnetic Reed Switch, 10k Resistors, Jumpers (Qty: 1)"]},
    {"id": 59, "domain": "Cybersecurity & Digital Forensics", "title": "Ransomware Behavior Isolation System", "category": "SOFTWARE",
     "desc": "Develop an endpoint security agent detecting rapid, high-entropy file modifications and autonomously isolating infected hosts from the network.",
     "components": []},
    {"id": 60, "domain": "Cybersecurity & Digital Forensics", "title": "Automated Phishing Threat Intelligence Pipeline", "category": "SOFTWARE",
     "desc": "Develop a triage pipeline extracting headers and URLs from suspicious user-submitted emails, querying sandboxes and updating security boundaries.",
     "components": []},

    # DOMAIN 08: Agriculture & Aquaculture
    {"id": 61, "domain": "Agriculture & Aquaculture", "title": "Water Management & Smart Irrigation", "category": "HARDWARE",
     "desc": "Develop an autonomous irrigation controller that evaluates localized soil moisture and temperature to govern multi-valve water delivery.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "Capacitive Soil Moisture Sensor V1.2 (Corrosion-Free) (Qty: 3)", "12V DC Solenoid Water Valve (1/2 Inch N/C) (Qty: 1)", "12V Mini Submersible Water Pump (Qty: 1)", "1-Channel Optoisolated 5V Relay Module (Qty: 1)", "RC522 RFID Module (Qty: 1)", "12V 5A 60W Industrial Metal SMPS Supply (Qty: 1)", "LM2596 DC-DC Step-Down Buck Module (Qty: 1)", "1N4007 Silicon Rectifier Diodes (Qty: 4)", "830 Breadboard, Barrier Terminals, Jumper Wires, Status LEDs, 18AWG Output Wire (Qty: 1)"]},
    {"id": 62, "domain": "Agriculture & Aquaculture", "title": "Precision Agriculture - Crop Health Monitoring", "category": "HARDWARE",
     "desc": "Develop a drone payload using calibrated multispectral/optical sensors to survey vegetative health and identify crop blight.",
     "components": ["ESP32-S3-WROOM-1 DevKit with OV2640 Camera (Qty: 1)", "DHT22 Digital Temperature & Humidity Sensor (Qty: 1)", "RC522 RFID Module (Qty: 1)", "MicroSD Card Module + 16GB Card (Qty: 1)", "0.96-inch I2C OLED Screen (Qty: 1)", "12V 3A SMPS Power Supply Unit (Qty: 1)", "LM2596 DC-DC Step-Down Buck Module (Qty: 1)", "AMS1117-3.3V LDO IC (Qty: 2)", "Miniature Coreless Motor & Propeller Set (Qty: 1)", "830 Breadboard, Jumper Wires, 10kΩ Pull-ups, Filter Capacitors (Qty: 1)"]},
    {"id": 63, "domain": "Agriculture & Aquaculture", "title": "Energy Management & Predictive Maintenance", "category": "HARDWARE",
     "desc": "Develop an edge diagnostic monitor detecting dry running, motor cavitation, phase unbalance, and abnormal pump vibration.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "ACS712 30A Current Sensor Module (Qty: 2)", "DS18B20 Waterproof Stainless Motor Temp Probe (Qty: 1)", "SW-420 Vibration Sensor Module (Qty: 1)", "1-Channel 30A High-Current Relay Module (Qty: 1)", "12V Mini Submersible Water Pump (Simulation Load) (Qty: 1)", "RC522 RFID Module (Qty: 1)", "12V 5A Industrial SMPS Power Supply (Qty: 1)", "LM2596 DC-DC Step-Down Buck Module (Qty: 1)", "TIP122 Darlington Transistor IC (Qty: 1)", "830 Breadboard, Terminal Blocks, Jumper Wires, Status LEDs, High-Gauge AC Wire (Qty: 1)"]},
    {"id": 64, "domain": "Agriculture & Aquaculture", "title": "Climate Resilience & Crop Protection", "category": "HARDWARE",
     "desc": "Develop a micro-climate forecasting node calculating frost points and automatically actuating protective thermal sprinklers or warm blowers.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "SHT31 High-Precision Temperature & Humidity Sensor (Qty: 1)", "BMP280 Barometric Pressure & Dew Point Sensor (Qty: 1)", "12V 2-Channel Relay Module (Qty: 1)", "12V PTC Heater & 5V Mini Pump (Sim) (Qty: 1)", "RC522 RFID Module (Qty: 1)", "12V 5A Enclosed Industrial SMPS Unit (Qty: 1)", "LM2596 DC-DC Step-Down Buck Module (Qty: 1)", "PC817 Optocoupler IC (Qty: 2)", "830 Breadboard, Barrier Terminals, 1N4007 Diodes, 18AWG Output Wire (Qty: 1)"]},
    {"id": 65, "domain": "Agriculture & Aquaculture", "title": "Soil Health Monitoring (Edge AI)", "category": "HARDWARE",
     "desc": "Develop a field probe evaluating soil electrical conductivity (EC), pH, and moisture parameters to summarize soil viability without internet.",
     "components": ["ESP32-S3 DevKit (TinyML Polynomial Fitting) (Qty: 1)", "Analog Soil pH Sensor Probe & Conditioning Board (Qty: 1)", "Analog Soil Electrical Conductivity (EC) Probe (Qty: 1)", "Capacitive Soil Moisture Sensor V1.2 (Qty: 1)", "RC522 RFID Module (Qty: 1)", "12V 3A SMPS Power Supply Unit (Qty: 1)", "LM2596 DC-DC Step-Down Buck Module (Qty: 1)", "LM358 Dual Op-Amp IC (Qty: 2)", "830 Breadboard, 0.96-inch OLED Screen, Calibration Trimpots, Bypass Caps (Qty: 1)"]},
    {"id": 66, "domain": "Agriculture & Aquaculture", "title": "Aquaculture & Water Quality Management", "category": "HARDWARE",
     "desc": "Develop an automated water quality system monitoring dissolved oxygen proxies, pH, and turbidity, driving aerators when parameters deteriorate.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "Analog Industrial pH Sensor Kit with BNC Interface (Qty: 1)", "DS18B20 Waterproof Stainless Water Temp Probe (Qty: 1)", "Analog Optical Turbidity Sensor Module (Qty: 1)", "4-Channel 5V Relay Module (Qty: 1)", "5V Submersible Pump & SG90 Servo (Sim) (Qty: 1)", "RC522 RFID Module (Qty: 1)", "12V 10A 120W Industrial SMPS Power Supply (Qty: 1)", "LM2596 DC-DC Step-Down Buck Module (Qty: 1)", "PC817 Optocoupler ICs (Qty: 4)", "830 Breadboard, Power Terminals, Waterproof Glands, 4.7kΩ Pull-ups (Qty: 1)"]},
    {"id": 67, "domain": "Agriculture & Aquaculture", "title": "Smart Greenhouse Climate & Fogging Automation", "category": "HARDWARE",
     "desc": "Develop an automated greenhouse system regulating vapor pressure deficits (VPD) through synchronized exhaust venting and ultrasonic misting.",
     "components": ["ESP32-WROOM-32 Dev Board (Qty: 1)", "DHT22 High-Accuracy Temperature & Humidity Sensor (Qty: 1)", "BH1750 Digital Ambient Light/Lux Sensor Module (Qty: 1)", "Capacitive Soil Moisture Sensor Module (Qty: 2)", "2-Channel 5V Optocoupled Relay Module (Qty: 1)", "12V Mini Exhaust Fan & 5V Mist Maker (Sim) (Qty: 1)", "RC522 RFID Module (Qty: 1)", "12V 5A 60W Metal Industrial SMPS Supply (Qty: 1)", "LM2596 DC-DC Step-Down Buck Module (Qty: 1)", "TIP122 Darlington Transistor IC (Qty: 2)", "830 Breadboard, Terminal Blocks, 1N4007 Diodes, Jumpers (Qty: 1)"]},
    {"id": 68, "domain": "Agriculture & Aquaculture", "title": "Crop Yield Prediction & Commodity Market Triage", "category": "SOFTWARE",
     "desc": "Develop a predictive analytics software pipeline fusing NDVI satellite imagery and commodity indices to suggest optimal harvest liquidation windows.",
     "components": []},
    {"id": 69, "domain": "Agriculture & Aquaculture", "title": "Aquaculture Feeding Rate Optimization Engine", "category": "SOFTWARE",
     "desc": "Develop an algorithmic feeding controller adjusting feeding schedules dynamically based on water temperature, dissolved oxygen, and fish biomass growth.",
     "components": []}
]

ps_titles = [f"PS #{ps['id']:02d}: {ps['title']}" for ps in PROBLEM_STATEMENTS]

# ==============================================================================
# VIEW 1: HOME PAGE (SIH THEME LISTING)
# ==============================================================================
if st.session_state.page == 'home':
    st.markdown("""
    <div class="hero-banner">
        <div class="inst-tag">Smart India Hackathon 2026 Initiative</div>
        <div class="hero-title">WCE National Hackathon 2026</div>
        <div class="hero-sub">Official Portal for Problem Statements, Prototyping Hardware Specifications, and Team Registration. Hosted by Walchand College of Engineering.</div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Official Problem Statement Compendium")
    
    # Compendium Preview / Download
    doc_filename = "Problem_Statements_Updated.docx"
    with st.expander("👁️ Click here to Preview the Official Compendium Document", expanded=False):
        encoded_doc_name = urllib.parse.quote(doc_filename)
        github_raw_url = f"https://github.com/Aditya-9600/hackathon-portal/raw/main/{encoded_doc_name}"
        viewer_url = f"https://docs.google.com/viewer?url={github_raw_url}&embedded=true"
        components.iframe(viewer_url, height=580, scrolling=True)

    if os.path.exists(doc_filename):
        with open(doc_filename, "rb") as fp:
            st.download_button("⬇️ Download Document (.docx)", data=fp, file_name=doc_filename, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    st.markdown("---")
    
    # Filter UI
    f_col1, f_col2, f_col3 = st.columns([1.5, 1, 1.5])
    domains = ["All Domains"] + sorted(list(set(ps["domain"] for ps in PROBLEM_STATEMENTS)))
    with f_col1:
        selected_domain = st.selectbox("Filter by Domain", domains)
    with f_col2:
        selected_cat = st.selectbox("Category", ["All Categories", "HARDWARE", "SOFTWARE"])
    with f_col3:
        search_query = st.text_input("Search Keyword or Title", placeholder="e.g. EV, Solar, Drone")

    filtered_list = PROBLEM_STATEMENTS
    if selected_domain != "All Domains":
        filtered_list = [ps for ps in filtered_list if ps["domain"] == selected_domain]
    if selected_cat != "All Categories":
        filtered_list = [ps for ps in filtered_list if ps["category"] == selected_cat]
    if search_query:
        q = search_query.lower()
        filtered_list = [ps for ps in filtered_list if q in ps["title"].lower() or q in ps["desc"].lower()]

    st.write(f"Showing **{len(filtered_list)}** problem statement(s):")

    # Interactive Problem Statement List (SIH Table style)
    for ps in filtered_list:
        with st.expander(f"PS #{ps['id']:02d}: {ps['title']}"):
            c_tag = "badge-hw" if ps['category'] == "HARDWARE" else "badge-sw"
            st.markdown(f'<span class="{c_tag}">{ps["category"]}</span> &nbsp; <b style="color:#1E3A8A;">{ps["domain"]}</b>', unsafe_allow_html=True)
            st.markdown(f"<p style='margin-top: 15px; font-size: 1.05rem;'>{ps['desc']}</p>", unsafe_allow_html=True)
            
            st.markdown("---")
            if ps["category"] == "SOFTWARE":
                st.info("ℹ️ **There is no hardware or components for this problem statement.** Evaluation will be based on software architecture and performance.")
            else:
                st.markdown("#### 📦 Expected Hardware Components:")
                col_c1, col_c2 = st.columns(2)
                mid_pt = (len(ps['components']) + 1) // 2
                with col_c1:
                    for comp in ps['components'][:mid_pt]:
                        st.markdown(f"🔹 {comp}")
                with col_c2:
                    for comp in ps['components'][mid_pt:]:
                        st.markdown(f"🔹 {comp}")

            # Register Now Button placed directly underneath the components
            st.markdown("<br>", unsafe_allow_html=True)
            ps_formatted_title = f"PS #{ps['id']:02d}: {ps['title']}"
            st.button(
                f"Register Now for PS #{ps['id']:02d}", 
                type="primary", 
                key=f"btn_reg_{ps['id']}", 
                on_click=navigate_to, 
                args=('registration', ps_formatted_title)
            )

# ==============================================================================
# VIEW 2: REGISTRATION & PAYMENT
# ==============================================================================
elif st.session_state.page == 'registration':
    st.button("⬅️ Back to Problem Statements", on_click=navigate_to, args=('home',))
    
    st.subheader("Team Registration & Checkout")
    st.write("Complete the details below to register your team. **All 5 team members are compulsory**.")
    st.info("💳 **Registration Fee: ₹350 per team**")

    default_ps_index = 0
    if st.session_state.selected_ps in ps_titles:
        default_ps_index = ps_titles.index(st.session_state.selected_ps)

    with st.form("team_registration_form"):
        st.markdown("#### 1. Team Profile")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            team_name = st.text_input("Team Name *", placeholder="e.g. Walchand Innovators")
        with col_t2:
            assigned_ps = st.selectbox("Allocated Problem Statement *", ps_titles, index=default_ps_index)

        st.markdown("---")
        st.markdown("#### 2. Core Members (All 5 Compulsory)")
        
        st.markdown("**Member 1 (Team Leader)**")
        col_m1a, col_m1b, col_m1c = st.columns(3)
        with col_m1a:
            leader_name = st.text_input("Leader Full Name *")
        with col_m1b:
            leader_email = st.text_input("Leader Email *")
        with col_m1c:
            leader_phone = st.text_input("Leader Phone Number *")

        col_m2, col_m3 = st.columns(2)
        with col_m2:
            m2_name = st.text_input("Member 2 Full Name *")
            m4_name = st.text_input("Member 4 Full Name *")
        with col_m3:
            m3_name = st.text_input("Member 3 Full Name *")
            m5_name = st.text_input("Member 5 Full Name *")

        st.markdown("---")
        st.markdown("#### 3. Custom Component Requests (Optional)")
        st.caption("If your team requires additional components beyond the expected list, categorize them below:")

        cat_col1, cat_col2 = st.columns(2)
        with cat_col1:
            cat_boards = st.text_input("Microcontrollers & Boards")
            cat_sensors = st.text_input("Sensors & Modules")
            cat_power = st.text_input("Power & Batteries")
        with cat_col2:
            cat_motors = st.text_input("Motors, Relays & Actuators")
            cat_displays = st.text_input("Displays & Indicators")
            cat_misc = st.text_input("Misc / Passives / Wiring")

        st.markdown("---")
        submit_btn = st.form_submit_button("Proceed to Payment Checkout (₹350)", type="primary")

    if submit_btn:
        if not team_name.strip():
            st.error("⚠️ Team Name is required.")
        elif not leader_name.strip() or not leader_email.strip() or not leader_phone.strip():
            st.error("⚠️ Team Leader Name, Email, and Phone Number are all compulsory.")
        elif not m2_name.strip() or not m3_name.strip() or not m4_name.strip() or not m5_name.strip():
            st.error("⚠️ All 5 team member names are compulsory.")
        else:
            hardware_summary = f"""Boards: {cat_boards.strip() or 'None'} | Sensors: {cat_sensors.strip() or 'None'} | Power: {cat_power.strip() or 'None'} | Actuators: {cat_motors.strip() or 'None'} | Displays: {cat_displays.strip() or 'None'} | Misc: {cat_misc.strip() or 'None'}"""
            
            order_id = f"WCE_{uuid.uuid4().hex[:6].upper()}"
            st.session_state["registration_record"] = {
                "order_id": order_id,
                "team_name": team_name,
                "ps": assigned_ps,
                "leader_name": leader_name,
                "leader_email": leader_email,
                "leader_phone": leader_phone,
                "m2_name": m2_name,
                "m3_name": m3_name,
                "m4_name": m4_name,
                "m5_name": m5_name,
                "custom_components": hardware_summary,
                "amount": 350.00,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.success("✅ Team registration profile validated! Please complete the UPI checkout below.")

    # Payment Checkout Block
    if "registration_record" in st.session_state:
        rec = st.session_state["registration_record"]
        st.markdown("---")
        st.subheader("UPI Payment & 12-Digit UTR Verification")

        col_pay1, col_pay2 = st.columns([1, 1.5])
        with col_pay1:
            upi_id = "9322753587@ptyes"  
            payee_name = "WCE Hackathon 2026"
            upi_string = f"upi://pay?pa={upi_id}&pn={urllib.parse.quote(payee_name)}&am=350.00&cu=INR&tn={rec['order_id']}"

            qr = qrcode.QRCode(version=1, box_size=8, border=3)
            qr.add_data(upi_string)
            qr.make(fit=True)
            img = qr.make_image(fill_color="#05234A", back_color="white")

            buf = BytesIO()
            img.save(buf, format="PNG")
            st.image(buf.getvalue(), caption="Scan via GPay, PhonePe, or Paytm (Fixed ₹350)", width=240)

        with col_pay2:
            st.markdown(f"""
            **Order ID:** `{rec['order_id']}`  
            **Registered Team:** {rec['team_name']}  
            **Selected Statement:** {rec['ps']}  
            **Registration Fee:** **₹350.00**  

            **Instructions:**
            1. Open any UPI application (Google Pay, PhonePe, Paytm, BHIM).
            2. Scan the QR code or transfer to the designated UPI ID.
            3. Copy the **12-digit UTR / UPI Transaction Reference Number** from your payment receipt and enter it below.
            """)

        with st.form("utr_verification_form"):
            utr_input = st.text_input("Enter 12-Digit UPI Transaction ID / UTR Number *", max_chars=12, placeholder="12 numeric digits")
            submit_utr = st.form_submit_button("Submit UTR & Finalize Registration", type="primary")

            if submit_utr:
                if not utr_input.isdigit() or len(utr_input) != 12:
                    st.error("❌ Invalid UTR format. Please provide a valid 12-digit numeric UPI reference number.")
                else:
                    with st.spinner("Connecting to WCE database & logging registration..."):
                        payload = rec.copy()
                        payload['utr'] = utr_input
                        
                        # ⚠️ CRITICAL: Replace the placeholder below with your GOOGLE APPS SCRIPT WEBHOOK URL.
                        webhook_url = "https://script.google.com/macros/s/YOUR_APPS_SCRIPT_WEBHOOK_URL_HERE/exec"
                        
                        try:
                            res = requests.post(webhook_url, json=payload, timeout=10)
                            if res.status_code == 200:
                                st.success(f"🎉 Payment reference `{utr_input}` successfully recorded for Team **{rec['team_name']}**!")
                                st.balloons()
                                st.info("Registration status: **Pending Verification**. The organizing committee will reconcile the UTR and issue your team credentials.")
                                del st.session_state["registration_record"]
                            else:
                                st.error("Database sync failed. Please verify your internet connection or resubmit.")
                        except Exception as e:
                            st.error("Webhook Error: Did you paste your Apps Script Deployment URL into the code? You cannot use the standard docs.google.com link here.")

# ==============================================================================
# FOOTER
# ==============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 1rem 0;">
    Walchand College of Engineering, Sangli • National Level Hackathon 2026 Portal<br>
    Built with Python & Streamlit • Autonomous Engineering Institute
</div>
""", unsafe_allow_html=True)
