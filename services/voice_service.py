import os
import uuid

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs


# -----------------------------------------
# Load environment variables
# -----------------------------------------

load_dotenv()


# -----------------------------------------
# Get ElevenLabs API key
# -----------------------------------------

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")


if not ELEVENLABS_API_KEY:
    raise ValueError(
        "ELEVENLABS_API_KEY is not set in the .env file."
    )


# -----------------------------------------
# Create ElevenLabs client
# -----------------------------------------

elevenlabs = ElevenLabs(
    api_key=ELEVENLABS_API_KEY
)


# -----------------------------------------
# Default voice
# -----------------------------------------

DEFAULT_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"


# -----------------------------------------
# Text To Speech
# -----------------------------------------

def text_to_speech(
    text: str,
    output_file: str = None,
    voice_id: str = DEFAULT_VOICE_ID
):
    """
    Convert text into speech using ElevenLabs.

    Returns:
        Path of the generated MP3 file.
    """

    try:

        # ---------------------------------
        # Validate text
        # ---------------------------------

        if not text or not text.strip():
            raise ValueError(
                "Text cannot be empty."
            )


        # ---------------------------------
        # Create unique filename
        # ---------------------------------

        if output_file is None:

            output_file = (
                f"response_{uuid.uuid4().hex}.mp3"
            )


        # ---------------------------------
        # Generate speech
        # ---------------------------------

        audio = elevenlabs.text_to_speech.convert(

            text=text,

            voice_id=voice_id,

            # Faster model for real-time use
            model_id="eleven_flash_v2_5",

            # Smaller audio file
            output_format="mp3_22050_32"
        )


        # ---------------------------------
        # Save audio file
        # ---------------------------------

        with open(
            output_file,
            "wb"
        ) as file:

            for chunk in audio:

                if chunk:
                    file.write(chunk)


        print(
            f"Voice generated successfully: "
            f"{output_file}"
        )


        return output_file


    except Exception as e:

        print(
            "ElevenLabs Voice Error:",
            e
        )

        return None