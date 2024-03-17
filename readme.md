# Verschu Anti Scraping

![screenshot](images/presentation.jpg)

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

## Roadmap
- [X] POC V1
- [ ] Changer le nom de la font en MD5 + Base64
- [ ] Modifier l'appel @font-face pour "data:application/font-woff;base64"
- [ ] Nom de classe CSS différent du nom de la font
- [ ] Convertir les polices TTF de base en WOFF
- [ ] Mélanger et encrypter le mapping des glyphs
- [ ] Fonction de conversion en phonétique pour les screenreaders
- [ ] Optimisation et tests de performances
- [ ] Faire le schéma d'encryption et le mettre en image principale du repo

## License

[Verschu License]