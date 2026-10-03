import edge_tts
import asyncio
import os


async def generate_voice(text, output_file, language="Tamil", gender="Male"):

    if language == "Tamil":
        if gender == "Male":
            voice = "ta-IN-ValluvarNeural"
        else:
            voice = "ta-IN-PallaviNeural"
    else:
        if gender == "Male":
            voice = "en-US-GuyNeural"
        else:
            voice = "en-US-JennyNeural"

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)


def create_audio(text, output_file, language="Tamil", gender="Male"):
    asyncio.run(
        generate_voice(
            text,
            output_file,
            language,
            gender
        )
    )


if __name__ == "__main__":

    text = "வணக்கம் நண்பர்களே! நீர் பாதுகாப்பு மிக முக்கியம்."

    output_file = "../output/scene_audio.mp3"

    create_audio(
        text,
        output_file,
        "Tamil",
        "Male"
    )

    print("Audio generated:", output_file)