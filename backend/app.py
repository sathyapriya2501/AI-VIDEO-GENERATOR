from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
from tts import create_audio
from scene_composer import create_scene
import os
import json

load_dotenv()

# --------------------------------------------------
# FLASK APP
# --------------------------------------------------

app = Flask(__name__)
CORS(app)


# --------------------------------------------------
# GROQ CLIENT
# --------------------------------------------------

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.route("/")
def home():
    return "AI Video Generator Backend is Running!"


# --------------------------------------------------
# SCENE PLANNER
# --------------------------------------------------

@app.route("/plan-scene", methods=["POST"])
def plan_scene():

    data = request.get_json()

    user_prompt = data.get("prompt")

    if not user_prompt:
        return jsonify({
            "success": False,
            "error": "Prompt is required"
        }), 400

    system_prompt = """
You are an AI Video Scene Planner.

Convert the user's video idea into ONLY valid JSON.

Use exactly this structure:
{
  "duration": number,
  "language": "Tamil or English",
  "character": "",
  "background": "",
  "script": "",
  "action": "",
  "expression": "",
  "props": [],
  "camera": "",
  "voice": {
    "gender": "Male or Female",
    "language": "Tamil or English"
  }
}

Available characters:
Farmer, Student, Doctor, Businessman

Available backgrounds:
Village, Farm, School, College, Hospital, Office, City,
Railway Station, Bus Stand, Temple

Available motions/actions:
Idle, Walk, Run, Sit, Stand, Wave, Point, Talk, Think, Turn

Available expressions:
Neutral, Happy, Sad, Angry, Surprised, Thinking, Excited, Worried

Available props:
Chair, Table, Laptop, Mobile, Book, Water Pot, Bicycle,
Tree, Plant, School Bag, Microphone

Available camera movements:
Static, Zoom In, Zoom Out, Pan Left, Pan Right, Close-up, Wide Shot

Available languages:
Tamil, English

Available voice genders:
Male, Female

Rules:
- Generate a short natural dialogue/script based on the user's video idea.
- The script must match the selected language.
- If language is Tamil, write the script in Tamil.
- If language is English, write the script in English.
- Keep the script suitable for the selected duration.
- Return ONLY valid JSON.
- Do not add explanations or markdown.
- Use ONLY the exact names from the lists above.
- Do not invent new characters, backgrounds, actions, expressions, props, or camera movements.
- If a requested item is unavailable, choose the closest available option.
- If the prompt is in Tamil, use Tamil language and Tamil voice.
- Keep duration between 5 and 60 seconds.
"""

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0
        )

        result = response.choices[0].message.content

        scene = json.loads(result)

        return jsonify({
            "success": True,
            "scene": scene
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# --------------------------------------------------
# TEXT TO SPEECH
# --------------------------------------------------

@app.route("/generate-audio", methods=["POST"])
def generate_audio():

    data = request.json

    script = data.get("script")
    voice = data.get("voice", {})

    language = voice.get("language", "Tamil")
    gender = voice.get("gender", "Male")

    if not script:
        return jsonify({
            "success": False,
            "error": "Script is required"
        }), 400

    output_file = "../output/scene_audio.mp3"

    try:

        create_audio(
            script,
            output_file,
            language,
            gender
        )

        return jsonify({
            "success": True,
            "audio": "scene_audio.mp3"
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# --------------------------------------------------
# GENERATE FINAL VIDEO
# --------------------------------------------------

@app.route("/generate-video", methods=["POST"])
def generate_video():

    data = request.json

    scene = data.get("scene")

    if not scene:
        return jsonify({
            "success": False,
            "error": "Scene data is required"
        }), 400

    try:

        # ------------------------------------------
        # 1. GET SCRIPT AND VOICE
        # ------------------------------------------

        script = scene.get("script")

        voice = scene.get("voice", {})

        language = voice.get("language", "Tamil")
        gender = voice.get("gender", "Male")

        if not script:
            return jsonify({
                "success": False,
                "error": "Script is missing"
            }), 400

        # ------------------------------------------
        # 2. GENERATE AUDIO
        # ------------------------------------------

        audio_file = "../output/scene_audio.mp3"

        create_audio(
            script,
            audio_file,
            language,
            gender
        )

        # ------------------------------------------
        # 3. CREATE VIDEO
        # ------------------------------------------

        create_scene(scene)

        # ------------------------------------------
        # 4. RETURN VIDEO NAME
        # ------------------------------------------

        return jsonify({
            "success": True,
            "video": "final_video.mp4"
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# --------------------------------------------------
# SERVE FINAL VIDEO
# --------------------------------------------------

@app.route("/video/<filename>")
def serve_video(filename):

    output_folder = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "output"
        )
    )

    return send_from_directory(
        output_folder,
        filename
    )


# --------------------------------------------------
# RUN SERVER
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)