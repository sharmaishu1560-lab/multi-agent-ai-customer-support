from services.voice_service import text_to_speech


text = (
    "Hello! Welcome to our customer support assistant. "
    "How can I help you today?"
)


audio_file = text_to_speech(
    text,
    output_file="test_response.mp3"
)


if audio_file:

    print(
        f"Audio created successfully: {audio_file}"
    )

else:

    print(
        "Failed to generate audio."
    )