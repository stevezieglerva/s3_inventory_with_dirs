import json


# Reads inventory list pre-deletion and tries to find it in an inventory of files on the external backup, then creates a sh script to copy
# to the upload directory

print("*** original files:")
with open("inventory_pre_delete.csv", "r") as file:
    lines = file.readlines()
    orig_lines = [l.strip() for l in lines[1:] if "original/" in l]
    original_keys = []
    for line in orig_lines:
        fields = line.split(",")
        year_and_filename = fields[1].replace('"', "").replace("original/", "")
        print(year_and_filename)
        if "/" in year_and_filename:
            key = year_and_filename.split("/")[1]
        else:
            key = year_and_filename
        original_keys.append(key)
count = len(original_keys)
print(f"Original keys: {count}")

print("*** external drive files:")
external_file_lookup = {}
with open("external_drive_find_output/all_pictures_drive_a_beatup.txt", "r") as file:
    lines = file.readlines()
    external_lines = [l.strip() for l in lines[1:]]
    for line in external_lines:
        fields = line.split("/")
        filename = fields[-1:][0]
        filename = filename.replace('"', "")
        external_file_lookup[filename] = line
count = len(external_file_lookup)
print(f"External filenames: {count}")

sh_text = ""
for count, file in enumerate(original_keys):
    try:
        lookup = external_file_lookup[file]
        if "small" not in lookup and "Master Starred Pictures" in lookup:
            absolute_filename = lookup.replace(
                "./Master Starred Pictures/",
                "/Volumes/My Passport/ZieglerPics/Master Starred Pictures/",
            )
            print(f"{file} -> {absolute_filename}")
            sh_text = (
                sh_text + f"echo \"Copying #{count} '{absolute_filename}' ...\" \n"
            )
            sh_text = (
                sh_text
                + f'cp "{absolute_filename}" "/Users/sziegler/Dropbox/ZieglerPics/Master Starred Pictures/copy between computers/Upload" \n\n'
            )
    except KeyError:
        print(f"Can't find '{file}'")


with open("clean_deletion_copy_script.sh", "w") as file:
    file.write(sh_text)
