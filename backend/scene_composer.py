import subprocess
import json


def create_scene(scene):

    character = scene.get("character", "Farmer")
    background_name = scene.get("background", "Village")
    props = scene.get("props", [])
    camera = scene.get("camera", "Static")

    # Load asset metadata
    with open("../assets/asset_metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # Get background
    background_path = metadata["backgrounds"].get(background_name)

    if not background_path:
        raise FileNotFoundError(
            f"Background asset not found: {background_name}"
        )

    # Get avatar
    avatar_path = metadata["avatars"].get(character)

    if not avatar_path:
        raise FileNotFoundError(
            f"Avatar asset not found: {character}"
        )

    background = "../assets/" + background_path
    avatar = "../assets/" + avatar_path

    # Get first available prop
    prop_path = None

    for prop_name in props:
        if prop_name in metadata["props"]:
            prop_path = metadata["props"][prop_name]
            break

    audio = "../output/scene_audio.mp3"
    output = "../output/final_video.mp4"

    # -------------------------
    # BACKGROUND
    # -------------------------

    if camera == "Zoom In":

        background_filter = (
            "[0:v]"
            "scale=1280:720:force_original_aspect_ratio=increase,"
            "crop=1280:720,"
            "zoompan="
            "z='min(zoom+0.0015,1.15)':"
            "x='iw/2-(iw/zoom/2)':"
            "y='ih/2-(ih/zoom/2)':"
            "d=1:"
            "s=1280x720:"
            "fps=25"
            "[bg];"
        )

    elif camera == "Zoom Out":

        background_filter = (
            "[0:v]"
            "scale=1280:720:force_original_aspect_ratio=increase,"
            "crop=1280:720,"
            "zoompan="
            "z='if(eq(on,1),1.15,max(zoom-0.0015,1))':"
            "x='iw/2-(iw/zoom/2)':"
            "y='ih/2-(ih/zoom/2)':"
            "d=1:"
            "s=1280x720:"
            "fps=25"
            "[bg];"
        )

    else:

        background_filter = (
            "[0:v]"
            "scale=1280:720:force_original_aspect_ratio=increase,"
            "crop=1280:720"
            "[bg];"
        )

    # -------------------------
    # AVATAR
    # -------------------------

    avatar_filter = (
        "[1:v]"
        "scale=400:400,"
        "fps=25,"
        "crop=400:400:"
        "x=0:"
        "y='sin(n/8)*5'"
        "[avatar];"
    )

    # -------------------------
    # COMMAND
    # -------------------------

    command = [
        "ffmpeg",
        "-y",

        "-loop", "1",
        "-i", background,

        "-loop", "1",
        "-i", avatar,
    ]

    # Add prop if available
    if prop_path:

        prop = "../assets/" + prop_path

        command += [
            "-loop", "1",
            "-i", prop,
        ]

    # Audio
    command += [
        "-i", audio,

        "-filter_complex",

        background_filter
        + avatar_filter
    ]

    # -------------------------
    # OVERLAYS
    # -------------------------

    if prop_path:

        filter_complex = (
            background_filter
            + avatar_filter
            + "[bg][avatar]"
            "overlay=440:250"
            "[tmp];"
            "[2:v]"
            "scale=180:-1"
            "[pot];"
            "[tmp][pot]"
            "overlay=900:480"
            "[video]"
        )

        command[-1] = filter_complex

        audio_index = "3:a"

    else:

        filter_complex = (
            background_filter
            + avatar_filter
            + "[bg][avatar]"
            "overlay=440:250"
            "[video]"
        )

        command[-1] = filter_complex

        audio_index = "2:a"

    # -------------------------
    # OUTPUT
    # -------------------------

    command += [
        "-map", "[video]",
        "-map", audio_index,

        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        "-r", "25",

        "-c:a", "aac",

        "-shortest",

        output
    ]

    subprocess.run(command, check=True)

    print()
    print("Dynamic video created!")
    print("Character :", character)
    print("Background:", background_name)
    print("Props     :", props)
    print("Camera    :", camera)
    print("Output    :", output)


if __name__ == "__main__":

    test_scene = {
        "character": "Farmer",
        "background": "Village",
        "props": ["Water Pot"],
        "camera": "Zoom In"
    }

    create_scene(test_scene)