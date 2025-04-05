# for_rinaszeg1.2

https://github.com/Hondanx/for_rinaszeg1.2.git

==============================================
   Enhanced NAT Translator - README
==============================================


Author: [HONDANX]
Version: 1.0
Date: [5/4/2025]

This document provides setup instructions, configuration guidance, and usage tips for the "Enhanced NAT Translator" tool.

----------------------------------------------------------
 I. OVERVIEW
----------------------------------------------------------
This tool provides a graphical interface (GUI) to securely map Private IPs to Public IPs using NAT (Network Translation). The application supports Active Directory authentication and logs all activities for auditing purposes. You can manually configure NAT rules, import/export IP mapping lists, and visualize IP relationships.

Compatible with both Windows and Linux systems.

----------------------------------------------------------
 II. PREREQUISITES
----------------------------------------------------------
Please run the setup script first to install required dependencies:
- Python 3.9 or later
- Required Python libraries:
  - `tkinter`
  - `pandas`
  - `ldap3`
  - `matplotlib`
  - `openpyxl`
  - `smtplib` (built-in)
  - `email.mime` (built-in)

----------------------------------------------------------
 III. CONFIGURATION - ENVIRONMENT VARIABLES
----------------------------------------------------------

Before using the main script, please **edit the following variables** to match your organization's environment.

1. **Active Directory Configuration:**
   AD_SERVER = "ldap://YOUR_AD_SERVER"
   AD_DOMAIN = "yourdomain.com"
   AD_SEARCH_BASE = "OU=YourOU,DC=yourdomain,DC=com"

2. **Email Notifications:**
   SMTP_SERVER = "your.smtp.server"
   SMTP_PORT = 587
   SENDER_EMAIL = "nat_system@example.com"
   SENDER_PASSWORD = "your_email_password"  # Use env vars in production
   ADMIN_EMAIL = "admin@example.com"

3. **README File Location:**
   README_PATH = "README.txt"
   ➤ Set the full path if it’s not in the same directory.

----------------------------------------------------------
 IV. USAGE GUIDE
----------------------------------------------------------

1. **Authentication:**
   - Enter your domain username and password.
   - Click “Login” to authenticate via Active Directory.
   - Upon success, NAT options and buttons are enabled.

2. **Manual NAT Configuration:**
   - Enter one Private IP and one Public IP per line.
   - Click “Configure NAT” to apply mappings.
   - Supported NAT commands:
     - Linux: Uses `iptables` and saves the rule with `iptables-save`
     - Windows: Uses `netsh interface portproxy`

3. **Importing IPs:**
   - Click “Import IP List” to load a file.
   - Accepted formats:
     - `.xlsx`: Two columns — Private_IP, Public_IP
     - `.txt`: Two-column CSV without header

4. **Exporting Results:**
   - After processing, export mappings to Excel by clicking “Export Results”.

5. **Visualization:**
   - Click “Visualize Data” to display IP mappings graphically.
   - A new window will show a table and a graph connecting private/public IP pairs.

6. **Help Button:**
   - Opens this README in a text editor for quick reference.

7. **Launch Terminal (Optional):**
   - Open CMD or PowerShell (Windows) / Terminal (Linux) for quick admin access.

----------------------------------------------------------
 V. SECURITY NOTES
----------------------------------------------------------
- Avoid hardcoding sensitive passwords in the script.
- Use secure vaults or environment variables (e.g., os.environ["SMTP_PASS"]).
- AD credentials are not stored—only verified in-session.

----------------------------------------------------------
 VI. TROUBLESHOOTING
----------------------------------------------------------
- Authentication fails: Ensure AD credentials and domain info are correct.
- NAT commands fail:
  - On Linux: Confirm iptables is installed and the script is run with sudo.
  - On Windows: Ensure netsh access is permitted and not blocked by firewall or policy.
- Import errors: Make sure the file has at least two columns and valid IP formats.

----------------------------------------------------------
 VII. LOGGING
----------------------------------------------------------
- All user actions, NAT changes, and errors are logged to nat_config.log.
- You can view this log for troubleshooting or auditing activity.

----------------------------------------------------------
 VIII. SAMPLE FILE FORMAT
----------------------------------------------------------

▶ Sample Excel (or TXT) file layout:

| Private_IP  | Public_IP     |
|-------------|---------------|
| 10.0.0.1    | 203.0.113.1   |
| 10.0.0.2    | 203.0.113.2   |

Each row must have one valid internal-to-external IP mapping.

----------------------------------------------------------
 IX. CONTACT / SUPPORT
----------------------------------------------------------
For bugs or enhancement requests, contact Me on:
[mohanedesmailux@gmail.com]

----------------------------------------------------------
 X. LICENSE
----------------------------------------------------------
This tool is provided as-is for internal use. You may modify it to suit your organization’s policies.

----------------------------------------------------------
 END OF README
----------------------------------------------------------
