from accessible_output2.outputs.auto import Auto
import json
import os

speaker = Auto()

def alert(message, interrupt=False):
    if voice_output_enabled():
        speaker.speak(message, interrupt=interrupt)

def voice_output_enabled():
    documents_dir = os.path.expanduser("~/Documents")
    app_data_dir = os.path.join(documents_dir, "ml_player_data")
    config_file = os.path.join(app_data_dir, "config.json")
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
            return config.get('voice_output_enabled', False)
    except FileNotFoundError:
        return False
