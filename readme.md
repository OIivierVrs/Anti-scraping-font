# ASF Anti Scraping Fonts 

![screenshot](images/presentation.jpg)

## Introduction

ASF is a new way to protect sensitive public data such as telephone numbers, email addresses, etc. This system uses fonts as an encryption key for your sensitive data, the data displayed on the screen is different of the data displayed in the source code, making data scraping considerably more difficult

## Installation

Create the .env file at the root of the project with these variables

```bash
ENCRYPT_KEY="" # Clé de 16 caractères alphanumériques
FONTS_FOLDER="" # Chemin absolu vers le dossier fonts
```

Install python dependencies

```bash
pip install -r requirements.txt
```

Generate encrypted fonts

```bash
python3 generate_fonts.py
```

Then we access the index.php in a browser and that's it!


## Downsides and areas for improvement

This method cannot be used on text that is intended to be indexed by search engines since the text read by robots is encrypted.
This method does not yet solve the problem of screen readers for visually impaired people. This problem can be solved with the integration of a phonetic conversion instead of the encryption method


## Roadmap
- [X] POC V1
- [ ] Change the font name to MD5 + Base64
- [ ] Use a CSS class name different from the font name
- [ ] Convert base TTF fonts to WOFF
- [ ] Shuffle and encrypt the glyph mapping
- [ ] Add a phonetic conversion function for screen readers
- [ ] Optimize and perform performance testing
- [ ] Create the encryption schema and set it as the main image of the repository

## License

AGPL v3