import os
from os import path
from .FilePackager import Package, build_pck_file


def repack(wav_path: str, input_path: str, output_path: str, logger):
    for i in os.scandir(wav_path):
        output_file_name = path.join(
            output_path, i.name + ".pck"
        )  # output_path + i.name + ".pck"
        if os.path.exists(output_file_name) == False:
            logger.info(f"packing {output_file_name}")
            modify_pck = Package()  # init
            modify_pck.addfile(
                open(path.join(input_path, i.name + ".pck"), "rb")
            )  # add the pck file you want to modify
            wav_file_path = path.join(wav_path, i.name)
            for f in os.scandir(wav_file_path):
                int_hash_value = int(
                    f.name.replace(".wem", ""), 16
                )  # In the unpacked file, its hash is in the file name
                modify_pck.add_wem(
                    2, 0, int_hash_value, open(path.join(wav_file_path, f.name), "rb")
                )  # override the wem file
                # Where 1 argument - external files
                # 0: soundbanks
                # 1: stream files
                # 2: external files

                # Where 2 argument - language id
                # You can not change it, since the genshin almost always has SFX

            with open(output_file_name, "wb") as f:
                build_pck_file(modify_pck, f, modify_pck.LANGUAGE_DEF)
