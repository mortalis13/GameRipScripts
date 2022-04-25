# Extracts fonts from the Assassin's Creed game data
# Use a tool that extracts the corresponding data file (e.g. Ubisoft Forge and Data tools by Delutto)
# and follow this chain:
# Game_Folder -> DataPC.forge -> 114-Game Bootstrap Settings.data -> 40-Font Manager ACVI.1641561018

import os

input_file = 'data/40-Font Manager ACVI.1641561018'
output_folder = 'export'


def save_data(source_file_, file_path):
  if not os.path.exists(os.path.dirname(file_path)):
    os.makedirs(os.path.dirname(file_path))
  
  output_file_ = open(file_path, 'wb')
  data_size = source_file_.read(4)
  data_size = int.from_bytes(data_size, 'little')
  output_file_.write(source_file_.read(data_size))
  output_file_.close()
  
  print(f'Saved file: {file_path}')


def run():
  input_file_ = open(input_file, 'rb')

  start_marker = b'\xec\xa7\xa6\x70'
  finder = b''
  i = 1

  while True:
    b = input_file_.read(1)
    if not b:
      break
    
    finder += b
    if finder.endswith(start_marker):
      save_data(input_file_, f'{output_folder}/Font_{i}.ttf')
      finder = b''
      i += 1
    
  print(f'Saved total of {i-1} files')

  input_file_.close()

# ---
run()
