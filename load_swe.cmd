rem
rem Setup directory structure for app, and install requirements.
rem
c:
cd \apps\
rmdir /s /q .\stmts-wo-email
git clone https://github.com/jcarter62/stmts-wo-email.git
cd stmts-wo-email
python -m venv venv
.\venv\Scripts\pip.exe install -r requirements.txt
exit
