import os
import sys
import platform
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from ldap3 import Server, Connection, ALL, NTLM
import re
import logging
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure Logging
logging.basicConfig(filename="nat_config.log", level=logging.INFO, 
                   format="%(asctime)s - %(levelname)s - %(message)s")

# Active Directory Configuration
AD_SERVER = "ldap://SERVER_NAME"
AD_DOMAIN = "company.com"
AD_SEARCH_BASE = "OU=Location-OD_COMPMGR,DC=company,DC=com"

# Path to README file - YOU NEED TO SET THIS PATH TO WHERE YOUR README FILE IS LOCATED
README_PATH = "README.txt"  # Change this to your actual README file path

# Email Configuration
SMTP_SERVER = "your.smtp.server"
SMTP_PORT = 587
SENDER_EMAIL = "nat_system@example.com"
SENDER_PASSWORD = "your_password"  # Consider using environment variables for security
ADMIN_EMAIL = "admin@example.com"

# Function to validate IP address
def is_valid_ip(ip):
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    return re.match(pattern, ip) is not None

# Function to authenticate user
def authenticate(username, password):
    if not username or not password:
        messagebox.showerror("Error", "Username and password are required!")
        return None
        
    user_dn = f"{AD_DOMAIN}\\{username}"
    server = Server(AD_SERVER, get_info=ALL)
    try:
        conn = Connection(server, user=user_dn, password=password, authentication=NTLM, auto_bind=True)
        logging.info(f"User {username} authenticated successfully.")
        messagebox.showinfo("Success", "Authentication successful!")
        return conn  # Return connection for AD queries
    except Exception as e:
        logging.error(f"AD Authentication failed for {username}: {e}")
        messagebox.showerror("Error", f"Authentication failed: {e}")
        return None

# Function to notify admin via email
def notify_admin(subject, message):
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = ADMIN_EMAIL
        msg['Subject'] = subject
        
        # Add body
        msg.attach(MIMEText(message, 'plain'))
        
        # Connect and send
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        logging.info(f"Admin notification sent to {ADMIN_EMAIL}")
        return True
    except Exception as e:
        logging.error(f"Failed to send admin notification: {e}")
        return False

# Function to search for asset info in AD
def get_asset_info(conn, username):
    # List of possible locations
    locations = ["Location1-OD_COMPMGR", "Location2-OD_COMPMGR", "Location3-OD_COMPMGR"]
    
    for location in locations:
        search_base = f"OU={location},DC=self,DC=local"
        conn.search(search_base, f"(sAMAccountName={username})", attributes=['cn', 'location'])
        if conn.entries:
            return conn.entries[0]['cn'], conn.entries[0]['location']
    
    return "Unknown", "Unknown"

# Function to configure NAT
def configure_nat(private_ip, public_ip):
    if not is_valid_ip(private_ip) or not is_valid_ip(public_ip):
        messagebox.showerror("Error", "Invalid IP address format!")
        return False
    
    os_type = platform.system()
    try:
        if os_type == "Linux":
            subprocess.run(["sudo", "iptables", "-t", "nat", "-A", "PREROUTING", 
                          "-d", public_ip, "-j", "DNAT", "--to-destination", private_ip], check=True)
            subprocess.run(["sudo", "iptables", "-t", "nat", "-A", "POSTROUTING", 
                          "-s", private_ip, "-j", "SNAT", "--to-source", public_ip], check=True)
            subprocess.run(["sudo", "iptables-save"], check=True)
        elif os_type == "Windows":
            subprocess.run(["netsh", "interface", "portproxy", "add", "v4tov4", 
                          "listenaddress=" + public_ip, "connectaddress=" + private_ip], check=True)
        
        # Notify admin
        username = username_entry.get()
        notify_admin("NAT Configuration Alert", 
                    f"NAT configured by {username}: {private_ip} <-> {public_ip}")
        
        logging.info(f"NAT configured: {private_ip} <-> {public_ip}")
        messagebox.showinfo("Success", f"NAT configured successfully!\n{private_ip} <-> {public_ip}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to configure NAT: {e}")
        messagebox.showerror("Error", f"Failed to configure NAT: {e}")
        return False

