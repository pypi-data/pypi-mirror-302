from audiobox import *

generate_example_files() # Generates two audio clips for example use

sfx("example_sfx") # Handles .mp3 and .wav | Only use the file name and not extension

wait(5) # 'wait' comes built in with this module but is really just 'time.sleep' disguised, I was used to using Lua's 'wait' instead so I just translated into Python.

play_music("example_music") # Handles .mp3 and .wav | Only use the file name and not extension
wait(165)