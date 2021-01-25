print("*** original files:")
with open("inventory_pre_delete.csv", "r") as file:
    lines = file.readlines()
    orig_lines = [l.strip() for l in lines[1:] if "original/2011" in l]
    for line in orig_lines:
        fields = line.split(",")
        key = fields[1].replace('"', "").replace("original/", "")
        print(key)

print("*** external drive files:")
with open("external_drive_find_output/all_pictures_drive_a_beatup.txt", "r") as file:
    lines = file.readlines()
    external_lines = [l.strip() for l in lines[1:] if "2011" in l]
    for line in external_lines:
        print(line)
        fields = line.split("/")
        print(fields)
        key = fields[-1:].replace('"', "")
        print(key)