# Function to import IP list
def import_ip_list():
    global df
    
    if not check_auth():
        return None
        
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("Text files", "*.txt")])
    if not file_path:
        return None
        
    try:
        if file_path.endswith(".xlsx"):
            # Try to read with expected column names
            try:
                df = pd.read_excel(file_path)
                # Verify columns exist
                if not all(col in df.columns for col in ['Private_IP', 'Public_IP']):
                    # Try first two columns if names don't match
                    if len(df.columns) >= 2:
                        df = pd.read_excel(file_path, header=0, names=['Private_IP', 'Public_IP'], usecols=[0,1])
                    else:
                        raise ValueError("Excel file must have at least two columns")
            except Exception:
                # If that fails, try without headers
                df = pd.read_excel(file_path, header=None, names=['Private_IP', 'Public_IP'])
                
        elif file_path.endswith(".txt"):
            df = pd.read_csv(file_path, header=None, names=['Private_IP', 'Public_IP'])
        else:
            messagebox.showerror("Error", "Unsupported file format")
            return None
            
        # Validate IPs
        invalid_ips = []
        for idx, row in df.iterrows():
            if not is_valid_ip(str(row['Private_IP'])) or not is_valid_ip(str(row['Public_IP'])):
                invalid_ips.append(f"Row {idx+1}: {row['Private_IP']} - {row['Public_IP']}")
        
        if invalid_ips:
            messagebox.showwarning("Warning", f"Found {len(invalid_ips)} invalid IP entries.\nFirst few: {invalid_ips[:5]}")
        
        # Update the text fields with imported IPs
        private_ip_entry.delete("1.0", tk.END)
        private_ip_entry.insert("1.0", "\n".join(df['Private_IP'].astype(str).tolist()))
        
        public_ip_entry.delete("1.0", tk.END)
        public_ip_entry.insert("1.0", "\n".join(df['Public_IP'].astype(str).tolist()))
            
        messagebox.showinfo("Success", f"Successfully imported {len(df)} entries!")
        return df
    except Exception as e:
        messagebox.showerror("Error", f"Failed to import file: {e}\n\nExpected format is an Excel file with columns 'Private_IP' and 'Public_IP'")
        return None

# Function to show import help
def show_import_help():
    messagebox.showinfo("Import Format Help", 
                       "Expected Excel Format:\n\n"
                       "Column 1: 'Private_IP' - The internal IP addresses\n"
                       "Column 2: 'Public_IP' - The corresponding external IP addresses\n\n"
                       "Each row should contain one mapping pair.\n"
                       "Example:\n"
                       "Private_IP | Public_IP\n"
                       "10.0.0.1  | 203.0.113.1\n"
                       "10.0.0.2  | 203.0.113.2")

# Function to export results
def export_results(data):
    if not check_auth():
        return
        
    if data is None or data.empty:
        messagebox.showerror("Error", "No data to export!")
        return
        
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", 
                                           filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        try:
            data.to_excel(file_path, index=False)
            messagebox.showinfo("Success", "Results exported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {e}")

# Function to display visualization
def visualize_data(data):
    if not check_auth():
        return
        
    if data is None or data.empty:
        messagebox.showerror("Error", "No data to visualize!")
        return
    
    # Create a figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # First subplot: Table view of mappings
    ax1.axis('tight')
    ax1.axis('off')
    table = ax1.table(cellText=data.values, 
                     colLabels=data.columns,
                     cellLoc='center', 
                     loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.2)
    ax1.set_title("NAT Mapping Table")
    
    # Second subplot: Network diagram
    ax2.scatter(range(len(data)), [1]*len(data), s=100, marker='o', color='blue', label='Private IPs')
    ax2.scatter(range(len(data)), [2]*len(data), s=100, marker='o', color='red', label='Public IPs')
    
    # Draw lines connecting private to public IPs
    for i in range(len(data)):
        ax2.plot([i, i], [1, 2], 'k-')
    
    # Set y-axis labels and remove ticks
    ax2.set_yticks([1, 2])
    ax2.set_yticklabels(['Private', 'Public'])
    ax2.set_xticks(range(len(data)))
    ax2.set_xticklabels(data.index, rotation=45)
    ax2.set_title("NAT Mapping Visualization")
    ax2.legend()
    
    plt.tight_layout()
    
    # Create a new window for the plot
    plot_window = tk.Toplevel(root)
    plot_window.title("NAT Mappings Visualization")
    
    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Function to handle manual NAT configuration
