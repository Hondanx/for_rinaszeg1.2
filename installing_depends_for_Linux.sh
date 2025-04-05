#!/bin/bash

echo "====================================================="
echo " Installing Prerequisites for NAT Script (Ubuntu/Debian)"
echo "====================================================="
echo

# Check for sudo/root privileges
if [ "$(id -u)" -ne 0 ]; then
    echo "This script requires sudo privileges to install packages."
    echo "Please run with sudo or as root."
    exit 1
fi

# Step 1: Update package list
echo "Updating package list..."
apt update -y

# Step 2: Install system-wide Python packages using APT
echo "Installing required system packages..."
apt install -y python3 python3-tk python3-ldap3 python3-pip iptables python3-pandas python3-matplotlib python3-openpyxl

# Step 3: Install any additional Python packages not available via apt
echo "Installing additional Python packages..."
pip3 install --upgrade pip setuptools

# Step 4: Enable IP Forwarding for NAT
echo "Enabling IP forwarding..."
sysctl -w net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward = 1" | tee -a /etc/sysctl.conf > /dev/null

# Step 5: Make sure iptables rules persist after reboot
echo "Setting up iptables persistence..."
apt install -y iptables-persistent
# Save current rules
echo "Saving current iptables rules..."
netfilter-persistent save

# Step 6: Verify Installations
echo "Verifying installations..."
python3 -c "import ldap3, tkinter, platform, pandas, matplotlib, smtplib; print('All modules installed successfully!')"

# Step 7: Make sure terminal emulator is available for the CMD/PowerShell equivalent buttons
echo "Checking for terminal emulator..."
if ! command -v x-terminal-emulator &> /dev/null; then
    echo "Installing terminal emulator..."
    apt install -y x-terminal-emulator
fi

echo
echo "====================================================="
echo " Prerequisites installation completed successfully!"
echo " You can now run the main script."
echo "====================================================="
echo