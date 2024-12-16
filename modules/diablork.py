import os
import subprocess
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION


def execute_diablork(domain):
    # Queries for Google Dorking
    queries = {
        "ADMIN": f"site:{domain} inurl:admin",
        "LOGIN": f"site:{domain} inurl:login | inurl:weblogin | inurl:webpanel | inurl:signin | intitle:login | intitle:signin | inurl:secure | inurl: user | inurl:auth",
        "PORTAL/PANEL": f"site:{domain} inurl:portal | inurl:webportal | inurl:panel | inurl:webpanel",
        "REMOTE": f"site:{domain} inurl:remote",
        "DASHBOARD": f"site:{domain} inurl:dashboard",
        "EXCHANGE": f"site:{domain} inurl:exchange",
        "FORGOT": f"site:{domain} inurl:Forgot",
        "TEST ENVIRONMENTS": f"site:{domain} inurl:test | inurl:env | inurl:dev | inurl:staging | inurl:sandbox | inurl:debug | inurl:temp | inurl:internal | inurl:demo",
        "API": f"site:{domain} inurl:api | site:*/rest | site:*/v1 | site:*/v2 | site:*/v3",
        "API DOCS": f"site:{domain} inurl:apidocs | inurl:api-docs | inurl:swagger | inurl:api-explorer",
        "REGISTER/SIGN UP": f"site:{domain} inurl:register | inurl:signup | inurl:sign-up",
        "SENSITIVE PARAMETERS": f"site:{domain} inurl:email= | inurl:phone= | inurl:password= | inurl:secret=",
        "XSS PRONE PARAMETERS": f"site:{domain} inurl:q= | inurl:s= | inurl:search= | inurl:query= | inurl:keyword= | inurl:lang= inurl:&",
        "OPEN REDIRECT PRONE PARAMETERS": f"site:{domain} inurl:url= | inurl:return= | inurl:next= | inurl:redirect= | inurl:redir= | inurl:ret= | inurl:r2= | inurl:page= inurl:http",
        "SQLI PRONE PARAMETERS": f"site:{domain} inurl:id= | inurl:pid= | inurl:category= | inurl:cat= | inurl:action= | inurl:sid= | inurl:dir= inurl:&",
        "SSRF PRONE PARAMETERS": f"site:{domain} inurl:http | inurl:url= | inurl:path= | inurl:dest= | inurl:html= | inurl:data= | inurl:domain=  | inurl:page= inurl:&",
        "LFI PRONE PARAMETERS": f"site:{domain} inurl:include | inurl:dir | inurl:detail= | inurl:file= | inurl:folder= | inurl:inc= | inurl:locate= | inurl:doc= | inurl:conf= inurl:&",
        "RCE PRONE PARAMETERS": f"site:{domain} inurl:cmd | inurl:exec= | inurl:query= | inurl:code= | inurl:do= | inurl:run= | inurl:read=  | inurl:ping= inurl:&",
        "FILE UPLOADS ENDPOINTS": f'site:{domain} "choose file" "upload file"',
        "JUICY EXTENSIONS": f"site:{domain} ext:log | ext:txt | ext:conf | ext:cnf | ext:ini | ext:env | ext:sh | ext:bak | ext:backup | ext:swp | ext:old | ext:~ | ext:git | ext:svn | ext:htpasswd | ext:htaccess | ext:json",
        "HIGH % INURL KEYWORDS": f"site:{domain} inurl:conf | inurl:env | inurl:cgi | inurl:bin | inurl:etc | inurl:root | inurl:sql | inurl:backup | inurl:admin | inurl:php",
        "PHPINFO()": f"site:{domain} ext:php intitle:phpinfo",
        "WORDPRESS SITES": f"site:{domain} inurl:wp-content | inurl:wp-includes",
        "DRUPAL SITES": f'site:{domain} intext:"Powered by" & intext:Drupal & inurl:user',
        "JOOMLA SITES": f"site:{domain} site:*/joomla/login",
        "APACHE SERVER STATUS EXPOSED": f"site:{domain} site:*/server-status apache",
        "SERVER ERRORS": f'site:{domain} inurl:"error" | intitle:"exception" | intitle:"failure" | intitle:"server at" | inurl:exception | "database error" | "SQL syntax" | "undefined index" | "unhandled exception" | "stack trace"',
        "DIRECTORY LISTING": f'site:{domain} intitle:"index of" "Parent Directory"',
        "GENERAL DOCUMENTS": f"site:{domain} ext:doc | ext:dot | ext:docm | ext:docx | ext:dotx | ext:xls | ext:xlsm | ext:xlsx | ext:csv | ext:xml | ext:ppt | ext:pptx",
        "PFD DOCUMENTS": f"site:{domain} ext:pdf",
        "SENSITIVE DOCUMENTS": f'site:{domain} ext:txt | ext:pdf | ext:xml | ext:xls | ext:xlsx | ext:ppt | ext:pptx | ext:doc | ext:docx intext:"confidential" | intext:"Not for Public Release" | intext:"internal use only" | intext:"do not distribute"',
        "JUICY EXTENSIONS": f"site:{domain} ext:log | ext:txt | ext:conf | ext:cnf | ext:cfg | ext:config | ext:ini | ext:env | ext:sh | ext:tmp | ext:temp | ext:~ | ext:git | ext:svn | ext:htpasswd | ext:htaccess | ext:json | ext:yml | ext:yaml",
        "WEB EXTENSIONS": f"site:{domain} ext:php | ext:asp | ext:aspx | ext:jsp | ext:axd | ext:py | ext:pl | | ext:js | ext:erb | ext:java | ext:cs",
        "CERTIFICADOS Y CLAVES": f"site:{domain} ext:pem | ext:crt | ext:cer | ext:key | ext:pfx | ext:p12 | ext:id_rsa | ext:pub | ext:sign",
        "INSTALL/SETUP FILES": f"site:{domain} inurl:readme | inurl:license | inurl:install | inurl:setup | inurl:config",
        "ARCHIVOS COMPRIMIDOS": f"site:{domain} ext:zip | ext:rar | ext:7z | ext:tar.gz | ext:gz | bz2",
        "BACKUP": f"site:{domain} inurl:backup | ext:bak | ext:backup | ext:bkf | ext:bkp | ext:swp | ext:old",
        "BBDD": f"site:{domain} ext:db | ext:sqlite | ext:sqlite3 | ext:sql | ext:mdb",
        ".GIT": f"site:{domain} inurl:.git | intitle:.git | ext:git",
        "GITHUB/GITLAB": f'"{domain}" site:github.com | site:gitlab.com | site:bitbucket.org',
        "CODE LEAKS": f'"{domain}" site:pastebin.com | site:jsfiddle.net | site:codebeautify.org | site:codepen.io'
    }

    filetypes = [
        "rtf", "dat",
        "html", "odt", "md", "ora", "reg",
        "bin", "crl", "crs", "der", "ovpn", "cgi", "rdp",
        "ods", "odp", "odg"
    ]

    index_checks = [
        "DCIM", "ftp", "backup", "mail", "password", "pub", ".git",
        "log", "src", "env", ".env", ".sql"
    ]

    # Generate HTML content
    html_content = """
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Diablork Results</title>
    <style>
        h1 { color: red; }
    </style>
</head>
<body>
    <h1>Diablork</h1>
    <h2>Google Dorking Results</h2>
    <h2>Basic Queries</h2>
    <ul>
"""
    for name, query in queries.items():
        html_content += f"        <li><a href='https://www.google.com/search?q={query}' target='_blank'>Checking {name}</a></li>\n"

    html_content += """
    </ul>
    <h2>Other Extra Filetype Searches</h2>
    <ul>
"""
    for filetype in filetypes:
        html_content += f"        <li><a href='https://www.google.com/search?q=site:{domain} filetype:{filetype}' target='_blank'>Checking {filetype.upper()}</a></li>\n"

    html_content += """
    </ul>
    <h2>Path Traversal Searches</h2>
    <ul>
"""
    for check in index_checks:
        html_content += f"        <li><a href='https://www.google.com/search?q=site:{domain} intitle:\"{check}\"' target='_blank'>Checking \"{check}\"</a></li>\n"

    html_content += """
    </ul>
</body>
</html>
"""

    RESULTS_FOLDERPATH = RESULTS_DIRECTORY+'/'+ domain +'/'
    dorks_file = RESULTS_FOLDERPATH + domain + '_dorks.html'

    # Save to HTML file
    with open(dorks_file, "w") as file:
        file.write(html_content)

    print("HTML file 'dorks_file' has been created.")
    subprocess.run(["firefox", dorks_file])


