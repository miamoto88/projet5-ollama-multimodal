"""
Assistant Multimodal Local - Projet 5 (Computer Vision, MIATE)
----------------------------------------------------------------
Combine :
- Ollama (LLM multimodal local, ex: gemma3:4b, llava, llama3.2-vision)
- Whisper (speech-to-text local, pour transcrire la voix)
- Gradio (interface web simple pour tester texte / image / audio)

Lancement :
    python multimodal_assistant.py
Puis ouvrez le lien affiché dans le terminal (ex: http://127.0.0.1:7860)
"""

import ollama
import whisper
import gradio as gr

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------
# Changez le nom du modèle selon ce que vous avez téléchargé avec `ollama pull`
MODEL_NAME = "gemma3:4b"          # alternatives : "llava", "llama3.2-vision", "moondream"
WHISPER_MODEL_SIZE = "base"       # "tiny" (plus rapide) ou "small"/"medium" (plus précis)

# ---------------------------------------------------------------------------
# WHISPER : transcription audio -> texte
# ---------------------------------------------------------------------------
_whisper_model = None


def get_whisper_model():
    """Charge le modèle Whisper une seule fois (mise en cache)."""
    global _whisper_model
    if _whisper_model is None:
        print(f"[INFO] Chargement du modèle Whisper '{WHISPER_MODEL_SIZE}'...")
        _whisper_model = whisper.load_model(WHISPER_MODEL_SIZE)
    return _whisper_model


def transcribe_audio(audio_path: str) -> str:
    """Transcrit un fichier audio en texte grâce à Whisper (local, hors-ligne)."""
    if not audio_path:
        return ""
    model = get_whisper_model()
    result = model.transcribe(audio_path)
    return result["text"].strip()


# ---------------------------------------------------------------------------
# OLLAMA : appel du modèle multimodal
# ---------------------------------------------------------------------------
def ask_ollama(prompt: str, image_path: str | None = None) -> str:
    """Envoie une requête (texte + éventuellement image) au modèle Ollama local."""
    message = {"role": "user", "content": prompt}
    if image_path:
        message["images"] = [image_path]

    response = ollama.chat(model=MODEL_NAME, messages=[message])
    return response["message"]["content"]


# ---------------------------------------------------------------------------
# PIPELINE MULTIMODAL PRINCIPAL
# ---------------------------------------------------------------------------
def multimodal_pipeline(text_input, image_input, audio_input):
    """
    Combine les 3 modalités d'entrée :
    - text_input  : texte tapé par l'utilisateur (str ou None)
    - image_input : chemin vers l'image uploadée (str ou None)
    - audio_input : chemin vers le fichier audio enregistré (str ou None)
    """
    prompt_parts = []

    # 1) Transcription vocale si un audio est fourni
    transcript = ""
    if audio_input:
        transcript = transcribe_audio(audio_input)
        prompt_parts.append(transcript)

    # 2) Ajout du texte tapé manuellement (si présent)
    if text_input:
        prompt_parts.append(text_input)

    final_prompt = " ".join(p for p in prompt_parts if p).strip()

    # 3) Valeur par défaut si aucune entrée texte/audio n'est donnée mais qu'il y a une image
    if not final_prompt:
        final_prompt = "Décris cette image en détail." if image_input else "Bonjour, peux-tu te présenter ?"

    # 4) Appel du modèle
    answer = ask_ollama(final_prompt, image_input)

    debug_info = f" Transcription vocale : {transcript}" if transcript else " (pas d'audio fourni)"
    return final_prompt, debug_info, answer


# ---------------------------------------------------------------------------
# INTERFACE GRADIO
# ---------------------------------------------------------------------------
with gr.Blocks(title="Assistant Multimodal Local - Ollama") as demo:
    gr.Markdown("#  Assistant Multimodal Local (Ollama + Whisper)")
    gr.Markdown(
        "Envoyez du **texte**, une **image** et/ou un **message vocal**. "
        "Tout tourne 100% en local, sans connexion internet ni API cloud."
    )

    with gr.Row():
        with gr.Column():
            text_in = gr.Textbox(
                label="Requête texte (optionnel)",
                placeholder="Ex : Que vois-tu sur l'image ?",
            )
            image_in = gr.Image(label="Image (optionnel)", type="filepath")
            audio_in = gr.Audio(
                label="Message vocal (optionnel — cliquez sur le micro pour enregistrer)",
                sources=["microphone", "upload"],
                type="filepath",
            )
            btn = gr.Button(" Envoyer", variant="primary")

        with gr.Column():
            prompt_out = gr.Textbox(label="Prompt final envoyé au modèle")
            transcript_out = gr.Textbox(label="Détails transcription")
            answer_out = gr.Textbox(label=" Réponse du modèle", lines=10)

    btn.click(
        fn=multimodal_pipeline,
        inputs=[text_in, image_in, audio_in],
        outputs=[prompt_out, transcript_out, answer_out],
    )

if __name__ == "__main__":
    demo.launch()
