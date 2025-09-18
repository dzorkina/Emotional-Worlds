from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app)

# Загружаем готовую модель эмоций
MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"
analyzer = pipeline("text-classification", model=MODEL_NAME)

# === Маппинг эмоций (кастомные категории) ===
def map_emotion(label: str, text: str) -> str:
    label = label.lower()
    t = text.lower()

    if label == "joy":
        if any(word in t for word in ["love", "in love", "crush", "romantic", "люблю", "влюблен"]):
            return "love"
    if label == "sadness":
        if any(word in t for word in ["tired", "sleep", "exhausted", "устал", "сонный"]):
            return "tired"
    if label == "fear":
        if any(word in t for word in ["nervous", "anxious", "worry", "нервн", "тревож"]):
            return "nervousness"
    if label in ["sadness", "fear"]:
        if any(word in t for word in ["embarrass", "awkward", "стыд", "смущ"]):
            return "embarrassment"

    return label

# === Генерация промпта под эмоцию ===
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
        ),
        "love": (
            "Generate a 15-second warm and romantic video. "
            "Use soft pink and red tones, blurred lights in the background, and smooth slow camera moves. "
            "The soundtrack should be gentle acoustic or romantic piano."
        ),
        "embarrassment": (
            "Generate a 15-second slightly awkward but light video. "
            "Use pale pastel tones, quick hesitant camera movements, and small visual stumbles like flickers. "
            "The soundtrack should be quirky, playful music with pauses."
        ),
        "nervousness": (
            "Generate a 15-second tense and jittery video. "
            "Use shaky handheld camera style, cold lighting, and fast small zooms. "
            "The soundtrack should be minimal high-pitched ambient with irregular beats."
        ),
        "tired": (
            "Generate a 15-second sleepy and slow video. "
            "Use dim warm lighting, soft blur, and very slow camera pans. "
            "The soundtrack should be a quiet lullaby-like ambient."
        )
    }
    return mapping.get(e, mapping["neutral"])

# === Flask endpoint ===
@app.post("/process-message")
def process_message():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = analyzer(text)[0]
    emotion = map_emotion(result["label"], text)
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

