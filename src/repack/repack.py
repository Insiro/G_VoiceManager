import os
from FilePackager import Package, build_pck_file

wav_path = './wem/'
input_path = './input_pck/'
output_path = './output_pck/'

for i in os.scandir(wav_path):
    if os.path.exists(output_path+i.name+'.pck') == False:
        print(output_path+i.name+'.pck')
        modify_pck = Package()  # init
        modify_pck.addfile(open(input_path+i.name+'.pck', 'rb'))  # add the pck file you want to modify
        for f in os.scandir(wav_path+i.name):
            int_hash_value = int(f.name.replace('.wem',''), 16) # In the unpacked file, its hash is in the file name
            modify_pck.add_wem(2, 0, int_hash_value, open(wav_path+i.name+'/'+f.name, 'rb'))  # override the wem file
            # Where 1 argument - external files
            # 0: soundbanks
            # 1: stream files
            # 2: external files

            # Where 2 argument - language id
            # You can not change it, since the genshin almost always has SFX

        with open(output_path+i.name+'.pck', 'wb') as f:
            build_pck_file(modify_pck, f, modify_pck.LANGUAGE_DEF)