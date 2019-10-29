from flask import *
import os
from werkzeug.utils import secure_filename
from MyLibs import logger, db, configure, auth


app = Flask(__name__)# Initialisiert die Flask app

global path
path = "Default"
app.secret_key = configure.SESSION_KEY # Session key
ALLOWED_EXTENSIONS = set(configure.ALLOWED_EXTENSIONS)# Erlaubte Datei typen


def allowed_file(filename):# Checkt ob eine Datei vom typ erlaubt ist
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/login', methods=['POST', 'GET'])# Login seite
def login():
    global path
    if request.method == 'POST':# Falls das Passwort gesendet wird
        password = request.form['pass']# Passwort empfangen
        username = request.form['user']
        if username != "" and password != "":
            login = auth.login(username, password)
            if login != "Wrong":# Passwort prüfen
                path = login
                auth.create(session, username, password)# Login session erstellen#
                print(request.remote_addr + ' - - logged in')
                logger.log(request.remote_addr + ' - - logged in')
                return redirect('/')
            else:#Passwort Falsch
                login = False
                print(request.remote_addr + ' - - specified a wrong password : ' + password)
                logger.log(request.remote_addr + ' - - specified a wrong password : ' + password)
                return render_template('login.html', login="Falsche Anmeldedaten")# Erneut die Login Seite
                login = True
        else:
            return render_template('login.html', login="Ungültige Eingabe")
    elif request.method == 'GET':
        return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])# Registrierungsseite seite
def register():

    global path
    if request.method == 'POST':
        password = request.form['pass']# Passwort empfangen
        username = request.form['user']
        if password != "" and username != "":
            if db.check_valid(username):
                
                db.insert(username, password, username)
                os.mkdir(username)
                path = username
                auth.create(session,username, password)
                print(request.remote_addr + ' - - registred as : ' + username)
                logger.log(request.remote_addr + ' - - registred as : ' + username)
                return redirect('/')
            else:
                return render_template('register.html', register="Benutzername bereits vergeben")
        else:
            return render_template('register.html', register="Ungültige Eingabe")
            
    if request.method == 'GET' :
        return render_template('register.html')

@app.route('/', methods=['POST', 'GET'])# Haubtmenü
def list_files():
    if auth.check(session) and path != "Default":
        if request.method == 'POST':# Logout
            session.pop('logged_in', None)# Login Session löschen
            return redirect('/login')
        elif request.method == 'GET':
            file_list = os.listdir(path)
            print(file_list)
            return render_template('index.html',files = file_list)# index.html mit liste der hochgeladenen Dateien zurückgeben
    else:
        return redirect('/login')

@app.route('/upload', methods=['POST', 'GET'])# Upload
def upload_file():
    if auth.check(session):
        if request.method == 'POST':
            if 'file' not in request.files:# Checken ob eine Datei gesendet wurde
                flash('Keine Datei gesendet')
                return redirect(request.url)
            file = request.files['file']# Datei empfangen
            if file.filename == '':# Dateiname checken
                flash('Keine Datei ausgwählt')
                return redirect(request.url)
            if file and allowed_file(file.filename):# Checken ob diese Datei erlaubt ist
                filename = secure_filename(file.filename)
                file.save(os.path.join(path , filename))# Datei in UPLOAD_FOLDER speichern
                logger.log(request.remote_addr + ' - - uploadet ' + filename)
                return redirect('/')
        elif request.method == 'GET':
            return render_template('upload.html')
    else:
        return redirect('/login')

@app.route('/upload/<filename>', methods=['GET'])# Datei anzeigen / runterladen
def uploaded_file(filename):
    if auth.check(session): # Login Session prüfen
        logger.log(request.remote_addr +  ' - - viewed ' + filename)
        return send_from_directory(path, filename)# Datei zurückgeben
    else: return redirect('/login')

@app.route('/delete', methods=['POST', 'GET'])# Dateien löschen
def delete_file():
    if auth.check(session):# Login Session prüfen
        if request.method == 'POST':
            filename = request.form['file']# Zu löschenden Dateinamen erhalten
            os.remove(os.path.join(path , filename))# Datei aus UPLOAD_FOLDER löschen
            logger.log(request.remote_addr + ' - - deleted ' + filename)
            return redirect('/')
        elif request.method == 'GET':
            return render_template('delete.html', files = os.listdir(path))
    else:
        return redirect('/login')

@app.errorhandler(404) 
def not_found(e):
    return render_template("error/404.html")

@app.errorhandler(500) 
def internal_error(e):
    return render_template("error/500.html") 
# App starten
if __name__ == "__main__":
    app.run(
        debug = configure.debug, # Wird nicht gedebugt
        host = configure.host,# Host setzen
        threaded = configure.threaded,# Multithreading erlaubt mehrere Clients gleichzeitig
        port = configure.port # Port setzen
        )
