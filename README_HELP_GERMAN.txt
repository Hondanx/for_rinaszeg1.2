# Verbesserter NAT-Übersetzer – Benutzerhandbuch

## Was dieses Tool macht
Dies ist eine plattformübergreifende Python-Anwendung mit grafischer Benutzeroberfläche, die Ihnen hilft, NAT-Mappings (Network Address Translation) zu verwalten und zu konfigurieren. Sie unterstützt Windows- und Linux-Systeme und verwendet Active Directory-Authentifizierung.

## Eingabedateiformat (Excel/Text)
Um NAT-Mappings aus einer Datei zu importieren, erstellen Sie eine Excel- oder TXT-Datei mit zwei Spalten:
Private_IP Public_IP
10.0.0.1  203.0.113.1
10.0.0.2  203.0.113.2

Anforderungen:
- Die Spaltenüberschriften müssen genau "Private_IP" und "Public_IP" lauten
- Jede Zeile stellt ein 1:1-NAT-Mapping dar
- Es werden nur gültige IP-Adressen akzeptiert

## Wie das Skript funktioniert
1. Melden Sie sich mit Ihren Active Directory-Anmeldeinformationen (Benutzername und Passwort) an
2. Nach der Authentifizierung können Sie:
   - NAT-Mappings manuell eingeben
   - Eine Liste aus einer Excel-/TXT-Datei importieren
3. Wählen Sie aus:
   - NAT-Regeln konfigurieren
   - IP-Mappings visualisieren
   - Ergebnisse exportieren
   - CMD/PowerShell-Terminals direkt nutzen

Alle Aktivitätsprotokolle werden in `nat_config.log` gespeichert.

## Beschreibung der GUI-Schaltflächen
| Schaltfläche    | Aktion                                                              |
|-----------------|--------------------------------------------------------------------|
| Login           | Authentifiziert mit Active Directory (NTLM)                       |
| Logout          | Beendet Ihre Sitzung und deaktiviert alle Aktionen                |
| Configure NAT   | Wendet NAT-Regeln basierend auf den angegebenen IPs an            |
| Import IP List  | Importiert eine Datei (Excel/TXT) mit NAT-Paaren                  |
| Import Help     | Zeigt das korrekte Format für Eingabedateien an                   |
| Export Results  | Speichert verarbeitete NAT-Mappings in eine neue Excel-Datei      |
| Visualize Data  | Öffnet ein Fenster mit Tabellen/Diagrammen der NAT-Mappings       |
| PowerShell      | Öffnet ein PowerShell-Terminal in einem neuen Fenster (nur Windows) |
| CMD             | Öffnet ein CMD-Terminal in einem neuen Fenster (nur Windows)       |
| Help            | Zeigt diese Bedienungsanleitung an                                |

## Wichtige Hinweise
### Verhalten unter Windows:
- CMD- und PowerShell-Schaltflächen öffnen sich in separaten Fenstern mit `subprocess.Popen()`
- Sie können nicht beide in einem eingebetteten Shell-Fenster in der App ausführen

### Verhalten unter Linux:
- Terminal-Schaltflächen öffnen den Standard-Terminalemulator (gnome-terminal, xterm usw.)
- Das Skript verwendet `iptables` für die NAT-Konfiguration

## Tipps zur Fehlerbehebung und Debugging
### Authentifizierung schlägt fehl?
- Überprüfen Sie das Benutzername-Format (normalerweise nur Kontoname, kein Domänenname)
- Vergewissern Sie sich, dass das Passwort korrekt ist
- Überprüfen Sie die AD-Server- und Domäneneinstellungen im Skript

### CMD/PowerShell-Schaltflächen funktionieren nicht?
- Windows: Stellen Sie sicher, dass der System-PATH cmd.exe und powershell.exe enthält
- Linux: x-terminal-emulator muss installiert und zugänglich sein

### Skript wendet NAT-Regeln nicht an?
- Führen Sie es als Administrator (Windows) oder mit sudo (Linux) aus
- Stellen Sie sicher, dass die IP-Adressen gültig und erreichbar sind
- Überprüfen Sie `nat_config.log` für Details

### DNS/Netzwerkfehler?
- Überprüfen Sie die System-DNS-Konfiguration
- Testen Sie die Domänenauflösung mit nslookup, dig oder ping

### Excel-Datei kann nicht importiert werden?
- Vergewissern Sie sich, dass die Spalten "Private_IP" und "Public_IP" vorhanden sind
- Prüfen Sie auf leere Zeilen oder zusammengeführte Zellen

## Sicherheits-Best Practices
- Nie Anmeldeinformationen fest einprogrammieren
- Umgebungsvariablen oder Geheimnisverwalter für sensible Werte verwenden
- Mit minimal erforderlichen Berechtigungen ausführen
- Protokolle regelmäßig auf verdächtige Aktivitäten überprüfen

Für zusätzlichen Support wenden Sie sich an Ihren Netzwerkadministrator.