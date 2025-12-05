from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app)

# готовая модель эмоций
MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"
analyzer = pipeline("text-classification", model=MODEL_NAME)

# Маппинг эмоций 
def map_emotion(label: str, text: str) -> str:
    label = label.lower()
    t = text.lower()

    if label == "joy":
        if any(word in t for word in ["love", "in love", "crush", "romantic"]):
            return "love"
    if label == "sadness":
        if any(word in t for word in ["tired", "sleep", "exhausted"]):
            return "tired"
    if label == "fear":
        if any(word in t for word in ["nervous", "anxious", "worry", "afriad", "stress", "panic"]):
            return "nervousness"
    if label in ["sadness", "fear"]:
        if any(word in t for word in ["embarrass", "awkward", "shame"]):
            return "embarrassment"

    return label

#  Генерация промпта под эмоцию 
def build_prompt(emotion: str) -> str:
    e = emotion.lower()
    mapping = {
        "joy": (
            "Generate a 15-second warm and uplifting video. "
            "Show a gentle walk through a sunlit park with butterflies drifting in the air. "
            "Use golden-hour lighting, soft pastel tones, and smooth camera movement. "
            "The atmosphere should feel peaceful, joyful, and emotionally comforting. "
        ),
        "sadness": (
            "Generate a 15-second calm and reflective video. "
            "Show a quiet walk through a dim forest during light rain, with soft mist and droplets on leaves. "
            "Use cool blue tones, slow camera pans, and a grounding, safe atmosphere. "
            "The scene should feel soothing and supportive rather than heavy. "
        ),
        "anger": (
            "Generate a 15-second grounding and calming video. "
            "Show a flowing river pushing through smooth rocks with steady, rhythmic motion. "
            "Use deep natural tones, slow stabilized camera movement, and a sense of release. "
            "The scene should help diffuse tension and restore balance. "
            "The soundtrack should be low rhythmic ambient with a calm pulse."
        ),,
       "fear": (
            "Generate a 15-second reassuring and peaceful video. "
            "Show a softly lit safe space, such as a warm cabin interior with a small lantern glowing. "
            "Use desaturated warm tones, gentle zooms, and calm shadow play. "
            "The atmosphere should feel protective and grounding. "
            "The soundtrack should be low, warm ambient sound."
        ),
        "disgust": (
            "Generate a 15-second clean and refreshing video. "
            "Show flowing clear water over smooth stones, with gentle ripples and soft sunlight. "
            "Use cool, fresh tones and slow cleansing camera movement. "
            "The scene should evoke purity, clarity, and emotional reset. "
            "The soundtrack should be soft water ambient with light chimes."
        ),
        "surprise": (
            "Generate a 15-second bright and playful video. "
            "Show the sudden reveal of a beautiful scenic overlook as the camera moves through soft curtains of light. "
            "Use vivid pops of color, light bursts, and smooth transitions. "
            "The atmosphere should feel exciting but positive and gentle. "
            "The soundtrack should be light, plucky melodies."
        ),
       "neutral": (
            "Generate a 15-second balanced and soothing video. "
            "Show soft clouds slowly drifting across a calm sky with gentle sunlight. "
            "Use neutral warm tones, smooth gradients, and very slow camera movement to evoke stability and ease. "
            "The atmosphere should feel steady, grounding, and emotionally neutral-positive. "
            "The soundtrack should be warm minimal ambient music with soft tones."
        ),,
        "love": (
            "Generate a 15-second warm and romantic video. "
            "Show glowing sky lanterns being released into a calm evening sky. "
            "Use soft pink and red tones, floating lights, and gentle slow-motion movement. "
            "The atmosphere should feel tender, hopeful, and emotionally supportive. "
            "The soundtrack should be gentle acoustic or soft romantic piano."
        ),
        "embarrassment": (
            "Generate a 15-second light and slightly awkward but comforting video. "
            "Show a cozy pastel-colored room with small, humorous visual stumbles like flickers or gentle camera hesitations. "
            "Use soft warm lighting and a friendly, non-judgmental atmosphere. "
            "The scene should feel relatable and safe. "
            "The soundtrack should be quirky, playful music with soft pauses."
        ),
        "nervousness": (
            "Generate a 15-second calming and grounding video. "
            "Show a close-up of warm string lights gently flickering in a quiet room. "
            "Use soft focus, slow breathing-like camera movement, and warm ambient light. "
            "The scene should reduce tension and provide reassurance. "
             "The soundtrack should be minimal ambient with steady, soothing tones."
    ),
        "tired": (
            "Generate a 15-second restful and soothing video. "
            "Show slow ocean waves rolling gently toward the shore at sunset. "
            "Use warm dim lighting, soft blur, and very slow camera pans to evoke relaxation. "
            "The atmosphere should feel restorative and peaceful. "
            "The soundtrack should be quiet lullaby-like ambient with ocean tones."
        ),
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

