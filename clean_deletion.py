import json

print("*** original files:")
with open("inventory_pre_delete.csv", "r") as file:
    lines = file.readlines()
    orig_lines = [l.strip() for l in lines[1:] if "original/2011/" in l]
    original_keys = []
    for line in orig_lines:
        fields = line.split(",")
        key = fields[1].replace('"', "").replace("original/2011/", "")
        original_keys.append(key)
count = len(original_keys)
print(f"Original keys: {count}")

print("*** external drive files:")
external_file_lookup = {}
with open("external_drive_find_output/all_pictures_drive_a_beatup.txt", "r") as file:
    lines = file.readlines()
    external_lines = [l.strip() for l in lines[1:] if "2011" in l]
    for line in external_lines:
        fields = line.split("/")
        filename = fields[-1:][0]
        filename = filename.replace('"', "")
        external_file_lookup[filename] = line
count = len(external_file_lookup)
print(f"External filenames: {count}")

for file in original_keys:
    lookup = external_file_lookup[file]
    print(f"{file} -> {lookup}")