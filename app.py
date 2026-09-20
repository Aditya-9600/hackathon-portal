import streamlit as st
import qrcode
from io import BytesIO
from datetime import datetime
import time
import requests
import json

# ---------------------------------------------------------
# 1. FULL DATA DEFINITIONS (75 Problem Statements)
# ---------------------------------------------------------
PROBLEM_STATEMENTS = {
    1: {"domain": "Smart Cities & Urbanization", "theme": "Smart Street Environment & Noise Monitoring", "category": "Hardware", "description": "Develop an loT-based system that dynamically controls streetlight brightness based on real-time pedestrian/vehicle activity while continuously monitoring urban noise levels and identifying abnormal noise events and recurring hotspots.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Acoustic Sensor": "MAX9814 Electret Microphone", "Motion Sensing": "HC-SR501 PIR Motion Sensor", "Light Sensing": "LDR Photoresistor Module", "Lighting Actuator": "12V 5W High-Power LED", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 3A SMPS Enclosed", "Voltage Regulator": "LM2596 Step-Down Buck", "Discrete ICs": "IRF520 MOSFET Driver", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "10µF Caps, Jumpers, Terminals"}},
    2: {"domain": "Smart Cities & Urbanization", "theme": "Automated Pothole Detection", "category": "Hardware", "description": "Develop a system that automatically detects potholes using vision or vibration-based sensing and maps their GPS locations for real-time reporting and city road maintenance.", "components": {"Microcontroller": "ESP32-S3-WROOM-1 DevKit", "Vibration Sensing": "MPU-6050 Accelerometer", "Location Data": "NEO-6M GPS Module", "Auth/Security": "RC522 RFID Module", "Power Supply": "5V 3A SMPS Car Converter", "Data Storage": "MicroSD Module + 16GB Card", "Discrete ICs": "AMS1117-3.3V LDO", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "Jumpers, LEDs, 10kΩ Resistors"}},
    3: {"domain": "Smart Cities & Urbanization", "theme": "Urban Flood Monitoring & Early Warning", "category": "Hardware", "description": "Develop a waterproof monitoring system that detects rapidly rising water levels in urban drains and underpasses and provides early warnings before flooding affects roads and citizens.", "components": {"Microcontroller": "ESP32-WROOM-32U", "Water Level": "JSN-SR04T Waterproof Ultrasonic", "Auth/Security": "RC522 RFID Module", "Alert System": "High-Decibel 12V Siren", "Power Supply": "12V 3A Weatherproof SMPS", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "PC817 Optocoupler & TIP122 Transistor", "Prototyping Base": "400-Point Breadboard & Enclosure", "Passives & Wiring": "Cable Glands, Diodes, Jumpers"}},
    4: {"domain": "Smart Cities & Urbanization", "theme": "Urban Underground Water Leak", "category": "Hardware", "description": "Develop a system that detects and helps locate underground water-pipe leaks using flow, pressure, and acoustic sensing without requiring excavation.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Acoustic Sensing": "Piezo Contact Sensor + LM358", "Flow Sensing": "YF-S201 Hall-Effect Sensor", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 2A SMPS", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "74HC14 Schmitt Trigger", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "Jumpers, Resistors, Filter Caps"}},
    5: {"domain": "Smart Cities & Urbanization", "theme": "Pedestrian Safety & Smart Crosswalk", "category": "Hardware", "description": "Develop a smart crosswalk system that detects waiting pedestrians, dynamically illuminates the crossing, and activates warning signals to alert approaching vehicles.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Pedestrian Detect": "RCWL-0516 Radar + HC-SR501 PIR", "Dynamic Lighting": "WS2812B RGB LED Strip", "Auth/Security": "RC522 RFID Module", "Power Supply": "5V 10A 50W Industrial SMPS", "Discrete ICs": "74HCT125 Level Shifter", "Prototyping Base": "830-Tie Breadboard & Terminals", "Passives & Wiring": "470Ω Resistor, 1000µF Cap, Jumpers"}},
    6: {"domain": "Smart Cities & Urbanization", "theme": "Underground Sewage Gas Safety", "category": "Hardware", "description": "Develop a low-power system that continuously monitors toxic and combustible gases in underground sewage systems and provides warnings when gas concentrations reach dangerous levels.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Toxic Gas Sensor": "MQ-136 H2S Gas Sensor", "Combustible Gas": "MQ-4 Methane Sensor", "Ventilation": "12V 1A DC Blower + Relay", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 5A Industrial SMPS", "Voltage Regulator": "LM2596S Buck Module", "Discrete ICs": "PC817 Optocoupler", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "Buzzer, Jumpers, LEDs"}},
    7: {"domain": "Smart Cities & Urbanization", "theme": "Dynamic Digital Traffic Signage", "category": "Hardware", "description": "Develop a connected digital signage system that receives real-time traffic or road-condition data and automatically displays alternative routes or detour instructions.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Matrix Display": "MAX7219 4-in-1 Dot Matrix", "Timekeeping": "DS3231 High-Precision RTC", "Auth/Security": "RC522 RFID Module", "Power Supply": "5V 4A SMPS Enclosed", "Discrete ICs": "74HC595 Shift Register", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "Jumpers, 10µF Caps, Resistors"}},
    8: {"domain": "Smart Cities & Urbanization", "theme": "Smart Waste Management", "category": "Hardware", "description": "Develop an loT-based waste management system that monitors garbage-bin fill levels, detects overflow conditions, and sends alerts for timely collection.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Fill Level Sensor": "HC-SR04 Ultrasonic Sensors", "Tamper/Tilt": "SW-520D Roller Tilt Sensor", "Auth/Security": "RC522 RFID Module", "Actuator": "SG90 Micro Servo", "Power Supply": "5V 2A SMPS Adapter", "Discrete ICs": "AMS1117-3.3V LDO", "Prototyping Base": "400-Tie Point Breadboard", "Passives & Wiring": "Jumpers, LEDs, 10kΩ Resistors"}},
    9: {"domain": "Health Tech Hackathon", "theme": "Elderly Care & Assistive Technology", "category": "Hardware", "description": "Develop a wearable system that detects accidental falls in elderly individuals, provides medication reminders, and automatically sends an SOS alert with location.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Motion Sensing": "MPU-6050 Accelerometer/Gyro", "Location Tracking": "NEO-6M GPS Module", "Cellular Comms": "SIM800L GPRS/GSM Module", "Real-Time Clock": "DS3231 RTC Module", "Haptic Alert": "3V Coin Vibration Motor", "Power Management": "TP4056 1A Li-Ion Charger", "Battery Source": "3.7V 1200mAh Li-Po", "Power Supply": "5V 2A SMPS Module", "Discrete ICs": "2N2222 NPN & AMS1117 LDO", "Prototyping Base": "Mini 170-Tie Breadboard", "Passives & Connectors": "Diodes, Push Button, Resistors"}},
    10: {"domain": "Health Tech Hackathon", "theme": "Hospital Patient Safety & Monitoring", "category": "Hardware", "description": "Develop a smart monitoring system that continuously detects the remaining level of an IV fluid bag and automatically alerts nursing staff when critically low.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Weight Sensing": "1kg Load Cell + HX711 ADC", "Display": "16x2 LCD with I2C", "Alert Subsystem": "5V Buzzer + Red LED", "Power Supply": "12V 2A SMPS Enclosed", "Step-Down Module": "LM2596S Buck Converter", "Discrete ICs": "HX711 IC & PC817 Optocoupler", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Connectors": "Diodes, Resistors, Jumpers"}},
    11: {"domain": "Health Tech Hackathon", "theme": "Blood Bank & Medical Inventory Management", "category": "Hardware", "description": "Develop an loT-based system that continuously monitors blood storage temperature, tracks blood bag inventory and expiry information, and generates alerts.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "RFID Subsystem": "RC522 RFID Reader Module", "RFID Transponders": "13.56MHz Mifare Tags (10x)", "Temperature Sensor": "DS18B20 Waterproof Probe", "Display": "20x4 LCD with I2C", "Power Supply": "12V 3A SMPS", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "DS18B20 IC & 74HC4050 Buffer", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Connectors": "Resistors, Capacitors, Buzzer"}},
    12: {"domain": "Health Tech Hackathon", "theme": "Neonatal & Maternal Healthcare", "category": "Hardware", "description": "Develop a smart incubator monitoring and control system that maintains stable temperature and humidity for premature babies.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Climate Sensing": "SHT31 I2C Temp & Humidity", "Surface Sensor": "DS18B20 Skin-Surface Probe", "Heating Actuator": "12V 50W PTC Air Heater", "Air Circulation": "12V Brushless Blower Fan", "Humidity Control": "Ultrasonic Mist Maker", "Driver Module": "IRF520 MOSFET Module", "Power Supply": "12V 10A 120W SMPS", "Voltage Regulator": "LM2596 Buck Converter", "Discrete ICs": "AMS1117 LDO & PC817 Opto", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Connectors": "Resistors, Terminals, Wires"}},
    13: {"domain": "Health Tech Hackathon", "theme": "Preventive Healthcare & Wellness", "category": "Hardware", "description": "Develop a smart bottle that automatically measures a user's water intake, monitors hydration patterns, and provides personalized reminders.", "components": {"Microcontroller": "ESP32-C3 SuperMini RISC-V", "Water Level Sensor": "Non-Contact Capacitive Level", "Access/User ID": "RC522 RFID Module", "Display / UI": "0.42-inch OLED I2C", "Power Supply": "5V 2A SMPS Adapter", "Battery Subsystem": "TP4056 Charger + 1000mAh LiPo", "Discrete ICs": "AMS1117-3.3V LDO", "Alert Module": "3V Coin Vibration Motor", "Prototyping Base": "Mini 170-Tie Breadboard", "Passives & Wiring": "Resistors, Caps, Pushbutton"}},
    14: {"domain": "Health Tech Hackathon", "theme": "Al-Based Disease Detection & Medical Diagnostics", "category": "Hardware", "description": "Develop a low-cost digital microscopy system that captures blood-smear images and uses computer vision or Al to identify cells containing abnormalities.", "components": {"Microcontroller": "ESP32-S3-WROOM-1 DevKit", "Optics": "OV5640 5MP Camera Module", "Illumination": "Precision Adjustable LED", "Auth/Security": "RC522 RFID Module", "Focus Actuator": "NEMA 17 Stepper Motor", "Power Supply": "12V 3A Enclosed SMPS", "Voltage Regulator": "LM2596 Buck Converter", "Discrete ICs": "A4988 Driver & AMS1117 LDO", "Prototyping Base": "830-Tie Breadboard & Zero PCB", "Passives & Wiring": "Caps, Limit Switches, Jumpers"}},
    15: {"domain": "Health Tech Hackathon", "theme": "Digital Healthcare & Organ Transplant Management", "category": "Software", "description": "Develop a secure digital platform that enables hospitals to efficiently match organ donors with eligible recipients while protecting identities.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Auth/Security": "RC522 RFID Smart Card Terminal", "Crypto Hardware": "ATECC608A Secure Crypto IC", "Display": "16x2 I2C LCD Display", "Power Supply": "5V 2A SMPS Regulated Adapter", "Discrete ICs": "74HC595 Shift Register", "Prototyping Base": "400-Tie Point Half Breadboard", "Passives & Wiring": "Pullup Resistors, LEDs, Jumpers"}},
    16: {"domain": "Electric Vehicle Hackathon", "theme": "EV Battery Safety & Thermal", "category": "Hardware", "description": "Develop a low-cost battery monitoring and protection system that detects early signs of thermal runaway and isolates the affected section.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Thermal Probes": "NTC 10k Precision Thermistors", "Gas Detection": "MQ-2 Flammable Gas Sensor", "Fault Isolation": "4-Channel 5V Relay Module", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 10A 120W SMPS", "Discrete ICs": "LM393 Dual Comparator IC", "Voltage Regulator": "LM2596S Buck Converter", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "Siren, Resistors, Harness"}},
    17: {"domain": "Electric Vehicle Hackathon", "theme": "EV Motor Fault Detection & Predictive", "category": "Hardware", "description": "Develop a sensorless motor-monitoring system that analyzes three-phase current signals to detect developing inter-turn winding faults.", "components": {"Microcontroller": "ESP32-WROOM-32", "Phase Monitoring": "ACS712 30A Current Sensors", "Signal Clamping": "LM358 Op-Amp ICs", "Auth/Security": "RC522 RFID Module", "Bench Power": "12V 5A Bench SMPS", "Voltage Regulator": "LM2596 Buck Module", "Display": "0.96-inch I2C OLED Display", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "Shielded Wire, Caps, Jumpers"}},
    18: {"domain": "Electric Vehicle Hackathon", "theme": "EV Charging Infrastructure Monitoring", "category": "Hardware", "description": "Develop a retrofit device that independently verifies whether an EV charging station is actually delivering electrical power and records genuine events.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Power Audit": "PZEM-004T V3.0 AC Meter", "Current Clamp": "SCT-013-000 100A Current Clamp", "Auth/Security": "RC522 RFID Reader", "Power Supply": "12V 2A Enclosed SMPS", "Voltage Regulator": "LM2596 Buck Module", "Display / UI": "0.96-inch I2C OLED", "Prototyping Base": "Breadboard & Terminal Blocks", "Passives & Wiring": "14AWG Wire, Caps, Jumpers"}},
    19: {"domain": "Electric Vehicle Hackathon", "theme": "Regenerative Braking & Energy Recovery", "category": "Hardware", "description": "Develop an intelligent regenerative-braking controller that dynamically determines the appropriate level of braking and maximizes energy recovery.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Current Sensing": "ACS712 30A Bidirectional Sensor", "Power Switching": "IRFB3077 N-MOSFET", "Gate Driver": "TC4427/IR2104 Gate Driver", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 10A 120W SMPS", "Voltage Regulator": "LM2596S Buck Converter", "Discrete ICs": "PC817 Optocoupler IC", "Prototyping Base": "Breadboard & Power Resistors", "Passives & Wiring": "1000µF Caps, 14AWG Wire"}},
    20: {"domain": "Electric Vehicle Hackathon", "theme": "EV Traction Control & Vehicle", "category": "Hardware", "description": "Develop an intelligent traction-control system that detects excessive wheel slip and dynamically adjusts motor torque to improve stability.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Speed Sensors": "LM393 Optical Wheel Sensors", "Motor Driver": "L298N Dual H-Bridge Module", "Actuators": "Dual TT DC Geared Motors", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 5A Bench SMPS", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "74HC14 Hex Inverting Schmitt", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "Jumpers, Caps, Status LEDs"}},
    21: {"domain": "Electric Vehicle Hackathon", "theme": "Vehicle-to-Grid Energy Management", "category": "Hardware", "description": "Develop a bidirectional EV energy-management system that determines when an EV should charge or supply energy based on grid demand.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Power Monitoring": "INA226 High-Accuracy Monitor", "Load Switching": "2-Channel Power Relay (30A)", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 10A 120W Enclosed SMPS", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "PC817 Opto & ULN2003 Driver", "Prototyping Base": "Breadboard & Power Terminals", "Passives & Wiring": "12AWG Silicone Wire, Jumpers"}},
    22: {"domain": "Electric Vehicle Hackathon", "theme": "EV Structural Health & Predictive Maintenance", "category": "Hardware", "description": "Develop an accelerometer-based system for detecting structural fatigue in an EV battery mounting system by identifying resonant-frequency changes.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Vibration Sensing": "ADXL345 3-Axis Accelerometer", "Shock Sensing": "SW-420 Shock Sensor", "Auth/Security": "RC522 RFID Module", "Display": "0.96-inch I2C OLED", "Power Supply": "12V 2A SMPS Power Supply", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "LM393 Dual Comparator IC", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "Jumpers, LEDs, 10kΩ Resistors"}},
    23: {"domain": "IoT Hackathon", "theme": "Smart Portable Freezer & Cold-Chain", "category": "Hardware", "description": "Develop an loT-enabled portable thermoelectric freezer that maintains low temperatures while monitoring status and sending alerts.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Cooling Element": "TEC1-12706 Peltier Cooler", "Heat Dissipation": "Heatsink + 12V Cooling Fan", "Thermal Sensing": "DS18B20 Temp Sensor", "Location Data": "NEO-6M GPS Module", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 10A 120W SMPS", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "IRF3205 N-MOSFET", "Prototyping Base": "Breadboard & Power Terminals", "Passives & Wiring": "High-Gauge Wire, Thermal Paste"}},
    24: {"domain": "IoT Hackathon", "theme": "Industrial Machine Predictive Maintenance", "category": "Hardware", "description": "Develop an loT-based monitoring system that analyzes motor vibration, temperature, and current to identify abnormal conditions before failure.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Vibration Sensor": "ADXL345 3-Axis Accelerometer", "Thermal Sensing": "MLX90614 Infrared Temp Sensor", "Current Monitor": "ACS712 30A Current Sensor", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 3A Industrial SMPS", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "PC817 Optocoupler IC", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "Shielded cables, Caps, Jumpers"}},
    25: {"domain": "IoT Hackathon", "theme": "Smart Grid & Grid Automation", "category": "Hardware", "description": "Develop an loT-based smart-grid monitoring system that continuously monitors voltage, current, frequency, and load conditions.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Voltage Sensor": "ZMPT101B AC Voltage Sensor", "Current Sensor": "SCT-013-000 100A AC Clamp", "Load Shedding": "4-Channel 5V Relay Module", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 5A Industrial SMPS", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "ULN2803A Transistor IC", "Prototyping Base": "Breadboard & Terminals", "Passives & Wiring": "Diodes, Snubber Caps, 14AWG"}},
    26: {"domain": "IoT Hackathon", "theme": "Al + IoT for Electrical Systems", "category": "Hardware", "description": "Develop an AloT system that analyzes real-time electrical parameters to identify abnormal patterns and predict equipment failures.", "components": {"Microcontroller": "ESP32-S3 DevKit", "Current Sensor": "ACS712 20A Current Sensors", "Voltage Sensor": "ZMPT101B AC Voltage Sensor", "Thermal Sensor": "DS18B20 Temp Sensors", "Vibration Sensor": "ADXL345 Accelerometer Module", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 3A SMPS Power Supply", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "LM358 Dual Op-Amp", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "Jumpers, Terminals, Caps"}},
    27: {"domain": "IoT Hackathon", "theme": "Smart Agriculture & Electrical", "category": "Hardware", "description": "Develop an loT-based agricultural automation system that uses soil moisture and weather data to automatically control irrigation.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Soil Sensing": "Capacitive Soil Moisture V1.2", "Pump Health": "ACS712 30A Current Sensor", "Pump Control": "1-Channel 30A Relay Module", "Water Level": "Capacitive Liquid Level Sensor", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 5A Industrial SMPS", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "PC817 Optocoupler IC", "Prototyping Base": "Breadboard & Terminals", "Passives & Wiring": "Diodes, Jumpers, Status LEDs"}},
    28: {"domain": "IoT Hackathon", "theme": "Smart Soil Erosion & Landslide", "category": "Hardware", "description": "Develop a sensor-based IoT warning system that monitors deep-soil moisture and ground tilt to detect conditions indicating potential landslides.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Moisture Sensing": "Capacitive Soil Probes", "Tilt/Motion": "ADXL345 High-Resolution Tilt", "Auth/Security": "RC522 RFID Module", "Warning Siren": "High-Decibel 12V Siren", "Power Supply": "12V 2A Weatherproof SMPS", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "TIP122 Transistor IC", "Prototyping Base": "Breadboard & IP65 Enclosure", "Passives & Wiring": "Jumpers, Resistors, Cable Glands"}},
    29: {"domain": "IoT Hackathon", "theme": "Smart Parcel & Delivery Security", "category": "Hardware", "description": "Develop a smart parcel locker that detects deliveries, monitors unauthorized access, and provides secure OTP/RFID-based access.", "components": {"Microcontroller": "ESP32-WROOM-32U DevKit", "Logic Expander": "Arduino Nano V3", "Auth/Security": "RC522 RFID Reader", "Manual Input": "4x4 Matrix Keypad", "Locking Actuator": "12V Solenoid Door Lock", "Parcel Detection": "VL53L0X Laser Sensor", "Power Supply": "12V 5A 60W SMPS", "Power Control": "2-Channel 5V Relay Module", "Voltage Regulator": "LM2596 Buck Converter", "Discrete ICs": "Bidirectional Level Converter", "Prototyping Base": "Breadboards (x2)", "Passives & Wiring": "Diodes, Reed Switch, Jumpers"}},
    30: {"domain": "EdTech Hackathon", "theme": "Multilingual Academic Learning", "category": "Software", "description": "Develop a multilingual academic support system that accepts questions in Marathi, Hindi, or English and provides clear explanations.", "components": {"Microcontroller": "ESP32-S3 DevKit", "Audio Input": "INMP441 I2S Microphone", "Audio Output": "MAX98357A I2S Amplifier", "Auth/Security": "RC522 RFID Module", "Speaker": "8Ω 3W Miniature Speaker", "Power Supply": "5V 2A SMPS Power Supply", "Discrete ICs": "AMS1117-3.3V LDO", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "Buttons, Jumpers, Filter Caps"}},
    31: {"domain": "EdTech Hackathon", "theme": "Personalized Educational Resource Recommendation", "category": "Software", "description": "Develop a system that analyzes student interactions to identify learning preferences and recommend educational resources.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Auth/Security": "RC522 RFID Reader Module", "User Input": "4-Key Touch Sensor (TTP224)", "Display / UI": "0.96-inch I2C OLED", "Power Supply": "5V 2A SMPS Adapter", "Discrete ICs": "74HC14 Schmitt Trigger IC", "Prototyping Base": "400-Tie Point Breadboard", "Passives & Wiring": "Jumpers, LEDs, 10kΩ Resistors"}},
    32: {"domain": "EdTech Hackathon", "theme": "Interactive Al-Powered Quantum Learning", "category": "Software", "description": "Develop an Al-powered interactive platform that enables users to learn quantum computing and design quantum circuits.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Auth/Security": "PN532 NFC/RFID Reader", "Display / UI": "20x4 LCD with I2C", "Access Control": "5V Buzzer & Relay", "Power Supply": "5V 2A SMPS Adapter", "Discrete ICs": "PC817 Optocoupler IC", "Prototyping Base": "400-Tie Point Breadboard", "Passives & Wiring": "Jumpers, LEDs, 4.7kΩ Pullups"}},
    33: {"domain": "EdTech Hackathon", "theme": "Academic-Industry Collaboration Platform", "category": "Software", "description": "Develop a platform that enables universities and industries to discover suitable partners and initiate collaborations.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Auth/Security": "PN532 NFC/RFID Reader", "Display / UI": "20x4 LCD with I2C", "Access Control": "5V Buzzer & Relay", "Power Supply": "5V 2A SMPS Adapter", "Discrete ICs": "PC817 Optocoupler IC", "Prototyping Base": "400-Tie Point Breadboard", "Passives & Wiring": "Jumpers, LEDs, Pullups"}},
    34: {"domain": "EdTech Hackathon", "theme": "Offline Low-Vision Reading", "category": "Hardware", "description": "Develop a compact handheld system that recognizes printed educational text and converts it into accessible audio.", "components": {"Microcontroller": "ESP32-S3-WROOM-1 DevKit", "Audio Output": "MAX98357A I2S Amplifier", "Speaker": "Mini 8Ω 2W Speaker", "Auth/Security": "RC522 RFID Module", "Power Source": "TP4056 Charger + 18650 Cell", "Discrete ICs": "AMS1117-3.3V LDO", "Prototyping Base": "400-Tie Point Breadboard", "Passives & Wiring": "Buttons, Caps, Jumpers"}},
    35: {"domain": "EdTech Hackathon", "theme": "Smart Handwriting Posture & Grip", "category": "Hardware", "description": "Develop a smart pen or wearable that detects incorrect writing posture or grip in real time and provides child-friendly feedback.", "components": {"Microcontroller": "ESP32-C3 SuperMini RISC-V", "Grip Sensing": "Force Sensing Resistor (FSR402)", "Posture Sensing": "MPU-6050 6-Axis Motion", "Haptic Alert": "Mini 3V Vibration Motor", "Auth/Security": "RC522 RFID Module", "Power Source": "TP4056 + 3.7V 300mAh LiPo", "Dock Power": "5V 1A SMPS Dock", "Discrete ICs": "2N2222 NPN Transistor", "Prototyping Base": "Mini 170-Tie Breadboard", "Passives & Wiring": "Resistors, Diodes, Silicone Wire"}},
    36: {"domain": "EdTech Hackathon", "theme": "Visual Pronunciation Learning", "category": "Hardware", "description": "Develop a device that uses microphone input and a display to provide visual mouth-shape guidance for pronunciation.", "components": {"Microcontroller": "ESP32-S3 DevKit", "Microphone": "MAX9814 Electret Microphone", "Display / UI": "1.8-inch SPI TFT Display", "Auth/Security": "RC522 RFID Module", "Power Supply": "5V 2A SMPS Adapter", "Discrete ICs": "AMS1117-3.3V LDO", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "Jumpers, Caps, Resistors"}},
    37: {"domain": "Renewable Energy", "theme": "Solar Energy & Battery Management", "category": "Hardware", "description": "Develop an energy-management controller that monitors solar generation and intelligently schedules battery charging.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Current Sensing": "ACS712 30A Current Sensors", "Voltage Sensing": "Voltage Detection Modules", "Power Switching": "IRF3205 N-MOSFET Switches", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 10A Industrial SMPS", "Voltage Regulator": "LM2596S Buck Module", "Discrete ICs": "IR2104 Gate Driver IC", "Prototyping Base": "Breadboard & Terminals", "Passives & Wiring": "Filter Caps, Shunts, 14AWG Wire"}},
    38: {"domain": "Renewable Energy", "theme": "Power Quality & Harmonic Management", "category": "Hardware", "description": "Develop a real-time power-quality monitoring system that detects and analyzes harmonic components.", "components": {"Microcontroller": "ESP32-WROOM-32", "AC Voltage Sensor": "ZMPT101B AC Voltage Sensor", "AC Current Sensor": "SCT-013-000 100A AC Clamp", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 2A SMPS Power Supply", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "LM358 Dual Op-Amp IC", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "Bias Resistors, Caps, Jumpers"}},
    39: {"domain": "Renewable Energy", "theme": "Solar Microgrid & Black-Start", "category": "Hardware", "description": "Develop a black-start controller that can safely restore a local renewable-energy microgrid after a complete outage.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "AC Line Sensing": "ZMPT101B AC Voltage Sensor", "Load Sensing": "ACS712 20A Current Sensors", "Load Restoration": "4-Channel 5V Relay Module", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 5A 60W SMPS", "Voltage Regulator": "LM2596S Buck Module", "Discrete ICs": "ULN2803A & PC817 Optocoupler", "Prototyping Base": "Breadboard & Terminals", "Passives & Wiring": "Diodes, Snubber Caps, Jumpers"}},
    40: {"domain": "Renewable Energy", "theme": "Electric Vehicles & Vehicle-to-Grid Technology", "category": "Hardware", "description": "Develop a smart V2G controller that coordinates EV charging and discharging according to grid demand.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Current Sensing": "ACS712 30A Bidirectional Sensor", "Comms Interface": "MCP2515 CAN Bus Controller", "Auth/Security": "RC522 RFID Reader", "Power Supply": "12V 10A 120W SMPS", "Power Switching": "IRF3205 MOSFET Switches", "Discrete ICs": "LM393 Dual Comparator", "Voltage Regulator": "LM2596S Buck Module", "Prototyping Base": "Breadboard & Terminals", "Passives & Wiring": "Caps, Shunts, 14AWG Wire"}},
    41: {"domain": "Renewable Energy", "theme": "Urban Renewable Energy", "category": "Hardware", "description": "Develop a small-scale energy-harvesting system that captures low-level wind or mechanical energy from urban activities.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Harvester 1": "Piezoelectric Vibration Discs", "Harvester 2": "Mini 3-Phase AC Wind Dynamo", "Storage Element": "2.7V 10F Supercapacitor", "Power IC": "LTC3588 Harvesting IC", "Auth/Security": "RC522 RFID Module", "Base Station Power": "5V 2A SMPS Power Supply", "Discrete ICs": "1N5819 Schottky Diode Array", "Prototyping Base": "400-Tie Point Breadboard", "Passives & Wiring": "Zener Diodes, Jumpers, Storage Caps"}},
    42: {"domain": "Renewable Energy", "theme": "Railway Energy Harvesting", "category": "Hardware", "description": "Develop a vibration-energy harvesting system that captures mechanical vibrations produced by railway operations.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Primary Harvester": "Piezoelectric Ceramic Harvester", "Telemetry Sensor": "INA219 I2C Monitor", "Vibration Sensor": "SW-420 Vibration Sensor", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 2A Enclosed SMPS", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "DB107 Diode Bridge Rectifier", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "Supercapacitors, Resistors, Jumpers"}},
    43: {"domain": "Renewable Energy", "theme": "Community Microgrid & Energy Sharing", "category": "Hardware", "description": "Develop an intelligent microgrid controller that manages local energy, prioritizes loads, and safely transitions islanded operations.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Energy Metering": "PZEM-004T AC Power Meter", "Load Switching": "2-Channel 5V Relay (30A)", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 5A 60W SMPS", "Display / UI": "16x2 I2C LCD Display", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "PC817 Optocoupler IC", "Prototyping Base": "Breadboard & Terminals", "Passives & Wiring": "16AWG Wiring, Snubber Caps"}},
    44: {"domain": "Renewable Energy", "theme": "Wind Energy & Predictive Maintenance", "category": "Hardware", "description": "Develop a wind-turbine condition-monitoring system that analyzes vibration and temperature to identify abnormal operations.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Vibration Sensor": "ADXL345 Accelerometer", "RPM Sensor": "LM393 Optical RPM Sensor", "Thermal Sensor": "DS18B20 Temp Probe", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 3A SMPS Power Supply", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "74HC14 Schmitt Trigger IC", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "Jumpers, Pull-ups, Status LEDs"}},
    45: {"domain": "Renewable Energy", "theme": "Regenerative Energy Recovery", "category": "Hardware", "description": "Develop a scaled regenerative-braking system that captures mechanical energy generated during the braking of an elevator.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Generator": "12V High-Torque DC Generator", "Power Sensing": "INA219 I2C Module", "Energy Storage": "Supercapacitor Bank (5.4V 5F)", "Dynamic Switching": "IRFB3077 N-MOSFET", "Auth/Security": "RC522 RFID Module", "Bench Power": "12V 5A SMPS Unit", "Voltage Regulator": "LM2596S Buck Module", "Discrete ICs": "TC4427 Driver & PC817 Opto", "Prototyping Base": "Breadboard & Terminals", "Passives & Wiring": "Ceramic Dump Resistors, Jumpers"}},
    46: {"domain": "Renewable Energy", "theme": "Renewable-Powered EV Charging", "category": "Hardware", "description": "Develop a smart EV charging controller that dynamically schedules charging based on renewable-energy availability.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Current Sensing": "ACS712 30A Current Sensor", "Voltage Sensing": "DC 0-25V Detection Module", "Power Relay": "1-Channel 30A Relay", "Auth/Security": "RC522 RFID Module", "Display / UI": "16x2 LCD with I2C", "Power Supply": "12V 10A 120W SMPS", "Voltage Regulator": "LM2596S Buck Converter", "Discrete ICs": "ULN2003A & AMS1117 LDO", "Prototyping Base": "Breadboard & Screw Terminals", "Passives & Wiring": "14AWG Cable, Diodes, LEDs"}},
    47: {"domain": "Renewable Energy", "theme": "Solar PV Predictive Maintenance & Soiling", "category": "Hardware", "description": "Develop a low-cost solar-PV monitoring system that compares expected irradiance with actual output to distinguish shading from dust.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Irradiance Sensor": "BH1750 Digital Lux Sensor", "Power Telemetry": "INA219 DC Power Sensor", "Surface Temp": "DS18B20 Temp Probe", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 2A SMPS", "Voltage Regulator": "LM2596S Buck Module", "Discrete ICs": "LM358 Op-Amp & AMS1117 LDO", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "Pull-Up Resistors, Filter Caps"}},
    48: {"domain": "Renewable Energy", "theme": "Wave Energy Conversion", "category": "Hardware", "description": "Develop an Oscillating Water Column system that converts wave-induced air displacement into electrical energy using an air turbine.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Pressure Sensing": "MPX5010DP Pressure Sensor", "Turbine/Generator": "Mini 12V Air Turbine Generator", "Telemetry Sensor": "INA219 I2C Energy Monitor", "Auth/Security": "RC522 RFID Module", "Bench Power": "12V 3A SMPS Power Supply", "Voltage Regulator": "LM2596S Buck Module", "Discrete ICs": "1N5819 Rectifier & LM324 Op-Amp", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "470µF Smoothing Caps, Terminals"}},
    49: {"domain": "Renewable Energy", "theme": "Triboelectric Energy Harvesting", "category": "Hardware", "description": "Develop a triboelectric nanogenerator that captures low-amplitude ambient vibrations using contact-separation principles.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "TENG Element": "Copper-PTFE Contact Mechanism", "Vibration Sensor": "ADXL345 Accelerometer", "High-Z Input Amp": "CA3140 Op-Amp IC", "Auth/Security": "RC522 RFID Module", "Power Supply": "5V 2A SMPS Power Supply", "Storage Element": "Film Capacitor Bank", "Discrete ICs": "1N4007 Diodes & AMS1117 LDO", "Prototyping Base": "400-Tie Point Half Breadboard", "Passives & Wiring": "High Value Resistors, Probes"}},
    50: {"domain": "Renewable Energy", "theme": "Biogas Energy & Digester Optimization", "category": "Hardware", "description": "Develop a smart monitoring system for biogas plants that measures parameters like temperature, pH, and gas production.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Methane Sensor": "MQ-4 Methane Sensor", "PH Sensor": "Analog pH Sensor Kit", "Thermal Sensor": "DS18B20 Temp Probe", "Feed Actuator": "12V Micro Solenoid Valve", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 3A SMPS", "Voltage Regulator": "LM2596S Buck Module", "Discrete ICs": "TIP122 Transistor IC", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "Flyback Diodes, Terminals, Jumpers"}},
    51: {"domain": "Renewable Energy", "theme": "Waste Heat Energy Conversion", "category": "Hardware", "description": "Develop a thermoacoustic energy-conversion system that uses a low-grade thermal gradient to generate electrical output.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Thermal Gradient": "MAX6675 Thermocouple Module", "Acoustic Sensor": "Electret / Piezo Acoustic Sensor", "Thermal Element": "TEC1-12706 Peltier Generator", "Telemetry Sensor": "INA219 Power Monitor", "Auth/Security": "RC522 RFID Module", "Bench Power": "12V 5A Industrial SMPS", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "LM358 Dual Op-Amp IC", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "Ceramic Caps, High-Watt Resistors"}},
    52: {"domain": "Aerial Systems", "theme": "UAV Safety & Autonomous Landing", "category": "Hardware", "description": "Develop an autonomous emergency-landing system that monitors UAV health, identifies a landing zone, and guides safe landing.", "components": {"Microcontroller": "ESP32-S3-DevKitC-1", "Flight Dynamics": "MPU-6050 6-DOF IMU", "Altitude Sensor": "BMP280 Barometric Pressure", "Deployment Actuator": "MG996R Metal Gear Servo", "Auth/Security": "RC522 RFID Module", "Ground Power": "12V 5A Bench SMPS", "Flight Power": "TP4056 + 3.7V 800mAh LiPo", "Discrete ICs": "PC817 Optocoupler IC", "Prototyping Base": "Mini 170-Tie Point Breadboard", "Passives & Wiring": "5V Buzzer, LED, Jumpers"}},
    53: {"domain": "Aerial Systems", "theme": "Autonomous Navigation & Collision", "category": "Hardware", "description": "Develop an autonomous obstacle-detection and path-planning system that enables a UAV to detect obstacles and modify its trajectory.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Primary Sensing": "VL53L0X Time-of-Flight Sensor", "Secondary Sensing": "HC-SR04 Ultrasonic Sensors", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 5A Bench SMPS", "Voltage Regulator": "LM2596 Buck Converter", "Discrete ICs": "74HC14 & Level Converter", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "I2C Pullup Resistors, Caps"}},
    54: {"domain": "Aerial Systems", "theme": "Energy-Efficient UAV Operations", "category": "Hardware", "description": "Develop an energy-aware UAV mission-planning system that monitors battery status to optimize flight routes.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Power Telemetry": "INA219 I2C Current Sensor", "Auth/Security": "RC522 RFID Module", "Ground Power": "12V 5A Industrial Bench SMPS", "Voltage Regulator": "LM2596 Buck Converter", "Display / UI": "0.96-inch OLED I2C", "Discrete ICs": "AMS1117-3.3V LDO", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "Power Shunts, Filter Caps"}},
    55: {"domain": "Aerial Systems", "theme": "Aircraft Electrical Systems & Fault", "category": "Hardware", "description": "Develop an aircraft electrical fault-management system that monitors voltage, current, and isolates faulty sections.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Current Sensors": "ACS712 20A Current Sensors", "Voltage Sensors": "ZMPT101B Voltage Sensors", "Fault Isolation": "4-Channel 5V Relay Module", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 10A 120W SMPS", "Discrete ICs": "ULN2803A & LM358 Op-Amp", "Voltage Regulator": "LM2596S Buck Module", "Prototyping Base": "Breadboard & Terminal Blocks"}},
    56: {"domain": "Aerial Systems", "theme": "Autonomous Search & Rescue", "category": "Hardware", "description": "Develop an autonomous search-and-rescue drone system capable of systematically scanning a designated area to locate targets.", "components": {"Microcontroller": "ESP32-S3-WROOM-1 DevKit", "Positioning": "NEO-6M GPS Module", "Auth/Security": "RC522 RFID Module", "Ground Power": "12V 3A SMPS Base Station", "UAV Power": "LM2596 Buck Module", "Alert Beacon": "5V Alarm Siren + 3W LED", "Discrete ICs": "TIP122 Transistor IC", "Prototyping Base": "Mini Solderless Breadboard", "Passives & Wiring": "Resistors, Diodes, Jumpers"}},
    57: {"domain": "Aerial Systems", "theme": "Aviation Safety & Bird Strike Prevention", "category": "Hardware", "description": "Develop a bird-detection and collision-risk assessment system that tracks movement and generates avoidance responses.", "components": {"Microcontroller": "ESP32-S3 DevKit", "Proximity Sensing": "HC-SR04 Waterproof Sensors", "Auth/Security": "RC522 RFID Module", "Ground Power": "12V 3A SMPS Unit", "Acoustic Driver": "PAM8403 3W Amplifier + Horn", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "2N2222 NPN Transistors", "Prototyping Base": "400-Tie Point Breadboard", "Passives & Wiring": "Audio Caps, Jumpers, Pins"}},
    58: {"domain": "Aerial Systems", "theme": "Satellite Fault Detection & Recovery", "category": "Hardware", "description": "Develop an autonomous satellite fault-management system that identifies abnormal behavior and initiates recovery procedures.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Power Telemetry": "INA219 Voltage/Current Sensor", "Thermal Sensing": "LM35 Precision Temp Sensor", "Auth/Security": "RC522 RFID Module", "Ground Power": "5V 3A Regulated SMPS", "Discrete ICs": "CD4051 8-Channel Multiplexer", "Display / UI": "0.96-inch OLED Screen", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "Jumpers, Resistors, LEDs"}},
    59: {"domain": "Aerial Systems", "theme": "Spacecraft Power Management", "category": "Hardware", "description": "Develop an intelligent satellite power-management system that prioritizes loads to maintain essential operations.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Power Monitors": "INA226 Power Monitor ICs", "Load Switching": "IRF540N N-Channel MOSFETs", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 10A 120W SMPS", "Voltage Regulator": "LM2596S Buck Converter", "Discrete ICs": "LM358 Op-Amp & PC817 Opto", "Prototyping Base": "Breadboard & Terminals", "Passives & Wiring": "16AWG Wiring, Resistors"}},
    60: {"domain": "Aerial Systems", "theme": "Space Safety & Debris Collision", "category": "Software", "description": "Develop a system that tracks simulated space-debris trajectories and calculates collision risk and avoidance maneuvers.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Auth/Security": "RC522 RFID Module", "Power Supply": "5V 2A SMPS Adapter", "Display / UI": "0.96-inch I2C OLED", "Discrete ICs": "74HC595 Shift Register IC", "Prototyping Base": "400-Tie Point Breadboard", "Passives & Wiring": "Pushbuttons, LEDs, Jumpers"}},
    61: {"domain": "Cybersecurity & Digital Forensics Domain", "theme": "Wireless Network Security", "category": "Hardware", "description": "Develop a low-cost Wi-Fi security system that detects abnormal deauthentication activity and rogue access points.", "components": {"Microcontroller": "ESP32-WROOM-32U DevKit", "Power Supply": "5V 2A SMPS Adapter", "Display / UI": "0.96-inch I2C OLED", "Alert Module": "5V Active Piezo Buzzer", "Storage/Logging": "MicroSD Adapter + 16GB Card", "Discrete ICs": "AMS1117-3.3V LDO IC", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Connectors": "Resistors, Caps, LEDs, Jumpers"}},
    62: {"domain": "Cybersecurity & Digital Forensics Domain", "theme": "USB Security & Hardware-Based Cybersecurity", "category": "Hardware", "description": "Develop an inline USB security device that identifies malicious USB devices and prevents access.", "components": {"Microcontroller": "ESP32-S3-DevKitC-1", "USB Host Handler": "MAX3421E USB Host Controller", "Auth/Security": "RC522 RFID Module", "Power Supply": "5V 2A SMPS Adapter", "Hardware Protection": "TPD4E001 ESD Diode IC", "Display / UI": "0.96-inch OLED Display", "Alert Module": "5V Active Piezo Buzzer", "Prototyping Base": "Breadboard + Breakout Boards", "Passives & Wiring": "Data Resistors, Jumpers"}},
    63: {"domain": "Cybersecurity & Digital Forensics Domain", "theme": "Digital Forensics & Evidence Analysis", "category": "Software", "description": "Develop an automated forensic software tool that extracts file metadata and reconstructs activity timelines.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Timekeeping": "DS3231 RTC Module", "Data Logging": "MicroSD Adapter + 16GB Card", "Auth/Security": "RC522 RFID Module", "Power Supply": "5V 2A SMPS Adapter", "Display": "0.96-inch I2C OLED", "Discrete ICs": "74HC4050 Hex Buffer IC", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "Tactile Buttons, Jumpers"}},
    64: {"domain": "Cybersecurity & Digital Forensics Domain", "theme": "Forensic Evidence Protection", "category": "Hardware", "description": "Develop a hardware write-blocking device that prevents write operations to digital storage media during acquisition.", "components": {"Microcontroller": "ESP32-S3-DevKitC-1", "USB Interface": "MAX3421E USB Host Shield", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 3A SMPS Dual-Rail", "Voltage Regulator": "LM2596S Buck Converter", "Discrete ICs": "TPS2051 Power Switch IC", "Display / UI": "16x2 I2C LCD + Buzzer", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "Shunt Resistors, LEDs, Jumpers"}},
    65: {"domain": "Cybersecurity & Digital Forensics Domain", "theme": "Cyber Incident Response & Digital Evidence", "category": "Software", "description": "Develop a tamper-evident system that links security alerts with digital evidence and maintains an immutable chain-of-custody.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Auth/Security": "RC522 RFID + Tokens", "Crypto & Time": "DS3231 RTC + ATECC608A IC", "Power Supply": "5V 2A SMPS Adapter", "Display / UI": "0.96-inch I2C OLED", "Discrete ICs": "74HC595 Shift Register IC", "Prototyping Base": "400-Tie Point Breadboard", "Passives & Wiring": "Pushbuttons, LEDs, Jumpers"}},
    66: {"domain": "Cybersecurity & Digital Forensics Domain", "theme": "Secure Digital Forensics & Field Investigation", "category": "Hardware", "description": "Develop an access-controlled forensic acquisition system that protects digital storage from physical and digital modification.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Locking Actuator": "12V Solenoid Cabinet Lock", "Auth/Security": "RC522 RFID Module", "Tamper Sensors": "SW-420 Tamper Tilt Sensor", "Power Supply": "12V 3A SMPS Enclosed", "Voltage Regulator": "LM2596 Buck Converter", "Discrete ICs": "ULN2003 Driver & Diodes", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "Reed Switch, Jumpers"}},
    67: {"domain": "Smart Agriculture & AgriTech", "theme": "Water Management & Smart Irrigation", "category": "Hardware", "description": "Develop a smart irrigation system that monitors field conditions and controls water supply accordingly to prevent waste.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Soil Sensing": "Capacitive Soil Moisture V1.2", "Water Actuator": "12V DC Solenoid Water Valve", "Valve Driver": "1-Channel 5V Relay Module", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 5A 60W SMPS", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "1N4007 Silicon Diodes", "Prototyping Base": "Breadboard & Barrier Terminals", "Passives & Wiring": "Jumpers, LEDs, 18AWG Wire"}},
    68: {"domain": "Smart Agriculture & AgriTech", "theme": "Precision Agriculture - Crop Health Monitoring", "category": "Hardware", "description": "Develop a UAV-based system using imaging and Al to monitor crop health and identify affected areas.", "components": {"Microcontroller": "ESP32-S3-WROOM-1 DevKit", "Climate Sensing": "DHT22 Temp & Humidity", "Auth/Security": "RC522 RFID Module", "Data Storage": "MicroSD Module + 16GB Card", "Display / UI": "0.96-inch I2C OLED Screen", "Power Supply": "12V 3A SMPS Power Supply", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "AMS1117-3.3V LDO IC", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "Jumpers, Resistors, Caps"}},
    69: {"domain": "Smart Agriculture & AgriTech", "theme": "Precision Agriculture - Smart Fertilization", "category": "Hardware", "description": "Develop a variable-rate fertilizer spraying system that adjusts fertilizer application according to specific field requirements.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Nutrient Proxy": "Analog Optical Turbidity Sensor", "Dosing Actuator": "12V Peristaltic Pump", "Pump Driver": "L298N Dual Motor Driver", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 5A Industrial SMPS", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "PC817 Optocoupler IC", "Prototyping Base": "830-Tie Point Breadboard", "Passives & Wiring": "Silicone Tubing, Diodes, Jumpers"}},
    70: {"domain": "Smart Agriculture & AgriTech", "theme": "Energy Management & Predictive Maintenance", "category": "Hardware", "description": "Develop a system that monitors agricultural pump health to prevent faults due to overheating or overloading.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Current Sensing": "ACS712 30A Current Sensor", "Thermal Sensing": "DS18B20 Motor Temp Probe", "Vibration Sensing": "SW-420 Vibration Sensor", "Power Control": "1-Channel 30A Relay Module", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 5A Industrial SMPS", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "TIP122 Transistor IC", "Prototyping Base": "Breadboard & Terminal Blocks", "Passives & Wiring": "Jumpers, LEDs, AC Wire"}},
    71: {"domain": "Smart Agriculture & AgriTech", "theme": "Climate Resilience & Crop Protection", "category": "Hardware", "description": "Develop a system that predicts frost conditions and automatically activates crop-protection mechanisms.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Climate Sensing": "SHT31 Temp & Humidity", "Barometric Data": "BMP280 Barometric Sensor", "Actuator Control": "12V 2-Channel Relay Module", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 5A Enclosed SMPS", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "PC817 Optocoupler IC", "Prototyping Base": "Breadboard & Terminals", "Passives & Wiring": "Flyback Diodes, 18AWG Wire"}},
    72: {"domain": "Smart Agriculture & AgriTech", "theme": "Soil Health Monitoring (Edge Al)", "category": "Hardware", "description": "Develop an edge-Al system that analyzes soil parameters locally and provides soil-health information.", "components": {"Microcontroller": "ESP32-S3 DevKit", "PH Sensing": "Analog Soil pH Sensor", "Salinity/EC": "Analog Soil EC Probe", "Moisture Sensing": "Capacitive Soil Moisture", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 3A SMPS Power Supply", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "LM358 Dual Op-Amp IC", "Prototyping Base": "Breadboard & 0.96-inch OLED", "Passives & Wiring": "Jumpers, Trimpots, Caps"}},
    73: {"domain": "Smart Agriculture & AgriTech", "theme": "Aquaculture & Water Quality Management", "category": "Hardware", "description": "Develop an automated system that monitors water parameters and controls equipment to prevent sudden dangerous changes.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "PH Sensing": "Analog Industrial pH Sensor", "Thermal Sensing": "DS18B20 Water Temp Probe", "Quality Proxy": "Analog Optical Turbidity", "Actuator Relays": "4-Channel 5V Relay Module", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 10A 120W SMPS", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "PC817 Optocoupler ICs", "Prototyping Base": "Breadboard & Terminals", "Passives & Wiring": "Resistors, Waterproof Glands"}},
    74: {"domain": "Smart Agriculture & AgriTech", "theme": "Smart Greenhouse & Environmental Monitoring", "category": "Hardware", "description": "Develop an loT-based system for real-time monitoring and automated environmental control in a greenhouse.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Climate Sensing": "DHT22 Temp & Humidity", "Light Sensing": "BH1750 Ambient Light Sensor", "Soil Sensing": "Capacitive Soil Moisture", "Climate Actuators": "2-Channel 5V Relay Module", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 5A 60W SMPS", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "TIP122 Transistor IC", "Prototyping Base": "Breadboard & Terminal Blocks", "Passives & Wiring": "Diodes, Jumpers, LEDs"}},
    75: {"domain": "Smart Agriculture & AgriTech", "theme": "Post-Harvest Management & Energy Optimization", "category": "Hardware", "description": "Develop a smart drying system that monitors drying conditions and optimizes heater and fan operation.", "components": {"Microcontroller": "ESP32-WROOM-32 Dev Board", "Drying Sensors": "SHT31 Temp & Humidity Sensor", "Spoilage Sensor": "MQ-135 Air Quality Sensor", "Energy Monitor": "ACS712 20A Current Sensor", "Actuator Control": "2-Channel High-Power Relay", "Auth/Security": "RC522 RFID Module", "Power Supply": "12V 10A 120W SMPS", "Voltage Regulator": "LM2596 Buck Module", "Discrete ICs": "PC817 Optocoupler ICs", "Prototyping Base": "Breadboard & Terminals", "Passives & Wiring": "Silicone Wire, Snubber Caps"}}
}

# ---------------------------------------------------------
# 2. HELPER FUNCTIONS: WEBHOOK & UPI QR
# ---------------------------------------------------------
def append_to_sheet(data_row):
    """Sends data directly to the Google Sheet using a Web App URL."""
    try:
        # ---> PASTE YOUR DEPLOYED GOOGLE APPS SCRIPT URL HERE <---
        WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbxRdLwG1d2iuadfsicKzk12QSuPn7dHTtFi5_PFu3diEjQY0BRGTrxLojXcYoq6YhmiQQ/exec" 
        
        headers = {'Content-Type': 'application/json'}
        response = requests.post(WEBHOOK_URL, data=json.dumps(data_row), headers=headers)
        
        if response.status_code == 200:
            return True, "Success"
        else:
            return False, f"Server returned status: {response.status_code}"
    except Exception as e:
        return False, str(e)

import razorpay

def generate_url_qr(url):
    """Generates a QR code for a standard web URL (like a Razorpay link)."""
    qr = qrcode.QRCode(version=1, box_size=8, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# ---------------------------------------------------------
# 3. STATE MANAGEMENT INITIALIZATION
# ---------------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 1
if "team_data" not in st.session_state:
    st.session_state.team_data = {}
if "selected_ps_id" not in st.session_state:
    st.session_state.selected_ps_id = 1
if "final_components" not in st.session_state:
    st.session_state.final_components = {}
if "custom_mode" not in st.session_state:
    st.session_state.custom_mode = False
if "payment_verified" not in st.session_state:
    st.session_state.payment_verified = False

# ---------------------------------------------------------
# SCREEN 1: TEAM REGISTRATION DETAILS
# ---------------------------------------------------------
if st.session_state.step == 1:
    st.title("Step 1: Team Registration")
    st.write("Please enter details for all 5 team members. Only the Team Leader and one alternate member provide phone contacts.")
    
    with st.form("team_form"):
        st.subheader("Leader & Contact Details")
        leader_name = st.text_input("Team Leader Name (Member 1)*")
        leader_phone = st.text_input("Team Leader Contact Number (10 Digits)*")
        
        st.subheader("Member 2 (Alternate Contact)")
        m2_name = st.text_input("Member 2 Name*")
        m2_phone = st.text_input("Alternate Contact Number (10 Digits)*")
        
        st.subheader("Remaining Members (Names Only)")
        m3_name = st.text_input("Member 3 Name*")
        m4_name = st.text_input("Member 4 Name*")
        m5_name = st.text_input("Member 5 Name*")
        
        submitted = st.form_submit_button("Proceed to Problem Statements")
        
        if submitted:
            if not (leader_name and leader_phone and m2_name and m2_phone and m3_name and m4_name and m5_name):
                st.error("Please fill in all member names and required contact numbers.")
            elif len(leader_phone) < 10 or len(m2_phone) < 10:
                st.error("Please provide valid 10-digit contact numbers.")
            else:
                st.session_state.team_data = {
                    "leader_name": leader_name,
                    "leader_phone": leader_phone,
                    "m2_name": m2_name,
                    "m2_phone": m2_phone,
                    "m3_name": m3_name,
                    "m4_name": m4_name,
                    "m5_name": m5_name
                }
                st.session_state.step = 2
                st.rerun()

# ---------------------------------------------------------
# SCREEN 2: 75 PROBLEM STATEMENTS SELECTION
# ---------------------------------------------------------
elif st.session_state.step == 2:
    st.title("Step 2: Select a Problem Statement")
    
    ps_options = {ps_id: f"PS {ps_id}: {data['theme']} ({data['domain']})" 
                  for ps_id, data in PROBLEM_STATEMENTS.items()}
    
    selected_id = st.selectbox(
        "Browse and choose from the 75 problem statements:",
        options=list(ps_options.keys()),
        format_func=lambda x: ps_options[x]
    )
    
    if st.button("View Problem Statement Details"):
        st.session_state.selected_ps_id = selected_id
        st.session_state.step = 3
        st.rerun()

# ---------------------------------------------------------
# SCREEN 3: PROBLEM STATEMENT BREAKDOWN
# ---------------------------------------------------------
elif st.session_state.step == 3:
    ps_id = st.session_state.selected_ps_id
    ps_data = PROBLEM_STATEMENTS[ps_id]
    
    st.title(f"Problem Statement {ps_id}")
    st.markdown("---")
    st.markdown(f"**1. Domain:** {ps_data['domain']}")
    st.markdown(f"**2. Theme:** {ps_data['theme']}")
    st.markdown(f"**3. Category:** {ps_data['category']}")
    st.markdown(f"**4. Detailed Problem Statement:**\n> {ps_data['description']}")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Back"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("Component List", type="primary"):
            st.session_state.final_components = ps_data["components"].copy()
            st.session_state.custom_mode = False
            st.session_state.step = 4
            st.rerun()

# ---------------------------------------------------------
# SCREEN 4: COMPONENT LIST & CUSTOM REPLACEMENT
# ---------------------------------------------------------
elif st.session_state.step == 4:
    ps_id = st.session_state.selected_ps_id
    default_comps = PROBLEM_STATEMENTS[ps_id]["components"]
    
    st.title("Step 4: Component Allotment")
    st.write("Review the components provided by the college for this statement.")
    
    table_data = [{"Criteria / Category": cat, "College Provided Component": comp} 
                  for cat, comp in default_comps.items()]
    st.table(table_data)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Use College Provided Components"):
            st.session_state.final_components = default_comps.copy()
            st.session_state.step = 5
            st.rerun()
    with col2:
        if st.button("Customize Components"):
            st.session_state.custom_mode = True
            
    if st.session_state.custom_mode:
        st.markdown("---")
        st.subheader("Customize Your Hardware")
        st.write("Enter your component preferences below. Unchanged textboxes will keep the default college choice.")
        
        custom_inputs = {}
        with st.form("custom_comp_form"):
            for criteria, college_comp in default_comps.items():
                custom_inputs[criteria] = st.text_input(
                    label=f"Criteria: {criteria}",
                    value="",
                    placeholder=f"Default: {college_comp}"
                )
            
            submit_custom = st.form_submit_button("Confirm and Merge Components")
            if submit_custom:
                merged = {}
                for criteria, college_comp in default_comps.items():
                    user_val = custom_inputs[criteria].strip()
                    merged[criteria] = user_val if user_val else college_comp
                st.session_state.final_components = merged
                st.session_state.step = 5
                st.rerun()

# ---------------------------------------------------------
# SCREEN 5: FINAL CONFIRMATION & RAZORPAY GATEWAY
# ---------------------------------------------------------
elif st.session_state.step == 5:
    st.title("Step 5: Review & Registration Fee Payment")
    
    st.subheader("Final Hardware Component List")
    final_table = [{"Criteria": cat, "Final Selected Component": comp} 
                   for cat, comp in st.session_state.final_components.items()]
    st.table(final_table)
    
    st.markdown("---")
    st.subheader("Pay Registration Fee (₹350)")
    
    # ---> PASTE YOUR RAZORPAY API KEYS HERE <---
    RAZORPAY_KEY_ID = "YOUR_RAZORPAY_KEY_ID"
    RAZORPAY_KEY_SECRET = "YOUR_RAZORPAY_KEY_SECRET"
    
    rzp_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
    
    # Generate a unique Razorpay Payment Link ONLY ONCE per session
    if "rzp_link_id" not in st.session_state:
        with st.spinner("Generating secure payment gateway..."):
            try:
                txn_ref = f"REG_{int(time.time())}"
                link_data = {
                    "amount": 35000, # Razorpay calculates in paise (35000 paise = ₹350)
                    "currency": "INR",
                    "description": "Hackathon Registration Fee",
                    "reference_id": txn_ref,
                    "customer": {
                        "name": st.session_state.team_data["leader_name"],
                        "contact": st.session_state.team_data["leader_phone"]
                    },
                    "notes": {
                        "Problem_Statement": f"PS {st.session_state.selected_ps_id}"
                    }
                }
                # Call Razorpay to generate the link
                payment_link = rzp_client.payment_link.create(link_data)
                
                # Store link details in memory
                st.session_state.rzp_link_id = payment_link['id']
                st.session_state.rzp_link_url = payment_link['short_url']
                st.session_state.txn_ref = txn_ref
            except Exception as e:
                st.error(f"Razorpay API Error: {str(e)}")
    
    # Display the Payment Link and Verification UI
    if "rzp_link_url" in st.session_state:
        st.write("Scan the QR code below or click the button to pay securely via Razorpay.")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            # Show Razorpay link as a QR code
            qr_img = generate_url_qr(st.session_state.rzp_link_url)
            st.image(qr_img, caption=f"Ref: {st.session_state.txn_ref}", width=250)
            
            # Show as a clickable URL
            st.markdown(f"[**👉 Click Here to Pay Online**]({st.session_state.rzp_link_url})")
        
        with col2:
            st.info("After completing the payment on the Razorpay screen, click the verification button below.")
            
            # True API Verification
            if st.button("Verify Payment Status"):
                with st.spinner("Contacting Razorpay servers..."):
                    try:
                        # Fetch the exact, real-time status of this specific link from Razorpay
                        link_status = rzp_client.payment_link.fetch(st.session_state.rzp_link_id)
                        
                        if link_status['status'] == 'paid':
                            st.session_state.payment_verified = True
                            
                            # Log to Google Sheets
                            team = st.session_state.team_data
                            ps_data = PROBLEM_STATEMENTS[st.session_state.selected_ps_id]
                            comp_summary = "; ".join([f"{k}: {v}" for k, v in st.session_state.final_components.items()])
                            
                            row_data = [
                                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                st.session_state.txn_ref,
                                "₹350 - VERIFIED",
                                team["leader_name"],
                                team["leader_phone"],
                                team["m2_name"],
                                team["m2_phone"],
                                team["m3_name"],
                                team["m4_name"],
                                team["m5_name"],
                                f"PS {st.session_state.selected_ps_id}: {ps_data['theme']}",
                                ps_data["domain"],
                                comp_summary
                            ]
                            
                            success, msg = append_to_sheet(row_data)
                            if success:
                                st.success("Payment Verified! Registration complete.")
                                st.balloons()
                                time.sleep(3)
                                st.session_state.step = 6
                                st.rerun()
                            else:
                                st.error(f"Payment verified by Razorpay, but Google Sheets failed: {msg}")
                        else:
                            # Prevents bypassing: Rejects if status is 'created', 'expired', or 'cancelled'
                            st.error(f"Payment not complete. Current Razorpay status: {link_status['status'].upper()}")
                    except Exception as e:
                        st.error(f"Verification Error: {str(e)}")
# ---------------------------------------------------------
# SCREEN 6: SUCCESS SCREEN
# ---------------------------------------------------------
elif st.session_state.step == 6:
    st.title("Registration Confirmed!")
    st.success("Your team registration and component configuration have been recorded.")
    st.write("A confirmation record has been securely logged to the Google Sheet.")
    if st.button("Register Another Team"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()