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
# 1. PAGE CONFIGURATION & INITIALIZATION
# ==============================================================================
st.set_page_config(
    page_title="WCE Electrical Dept | Hackathon 2026",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session States
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_ps' not in st.session_state:
    st.session_state.selected_ps = None
if 'active_ps' not in st.session_state:
    st.session_state.active_ps = None  
if 'ps_locked' not in st.session_state:
    st.session_state.ps_locked = False

def navigate_to(page_name, ps_title=None):
    st.session_state.page = page_name
    if page_name == 'home':
        # Unlock the dropdown if they go back home to choose a different PS
        st.session_state.ps_locked = False
        
    if ps_title:
        st.session_state.selected_ps = ps_title
        # Lock the dropdown because they came from a specific "Register Now" button
        st.session_state.ps_locked = True
        
    st.session_state.active_ps = None 

# ==============================================================================
# 2. THEME STYLING (ANIMATIONS & CUSTOM COMPONENTS)
# ==============================================================================
st.markdown("""
<style>
    /* HIDE STREAMLIT & GITHUB ICONS (Security/Clean UI) */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .viewerBadge_container__1QSob {display: none !important;}
    .stDeployButton {display:none !important;}
    [data-testid="stToolbar"] {display: none !important;}

    /* Lightweight Tech Background */
    .stApp {
        background-color: #F0F4F8 !important;
        background-image: radial-gradient(#CBD5E1 1px, transparent 1px) !important;
        background-size: 25px 25px !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Ensure Native Text is Dark for Readability */
    .stApp p, .stApp span, .stApp label, .stApp div, .stApp h3, .stApp h4 { 
        color: #0F172A; 
    }

    /* Animated Hero Banner with Accent */
    @keyframes gradientPan {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .hero-banner {
        background: linear-gradient(-45deg, #05234A, #0A3D85, #001233, #082F66);
        background-size: 400% 400%;
        animation: gradientPan 12s ease infinite;
        border-radius: 12px;
        padding: 3rem 4rem;
        margin-bottom: 2.5rem;
        box-shadow: 0 15px 35px -10px rgba(5, 35, 74, 0.5);
        border-bottom: 6px solid;
        border-image: linear-gradient(to right, #FF9933 33%, #FFFFFF 33%, #FFFFFF 66%, #138808 66%) 1;
        position: relative;
    }
    .hero-banner h1, .hero-banner p, .hero-banner div {
        color: #FFFFFF !important;
    }
    .inst-tag {
        display: inline-block;
        background: #FF9933; 
        color: #FFFFFF !important;
        padding: 6px 18px;
        border-radius: 4px;
        font-size: 0.9rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 10px rgba(255, 153, 51, 0.4);
    }
    .hero-title {
        font-size: 3.2rem; font-weight: 900; line-height: 1.2; margin: 0; letter-spacing: -0.5px;
    }
    .hero-sub {
        font-size: 1.25rem; opacity: 0.95; margin-top: 1rem; font-weight: 400; max-width: 800px;
    }
    
    /* Category Badges (Hardware/Software) */
    .badge-hw {
        background-color: #E6F4EA; color: #137333 !important; padding: 6px 16px;
        border-radius: 50px; font-weight: 800; font-size: 0.85rem; border: 1px solid #CEEAD6;
        display: inline-block; text-align: center;
    }
    .badge-sw {
        background-color: #E8F0FE; color: #1967D2 !important; padding: 6px 16px;
        border-radius: 50px; font-weight: 800; font-size: 0.85rem; border: 1px solid #D2E3FC;
        display: inline-block; text-align: center;
    }

    /* Download Button - Highly Visible Vibrant Blue Gradient */
    [data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%) !important;
        border: none !important;
        border-radius: 6px !important;
        box-shadow: 0 4px 10px rgba(30, 58, 138, 0.3) !important;
        padding: 0.6rem 1.5rem !important;
    }
    [data-testid="stDownloadButton"] button p {
        color: #FFFFFF !important; /* Forces text to be white */
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        margin: 0 !important;
    }
    [data-testid="stDownloadButton"] button:hover {
        box-shadow: 0 6px 15px rgba(30, 58, 138, 0.5) !important;
        transform: translateY(-1px);
    }

    /* Pulsating Primary Buttons (Register Now) */
    @keyframes pulse-btn {
        0% { box-shadow: 0 4px 10px rgba(255, 153, 51, 0.4); }
        50% { box-shadow: 0 8px 20px rgba(255, 153, 51, 0.7); }
        100% { box-shadow: 0 4px 10px rgba(255, 153, 51, 0.4); }
    }
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #FF9933 0%, #E67E22 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 6px;
        font-weight: 800;
        font-size: 1.1rem;
        padding: 0.8rem 2rem;
        animation: pulse-btn 2.5s infinite;
        transition: transform 0.2s;
    }
    .stButton>button[kind="primary"]:hover {
        transform: translateY(-2px);
    }

    /* Standard Buttons (Back Button, Accordion Toggles) */
    .stButton>button[kind="secondary"] {
        background: #F8FAFC !important;
        border: 1px solid #CBD5E1 !important;
        color: #05234A !important;
        font-weight: 700;
    }
    .stButton>button[kind="secondary"]:hover {
        background: #F1F5F9 !important;
        border-color: #05234A !important;
    }

    /* Forms & Inputs */
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {
        background-color: #FFFFFF !important; border: 1.5px solid #CBD5E1 !important;
        border-radius: 8px !important; color: #0F172A !important; padding: 0.6rem !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #05234A !important; box-shadow: 0 0 0 2px rgba(5, 35, 74, 0.15) !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. PROBLEM STATEMENTS DATABASE
# ==============================================================================
PROBLEM_STATEMENTS = [
    # DOMAIN 01: Smart Cities & Urbanization
    {"id": 1, "domain": "Smart Cities & Urbanization", "title": "Smart Street Environment & Noise Monitoring", "category": "HARDWARE",
     "desc": "Develop an IoT-based system that dynamically controls streetlight brightness based on real-time pedestrian/vehicle activity while continuously monitoring urban noise levels.",
     "components": ["ESP32-WROOM-32 Dev Board", "MAX9814 Electret Mic Module with AGC", "LDR Photoresistor Module", "IRF520 MOSFET Driver Module", "12V LED Spotlight / Strip", "LM2596 Buck Converter"]},
    {"id": 2, "domain": "Smart Cities & Urbanization", "title": "Urban Flood Monitoring & Early Warning", "category": "HARDWARE",
     "desc": "Develop a waterproof monitoring system that detects rapidly rising water levels in urban drains and underpasses and provides early warnings.",
     "components": ["ESP32-WROOM-32U (External Antenna)", "JSN-SR04T Waterproof Ultrasonic Level Sensor", "High-Decibel 12V Siren Module", "SIM800L GPRS/GSM Module", "12V 2A SMPS Power Supply"]},
    {"id": 3, "domain": "Smart Cities & Urbanization", "title": "Urban Underground Water Leak Detection", "category": "HARDWARE",
     "desc": "Develop a system that detects and helps locate underground water-pipe leaks using flow, pressure, and acoustic sensing without excavation.",
     "components": ["ESP32 DevKit", "YF-S201 Hall-Effect Water Flow Sensor", "MPX5010DP Pressure Sensor", "Piezoelectric Acoustic Contact Sensor + LM358 PreAmp", "OLED Display 0.96-inch"]},
    {"id": 4, "domain": "Smart Cities & Urbanization", "title": "Underground Sewage Gas Safety", "category": "HARDWARE",
     "desc": "Develop a low-power system that continuously monitors toxic and combustible gases in underground sewage systems and provides warnings.",
     "components": ["ESP32 DevKit", "MQ-136 H2S Gas Sensor Module", "MQ-4 Methane Sensor Module", "5V Loud Active Buzzer", "16x2 I2C Character LCD"]},
    {"id": 5, "domain": "Smart Cities & Urbanization", "title": "Dynamic Digital Traffic Signage", "category": "HARDWARE",
     "desc": "Develop a connected digital signage system that receives real-time traffic data and automatically displays alternative routes or detour instructions.",
     "components": ["ESP32-S3 DevKit", "MAX7219 4-in-1 Dot Matrix LED Display Module", "NEO-6M GPS Module", "5V 4A SMPS Power Supply"]},
    {"id": 6, "domain": "Smart Cities & Urbanization", "title": "Smart Waste Management", "category": "HARDWARE",
     "desc": "Develop an IoT-based waste management system that monitors garbage-bin fill levels, detects overflow conditions, and sends alerts.",
     "components": ["ESP32 DevKit", "HC-SR04 Ultrasonic Distance Sensor", "SW-520D Tilt/Overflow Sensor", "SG90 Micro Servo Motor", "TP4056 Battery Charger + Li-ion Cell"]},
    {"id": 7, "domain": "Smart Cities & Urbanization", "title": "AI-Powered Traffic Flow Optimization", "category": "SOFTWARE",
     "desc": "Develop a centralized software platform that ingests real-time transit and ride-sharing GPS data to dynamically adjust traffic light timings.",
     "components": []},
    {"id": 8, "domain": "Smart Cities & Urbanization", "title": "Civic Issue Crowdsourcing & Triage", "category": "SOFTWARE",
     "desc": "Develop a web/mobile application that allows citizens to report civic issues with geotagged photos, using AI to route to municipal departments.",
     "components": []},

    # DOMAIN 02: Healthcare & Medical Technology
    {"id": 9, "domain": "Healthcare & Medical Technology", "title": "Elderly Care & Assistive Technology", "category": "HARDWARE",
     "desc": "Develop a wearable system that detects accidental falls in elderly individuals, provides medication reminders, and sends SOS alerts with GPS location.",
     "components": ["ESP32-C3 SuperMini RISC-V Dev Board", "MPU-6050 6-DOF IMU Sensor", "NEO-6M GPS Module", "Mini 3V Coin Vibration Motor", "3.7V 800mAh LiPo Cell + TP4056"]},
    {"id": 10, "domain": "Healthcare & Medical Technology", "title": "Hospital Patient Safety & Monitoring", "category": "HARDWARE",
     "desc": "Develop a smart monitoring system that continuously detects the remaining level of an IV fluid bag and automatically alerts nursing staff.",
     "components": ["ESP32 Dev Board", "1kg Straight Bar Load Cell + HX711 24-bit ADC Module", "Non-Contact Capacitive Liquid Level Sensor", "0.96-inch I2C OLED Display"]},
    {"id": 11, "domain": "Healthcare & Medical Technology", "title": "Blood Bank & Medical Inventory Management", "category": "HARDWARE",
     "desc": "Develop an IoT-based system that continuously monitors blood storage temperature and tracks blood bag inventory/expiry information.",
     "components": ["ESP32 DevKit", "DS18B20 Waterproof Stainless Digital Temperature Probe", "RC522 13.56MHz RFID Reader + Mifare Tags", "16x2 I2C Character LCD"]},
    {"id": 12, "domain": "Healthcare & Medical Technology", "title": "Neonatal & Maternal Healthcare", "category": "HARDWARE",
     "desc": "Develop a smart incubator monitoring and control system that maintains stable temperature and humidity for premature babies.",
     "components": ["ESP32 Dev Board", "SHT31 High-Precision Temp & Humidity Sensor", "12V 50W PTC Ceramic Heating Element", "12V DC Blower Fan", "2-Channel 5V Optocoupled Relay Module"]},
    {"id": 13, "domain": "Healthcare & Medical Technology", "title": "Preventive Healthcare & Wellness", "category": "HARDWARE",
     "desc": "Develop a smart bottle that automatically measures water intake, monitors hydration patterns, and provides personalized reminders.",
     "components": ["Arduino Nano / ESP32-C3", "Non-Contact Capacitive Liquid Level Sensor", "0.42-inch OLED I2C Display Module", "Coin Vibration Motor", "TP4056 Charger + LiPo"]},
    {"id": 14, "domain": "Healthcare & Medical Technology", "title": "AI-Based Disease Detection & Medical Diagnostics", "category": "HARDWARE",
     "desc": "Develop a low-cost digital microscopy system that captures blood-smear images and uses computer vision to highlight malaria/dengue cells.",
     "components": ["ESP32-S3 DevKit with OV2640 / OV5640 Camera", "Precision Adjustable LED Spotlight Condenser", "MicroSD Card Module + 16GB Card", "A4988 Stepper Driver + NEMA 17 Motor"]},
    {"id": 15, "domain": "Healthcare & Medical Technology", "title": "Digital Healthcare & Organ Transplant Management", "category": "SOFTWARE",
     "desc": "Develop a secure platform that enables hospitals to efficiently match organ donors with eligible recipients based on compatibility factors.",
     "components": []},
    {"id": 16, "domain": "Healthcare & Medical Technology", "title": "Predictive Hospital Bed Management", "category": "SOFTWARE",
     "desc": "Develop a software solution integrating with EHR to forecast patient admission rates and discharge times using machine learning.",
     "components": []},

    # DOMAIN 03: Electric Vehicles (EV) & Mobility
    {"id": 17, "domain": "Electric Vehicles (EV) & Mobility", "title": "EV Battery Safety & Thermal Runaway", "category": "HARDWARE",
     "desc": "Develop a low-cost battery monitoring system that detects early signs of thermal runaway at the cell level and isolates the affected module.",
     "components": ["ESP32 Dev Board", "NTC 10k Precision Thermistors (Pack of 5 Cell Probes)", "MQ-2 Flammable Gas Sensor", "4-Channel 5V Relay Module", "12V 10A Industrial SMPS"]},
    {"id": 18, "domain": "Electric Vehicles (EV) & Mobility", "title": "EV Motor Fault Detection & Predictive Maintenance", "category": "HARDWARE",
     "desc": "Develop a sensorless motor-monitoring system analyzing three-phase current signals to detect developing inter-turn winding faults.",
     "components": ["ESP32 DevKit", "ACS712 30A Current Sensor Modules", "LM358 Signal Conditioning ICs", "Small 3-Phase BLDC Motor + ESC", "0.96-inch OLED Display Module"]},
    {"id": 19, "domain": "Electric Vehicles (EV) & Mobility", "title": "EV Charging Infrastructure Monitoring", "category": "HARDWARE",
     "desc": "Develop a retrofit device that independently verifies whether an EV charging station is delivering power and logs genuine charging events.",
     "components": ["ESP32 DevKit", "PZEM-004T V3.0 AC Multi-Function Energy Meter", "SCT-013-000 100A Current Transformer", "RC522 RFID Reader", "5V 2A USB Dummy Load"]},
    {"id": 20, "domain": "Electric Vehicles (EV) & Mobility", "title": "Regenerative Braking & Energy Recovery", "category": "HARDWARE",
     "desc": "Develop an intelligent regenerative-braking controller that dynamically manages regen levels based on motor status and battery state.",
     "components": ["ESP32 Dev Board", "IRFB3077 High Current N-MOSFET", "TC4427/IR2104 Gate Driver IC", "12V 10A Industrial SMPS", "Power Dump Resistors"]},
    {"id": 21, "domain": "Electric Vehicles (EV) & Mobility", "title": "EV Traction Control & Vehicle Stability", "category": "HARDWARE",
     "desc": "Develop an intelligent traction-control system that detects excessive wheel slip and dynamically adjusts motor torque.",
     "components": ["ESP32 Dev Board", "LM393 Optical Wheel Speed Sensors", "L298N Dual H-Bridge Motor Driver Module", "Dual TT DC Geared Motors with Encoders", "12V 5A Bench SMPS"]},
    {"id": 22, "domain": "Electric Vehicles (EV) & Mobility", "title": "EV Structural Health & Predictive Maintenance", "category": "HARDWARE",
     "desc": "Develop an accelerometer-based system for detecting structural fatigue in an EV battery mounting system by analyzing resonant frequency.",
     "components": ["ESP32 DevKit", "ADXL345 3-Axis Digital Accelerometer", "SW-420 High Sensitivity Vibration Sensor", "12V 2A SMPS Power Supply", "0.96-inch I2C OLED Display"]},
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
     "components": ["ESP32-C3 SuperMini RISC-V Dev Board", "FSR402 Force Sensing Resistors", "MPU-6050 6-Axis Motion Sensor", "Miniature 3V Coin Vibration Motor", "TP4056 LiPo Charger"]},
    {"id": 30, "domain": "Education & Academic Learning", "title": "Visual Pronunciation Learning Device", "category": "HARDWARE",
     "desc": "Develop a standalone device that uses microphone input and a small display to provide visual mouth-shape feedback to improve pronunciation.",
     "components": ["ESP32-S3 DevKit (DSP Classifier)", "MAX9814 Electret Microphone with AGC", "1.8-inch SPI ST7735 Full-Color TFT Display Module", "5V 2A Low-Noise SMPS", "Audio Filter Capacitors"]},
    {"id": 31, "domain": "Education & Academic Learning", "title": "AI-Driven Academic Integrity Detector", "category": "SOFTWARE",
     "desc": "Develop a natural language processing software tool that analyzes student submissions to differentiate human writing, plagiarized text, and AI text.",
     "components": []},

    # DOMAIN 05: Renewable Energy & Power Systems
    {"id": 32, "domain": "Renewable Energy & Power Systems", "title": "Solar Energy & Battery Management", "category": "HARDWARE",
     "desc": "Develop an energy-management controller that monitors solar generation and load demand, intelligently scheduling battery cycles.",
     "components": ["ESP32 DevKit", "6V 3W Mini Solar Panel", "ACS712 30A Current Sensors", "IRF3205 N-MOSFET Switches", "IR2104 Gate Driver IC", "12V 10A Industrial SMPS"]},
    {"id": 33, "domain": "Renewable Energy & Power Systems", "title": "Power Quality & Harmonic Management", "category": "HARDWARE",
     "desc": "Develop a real-time power-quality monitoring system detecting harmonic distortions and evaluating the impact of active compensation.",
     "components": ["ESP32 Dev Board (Fast FFT)", "ZMPT101B Active AC Voltage Transformer", "SCT-013-000 100A AC Current Clamp", "AC/DC Non-Linear Load Simulator", "LM358 Dual Op-Amps"]},
    {"id": 34, "domain": "Renewable Energy & Power Systems", "title": "Solar Microgrid & Black-Start", "category": "HARDWARE",
     "desc": "Develop a black-start controller that safely restores a renewable-energy microgrid after a complete blackout by sequencing loads.",
     "components": ["ESP32 Dev Board", "6V 3W Mini Solar Panel", "ZMPT101B AC Voltage Sensor", "4-Channel 5V Relay Module", "12V 5A 60W SMPS", "ULN2803A Darlington Transistor Array IC"]},
    {"id": 35, "domain": "Renewable Energy & Power Systems", "title": "Electric Vehicles & Vehicle-to-Grid (V2G) Tech", "category": "HARDWARE",
     "desc": "Develop a smart V2G controller that coordinates EV power feed back into the grid based on peak demand while maintaining minimum battery availability.",
     "components": ["ESP32 Dev Board", "ACS712 30A Bidirectional Current Sensors", "MCP2515 CAN Bus Controller SPI Module", "12V 10A 120W SMPS", "IRF3205 Power Switch Modules"]},
    {"id": 36, "domain": "Renewable Energy & Power Systems", "title": "Urban Renewable Energy", "category": "HARDWARE",
     "desc": "Develop a small-scale energy harvesting system capturing low-level wind or footfall kinetic energy and converting it into electrical storage.",
     "components": ["ESP32 Dev Board", "Piezoelectric Vibration Transducers", "Mini 3-Phase AC Wind Dynamo Generator", "LTC3588 Energy Harvesting IC", "2.7V 10F Supercapacitors"]},
    {"id": 37, "domain": "Renewable Energy & Power Systems", "title": "Railway Energy Harvesting", "category": "HARDWARE",
     "desc": "Develop a vibration-energy harvesting system capturing mechanical track vibrations from train transit for self-powered track monitors.",
     "components": ["ESP32 Dev Board", "Piezoelectric Ceramic Energy Harvester", "INA219 I2C Micro-Power Monitor", "SW-420 High Sensitivity Vibration Sensor", "Supercapacitors (5V)"]},
    {"id": 38, "domain": "Renewable Energy & Power Systems", "title": "Community Microgrid & Energy Sharing", "category": "HARDWARE",
     "desc": "Develop an intelligent microgrid controller that manages distributed renewable assets and balances islanded microgrid clusters.",
     "components": ["ESP32 Dev Board", "PZEM-004T Multi-Function AC Power Meter", "2-Channel 5V Optocoupled Relay Module (30A)", "12V 5A 60W SMPS", "16x2 I2C Character LCD Display"]},
    {"id": 39, "domain": "Renewable Energy & Power Systems", "title": "Wind Energy & Predictive Maintenance", "category": "HARDWARE",
     "desc": "Develop a wind-turbine condition monitoring unit tracking vibration, bearing temperature, RPM, and power output to predict failures.",
     "components": ["ESP32 Dev Board", "ADXL345 3-Axis Accelerometer", "LM393 Optical IR Speed/RPM Sensor", "DS18B20 Waterproof Temperature Sensor", "12V DC Motor (Turbine Drive Sim)"]},
    {"id": 40, "domain": "Renewable Energy & Power Systems", "title": "Regenerative Energy Recovery", "category": "HARDWARE",
     "desc": "Develop a scaled regenerative braking system capturing energy from descending elevators and safely storing or dumping excess power.",
     "components": ["ESP32 Dev Board", "12V High-Torque DC Motor/Generator", "INA219 Bidirectional Power Monitor", "Supercapacitor Bank", "IRFB3077/IRF3205 N-MOSFET Dump Controllers"]},
    {"id": 41, "domain": "Renewable Energy & Power Systems", "title": "Solar PV Predictive Maintenance & Soiling", "category": "HARDWARE",
     "desc": "Develop a low-cost PV monitoring device comparing expected irradiance with actual output to identify persistent soiling and dust buildup.",
     "components": ["ESP32 Dev Board", "6V 3W Mini Solar Panel", "BH1750 Digital Ambient Light / Lux Sensor", "INA219 High-Side Power Sensor", "DS18B20 Digital Temperature Probe"]},
    {"id": 42, "domain": "Renewable Energy & Power Systems", "title": "Solar Farm Yield Forecasting", "category": "SOFTWARE",
     "desc": "Develop a software system integrating meteorological satellite feeds to predict hour-ahead solar power generation for transmission grid stability.",
     "components": []},
    {"id": 43, "domain": "Renewable Energy & Power Systems", "title": "Microgrid Load Balancing Algorithm", "category": "SOFTWARE",
     "desc": "Develop an autonomous software engine that dynamically redistributes renewable power among peer-to-peer consumers to avoid localized blackouts.",
     "components": []},

    # DOMAIN 06: Aerospace, Aviation & Space Tech
    {"id": 44, "domain": "Aerospace, Aviation & Space Tech", "title": "UAV Safety & Autonomous Landing", "category": "HARDWARE",
     "desc": "Develop an autonomous emergency landing unit for drones that detects in-flight propulsion failure and guides descent to a safe landing zone.",
     "components": ["ESP32-S3-DevKitC-1", "MPU-6050 6-DOF IMU Accelerometer Module", "BMP280 Barometric Pressure Sensor", "MG996R High-Torque Metal Gear Servo", "TP4056 Module + 3.7V LiPo"]},
    {"id": 45, "domain": "Aerospace, Aviation & Space Tech", "title": "Autonomous Navigation & Collision Avoidance", "category": "HARDWARE",
     "desc": "Develop an obstacle detection and path replanning module enabling UAVs to detect powerlines and obstacles in real time.",
     "components": ["ESP32 Dev Board", "VL53L0X Time-of-Flight Laser Sensors", "HC-SR04 Ultrasonic Distance Sensors", "Bidirectional Logic Level Converters", "74HC14 Schmitt Trigger IC"]},
    {"id": 46, "domain": "Aerospace, Aviation & Space Tech", "title": "Energy-Efficient UAV Operations", "category": "HARDWARE",
     "desc": "Develop an energy-aware UAV mission computer that recalculates flight paths dynamically based on instantaneous battery discharge and headwind.",
     "components": ["ESP32 Dev Board", "INA219 High-Side I2C Current Sensors", "0.96-inch OLED I2C Display", "12V 5A Industrial Bench SMPS", "LM2596 DC-DC Buck Converter"]},
    {"id": 47, "domain": "Aerospace, Aviation & Space Tech", "title": "Aircraft Electrical Systems & Fault Management", "category": "HARDWARE",
     "desc": "Develop a multi-bus electrical fault isolation system that disconnects shorted avionics lines and reroutes power via alternate buses.",
     "components": ["ESP32 Dev Board", "ACS712 20A Current Sensors", "ZMPT101B Active Voltage Sensors", "4-Channel 5V Relay Isolation Module", "ULN2803A Darlington Transistor Driver IC"]},
    {"id": 48, "domain": "Aerospace, Aviation & Space Tech", "title": "Autonomous Search & Rescue", "category": "HARDWARE",
     "desc": "Develop a compact drone payload that scans disaster zones, detects human presence using thermal signatures, and beacons GPS coordinates.",
     "components": ["ESP32-S3 DevKit with OV2640 Camera", "NEO-6M GPS Module", "High-Decibel 5V Alarm Siren + 3W LED", "TIP122 Darlington Transistor IC", "12V 3A SMPS Power Supply"]},
    {"id": 49, "domain": "Aerospace, Aviation & Space Tech", "title": "Spacecraft Power Management", "category": "HARDWARE",
     "desc": "Develop a fault-tolerant satellite EPS module prioritizing onboard instrument power and shedding non-critical payload during eclipse periods.",
     "components": ["ESP32 Dev Board", "INA226 I2C Power Monitor ICs", "IRF540N N-Channel Power MOSFET Switches", "12V 10A 120W SMPS", "LM2596S Adjustable Buck Converters"]},
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
     "components": ["ESP32-WROOM-32U DevKit + Antenna", "0.96-inch I2C OLED Display", "5V Active Piezo Buzzer", "MicroSD Card Adapter Module", "AMS1117-3.3V LDO Voltage Regulators"]},
    {"id": 54, "domain": "Cybersecurity & Digital Forensics", "title": "USB Security & Hardware-Based Cybersecurity", "category": "HARDWARE",
     "desc": "Develop an inline hardware security device that screens incoming USB endpoints, dropping rogue Human Interface Device (HID) keystroke injection.",
     "components": ["ESP32-S3-DevKitC-1 (Dual Type-C)", "MAX3421E USB Host Controller IC", "TPD4E001 ESD Protection Diode Array IC", "0.96-inch OLED Display", "5V Active Piezo Buzzer"]},
    {"id": 55, "domain": "Cybersecurity & Digital Forensics", "title": "Digital Forensics & Evidence Analysis", "category": "SOFTWARE",
     "desc": "Develop an automated digital forensic tool parsing file system metadata, generating cryptographic SHA-256 hashes, and building forensic timelines.",
     "components": []},
    {"id": 56, "domain": "Cybersecurity & Digital Forensics", "title": "Forensic Evidence Protection (Write-Blocker)", "category": "HARDWARE",
     "desc": "Develop an inline forensic write-blocker intercepting SD/USB mass storage commands, allowing investigators read-only analysis without contamination.",
     "components": ["ESP32-S3-DevKitC-1 (Dual Type-C)", "MAX3421E USB Host Controller Module", "TPS2051 Power Distribution Switch IC", "16x2 I2C LCD Display", "12V 3A Dual-Rail SMPS"]},
    {"id": 57, "domain": "Cybersecurity & Digital Forensics", "title": "Cyber Incident Response & Digital Evidence", "category": "SOFTWARE",
     "desc": "Develop an evidence repository establishing tamper-evident chains of custody using Merkle trees and cryptographic verification.",
     "components": []},
    {"id": 58, "domain": "Cybersecurity & Digital Forensics", "title": "Secure Digital Forensics & Field Investigation", "category": "HARDWARE",
     "desc": "Develop a portable, biometric/RFID access-controlled storage imager that logs session operators and detects physical chassis tampering.",
     "components": ["ESP32 Dev Board", "12V Micro Solenoid Cabinet Lock", "SW-420 Vibration/Tamper Sensor", "ULN2003 Driver IC", "12V 3A SMPS Enclosed Industrial Unit"]},
    {"id": 59, "domain": "Cybersecurity & Digital Forensics", "title": "Ransomware Behavior Isolation System", "category": "SOFTWARE",
     "desc": "Develop an endpoint security agent detecting rapid, high-entropy file modifications and autonomously isolating infected hosts from the network.",
     "components": []},
    {"id": 60, "domain": "Cybersecurity & Digital Forensics", "title": "Automated Phishing Threat Intelligence Pipeline", "category": "SOFTWARE",
     "desc": "Develop a triage pipeline extracting headers and URLs from suspicious user-submitted emails, querying sandboxes and updating security boundaries.",
     "components": []},

    # DOMAIN 08: Agriculture & Aquaculture
    {"id": 61, "domain": "Agriculture & Aquaculture", "title": "Water Management & Smart Irrigation", "category": "HARDWARE",
     "desc": "Develop an autonomous irrigation controller that evaluates localized soil moisture and temperature to govern multi-valve water delivery.",
     "components": ["ESP32 Dev Board", "Capacitive Soil Moisture Sensors", "12V DC Solenoid Water Valve", "12V Mini Submersible Water Pump", "1-Channel Optoisolated 5V Relay", "12V 5A SMPS"]},
    {"id": 62, "domain": "Agriculture & Aquaculture", "title": "Precision Agriculture - Crop Health Monitoring", "category": "HARDWARE",
     "desc": "Develop a drone payload using calibrated multispectral/optical sensors to survey vegetative health and identify crop blight.",
     "components": ["ESP32-S3 DevKit with OV2640 Camera", "DHT22 Digital Temperature & Humidity Sensor", "MicroSD Card Module", "0.96-inch OLED Screen", "Miniature Coreless Motor & Propeller (Sim)"]},
    {"id": 63, "domain": "Agriculture & Aquaculture", "title": "Energy Management & Predictive Maintenance", "category": "HARDWARE",
     "desc": "Develop an edge diagnostic monitor detecting dry running, motor cavitation, phase unbalance, and abnormal pump vibration.",
     "components": ["ESP32 Dev Board", "ACS712 30A Current Sensor", "DS18B20 Waterproof Temp Probe", "SW-420 Vibration Sensor", "30A High-Current Relay", "12V Mini Submersible Pump"]},
    {"id": 64, "domain": "Agriculture & Aquaculture", "title": "Climate Resilience & Crop Protection", "category": "HARDWARE",
     "desc": "Develop a micro-climate forecasting node calculating frost points and automatically actuating protective thermal sprinklers or warm blowers.",
     "components": ["ESP32 Dev Board", "SHT31 Precision Temp/Humidity Sensor", "BMP280 Barometric Pressure Sensor", "2-Channel Relay Module", "12V PTC Heater & 5V Mini Pump (Sim)"]},
    {"id": 65, "domain": "Agriculture & Aquaculture", "title": "Soil Health Monitoring (Edge AI)", "category": "HARDWARE",
     "desc": "Develop a field probe evaluating soil electrical conductivity (EC), pH, and moisture parameters to summarize soil viability without internet.",
     "components": ["ESP32-S3 DevKit (TinyML)", "Analog Soil pH Sensor Probe", "Analog Soil EC Probe", "Capacitive Soil Moisture Sensor", "LM358 Dual Op-Amp ICs", "0.96-inch OLED"]},
    {"id": 66, "domain": "Agriculture & Aquaculture", "title": "Aquaculture & Water Quality Management", "category": "HARDWARE",
     "desc": "Develop an automated water quality system monitoring dissolved oxygen proxies, pH, and turbidity, driving aerators when parameters deteriorate.",
     "components": ["ESP32 Dev Board", "Analog Industrial pH Sensor Kit", "DS18B20 Temp Probe", "Analog Optical Turbidity Sensor", "4-Channel Relay", "5V Submersible Pump (Sim)"]},
    {"id": 67, "domain": "Agriculture & Aquaculture", "title": "Smart Greenhouse Climate & Fogging Automation", "category": "HARDWARE",
     "desc": "Develop an automated greenhouse system regulating vapor pressure deficits (VPD) through synchronized exhaust venting and ultrasonic misting.",
     "components": ["ESP32 Dev Board", "DHT22 Sensor", "BH1750 Ambient Light Sensor", "Capacitive Soil Moisture Sensors", "2-Channel Relay", "12V Mini Exhaust Fan & 5V Mist Maker (Sim)"]},
    {"id": 68, "domain": "Agriculture & Aquaculture", "title": "Crop Yield Prediction & Commodity Market Triage", "category": "SOFTWARE",
     "desc": "Develop a predictive analytics software pipeline fusing NDVI satellite imagery and commodity indices to suggest optimal harvest liquidation windows.",
     "components": []},
    {"id": 69, "domain": "Agriculture & Aquaculture", "title": "Aquaculture Feeding Rate Optimization Engine", "category": "SOFTWARE",
     "desc": "Develop an algorithmic feeding controller adjusting feeding schedules dynamically based on water temperature, dissolved oxygen, and fish biomass growth.",
     "components": []}
]

ps_titles = [f"PS #{ps['id']:02d}: {ps['title']}" for ps in PROBLEM_STATEMENTS]


# ==============================================================================
# VIEW 1: HOME PAGE (LISTING WITH EXCLUSIVE ACCORDIONS)
# ==============================================================================
if st.session_state.page == 'home':
    st.markdown("""
    <div class="hero-banner">
        <div class="inst-tag">Organized by Department of Electrical Engineering</div>
        <div class="hero-title">WCE National Technical Hackathon 2026</div>
        <div class="hero-sub">Official Portal for Problem Statements, Prototyping Hardware Specifications, and Team Registration. Hosted by Walchand College of Engineering, Sangli.</div>
    </div>
    """, unsafe_allow_html=True)

    # Document Preview & Download
    doc_filename = "Problem_Statements_Updated.docx"
    with st.expander("👁️ Click here to Preview the Official Compendium Document", expanded=False):
        encoded_doc_name = urllib.parse.quote(doc_filename)
        github_raw_url = f"https://github.com/Aditya-9600/hackathon-portal/raw/main/{encoded_doc_name}"
        viewer_url = f"https://docs.google.com/viewer?url={github_raw_url}&embedded=true"
        components.iframe(viewer_url, height=580, scrolling=True)

    if os.path.exists(doc_filename):
        with open(doc_filename, "rb") as fp:
            st.download_button("⬇️ Download Compendium (.docx)", data=fp, file_name=doc_filename, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

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

    # ==========================================
    # CUSTOM ACCORDION (ONLY 1 OPEN AT A TIME)
    # ==========================================
    for ps in filtered_list:
        with st.container(border=True):
            # Header Row: [ Title ] [ Badge ] [ Button ]
            row_c1, row_c2, row_c3 = st.columns([5, 1.5, 2])
            
            with row_c1:
                st.markdown(f"<h4 style='margin-bottom: 0px;'>PS #{ps['id']:02d}: {ps['title']}</h4>", unsafe_allow_html=True)
            
            with row_c2:
                # Badge appears beside the name *before* opening
                c_tag = "badge-hw" if ps['category'] == "HARDWARE" else "badge-sw"
                st.markdown(f'<div style="margin-top: 5px;"><span class="{c_tag}">{ps["category"]}</span></div>', unsafe_allow_html=True)
                
            with row_c3:
                # Toggle logic
                is_active = st.session_state.active_ps == ps['id']
                btn_lbl = "🔼 Hide Details" if is_active else "🔽 View Details"
                if st.button(btn_lbl, key=f"tgl_{ps['id']}", use_container_width=True, type="secondary"):
                    if is_active:
                        st.session_state.active_ps = None
                    else:
                        st.session_state.active_ps = ps['id']
                    st.rerun() 

            # Expanded Details Content
            if st.session_state.active_ps == ps['id']:
                st.markdown("<hr style='margin: 15px 0px; border: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
                
                # Badge also appears inside
                st.markdown(f'<span class="{c_tag}">{ps["category"]}</span> &nbsp; <b style="color:#05234A; font-size: 1.1rem;">Domain: {ps["domain"]}</b>', unsafe_allow_html=True)
                st.markdown(f"<p style='margin-top: 15px; font-size: 1.05rem; line-height: 1.6;'>{ps['desc']}</p>", unsafe_allow_html=True)
                
                # Components List inside details
                if ps["category"] == "SOFTWARE":
                    st.info("ℹ️ **There is no hardware or components for this problem statement.** Evaluation will be based on software architecture and performance.")
                else:
                    st.markdown("#### 📦 Expected Prototyping Hardware Components:")
                    col_c1, col_c2 = st.columns(2)
                    mid_pt = (len(ps['components']) + 1) // 2
                    with col_c1:
                        for comp in ps['components'][:mid_pt]:
                            st.markdown(f"🔹 {comp}")
                    with col_c2:
                        for comp in ps['components'][mid_pt:]:
                            st.markdown(f"🔹 {comp}")

                # Register Now Button
                st.markdown("<br>", unsafe_allow_html=True)
                ps_formatted_title = f"PS #{ps['id']:02d}: {ps['title']}"
                
                st.button(
                    f"🚀 Register Now for PS #{ps['id']:02d}", 
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

    # Determine Dropdown Index
    default_ps_index = 0
    if st.session_state.selected_ps in ps_titles:
        default_ps_index = ps_titles.index(st.session_state.selected_ps)

    with st.form("team_registration_form"):
        st.markdown("#### 1. Team Profile")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            team_name = st.text_input("Team Name *", placeholder="e.g. Walchand Innovators")
        with col_t2:
            # Dropdown locks automatically if user navigated via "Register Now"
            is_ps_locked = st.session_state.get('ps_locked', False)
            assigned_ps = st.selectbox(
                "Allocated Problem Statement *", 
                ps_titles, 
                index=default_ps_index,
                disabled=is_ps_locked
            )
            if is_ps_locked:
                st.caption("🔒 *Locked based on your selection. To change, go back.*")

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
                        webhook_url = "https://script.google.com/u/0/home/projects/1K1qp6OBexjHi71dDcG6Exu3C6MEg1o9XBoapOq5w5oXus2yAucTt4thA/triggers"
                        
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
    Walchand College of Engineering, Sangli • Department of Electrical Engineering<br>
    Built with Python & Streamlit • Autonomous Engineering Institute
</div>
""", unsafe_allow_html=True)
