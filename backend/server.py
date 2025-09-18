from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app)

# Загружаем готовую модель эмоций
MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"
analyzer = pipeline("text-classification", model=MODEL_NAME)

def build_prompt(emotion: str) -> str:
    e = emotion.lower()
    mapping = {
        "joy": (
            "Generate a 15-second bright and uplifting video. "
            "Use golden-hour lighting, a warm pastel color palette, and a gentle camera push-in. "
            "Add floating confetti-like particles. "
            "The soundtrack should be upbeat acoustic music."
        ),
        "sadness": (
            "Generate a 15-second calm and introspective video. "
            "Use cool blue tones, show light rain on a window, and apply a slow dolly camera movement with soft bokeh. "
            "The soundtrack should be sparse piano ambient in a minor key."
        ),
        "anger": (
            "Generate a 15-second intense and high-contrast video. "
            "Use deep reds and blacks, quick cuts, and a handheld camera feel with subtle glitch effects. "
            "The soundtrack should be a percussive dark synth rhythm."
        ),
        "fear": (
            "Generate a 15-second suspenseful and dimly lit video. "
            "Use a desaturated palette, slow zooms, mist ambience, and long shadows. "
            "The soundtrack should be a low, droning ambient sound."
        ),
        "disgust": (
            "Generate a 15-second uneasy and textured video. "
            "Apply a sickly green tint, show macro shots of organic surfaces, and use erratic camera shifts. "
            "The soundtrack should be dissonant ambient textures."
        ),
        "surprise": (
            "Generate a 15-second dynamic and playful video. "
            "Use bright pops of color, quick reveals, whip-pan transitions, and bursts of particles. "
            "The soundtrack should be light, plucky melodies."
        ),
        "neutral": (
            "Generate a 15-second balanced and ambient video. "
            "Use soft neutral tones, gentle gradients, and slow camera movements. "
            "The soundtrack should be warm, minimal background music."
        )
    }
    return mapping.get(e, mapping["neutral"])

@app.post("/process-message")
def process_message():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Анализируем эмоцию через модель
    result = analyzer(text)[0] 
    emotion = result["label"].lower()
    score = float(result["score"])
    prompt = build_prompt(emotion)

    return jsonify({
        "text": text,
        "emotion": emotion,
        "score": score,
        "prompt": prompt
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