def manual_configure():
    if not check_auth():
        return
        
    private_ips = private_ip_entry.get("1.0", tk.END).strip().split('\n')
    public_ips = public_ip_entry.get("1.0", tk.END).strip().split('\n')
    
    # Remove empty lines
    private_ips = [ip for ip in private_ips if ip]
    public_ips = [ip for ip in public_ips if ip]
    
    if not private_ips or not public_ips:
        messagebox.showerror("Error", "Please enter at least one private and one public IP!")
        return
        
    if len(private_ips) != len(public_ips):
        messagebox.showerror("Error", "Number of private and public IPs must match!")
        return
        
    for private_ip, public_ip in zip(private_ips, public_ips):
        if not is_valid_ip(private_ip) or not is_valid_ip(public_ip):
            messagebox.showerror("Error", f"Invalid IP format:\nPrivate: {private_ip}\nPublic: {public_ip}")
            return
            
    success_count = 0
    for private_ip, public_ip in zip(private_ips, public_ips):
        if configure_nat(private_ip, public_ip):
            success_count += 1
            
    messagebox.showinfo("Summary", f"Successfully configured {success_count}/{len(private_ips)} NAT mappings!")

# Check if user is authenticated
def check_auth():
    if not hasattr(root, 'authenticated') or not root.authenticated:
        messagebox.showerror("Error", "Please authenticate first!")
        return False
    return True

# Login function
def login():
    username = username_entry.get()
    password = password_entry.get()
    
    conn = authenticate(username, password)
    if conn:
        root.authenticated = True
        login_button.config(state=tk.DISABLED)
        logout_button.config(state=tk.NORMAL)
        enable_function_buttons(True)

# Logout function
def logout():
    root.authenticated = False
    login_button.config(state=tk.NORMAL)
    logout_button.config(state=tk.DISABLED)
    enable_function_buttons(False)
    messagebox.showinfo("Info", "You have been logged out.")

# Enable/disable function buttons based on auth status
def enable_function_buttons(enabled):
    state = tk.NORMAL if enabled else tk.DISABLED
    import_button.config(state=state)
    export_button.config(state=state)
    visualize_button.config(state=state)
    manual_config_button.config(state=state)
    powershell_button.config(state=state)
    cmd_button.config(state=state)
    help_button.config(state=state)
    import_help_button.config(state=state)

# GUI Setup
root = tk.Tk()
root.title("Enhanced NAT Translator")
root.geometry("800x600")
root.configure(bg="#f0f0f0")

# Set initial auth state
root.authenticated = False

# Style configuration
style = ttk.Style()
style.configure("TFrame", background="#f0f0f0")
style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
style.configure("TButton", font=("Arial", 10), padding=5)
style.configure("Header.TLabel", font=("Arial", 12, "bold"))

# Main frames
header_frame = ttk.Frame(root, padding="10")
header_frame.pack(fill=tk.X)

auth_frame = ttk.Frame(root, padding="10")
auth_frame.pack(fill=tk.X, pady=5)

ip_entry_frame = ttk.Frame(root, padding="10")
ip_entry_frame.pack(fill=tk.BOTH, expand=True)

button_frame = ttk.Frame(root, padding="10")
button_frame.pack(fill=tk.X, pady=5)

# Header
ttk.Label(header_frame, text="Enhanced NAT Translator", style="Header.TLabel").pack()

# Authentication section
ttk.Label(auth_frame, text="Username:").grid(row=0, column=0, sticky=tk.W)
username_entry = ttk.Entry(auth_frame)
username_entry.grid(row=0, column=1, padx=5, pady=2)

ttk.Label(auth_frame, text="Password:").grid(row=1, column=0, sticky=tk.W)
password_entry = ttk.Entry(auth_frame, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=2)

login_button = ttk.Button(auth_frame, text="Login", command=login)
login_button.grid(row=0, column=2, rowspan=2, padx=5, sticky=tk.NSEW)

