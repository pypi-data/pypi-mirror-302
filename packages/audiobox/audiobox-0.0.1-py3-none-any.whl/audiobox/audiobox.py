"""AudioBox code. This code allows the user to play music or sfx in the background."""

# Import statements
from altcolor import colored_text
from time import sleep as wait
import os
import sys
from threading import Thread
import shutil

old_stdout = sys.stdout
sys.stdout = open(os.devnull, 'w')

import pygame

sys.stdout.close()
sys.stdout = old_stdout

pygame.mixer.init()

# Global variables
music_on: bool = False
music_file: str = "null"
current_dir = os.path.dirname(__file__)

# Credits
print(colored_text("BLUE", "\n\nThanks for using AudioBox! Check out our other products at 'https://tairerullc.vercel.app'"))
print(colored_text("MAGENTA", "\n\nNote: \nThe music, not the sfx, is by Sadie Jean. The song is called 'Locksmith' and is avalible via Spotify.\nPlease note this song is copywrighted material and we use it only as an example, we are not endorsed by them nor are they endorsed by us.\n\n"))

# Functions
def generate_example_files():
    """Generates two audio clips for example use"""
    
    # Grab the source files for examples
    example_sfx = f"{current_dir}/example_sfx.wav"
    example_music = f"{current_dir}/example_music.mp3"
    
    # Set the location of clones
    cloned_sfx = "example_sfx.wav"
    cloned_music = "example_music.mp3"
    
    shutil.copyfile(example_sfx, cloned_sfx)
    shutil.copyfile(example_music, cloned_music)

def sfx(filename, times=1):
    """Plays an sound effect"""
    
    # Check if the file is .wav or .mp3
    if os.path.isfile(f"{filename}.wav"):
        filepath = f"{filename}.wav"
    elif os.path.isfile(f"{filename}.mp3"):
        filepath = f"{filename}.mp3"
    else:
        raise FileNotFoundError(f"Neither {filename} nor {filename}.mp3 found in system!")
    
    # Load the sound effect
    pygame.mixer.music.set_volume(0.5)
    sound_effect = pygame.mixer.Sound(filepath)
    sound_effect.play(times - 1)
    pygame.mixer.music.set_volume(1)
    wait(1)

def play_music(filename, stop_other=False):
    """This function plays music."""

    global music_file

    if not music_on:
        return

    music_file = filename

    # Check if the file is .wav or .mp3
    if os.path.isfile(f"{filename}.wav"):
        filepath = f"{filename}.wav"
    elif os.path.isfile(f"{filename}.mp3"):
        filepath = f"{filename}.mp3"
    else:
        raise FileNotFoundError(f"Neither {filename} nor {filename}.mp3 found in system!")

    if pygame.mixer.music.get_busy():
        if music_file == filepath:
            # The same music is already playing, do nothing.
            return

    def play_and_wait():
        global music_file
        
        if not music_on:
            return 
        else:
        
            try:
                pygame.mixer.music.load(filepath)
                song_length = pygame.mixer.Sound(filepath).get_length()
                pygame.mixer.music.play()
                pygame.mixer.music.set_volume(1)

                # Wait for the song to finish
                if not music_on:
                    return
                
                # Update the music_file variable
                music_file = filepath
            except pygame.error as e:
                print(f"Error loading or playing music file: {e}")

    # Stop the current music (if any)
    if stop_other:
        pygame.mixer.music.stop()

        # Start a new thread to play the music
        music_thread: Thread = Thread(target=play_and_wait)
        music_thread.start()