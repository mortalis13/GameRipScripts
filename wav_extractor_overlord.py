# Extracts WAV audio data from binary resource files from the Overlord game
# Uses the same code as the 'wav_extractor.py' but also finds output file names
# in the .pvp files which are placed before the 'RIFF' header for each WAV block

import codecs, os

# --- DATA
input_files = [
  'data/MinionVoiceData_ENGLISH.pvp'
]
output_folder = 'export'
# --------


def get_out_file_name(input_file_, item_pos):
  input_file_.seek(item_pos)
  input_file_.read(1)

  wav_name = b''
  finder = b'    '
  ext_found = False

  while True:
    input_file_.seek(-2, 1)
    byte = input_file_.read(1)
    
    if ext_found:
      if byte == b'\x00':
        break
      wav_name = byte + wav_name
    else:
      finder = byte + finder
      finder = finder[:-1]
      if finder.lower() == b'.wav':
        ext_found = True
        wav_name = finder

  wav_name = wav_name.decode()
  print('{}  ::  [{}]'.format(wav_name, hex(item_pos)))
  
  return wav_name


def save_wav(input_file_, item_pos, output_file):
  output_file_ = codecs.open(output_file, 'wb')
  input_file_.seek(item_pos)
  
  finder = b'    '
  while True:
    byte = input_file_.read(1)
    output_file_.write(byte)
    
    finder += byte
    finder = finder[1:]
    if finder == b'data':
      size_b = input_file_.read(4)
      output_file_.write(size_b)
      
      datasize = int.from_bytes(size_b, 'little')
      wav_data = input_file_.read(datasize)
      output_file_.write(wav_data)
      break
  
  output_file_.close()


def extract_audio(input_file, output_folder):
  print('..extract_audio(): {}\n'.format(input_file))
  input_file_ = codecs.open(input_file, 'rb')
  
  output_folder += '/' + os.path.splitext(os.path.basename(input_file))[0] + '/'
  
  rifflen = 4
  finder = b'    '
  c = 0
  pos = 0
  
  # -- get RIFF positions
  riff_list = []
  while True:
    byte = input_file_.read(1)
    if not byte:
      break
    
    pos += 1
    finder += byte
    finder = finder[1:]
    if finder == b'RIFF':
      riff_list.append(pos-rifflen)
  
  print('items:', len(riff_list))
  
  
  # -- save
  if len(riff_list) and not os.path.exists(output_folder):
    os.makedirs(output_folder)
  
  extracted_count = 0
  for item_pos in riff_list:
    wav_name = get_out_file_name(input_file_, item_pos)
    
    if wav_name.endswith('.wav'):
      save_wav(input_file_, item_pos, output_folder + wav_name)
      extracted_count += 1
    else:
      print('not a WAV name')
  
  input_file_.close()
  
  if extracted_count == len(riff_list):
    print('\n== [{}] -> All WAVs extracted: {}\n\n'.format(output_folder, extracted_count))
  else:
    print('\n== [{}] -> Missing some WAVs: extracted {} of {}\n\n'.format(extracted_count, len(riff_list)))
  

def run():
  for input_file in input_files:
    extract_audio(input_file, output_folder)
  
# ---
run()
