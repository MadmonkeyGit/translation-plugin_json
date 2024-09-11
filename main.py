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
            txt_translated[key] = translate(txt[key])
    return txt_translated


def nested_dict_get(dataDict: dict, keys: list):
    for k in keys: dataDict = dataDict[k]
    return dataDict


def nested_dict_add_key(dic: dict, keys: list):
    if len(keys) == 1:
        dic.setdefault(keys[0], 1)
    else:
        key = keys[0]
        if key not in dic:
            dic[key] = {}
        nested_dict_add_key(dic[key], keys[1:])


def nested_dict_set(dic: dict, keys: list, value: any):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value


def nested_dict_delete(dic: dict, keys: list):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    del dic[keys[-1]]


def add_missing_keys(master_file: dict, slave_file: dict) -> dict:
    diff = DeepDiff(master_file, slave_file, ignore_order=False)
    if 'dictionary_item_removed' in diff:
        for idx, value in enumerate(diff['dictionary_item_removed']):
            key_list = value.split('[')[1:]
            for i in range(len(key_list)):
                key_list[i] = key_list[i].strip("']")
            nested_dict_add_key(slave_file, key_list)
            nested_dict_set(slave_file, key_list, translate(nested_dict_get(master_file, key_list)))
    if 'dictionary_item_added' in diff:
        for idx, value in enumerate(diff['dictionary_item_added']):
            key_list = value.split('[')[1:]
            for i in range(len(key_list)):
                key_list[i] = key_list[i].strip("']")
            nested_dict_delete(slave_file, key_list)
    if 'type_changes' in diff:
        for idx, value in enumerate(diff['type_changes']):
            key_list = value.split('[')[1:]
            for i in range(len(key_list)):
                key_list[i] = key_list[i].strip("']")
            nested_dict_delete(slave_file, key_list)
            nested_dict_set(slave_file, key_list, translate(nested_dict_get(master_file, key_list)))
    return slave_file


def main() -> None:
    path_resources = os.path.join(os.getcwd(), "resource")
    name_main_file = "de.json"
    translation_file_names = ["en.json", "fr.json", "it.json"]
    translation_files = [""] * len(translation_file_names)

    with open(os.path.join(path_resources, name_main_file), 'r') as file:
        main_file = json.load(file)
    print(f"{main_file = }")

    for idx, file_name in enumerate(translation_file_names):
        with open(os.path.join(path_resources, file_name), 'r') as file:
            translation_files[idx] = json.load(file)
        translation_files[idx] = add_missing_keys(main_file, translation_files[idx])
        print(f"translation_files[{idx}] = {translation_files[idx]}")


if __name__ == '__main__':
    print(f"**********| Start  |**********\n")
    _tStart = time.perf_counter()
    main()
    print(f"\n**********| {time.perf_counter() - _tStart:.3f}s |**********")