import time
import os
import json
from deepdiff import DeepDiff


def translate_str(txt: str) -> str:
    txt_translated = "---translated"
    return txt_translated


def translate(txt: str | dict) -> str | dict:
    if type(txt) == str:
        txt_translated = translate_str(txt)
    else:
        txt_translated = txt
        for key in list(txt.keys()):
            txt_translated[key] = translate_str(txt[key])
    return txt_translated


def add_missing_keys(master_file: dict, slave_file: dict) -> dict:
    diff = DeepDiff(master_file, slave_file, ignore_order=False)
    slave_file_tmp = slave_file
    if 'dictionary_item_removed' in diff:
        for idx, value in enumerate(diff['dictionary_item_removed']):
            key_list = value.split('[')[1:]
            for i in range(len(key_list)):
                key_list[i] = key_list[i].strip("']")

            if len(key_list) == 1:
                pos = list(master_file.keys()).index(key_list[0])
                items = list(slave_file_tmp.items())
                items.insert(pos, (key_list[0], translate(master_file[key_list[0]])))
                slave_file_tmp = dict(items)

            elif len(key_list) == 2:
                pos = list(master_file[key_list[0]].keys()).index(key_list[1])
                items = list(slave_file_tmp[key_list[0]].items())
                items.insert(pos, (key_list[1], translate(master_file[key_list[0]][key_list[1]])))
                slave_file_tmp[key_list[0]] = dict(items)

            else:
                raise Exception(f"Depth of json-file is maximum two, now it's: {len(key_list)}")
    return slave_file_tmp


def main() -> None:
    path_resources = os.path.join(os.getcwd(), "resource")
    name_main_file = "de.json"
    translation_file_names = ["en.json", "fr.json", "it.json"]
    translation_files = [""] * len(translation_file_names)

    with open(os.path.join(path_resources, name_main_file), 'r') as file:
        main_file = json.load(file)

    for idx, file_name in enumerate(translation_file_names):
        with open(os.path.join(path_resources, file_name), 'r') as file:
            translation_files[idx] = json.load(file)
        translation_files[idx] = add_missing_keys(main_file, translation_files[idx])
        print(translation_files[idx])


if __name__ == '__main__':
    print(f"**********| Start  |**********\n")
    _tStart = time.perf_counter()
    main()
    print(f"\n**********| {time.perf_counter() - _tStart:.3f}s |**********")