import subprocess
import time
import threading
import sys
import os
import json

# Configuration defaults
config = {
    "shutdown_delay_seconds": 30,
    "check_interval_seconds": 2
}

CONFIG_FILE = "config.json"

# Load configuration from config.json if it exists or create it with defaults
def load_or_create_config():
    global config
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                file_config = json.load(f)
                config.update(file_config)
                print(f"[*] Loaded configuration: {config}")
        except json.JSONDecodeError:
            print("[!] Invalid JSON format in config.json. Using default values.")
    else:
        print("[!] config.json not found. Creating with default values.")
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
        print(f"[*] Created {CONFIG_FILE} with defaults: {config}")

# Function to install the required dependencies
def install_dependencies():
    try:
        print("[*] Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "screen_brightness_control"])
        print("[+] Dependencies installed successfully.")
    except subprocess.CalledProcessError:
        print("[-] Failed to install dependencies. Please install 'screen_brightness_control' manually.")
        sys.exit(1)

# Function to check if brightness can be read
def check_brightness_compatibility():
    try:
        import screen_brightness_control as sbc
        sbc.get_brightness()
        return True
    except Exception as e:
        print(f"[-] Error: {e} - Monitor might not be compatible with brightness control.")
        input("[!] Monitor not compatible. Press any key to exit...")
        sys.exit(1)

# Shutdown command
shutdown_command = "shutdown /s /f /t 0"
shutdown_timer = None
monitor_active = None

# Function to shut down the PC
def shutdown_pc():
    print("[!] Shutting down the system now...")
    subprocess.call(shutdown_command, shell=True)

# Function to cancel the shutdown
def cancel_shutdown():
    global shutdown_timer
    if shutdown_timer and shutdown_timer.is_alive():
        shutdown_timer.cancel()
        print("[+] Monitor turned back on. Shutdown canceled.")

# Function to check if monitor is off
def is_monitor_off():
    try:
        import screen_brightness_control as sbc
        brightness = sbc.get_brightness()
        print(f"Current Brightness: {brightness}")
        return False
    except Exception as e:
        print(f"Error: {e} - Monitor might be off.")
        return True

# Function to start shutdown timer
def start_shutdown_timer():
    global shutdown_timer
    print(f"[!] Monitor is off. Shutdown will occur in {config['shutdown_delay_seconds']} seconds.")
    shutdown_timer = threading.Timer(config['shutdown_delay_seconds'], shutdown_pc)
    shutdown_timer.start()

# Main function
def main():
    global monitor_active
    load_or_create_config()
    monitor_active = not is_monitor_off()
    print(f"Monitor is {'on' if monitor_active else 'off'}.")

    while True:
        time.sleep(config['check_interval_seconds'])
        monitor_status = is_monitor_off()

        if monitor_status and monitor_active:
            print("[!] Monitor is off, starting shutdown timer...")
            start_shutdown_timer()
            monitor_active = False
        elif not monitor_status and not monitor_active:
            print("[+] Monitor turned back on. Cancelling shutdown timer...")
            cancel_shutdown()
            monitor_active = True

if __name__ == "__main__":
    install_dependencies()
    if not check_brightness_compatibility():
        sys.exit(1)
    main()
