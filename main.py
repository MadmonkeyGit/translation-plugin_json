import time
import os
import json
from deepdiff import DeepDiff

def add_missing_keys(master_file: dict, slave_file) -> None:
    diff = DeepDiff(master_file, slave_file, ignore_order=False)

    # print(diff['dictionary_item_removed'])
    if 'dictionary_item_removed' in diff:
        for idx, value in enumerate(diff['dictionary_item_removed']):
            # print(f"{idx = }: {value}")
            key_list = value.split('[')[1:]
            for i in range(len(key_list)):
                key_list[i] = key_list[i].strip("']")

            if len(key_list) == 1:
                slave_file[key_list[0]] = master_file[key_list[0]]
            else:
                slave_file[key_list[0]][key_list[1]] = master_file[key_list[0]][key_list[1]]


            # print(f"{key_list = }")
            # print(f"{master_file[key_list[0]][key_list[1]] = }")
    # print(f"{slave_file = }")


def main() -> None:
    path_resources = os.path.join(os.getcwd(), "resource")
    name_main_file = "de.json"
    translation_file_names = ["en.json", "fr.json", "it.json"]
    translation_files = [dict] * len(translation_file_names)

    with open(os.path.join(path_resources, name_main_file), 'r') as file:
        main_file = json.load(file)

    for idx, file_name in enumerate(translation_file_names):
        with open(os.path.join(path_resources, file_name), 'r') as file:
            translation_files[idx] = json.load(file)
        add_missing_keys(main_file, translation_files[idx])
        print(translation_files[idx])


if __name__ == '__main__':
    print(f"**********| Start  |**********\n")
    _tStart = time.perf_counter()
    main()
    print(f"\n**********| {time.perf_counter() - _tStart:.3f}s |**********")