with open("all_pictures_drive_a_beatup.txt", "r") as file:
    formatted_text = '"bucket","key","date","size","parent1","parent2","parent3","parent4","parent5","parent6","parent7","parent8","parent9","parent10"\n'
    for line in file.readlines():
        formatted_line = line.strip()
        filename = formatted_line
        folders = formatted_line.split("/")[:-1]
        parents = {}
        for i in range(1, 11):
            index = f"parent{i}"
            if i <= len(folders):
                parents[index] = folders[i - 1]
            else:
                parents[index] = ""
        new_line = f'"drive_a_beatup","{filename}",,,"{parents["parent1"]}","{parents["parent2"]}","{parents["parent3"]}","{parents["parent4"]}","{parents["parent5"]}","{parents["parent6"]}","{parents["parent7"]}","{parents["parent8"]}","{parents["parent9"]}","{parents["parent10"]}"\n'
        formatted_text = formatted_text + new_line
    print(len(formatted_text))
    with open("all_pictures_drive_a_beatup_formatted.csv", "w") as results_file:
        results_file.write(formatted_text)
