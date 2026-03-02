
* ✅ Génération du `requirements.txt`
* ✅ Installation depuis `requirements.txt`
* ✅ Structure projet propre
* ✅ Ajout `.gitignore`
* ✅ Bonnes pratiques formation

---

````markdown
# Étapes pour créer un projet Flask

## Prérequis

- **Installer Python 3.9+**  
  Téléchargez l'installateur depuis https://www.python.org/downloads/windows/ et assurez-vous de cocher **Add Python to PATH** pendant l'installation.

---

## 1. Créer le répertoire du projet

```bash
mkdir my_flask_app && cd my_flask_app
````

---

## 2. Initialiser un environnement virtuel

```bash
python -m venv venv
.\venv\Scripts\activate   # PowerShell ou CMD
```

---

## 3. Installer Flask (dans le venv activé)

```bash
pip install Flask
```

---

## 4. Créer le fichier `requirements.txt`

Après installation des dépendances, générer le fichier :

```bash
pip freeze > requirements.txt
```

Le fichier contiendra par exemple :

```txt
blinker==1.9.0
click==8.1.3
colorama==0.4.6
Flask==3.1.3
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
Werkzeug==3.1.3
```

Ce fichier permet de :

* Reproduire exactement l’environnement
* Partager le projet
* Garantir les mêmes versions

---

## 5. Créer le fichier `app.py`

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 6. Lancer l'application

```bash
python app.py
```

Ouvrez votre navigateur à l’adresse :

```
http://127.0.0.1:5000/
```

---

## 7. Réinstaller les dépendances plus tard

Si vous clonez le projet :

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

## 8. Ajouter un `.gitignore`

Créer un fichier `.gitignore` :

```txt
venv/
__pycache__/
*.pyc
.env
```

Cela évite de versionner l’environnement virtuel.

---

## Structure finale recommandée

```
my_flask_app/
│
├── venv/
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

### Script batch automatisé (optionnel)

Enregistrez le script suivant sous `create_flask_project.bat` et exécutez-le avec le nom du projet :

```bat
@echo off
set "PROJECT_NAME=%1"
if "%PROJECT_NAME%"=="" set "PROJECT_NAME=my_flask_app"
mkdir "%PROJECT_NAME%"
cd "%PROJECT_NAME%"
python -m venv venv
call venv\Scripts\activate
pip install Flask > nul
pip freeze > requirements.txt
> app.py echo from flask import Flask
>> app.py echo ^
>> app.py echo app = Flask(__name__)
>> app.py echo ^
>> app.py echo @app.route("/")
>> app.py echo def home():
>> app.py echo ^    return "Hello, Flask!"
>> app.py echo ^
>> app.py echo if __name__ == "__main__":
>> app.py echo ^    app.run(debug=True)

echo Flask project "%PROJECT_NAME%" created.
```

Utilisation :

```bash
create_flask_project.bat mon_projet
```

---

*Généré par Antigravity*

```

---

Si tu veux, je peux aussi te générer :

- 🔹 Version pédagogique commentée (pour formation)
- 🔹 Version “pro” avec structure modulaire
- 🔹 Version API REST avec Blueprints
- 🔹 Version avec SQLite + SQLAlchemy
- 🔹 Version dockerisée

On continue vers quoi ?
```
