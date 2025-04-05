# Enhanced NAT Translator – Usage Guide

## What this Tool Does
This is a cross-platform Python application with a graphical interface that helps you manage and configure NAT (Network Address Translation) mappings. It supports Windows and Linux systems and uses Active Directory authentication.

## Input File Format (Excel/Text)
To import NAT mappings from a file, prepare an Excel or TXT file with two columns:
Private_IP Public_IP
10.0.0.1 203.0.113.1
10.0.0.2 203.0.113.2

Requirements:
- Column headers must be exactly "Private_IP" and "Public_IP"
- Each row represents a one-to-one NAT mapping
- Only valid IP addresses are accepted

## How the Script Works
1. Login with your Active Directory credentials (Username and Password)
2. Once authenticated, you can:
   - Manually enter NAT mappings
   - Import a list from Excel/TXT file
3. Choose to:
   - Configure NAT rules
   - Visualize IP mappings
   - Export results
   - Use CMD/PowerShell terminals directly

All activity logs are saved in `nat_config.log`.

##  GUI Button Descriptions
| Button          | Action                                                                 |
|-----------------|-----------------------------------------------------------------------|
| Login           | Authenticates using Active Directory (NTLM)                           |
| Logout          | Ends your session and disables all actions                           |
| Configure NAT   | Applies NAT rules based on provided IPs                              |
| Import IP List  | Imports a file (Excel/TXT) containing NAT pairs                      |
| Import Help     | Shows the correct format for input files                             |
| Export Results  | Saves processed NAT mappings into a new Excel file                   |
| Visualize Data  | Opens a window with tables/diagrams showing NAT mappings            |
| PowerShell      | Opens a PowerShell terminal in new window (Windows only)            |
| CMD             | Opens a CMD terminal in new window (Windows only)                   |
| Help            | Displays this instruction guide                                     |

##  Important Notes
### Windows Behavior:
- CMD and PowerShell buttons open in separate windows using `subprocess.Popen()`
- You cannot run both inside the same embedded shell window in the app

### Linux Behavior:
- Terminal buttons open the default terminal emulator (gnome-terminal, xterm, etc.)
- The script uses `iptables` for NAT configuration

##  Troubleshooting and Debugging Tips
### Authentication fails?
- Check username format (usually just account name, no domain)
- Verify password is correct
- Confirm AD server and domain settings in the script

### CMD/PowerShell buttons not working?
- Windows: Ensure system PATH includes cmd.exe and powershell.exe
- Linux: x-terminal-emulator must be installed and accessible

### Script not applying NAT rules?
- Run as Administrator (Windows) or with sudo (Linux)
- Confirm IP addresses are valid and reachable
- Check `nat_config.log` for details

### DNS/Network Errors?
- Verify system DNS configuration
- Test domain resolution using nslookup, dig, or ping

### Can't import Excel file?
- Verify "Private_IP" and "Public_IP" columns exist
- Check for blank rows or merged cells

##  Security Best Practices
- Never hardcode credentials
- Use environment variables or secrets managers for sensitive values
- Run with minimum required privileges
- Review logs regularly for suspicious activity

For additional support, contact your network administrator.