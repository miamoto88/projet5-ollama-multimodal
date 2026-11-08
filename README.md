# Projet 5 — Assistant Multimodal Local avec Ollama

Guide complet, étape par étape, pour réaliser ce projet sur votre PC (Windows, Mac ou Linux).

## Note sur le modèle
L'énoncé mentionne "Gemma 4", qui n'existe pas sur Ollama à ce jour. Utilisez à la place un
modèle multimodal réellement disponible :
- **`gemma3:4b`** (recommandé — léger, ~3 Go, bonne qualité) — probablement ce que l'énoncé visait
- `llava` (alternative classique, bien documentée)
- `llama3.2-vision` (plus lourd, meilleure précision)
- `moondream` (très léger, pour PC modestes)

Vous pouvez mentionner ce choix dans votre rapport : "Gemma 4 n'étant pas disponible sur Ollama,
nous avons utilisé Gemma 3 (4B), le modèle multimodal équivalent le plus récent."

---

## Étape 1 — Installer Ollama

1. Allez sur https://ollama.com/download
2. Téléchargez et installez la version correspondant à votre OS (Windows / macOS / Linux).
3. Vérifiez l'installation dans un terminal :
   ```
   ollama --version
   ```

## Étape 2 — Télécharger le modèle multimodal

Dans un terminal :
```bash
ollama pull gemma3:4b
```
(Comptez quelques minutes selon votre connexion — le modèle fait ~3 Go.)

Testez rapidement en ligne de commande :
```bash
ollama run gemma3:4b
```
Tapez un message, vérifiez que ça répond, puis quittez avec `/bye`.

## Étape 3 — Installer Python et les dépendances

Assurez-vous d'avoir Python 3.10+ installé (`python --version`).

Il est recommandé de créer un environnement virtuel :
```bash
python -m venv venv
# Windows :
venv\Scripts\activate
# Mac/Linux :
source venv/bin/activate
```

Installez les dépendances (fichier `requirements.txt` fourni) :
```bash
pip install -r requirements.txt
```

**Important pour Whisper** : il a besoin de `ffmpeg`.
- Windows : `winget install ffmpeg` (ou téléchargez depuis ffmpeg.org et ajoutez au PATH)
- Mac : `brew install ffmpeg`
- Linux : `sudo apt install ffmpeg`

## Étape 4 — Lancer l'assistant multimodal

Dans le dossier contenant `multimodal_assistant.py` :
```bash
python multimodal_assistant.py
```

Un lien va s'afficher dans le terminal, par exemple :
```
Running on local URL: http://127.0.0.1:7860
```
Ouvrez ce lien dans votre navigateur : c'est votre interface de test.

## Étape 5 — Tester les 3 modalités (pour vos captures d'écran)

Pour valider le projet, testez et capturez :

1. **Texte seul** : tapez une question dans la zone "Requête texte" → capture de la réponse.
2. **Image seule** : uploadez une photo, laissez le texte vide, cliquez sur "Envoyer" → le
   modèle décrit l'image automatiquement.
3. **Voix + image (le cas demandé par l'énoncé)** : uploadez une image, cliquez sur le micro
   dans "Message vocal", enregistrez une question du type *"Que vois-tu sur cette image ?"*,
   puis cliquez sur "Envoyer". L'interface affiche :
   - la transcription Whisper de votre voix,
   - le prompt final envoyé au modèle,
   - la réponse du modèle sur l'image.

Faites une capture d'écran de chaque cas — c'est exactement ce que demande la consigne
("asking the model to describe a local image using your voice").

## Étape 6 — Dépannage rapide

| Problème | Solution |
|---|---|
| `ollama.chat` renvoie une erreur de connexion | Vérifiez qu'Ollama tourne bien en arrière-plan (`ollama serve` si besoin) |
| Whisper très lent | Utilisez `WHISPER_MODEL_SIZE = "tiny"` dans le script |
| Le modèle ne "voit" pas l'image | Vérifiez que vous utilisez bien un modèle **multimodal** (gemma3, llava, llama3.2-vision) et non un modèle texte-seul comme `llama3` classique |
| Erreur ffmpeg / audio non transcrit | Installez ffmpeg (voir Étape 3) et redémarrez le terminal |

## Structure à rendre

- `multimodal_assistant.py` (le code)
- Captures d'écran des 3 tests (texte, image, voix+image)
- Un court paragraphe expliquant votre choix de modèle et pipeline (Ollama + Whisper + Gradio)
