# for_rinaszeg1.2

https://github.com/Hondanx/for_rinaszeg1.2.git

==============================================
   Verbesserter NAT-Übersetzer - README
==============================================

Autor: [HONDANX]
Version: 1.0
Datum: [5.4.2025]

Dieses Dokument enthält Installationsanweisungen, Konfigurationshinweise und Nutzungstipps für das Tool "Verbesserter NAT-Übersetzer".

----------------------------------------------------------
 I. ÜBERSICHT
----------------------------------------------------------
Dieses Tool bietet eine grafische Benutzeroberfläche (GUI), um private IPs sicher auf öffentliche IPs mittels NAT (Network Address Translation) abzubilden. Die Anwendung unterstützt Active Directory-Authentifizierung und protokolliert alle Aktivitäten zu Prüfzwecken. Sie können NAT-Regeln manuell konfigurieren, IP-Mapping-Listen importieren/exportieren und IP-Beziehungen visualisieren.

Kompatibel mit Windows- und Linux-Systemen.

----------------------------------------------------------
 II. VORAUSSETZUNGEN
----------------------------------------------------------
Bitte führen Sie zuerst das Setup-Skript aus, um die erforderlichen Abhängigkeiten zu installieren:
- Python 3.9 oder höher
- Erforderliche Python-Bibliotheken:
  - `tkinter`
  - `pandas`
  - `ldap3`
  - `matplotlib`
  - `openpyxl`
  - `smtplib` (eingebaut)
  - `email.mime` (eingebaut)

----------------------------------------------------------
 III. KONFIGURATION - UMGEBUNGSVARIABLEN
----------------------------------------------------------

Vor der Nutzung des Haupt-Skripts passen Sie bitte die folgenden Variablen an die Umgebung Ihrer Organisation an.

1. **Active Directory-Konfiguration:**
   AD_SERVER = "ldap://IHR_AD_SERVER"
   AD_DOMAIN = "ihredomäne.com"
   AD_SEARCH_BASE = "OU=IhreOU,DC=ihredomäne,DC=com"

2. **E-Mail-Benachrichtigungen:**
   SMTP_SERVER = "ihr.smtp.server"
   SMTP_PORT = 587
   SENDER_EMAIL = "nat_system@beispiel.com"
   SENDER_PASSWORD = "ihr_email_passwort"  # Verwenden Sie in der Produktion Umgebungsvariablen
   ADMIN_EMAIL = "admin@beispiel.com"

3. **README-Dateipfad:**
   README_PATH = "README.txt"
   ➤ Geben Sie den vollständigen Pfad an, falls sich die Datei nicht im gleichen Verzeichnis befindet.

----------------------------------------------------------
 IV. NUTZUNGSANLEITUNG
----------------------------------------------------------

1. **Authentifizierung:**
   - Geben Sie Ihren Domänen-Benutzernamen und Ihr Passwort ein.
   - Klicken Sie auf "Login", um sich über Active Directory zu authentifizieren.
   - Bei Erfolg werden NAT-Optionen und Schaltflächen aktiviert.

2. **Manuelle NAT-Konfiguration:**
   - Geben Sie pro Zeile eine private IP und eine öffentliche IP ein.
   - Klicken Sie auf "Configure NAT", um die Zuordnungen anzuwenden.
   - Unterstützte NAT-Befehle:
     - Linux: Nutzt `iptables` und speichert die Regel mit `iptables-save`
     - Windows: Nutzt `netsh interface portproxy`

3. **IPs importieren:**
   - Klicken Sie auf "Import IP List", um eine Datei zu laden.
   - Akzeptierte Formate:
     - `.xlsx`: Zwei Spalten — Private_IP, Public_IP
     - `.txt`: Zweispaltiges CSV ohne Kopfzeile

4. **Ergebnisse exportieren:**
   - Nach der Verarbeitung exportieren Sie die Zuordnungen nach Excel, indem Sie auf "Export Results" klicken.

5. **Visualisierung:**
   - Klicken Sie auf "Visualize Data", um IP-Zuordnungen grafisch anzuzeigen.
   - Ein neues Fenster zeigt eine Tabelle und ein Diagramm mit Verbindungen zwischen privaten/öffentlichen IP-Paaren.

6. **Hilfe-Schaltfläche:**
   - Öffnet dieses README in einem Texteditor als schnelle Referenz.

7. **Terminal starten (optional):**
   - Öffnen Sie CMD oder PowerShell (Windows) / Terminal (Linux) für schnellen Admin-Zugriff.

----------------------------------------------------------
 V. SICHERHEITSHINWEISE
----------------------------------------------------------
- Vermeiden Sie das Festlegen sensibler Passwörter im Skript.
- Verwenden Sie sichere Tresore oder Umgebungsvariablen (z. B. os.environ["SMTP_PASS"]).
- AD-Anmeldeinformationen werden nicht gespeichert – nur während der Sitzung verifiziert.

----------------------------------------------------------
 VI. FEHLERBEHEBUNG
----------------------------------------------------------
- Authentifizierung schlägt fehl: Stellen Sie sicher, dass AD-Anmeldeinformationen und Domäneninformationen korrekt sind.
- NAT-Befehle schlagen fehl:
  - Unter Linux: Vergewissern Sie sich, dass iptables installiert ist und das Skript mit sudo ausgeführt wird.
  - Unter Windows: Stellen Sie sicher, dass netsh-Zugriff erlaubt ist und nicht durch Firewall oder Richtlinien blockiert wird.
- Importfehler: Prüfen Sie, ob die Datei mindestens zwei Spalten und gültige IP-Formate enthält.

----------------------------------------------------------
 VII. PROTOKOLLIERUNG
----------------------------------------------------------
- Alle Benutzeraktionen, NAT-Änderungen und Fehler werden in nat_config.log protokolliert.
- Sie können dieses Protokoll zur Fehlerbehebung oder Aktivitätsprüfung einsehen.

----------------------------------------------------------
 VIII. BEISPIEL-DATEIFORMAT
----------------------------------------------------------

▶ Beispiel-Excel- (oder TXT-) Dateistruktur:

| Private_IP  | Public_IP     |
|-------------|---------------|
| 10.0.0.1    | 203.0.113.1   |
| 10.0.0.2    | 203.0.113.2   |

Jede Zeile muss eine gültige Zuordnung von interner zu externer IP enthalten.

----------------------------------------------------------
 IX. KONTAKT / SUPPORT
----------------------------------------------------------
Für Fehlerberichte oder Verbesserungsvorschläge kontaktieren Sie mich unter:
[mohanedesmailux@gmail.com]

----------------------------------------------------------
 X. LIZENZ
----------------------------------------------------------
Dieses Tool wird wie besehen für den internen Gebrauch bereitgestellt. Sie können es an die Richtlinien Ihrer Organisation anpassen.

----------------------------------------------------------
 ENDE DES README
----------------------------------------------------------