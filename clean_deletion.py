import json


# Reads inventory list pre-deletion and tries to find it in an inventory of files on the external backup, then creates a sh script to copy
# to the upload directory

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

sh_text = ""
for count, file in enumerate(original_keys):
    lookup = external_file_lookup[file]
    absolute_filename = lookup.replace(
        "./Master Starred Pictures/",
        "/Volumes/My Passport/ZieglerPics/Master Starred Pictures/",
    )
    print(f"{file} -> {absolute_filename}")
    sh_text = sh_text + f"echo \"Copying #{count} '{absolute_filename}' ...\" \n"
    sh_text = (
        sh_text
        + f'cp "{absolute_filename}" "/Users/sziegler/Dropbox/ZieglerPics/Master Starred Pictures/copy between computers/Upload" \n\n'
    )

with open("clean_deletion_copy_script.sh", "w") as file:
    file.write(sh_text)
