from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import QUrl
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
soundeffects_folder = os.path.join(script_dir, "soundeffects") # Assuming your soundeffects are in a subfolder named 'soundeffects'

sound_effects = {}

def load_sound(sound_name, filename):
    sound_path = os.path.join(soundeffects_folder, filename)
    if not os.path.exists(sound_path):
        print(f"Warning: Sound file not found at {sound_path}")
        return

    effect = QSoundEffect()
    effect.setSource(QUrl.fromLocalFile(sound_path))
    sound_effects[sound_name] = effect

def play_sound(sound_name):
    if sound_name in sound_effects and sound_effects[sound_name].isLoaded():
        sound_effects[sound_name].play()
    else:
        print(f"Warning: Sound '{sound_name}' not loaded or found.")

load_sound("move", "move.wav") # Assuming you have a file named 'move.wav' in your 'soundeffects' folder
load_sound("checkmate", "checkmate.wav") # Another example