logout_button = ttk.Button(auth_frame, text="Logout", command=logout, state=tk.DISABLED)
logout_button.grid(row=0, column=3, rowspan=2, padx=5, sticky=tk.NSEW)

# IP Entry section
ip_entry_frame.columnconfigure(0, weight=1)
ip_entry_frame.columnconfigure(1, weight=1)
ip_entry_frame.rowconfigure(1, weight=1)

ttk.Label(ip_entry_frame, text="Private IP(s) (one per line):").grid(row=0, column=0, sticky=tk.W)
private_ip_entry = tk.Text(ip_entry_frame, height=10, width=30, wrap=tk.NONE)
private_ip_entry.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)

ttk.Label(ip_entry_frame, text="Public IP(s) (one per line):").grid(row=0, column=1, sticky=tk.W)
public_ip_entry = tk.Text(ip_entry_frame, height=10, width=30, wrap=tk.NONE)
public_ip_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)

# Add scrollbars
private_scroll_y = ttk.Scrollbar(ip_entry_frame, orient=tk.VERTICAL, command=private_ip_entry.yview)
private_scroll_y.grid(row=1, column=0, sticky=tk.NE+tk.SE)
private_ip_entry['yscrollcommand'] = private_scroll_y.set

private_scroll_x = ttk.Scrollbar(ip_entry_frame, orient=tk.HORIZONTAL, command=private_ip_entry.xview)
private_scroll_x.grid(row=2, column=0, sticky=tk.EW)
private_ip_entry['xscrollcommand'] = private_scroll_x.set

public_scroll_y = ttk.Scrollbar(ip_entry_frame, orient=tk.VERTICAL, command=public_ip_entry.yview)
public_scroll_y.grid(row=1, column=1, sticky=tk.NE+tk.SE)
public_ip_entry['yscrollcommand'] = public_scroll_y.set

public_scroll_x = ttk.Scrollbar(ip_entry_frame, orient=tk.HORIZONTAL, command=public_ip_entry.xview)
public_scroll_x.grid(row=2, column=1, sticky=tk.EW)
public_ip_entry['xscrollcommand'] = public_scroll_x.set

# Buttons
manual_config_button = ttk.Button(button_frame, text="Configure NAT", command=manual_configure, state=tk.DISABLED)
manual_config_button.pack(side=tk.LEFT, padx=5)

import_button = ttk.Button(button_frame, text="Import IP List", command=import_ip_list, state=tk.DISABLED)
import_button.pack(side=tk.LEFT, padx=5)

import_help_button = ttk.Button(button_frame, text="Import Help", command=show_import_help, state=tk.DISABLED)
import_help_button.pack(side=tk.LEFT, padx=5)

export_button = ttk.Button(button_frame, text="Export Results", command=lambda: export_results(df), state=tk.DISABLED)
export_button.pack(side=tk.LEFT, padx=5)

visualize_button = ttk.Button(button_frame, text="Visualize Data", command=lambda: visualize_data(df), state=tk.DISABLED)
visualize_button.pack(side=tk.LEFT, padx=5)

# Use Popen to open in new window without blocking main app
powershell_button = ttk.Button(button_frame, text="PowerShell", 
                             command=lambda: subprocess.Popen("powershell" if platform.system() == "Windows" else "x-terminal-emulator"), 
                             state=tk.DISABLED)
powershell_button.pack(side=tk.LEFT, padx=5)

cmd_button = ttk.Button(button_frame, text="CMD", 
                       command=lambda: subprocess.Popen("cmd" if platform.system() == "Windows" else "x-terminal-emulator"), 
                       state=tk.DISABLED)
cmd_button.pack(side=tk.LEFT, padx=5)

help_button = ttk.Button(button_frame, text="Help", 
                        command=lambda: subprocess.Popen(["notepad", README_PATH] if platform.system() == "Windows" else ["gedit", README_PATH]), 
                        state=tk.DISABLED)
help_button.pack(side=tk.LEFT, padx=5)

# Initialize empty DataFrame for IP mappings
df = pd.DataFrame(columns=['Private_IP', 'Public_IP'])

# Start the application
root.mainloop()
