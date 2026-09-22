import streamlit as st
import qrcode
from io import BytesIO
import urllib.parse
import uuid
import datetime
import os

# ==============================================================================
# 1. PAGE SETUP & STYLING
# ==============================================================================
st.set_page_config(
    page_title="Hackathon 2026 Portal",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 800; color: #1E293B; margin-bottom: 0.2rem; }
    .sub-title { font-size: 1.05rem; color: #64748B; margin-bottom: 1.5rem; }
    .badge-hw { background-color: #DCFCE7; color: #15803D; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.85rem; }
    .badge-sw { background-color: #E0E7FF; color: #4338CA; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.85rem; }
    .card-box { padding: 1.2rem; border-radius: 10px; background-color: #F8FAFC; border: 1px solid #E2E8F0; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. PROBLEM STATEMENTS DATABASE
# ==============================================================================
PROBLEM_STATEMENTS = [
    # DOMAIN 01: Smart Cities & Urbanization
    {"id": 1, "domain": "Smart Cities & Urbanization", "title": "Smart Street Environment & Noise Monitoring", "category": "HARDWARE",
     "desc": "Develop an IoT-based system that dynamically controls streetlight brightness based on real-time pedestrian/vehicle activity while continuously monitoring urban noise levels.",
     "components": ["ESP32-WROOM-32 Dev Board", "MAX9814 Electret Mic Module with AGC", "LDR Photoresistor Module", "IRF520 MOSFET Driver Module", "12V LED Spotlight / Strip", "LM2596 Buck Converter"]},
    {"id": 2, "domain": "Smart Cities & Urbanization", "title": "Urban Flood Monitoring & Early Warning", "category": "HARDWARE",
     "desc": "Develop a waterproof monitoring system that detects rapidly rising water levels in urban drains and underpasses and provides early warnings.",
     "components": ["ESP32-WROOM-32 Dev Board", "JSN-SR04T Waterproof Ultrasonic Level Sensor", "High-Decibel 12V Siren Module", "SIM800L GPRS/GSM Module", "12V 2A SMPS Power Supply"]},
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
    {"id": 17, "domain": "Electric Vehicles (EV) & Mobility", "title": "EV Battery Safety & Thermal Runaway Detection", "category": "HARDWARE",
     "desc": "Develop a low-cost battery monitoring system that detects early signs of thermal runaway at the cell level and isolates the affected module.",
     "components": ["ESP32 Dev Board", "NTC 10k Precision Thermistors (Pack of 5 Cell Probes)", "IRFB3077 High Current Power MOSFET", "1-Channel 30A High-Current Relay", "Active Piezo Buzzer"]},
    {"id": 18, "domain": "Electric Vehicles (EV) & Mobility", "title": "EV Motor Fault Detection & Predictive Maintenance", "category": "HARDWARE",
     "desc": "Develop a sensorless motor-monitoring system analyzing three-phase current signals to detect developing inter-turn winding faults.",
     "components": ["ESP32 DevKit", "LM358 Operational Amplifier Signal Conditioning IC", "LM393 Optical Wheel Speed Sensor Module", "74HC14 Schmitt Trigger IC"]},
    {"id": 19, "domain": "Electric Vehicles (EV) & Mobility", "title": "EV Charging Infrastructure Monitoring", "category": "HARDWARE",
     "desc": "Develop a retrofit device that independently verifies whether an EV charging station is delivering power and logs genuine charging events.",
     "components": ["ESP32 DevKit", "MCP2515 CAN Bus Controller SPI Module + TJA1050", "RC522 13.56MHz RFID Reader", "MicroSD Card Module + 16GB Card"]},
    {"id": 20, "domain": "Electric Vehicles (EV) & Mobility", "title": "Regenerative Braking & Energy Recovery", "category": "HARDWARE",
     "desc": "Develop an intelligent regenerative-braking controller that dynamically manages regen levels based on motor status and battery state.",
     "components": ["Arduino Nano / ESP32", "IRFB3077/IRF3205 N-MOSFET", "Supercapacitor Bank (5.4V 5F)", "1N5822 3A Schottky Flyback Diodes", "Ceramic Power Dump Resistors (10Ω 10W)"]},
    {"id": 21, "domain": "Electric Vehicles (EV) & Mobility", "title": "EV Traction Control & Vehicle Stability", "category": "HARDWARE",
     "desc": "Develop an intelligent traction-control system that detects excessive wheel slip and dynamically adjusts motor torque.",
     "components": ["ESP32 Dev Board", "MPU-6050 6-Axis Accelerometer/Gyro", "Dual TT DC Geared Motors with Encoders", "L298N Dual Motor Driver Module", "2WD Robot Chassis Kit"]},
    {"id": 22, "domain": "Electric Vehicles (EV) & Mobility", "title": "EV Structural Health & Predictive Maintenance", "category": "HARDWARE",
     "desc": "Develop an accelerometer-based system for detecting structural fatigue in an EV battery mounting system by analyzing resonant frequency.",
     "components": ["ESP32 DevKit", "ADXL345 High-Speed 3-Axis Digital Accelerometer", "SW-420 High Sensitivity Vibration Sensor", "MicroSD Card Module + 16GB Card"]},
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
     "components": ["Mini 170-Tie Point Breadboard (Wearable size)", "FSR402 Force Sensing Resistors", "ADXL345 3-Axis Accelerometer", "Miniature 3V Coin Vibration Motor", "3.7V 300mAh LiPo + TP4056"]},
    {"id": 30, "domain": "Education & Academic Learning", "title": "Visual Pronunciation Learning Device", "category": "HARDWARE",
     "desc": "Develop a standalone device that uses microphone input and a small display to provide visual mouth-shape feedback to improve pronunciation.",
     "components": ["ESP32-S3 DevKit (16MB Flash, 8MB PSRAM)", "MAX9814 Microphone with AGC", "1.8-inch SPI ST7735 Full-Color TFT Display", "PAM8403 3W Audio Amplifier + Speaker"]},
    {"id": 31, "domain": "Education & Academic Learning", "title": "AI-Driven Academic Integrity Detector", "category": "SOFTWARE",
     "desc": "Develop a natural language processing software tool that analyzes student submissions to differentiate human writing, plagiarized text, and AI text.",
     "components": []},

    # DOMAIN 05: Renewable Energy & Power Systems
    {"id": 32, "domain": "Renewable Energy & Power Systems", "title": "Solar Energy & Battery Management", "category": "HARDWARE",
     "desc": "Develop an energy-management controller that monitors solar generation and load demand, intelligently scheduling battery cycles.",
     "components": ["ESP32 DevKit", "6V 3W Mini Solar Panel", "TP4056 Battery Charger + 18650 Cell", "LM2596 Buck Converter", "ACS712 Current Sensor / Shunts", "2-Channel 5V Relay Module"]},
    {"id": 33, "domain": "Renewable Energy & Power Systems", "title": "Power Quality & Harmonic Management", "category": "HARDWARE",
     "desc": "Develop a real-time power-quality monitoring system detecting harmonic distortions and evaluating the impact of active compensation.",
     "components": ["ESP32 Dev Board", "LM358 Operational Amplifier Signal Conditioning IC", "AC/DC Non-Linear Load Simulator", "14AWG Wire & High-Voltage Diodes"]},
    {"id": 34, "domain": "Renewable Energy & Power Systems", "title": "Solar Microgrid & Black-Start Controller", "category": "HARDWARE",
     "desc": "Develop a black-start controller that safely restores a renewable-energy microgrid after a complete blackout by sequencing loads.",
     "components": ["ESP32 DevKit", "4-Channel 5V Relay Module (Step-Load Sequencing)", "12V 5A Industrial SMPS Supply", "12V DC Motor Simulator", "PC817 Optocoupler ICs"]},
    {"id": 35, "domain": "Renewable Energy & Power Systems", "title": "Electric Vehicles & Vehicle-to-Grid (V2G) Tech", "category": "HARDWARE",
     "desc": "Develop a smart V2G controller that coordinates EV power feed back into the grid based on peak demand while maintaining minimum battery availability.",
     "components": ["ESP32 Dev Board", "IRFB3077 High Current N-MOSFET", "MCP2515 CAN Bus Controller Module", "12V Solenoid Interlock", "PC817 Optocoupler ICs"]},
    {"id": 36, "domain": "Renewable Energy & Power Systems", "title": "Urban Renewable Energy Harvesting", "category": "HARDWARE",
     "desc": "Develop a small-scale energy harvesting system capturing low-level wind or footfall kinetic energy and converting it into electrical storage.",
     "components": ["Piezoelectric Ceramic Energy Harvester Module", "LTC3588 Energy Harvesting Power Supply Module", "2.7V 10F Supercapacitor", "Mini 3-Phase AC Wind Dynamo"]},
    {"id": 37, "domain": "Renewable Energy & Power Systems", "title": "Railway Energy Harvesting", "category": "HARDWARE",
     "desc": "Develop a vibration-energy harvesting system capturing mechanical track vibrations from train transit for self-powered track monitors.",
     "components": ["Piezoelectric Vibration Transducer Discs", "Custom Copper-PTFE Triboelectric Contact Plate", "1N5819 Schottky Diode Bridge Rectifier", "Supercapacitor 2.7V 10F", "ESP32-C3 SuperMini"]},
    {"id": 38, "domain": "Renewable Energy & Power Systems", "title": "Community Microgrid & Energy Sharing", "category": "HARDWARE",
     "desc": "Develop an intelligent microgrid controller that manages distributed renewable assets and balances islanded microgrid clusters.",
     "components": ["ESP32 Dev Board", "4-Channel 5V Relay Isolation Module", "ACS712 Current Sensors", "20x4 Character LCD with I2C Backpack", "12V 3A SMPS"]},
    {"id": 39, "domain": "Renewable Energy & Power Systems", "title": "Wind Energy & Predictive Maintenance", "category": "HARDWARE",
     "desc": "Develop a wind-turbine condition monitoring unit tracking vibration, bearing temperature, RPM, and power output to predict failures.",
     "components": ["Mini 12V Air Turbine DC Generator Motor", "SW-420 Vibration Sensor Module", "DS18B20 Digital Temperature Sensor", "LM393 Optical IR Speed/RPM Sensor", "ESP32 Dev Board"]},
    {"id": 40, "domain": "Renewable Energy & Power Systems", "title": "Regenerative Energy Recovery (Elevators/Lifts)", "category": "HARDWARE",
     "desc": "Develop a scaled regenerative braking system capturing energy from descending elevators and safely storing or dumping excess power.",
     "components": ["12V High-Torque DC Motor/Generator", "IRFB3077 N-MOSFET (Regen Controller)", "Supercapacitor Bank (5.4V 5F)", "Ceramic Power Dump Resistors (10Ω 10W)", "Arduino Nano"]},
    {"id": 41, "domain": "Renewable Energy & Power Systems", "title": "Solar PV Predictive Maintenance & Soiling Detection", "category": "HARDWARE",
     "desc": "Develop a low-cost PV monitoring device comparing expected irradiance with actual output to identify persistent soiling and dust buildup.",
     "components": ["6V 3W Mini Solar Panel", "BH1750 Digital Ambient Light / Lux Sensor (I2C)", "LM35 Precision Analog Temperature Sensor", "INA219 / Current Sensing Resistors", "ESP32 DevKit"]},
    {"id": 42, "domain": "Renewable Energy & Power Systems", "title": "Solar Farm Yield Forecasting", "category": "SOFTWARE",
     "desc": "Develop a software system integrating meteorological satellite feeds to predict hour-ahead solar power generation for transmission grid stability.",
     "components": []},
    {"id": 43, "domain": "Renewable Energy & Power Systems", "title": "Microgrid Load Balancing Algorithm", "category": "SOFTWARE",
     "desc": "Develop an autonomous software engine that dynamically redistributes renewable power among peer-to-peer consumers to avoid localized blackouts.",
     "components": []},

    # DOMAIN 06: Aerospace, Aviation & Space Tech
    {"id": 44, "domain": "Aerospace, Aviation & Space Tech", "title": "UAV Safety & Autonomous Landing", "category": "HARDWARE",
     "desc": "Develop an autonomous emergency landing unit for drones that detects in-flight propulsion failure and guides descent to a safe landing zone.",
     "components": ["ESP32-S3 DevKit", "BMP280 Barometric Pressure Sensor", "VL53L0X Time-of-Flight Laser Distance Sensor", "MPU-6050 6-Axis IMU", "SG90 Parachute Release Servo"]},
    {"id": 45, "domain": "Aerospace, Aviation & Space Tech", "title": "Autonomous Navigation & Collision Avoidance", "category": "HARDWARE",
     "desc": "Develop an obstacle detection and path replanning module enabling UAVs to detect powerlines and obstacles in real time.",
     "components": ["ESP32-S3 DevKit", "VL53L0X Laser Distance Sensors (Pack of 3)", "HC-SR04 Ultrasonic Sensors", "Small BLDC Motor + ESC", "Mini Buzzer"]},
    {"id": 46, "domain": "Aerospace, Aviation & Space Tech", "title": "Energy-Efficient UAV Mission Planning", "category": "HARDWARE",
     "desc": "Develop an energy-aware UAV mission computer that recalculates flight paths dynamically based on instantaneous battery discharge and headwind.",
     "components": ["ESP32-WROOM-32U (External Antenna)", "NEO-6M GPS Module", "BMP280 Pressure Sensor", "LM2596 Step-Down Buck Module"]},
    {"id": 47, "domain": "Aerospace, Aviation & Space Tech", "title": "Aircraft Electrical Systems Fault Management", "category": "HARDWARE",
     "desc": "Develop a multi-bus electrical fault isolation system that disconnects shorted avionics lines and reroutes power via alternate buses.",
     "components": ["ESP32 DevKit", "4-Channel 5V Relay Isolation Module", "PC817 Optocoupler ICs", "12V 5A Industrial Metal SMPS", "Status Indicator LEDs"]},
    {"id": 48, "domain": "Aerospace, Aviation & Space Tech", "title": "Autonomous Search & Rescue Drone Payload", "category": "HARDWARE",
     "desc": "Develop a compact drone payload that scans disaster zones, detects human presence using thermal signatures, and beacons GPS coordinates.",
     "components": ["ESP32-S3 DevKit with OV2640 Camera", "MLX90614 Non-Contact Infrared Temperature Sensor", "NEO-6M GPS Module with Active Ceramic Antenna", "High-Decibel Siren Module"]},
    {"id": 49, "domain": "Aerospace, Aviation & Space Tech", "title": "Spacecraft Power Management System", "category": "HARDWARE",
     "desc": "Develop a fault-tolerant satellite EPS module prioritizing onboard instrument power and shedding non-critical payload during eclipse periods.",
     "components": ["ESP32-C3 Dev Board", "6V Mini Solar Panel", "TP4056 Charger + Li-ion Cell", "TPS2051 Current-Limited Power Distribution Switch IC", "INA219 Power Monitor"]},
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
    {"id": 53, "domain": "Cybersecurity & Digital Forensics", "title": "Wireless Network Rogue AP & Deauth Defense", "category": "HARDWARE",
     "desc": "Develop an edge intrusion monitor that detects 802.11 deauthentication attacks, rogue Wi-Fi clones, and maintains an offline alert log.",
     "components": ["ESP32-WROOM-32 Dev Board", "0.96-inch I2C OLED Display (SSD1306)", "Active Piezo Buzzer", "MicroSD Card Module + 16GB Card", "TP4056 + Battery"]},
    {"id": 54, "domain": "Cybersecurity & Digital Forensics", "title": "Hardware USB Firewall & BadUSB Filter", "category": "HARDWARE",
     "desc": "Develop an inline hardware security device that screens incoming USB endpoints, dropping rogue Human Interface Device (HID) keystroke injection.",
     "components": ["MAX3421E USB Host Controller Module", "Arduino Nano / ESP32-S3", "0.96-inch OLED Screen", "Status Indicator LEDs", "TPD4E001 ESD Protection Array"]},
    {"id": 55, "domain": "Cybersecurity & Digital Forensics", "title": "Digital Forensics & Chronological Evidence Analysis", "category": "SOFTWARE",
     "desc": "Develop an automated digital forensic tool parsing file system metadata, generating cryptographic SHA-256 hashes, and building forensic timelines.",
     "components": []},
    {"id": 56, "domain": "Cybersecurity & Digital Forensics", "title": "Forensic Hardware Write-Blocker", "category": "HARDWARE",
     "desc": "Develop an inline forensic write-blocker intercepting SD/USB mass storage commands, allowing investigators read-only analysis without contamination.",
     "components": ["MicroSD Card Adapter Module (SPI)", "Arduino Nano V3", "74HC14 Schmitt Trigger IC", "0.96-inch OLED Screen", "Tactile Status Buttons"]},
    {"id": 57, "domain": "Cybersecurity & Digital Forensics", "title": "Cyber Incident Immutable Chain-of-Custody", "category": "SOFTWARE",
     "desc": "Develop an evidence repository establishing tamper-evident chains of custody using Merkle trees and cryptographic verification.",
     "components": []},
    {"id": 58, "domain": "Cybersecurity & Digital Forensics", "title": "Secure Digital Forensics Field Acquisition Kit", "category": "HARDWARE",
     "desc": "Develop a portable, biometric/RFID access-controlled storage imager that logs session operators and detects physical chassis tampering.",
     "components": ["ESP32 DevKit", "RC522 13.56MHz RFID Module + Master Admin Card", "SW-420 Tamper/Vibration Sensor", "MicroSD Card Module", "12V Solenoid Cabinet Lock", "TIP122 Darlington Transistor"]},
    {"id": 59, "domain": "Cybersecurity & Digital Forensics", "title": "Ransomware Behavior Isolation System", "category": "SOFTWARE",
     "desc": "Develop an endpoint security agent detecting rapid, high-entropy file modifications and autonomously isolating infected hosts from the network.",
     "components": []},
    {"id": 60, "domain": "Cybersecurity & Digital Forensics", "title": "Automated Phishing Threat Intelligence Pipeline", "category": "SOFTWARE",
     "desc": "Develop a triage pipeline extracting headers and URLs from suspicious user-submitted emails, querying sandboxes and updating security boundaries.",
     "components": []},

    # DOMAIN 08: Agriculture & Aquaculture
    {"id": 61, "domain": "Agriculture & Aquaculture", "title": "Water Management & Smart Precision Irrigation", "category": "HARDWARE",
     "desc": "Develop an autonomous irrigation controller that evaluates localized soil moisture and temperature to govern multi-valve water delivery.",
     "components": ["ESP32 DevKit", "Capacitive Soil Moisture Sensor V1.2 (Corrosion Proof)", "DS18B20 Waterproof Soil Temp Probe", "12V DC Solenoid Water Valve (1/2 Inch)", "TIP122 Transistor / 1-Channel Relay", "12V 2A SMPS"]},
    {"id": 62, "domain": "Agriculture & Aquaculture", "title": "Precision Agriculture – Drone Crop Health Surveillance", "category": "HARDWARE",
     "desc": "Develop a drone payload using calibrated multispectral/optical sensors to survey vegetative health and identify crop blight.",
     "components": ["ESP32-S3 DevKit with OV5640 5MP Camera", "MicroSD Card Module + 16GB Fast Card", "BH1750 Ambient Light Sensor", "LM2596 DC-DC Buck Converter (from drone battery)"]},
    {"id": 63, "domain": "Agriculture & Aquaculture", "title": "Agricultural Pump Health & Energy Optimization", "category": "HARDWARE",
     "desc": "Develop an edge diagnostic monitor detecting dry running, motor cavitation, phase unbalance, and abnormal pump vibration.",
     "components": ["ESP32 Dev Board", "SW-420 Vibration Sensor Module", "DS18B20 Waterproof Stainless Motor Temp Probe", "1-Channel 30A High-Current Relay Module", "16x2 I2C Character LCD"]},
    {"id": 64, "domain": "Agriculture & Aquaculture", "title": "Crop Frost Early Warning & Automated Mitigation", "category": "HARDWARE",
     "desc": "Develop a micro-climate forecasting node calculating frost points and automatically actuating protective thermal sprinklers or warm blowers.",
     "components": ["ESP32 DevKit", "SHT31 Precision Temp & Humidity Sensor", "BMP280 Barometric Pressure & Dew Point Sensor", "12V 2-Channel Relay Module (Sprinkler/Heater)", "12V Mini Submersible Water Pump"]},
    {"id": 65, "domain": "Agriculture & Aquaculture", "title": "Soil Health & NPK Proxy Edge Monitoring", "category": "HARDWARE",
     "desc": "Develop a field probe evaluating soil electrical conductivity (EC), pH, and moisture parameters to summarize soil viability without internet.",
     "components": ["ESP32-S3 DevKit", "Analog Soil pH Sensor Probe & Board", "Analog Soil Electrical Conductivity (EC) Probe", "Capacitive Soil Moisture Probes", "CA3140 High-Impedance Op-Amp IC", "1.8-inch TFT Display"]},
    {"id": 66, "domain": "Agriculture & Aquaculture", "title": "Aquaculture & Water Quality Management", "category": "HARDWARE",
     "desc": "Develop an automated water quality system monitoring dissolved oxygen proxies, pH, and turbidity, driving aerators when parameters deteriorate.",
     "components": ["ESP32 DevKit", "Analog pH Sensor Kit with BNC Glass Electrode", "Analog Optical Turbidity Sensor Module", "DS18B20 Waterproof Digital Temp Sensor", "4-Channel 5V Relay Module (Aerator Relays)", "12V 3A SMPS"]},
    {"id": 67, "domain": "Agriculture & Aquaculture", "title": "Smart Greenhouse Climate & Fogging Automation", "category": "HARDWARE",
     "desc": "Develop an automated greenhouse system regulating vapor pressure deficits (VPD) through synchronized exhaust venting and ultrasonic misting.",
     "components": ["ESP32 DevKit", "SHT31 Temp & Relative Humidity Sensor", "BH1750 Digital Lux Sensor", "5V/12V Ultrasonic Mist Maker Disk", "12V Brushless DC Blower Fan", "2-Channel Relay Module"]},
    {"id": 68, "domain": "Agriculture & Aquaculture", "title": "Crop Yield Prediction & Commodity Market Triage", "category": "SOFTWARE",
     "desc": "Develop a predictive analytics software pipeline fusing NDVI satellite imagery and commodity indices to suggest optimal harvest liquidation windows.",
     "components": []},
    {"id": 69, "domain": "Agriculture & Aquaculture", "title": "Aquaculture Feeding Rate Optimization Engine", "category": "SOFTWARE",
     "desc": "Develop an algorithmic feeding controller adjusting feeding schedules dynamically based on water temperature, dissolved oxygen, and fish biomass growth.",
     "components": []}
]

# ==============================================================================
# 3. NAVIGATION TABS
# ==============================================================================
st.markdown('<div class="main-title">⚡ Hackathon 2026 Registration & Resource Portal</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Explore problem statements, inspect components, and complete your team registration.</div>', unsafe_allow_html=True)

ps_titles = [f"PS #{ps['id']:02d}: {ps['title']}" for ps in PROBLEM_STATEMENTS]

# Reordered tabs: 1. Statements, 2. Components, 3. Registration
tab_explore, tab_components, tab_register = st.tabs([
    "🔍 1. Problem Statements",
    "📦 2. Component List",
    "📝 3. Team Registration & Payment"
])

# ==============================================================================
# TAB 1: PROBLEM STATEMENTS & COMPENDIUM
# ==============================================================================
with tab_explore:
    st.write("### Official Problem Statement Compendium")
    st.write("Browse all published problem statements across eight technical domains. You can also download the complete compendium Word document below:")

    # Document Download Section
    col_doc1, col_doc2 = st.columns([2, 1])
    with col_doc1:
        st.info("📄 **Problem_Statement_Compendium_v2.docx** contains detailed technical scope, problem descriptions, and submission criteria.")
    with col_doc2:
        doc_filename = "Problem_Statement_Compendium_v2.docx"
        if os.path.exists(doc_filename):
            with open(doc_filename, "rb") as fp:
                st.download_button(
                    label="⬇️ Download Compendium (.docx)",
                    data=fp,
                    file_name="Problem_Statement_Compendium_v2.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
        else:
            st.button(
                label="⬇️ Download Compendium (Unavailable)",
                disabled=True,
                help=f"File '{doc_filename}' not found in the root directory. Place the document in the repository root to enable downloads.",
                use_container_width=True
            )

    st.markdown("---")

    # Filter Controls
    f_col1, f_col2, f_col3 = st.columns([1.5, 1, 1.5])
    domains = ["All Domains"] + sorted(list(set(ps["domain"] for ps in PROBLEM_STATEMENTS)))
    with f_col1:
        selected_domain = st.selectbox("Filter by Technical Domain", domains)
    with f_col2:
        selected_cat = st.selectbox("Category Filter", ["All Categories", "HARDWARE", "SOFTWARE"])
    with f_col3:
        search_query = st.text_input("Search Title or Keywords", placeholder="e.g. Flood, Solar, Battery, AI")

    # Filter dataset
    filtered_list = PROBLEM_STATEMENTS
    if selected_domain != "All Domains":
        filtered_list = [ps for ps in filtered_list if ps["domain"] == selected_domain]
    if selected_cat != "All Categories":
        filtered_list = [ps for ps in filtered_list if ps["category"] == selected_cat]
    if search_query:
        q = search_query.lower()
        filtered_list = [ps for ps in filtered_list if q in ps["title"].lower() or q in ps["desc"].lower()]

    st.write(f"Showing **{len(filtered_list)}** matching problem statement(s):")

    # Render Statements
    for ps in filtered_list:
        with st.expander(f"PS #{ps['id']:02d}: {ps['title']} ({ps['category']})"):
            c_tag = "badge-hw" if ps['category'] == "HARDWARE" else "badge-sw"
            st.markdown(f'<span class="{c_tag}">{ps["category"]}</span> &nbsp; <b>Domain:</b> {ps["domain"]}', unsafe_allow_html=True)
            st.markdown(f"<p style='margin-top: 10px; font-size: 1.05rem;'>{ps['desc']}</p>", unsafe_allow_html=True)
            if ps["category"] == "HARDWARE":
                st.caption(f"Suggested Components: {', '.join(ps['components'][:4])}...")
            else:
                st.caption("No hardware required for this problem statement (Software Track).")


# ==============================================================================
# TAB 2: COMPONENT LIST (HARDWARE INSPECTOR)
# ==============================================================================
with tab_components:
    st.write("### Expected Component List")
    st.write("Select any problem statement to examine its hardware requirements. For software track problems, no hardware components are required.")

    # Dropdown selector
    selected_ps_str = st.selectbox("Choose a Problem Statement to inspect:", ps_titles)
    
    # Extract ID
    selected_ps_id = int(selected_ps_str.split(":")[0].replace("PS #", ""))
    ps_data = next(item for item in PROBLEM_STATEMENTS if item["id"] == selected_ps_id)

    st.markdown("---")
    st.subheader(f"PS #{ps_data['id']:02d}: {ps_data['title']}")
    st.write(f"**Domain:** {ps_data['domain']}")

    # Hardware vs. Software conditional UI
    if ps_data["category"] == "SOFTWARE":
        st.markdown('<span class="badge-sw">SOFTWARE TRACK</span>', unsafe_allow_html=True)
        st.info("ℹ️ **There is no hardware or components for this problem statement.**")
        st.markdown("""
        Teams choosing this statement will develop pure software solutions (web, mobile, cloud, or ML pipelines). 
        Evaluation focuses on architecture, algorithm design, user experience, and computational performance.
        """)
    else:
        st.markdown('<span class="badge-hw">HARDWARE TRACK</span>', unsafe_allow_html=True)
        st.write("#### Expected components list for this problem statement:")
        
        for idx, comp in enumerate(ps_data["components"], 1):
            st.markdown(f"- **{idx}.** {comp}")
            
        st.caption("Note: This list represents the expected components required to prototype a functional solution for this problem statement.")


# ==============================================================================
# TAB 3: REGISTRATION & PAYMENT
# ==============================================================================
with tab_register:
    st.write("### Team Registration & Seat Confirmation")
    st.write("Each team can have up to **5 members**. A minimum of **3 members** is required (Members 4 and 5 are completely optional).")
    st.info("💳 **Registration Fee: ₹350 per team**")

    with st.form("team_registration_form"):
        st.subheader("1. Team Profile")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            team_name = st.text_input("Team Name *", placeholder="e.g. CodeStormers")
        with col_t2:
            assigned_ps = st.selectbox("Selected Problem Statement *", ps_titles)

        st.markdown("---")
        st.subheader("2. Core Members (Compulsory)")
        
        st.markdown("**Member 1 (Team Leader)**")
        col_m1a, col_m1b = st.columns(2)
        with col_m1a:
            leader_name = st.text_input("Leader Full Name *", placeholder="Leader Name")
        with col_m1b:
            leader_phone = st.text_input("Leader Phone Number *", placeholder="10-digit mobile number")

        st.markdown("**Member 2**")
        m2_name = st.text_input("Member 2 Full Name *", placeholder="Full Name")

        st.markdown("**Member 3**")
        m3_name = st.text_input("Member 3 Full Name *", placeholder="Full Name")

        st.markdown("---")
        st.subheader("3. Additional Members (Optional)")
        st.caption("Leave Member 4 and Member 5 blank if your team consists of 3 members.")

        col_m4a, col_m5a = st.columns(2)
        with col_m4a:
            m4_name = st.text_input("Member 4 Full Name (Optional)", placeholder="Leave blank if none")
        with col_m5a:
            m5_name = st.text_input("Member 5 Full Name (Optional)", placeholder="Leave blank if none")
            
        st.markdown("---")
        st.subheader("4. Custom Component Requests (Optional)")
        st.write("Review the **Component List** tab for standard hardware. If your project requires additional or alternative hardware, list it below.")
        custom_components = st.text_area("Custom Components List", placeholder="e.g., 2x NEMA 17 Stepper Motors, 1x Relay Module...")

        st.markdown("---")
        submit_btn = st.form_submit_button("Generate Payment QR Code (₹350)")

    # Form Submission and Validation
    if submit_btn:
        # Enforce compulsory fields without emails
        if not team_name.strip():
            st.error("⚠️ Team Name is required.")
        elif not leader_name.strip() or not leader_phone.strip():
            st.error("⚠️ Leader Name and Phone Number are required.")
        elif not m2_name.strip():
            st.error("⚠️ Member 2 Name is required.")
        elif not m3_name.strip():
            st.error("⚠️ Member 3 Name is required.")
        else:
            # Store in session state
            order_id = f"HACK_{uuid.uuid4().hex[:6].upper()}"
            st.session_state["registration_record"] = {
                "order_id": order_id,
                "team_name": team_name,
                "ps": assigned_ps,
                "leader_name": leader_name,
                "leader_phone": leader_phone,
                "m2_name": m2_name,
                "m3_name": m3_name,
                "m4_name": m4_name if m4_name.strip() else "N/A",
                "m5_name": m5_name if m5_name.strip() else "N/A",
                "custom_components": custom_components if custom_components.strip() else "None requested",
                "amount": 350.00,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.success("✅ Team details validated! Proceed with the payment below.")

    # Render Payment Section if registration session exists
    if "registration_record" in st.session_state:
        rec = st.session_state["registration_record"]
        st.markdown("---")
        st.write("### Payment Checkout")

        col_pay1, col_pay2 = st.columns([1, 1.5])
        with col_pay1:
            # Generate UPI QR Code for ₹350
            upi_id = "9322753587@ptyes"  # Replace with actual UPI ID
            payee_name = "Hackathon Organizing Team"
            upi_string = f"upi://pay?pa={upi_id}&pn={urllib.parse.quote(payee_name)}&am=350.00&cu=INR&tn={rec['order_id']}"

            qr = qrcode.QRCode(version=1, box_size=8, border=3)
            qr.add_data(upi_string)
            qr.make(fit=True)
            img = qr.make_image(fill_color="#1E293B", back_color="white")

            buf = BytesIO()
            img.save(buf, format="PNG")
            st.image(buf.getvalue(), caption="Scan with GPay, PhonePe, or Paytm", width=240)

        with col_pay2:
            st.markdown(f"""
            **Order Reference:** `{rec['order_id']}`  
            **Team Name:** {rec['team_name']}  
            **Problem Statement:** {rec['ps']}  
            **Total Payable:** **₹350.00**  
            
            **Instructions:**
            1. Open any UPI application on your mobile device.
            2. Scan the QR code on the left. The amount is fixed at **₹350**.
            3. Once the transaction completes, copy the 12-digit **UTR / Transaction Reference Number** from your payment app and submit it below to finalize your registration.
            """)

        # UTR Verification Input
        with st.form("utr_verification_form"):
            utr_input = st.text_input("Enter 12-Digit UPI Transaction ID / UTR Number", max_chars=12, placeholder="12 numeric digits")
            submit_utr = st.form_submit_button("Submit Payment Reference")

            if submit_utr:
                if not utr_input.isdigit() or len(utr_input) != 12:
                    st.error("❌ Please provide a valid 12-digit numeric UPI UTR number.")
                else:
                    st.success(f"🎉 Payment reference `{utr_input}` submitted successfully for Team **{rec['team_name']}**!")
                    st.balloons()
                    st.info("Your registration status has been set to **Pending Verification**. A confirmation email will be dispatched once our settlement reconciles.")

# ==============================================================================
# FOOTER
# ==============================================================================
st.markdown("---")
st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 13px;'>Hackathon 2026 Technical Portal • Built with Streamlit</p>", unsafe_allow_html=True)
