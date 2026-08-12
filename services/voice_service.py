import os

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
#
# This is an example voice ID.
# Later we can replace it with the voice
# you choose from your ElevenLabs account.
#
# -----------------------------------------

DEFAULT_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"


# -----------------------------------------
# Text To Speech
# -----------------------------------------

def text_to_speech(
    text: str,
    output_file: str = "response.mp3",
    voice_id: str = DEFAULT_VOICE_ID
):
    """
    Convert text into speech using ElevenLabs.

    Parameters:
        text:
            Text that should be spoken.

        output_file:
            Location where the MP3 file
            should be saved.

        voice_id:
            ElevenLabs voice ID.

    Returns:
        Path of the generated audio file.
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
        # Generate speech
        # ---------------------------------

        audio = elevenlabs.text_to_speech.convert(

            text=text,

            voice_id=voice_id,

            model_id="eleven_multilingual_v2",

            output_format="mp3_44100_128"
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