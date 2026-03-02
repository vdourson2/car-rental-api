# Étapes pour créer un projet Flask

1. **Créer le répertoire du projet**
   ```bash
   mkdir my_flask_app && cd my_flask_app
   ```
2. **Initialiser un environnement virtuel**
   ```bash
   python -m venv venv
   .\\venv\\Scripts\\activate   # PowerShell ou CMD
   ```
3. **Installer Flask**
   ```bash
   pip install Flask
   ```
4. **Créer le fichier `app.py`**
   ```python
   from flask import Flask
   app = Flask(__name__)

   @app.route('/')
   def home():
       return "Hello, Flask!"

   if __name__ == '__main__':
       app.run(debug=True)
   ```
5. **Lancer l'application**
   ```bash
   python app.py
   ```
   Ouvrez votre navigateur à l’adresse `http://127.0.0.1:5000/`.

---

### Script batch automatisé (optionnel)
Enregistrez le script suivant sous `create_flask_project.bat` et exécutez‑le avec le nom du projet :
```bat
@echo off
set "PROJECT_NAME=%1"
if "%PROJECT_NAME%"=="" set "PROJECT_NAME=my_flask_app"
mkdir "%PROJECT_NAME%"
cd "%PROJECT_NAME%"
python -m venv venv
call venv\Scripts\activate
pip install Flask > nul
> app.py echo from flask import Flask
>> app.py echo ^
>> app.py echo app = Flask(__name__)
>> app.py echo ^
>> app.py echo @app.route("/^")
>> app.py echo def home():
>> app.py echo ^    return "Hello, Flask!"
>> app.py echo ^
>> app.py echo if __name__ == "__main__":
>> app.py echo ^    app.run(debug=True)

echo Flask project "%PROJECT_NAME%" created.
```
Utilisation : `create_flask_project.bat mon_projet`
---
*Généré par Antigravity*
