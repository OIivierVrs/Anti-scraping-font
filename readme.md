# Verschu Anti Scraping

## Installation

Créer le fichier .env à la racine du projet avec ces variables

```bash
ENCRYPT_KEY="" # Clé de 16 caractères alphanumériques
FONTS_FOLDER="" # Chemin absolu vers le dossier fonts
```

Pour installer les dépendances python :

```bash
pip install -r requirements.txt
```

On génère ensuite les fonts encryptées

```bash
python3 generate_fonts.py
```
Puis on accède à l'index.php dans un navigateur et c'est tout!


## License

[Verschu License]