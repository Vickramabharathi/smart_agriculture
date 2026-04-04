#!/usr/bin/env python3
import subprocess
import sys
import os

# Change to project directory
os.chdir(r'C:\Users\HP\OneDrive\Desktop\smart_agriculture')

# Upgrade Flask-SQLAlchemy
print("Installing Flask-SQLAlchemy 3.1.1...")
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Flask-SQLAlchemy==3.1.1', '--upgrade'])

print("\nStarting Flask app...")
subprocess.call([sys.executable, 'app.py'])
