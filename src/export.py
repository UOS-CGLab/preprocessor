def remove_all_files(depth_of_subdivision):
    path = "./output/"
    for i in range(depth_of_subdivision):
        with open(path + "face_offsets" + str(i) + ".txt", "w") as file:
            file.write("")
        with open(path + "face_valences" + str(i) + ".txt", "w") as file:
            file.write("")
        with open(path + "face_data" + str(i) + ".txt", "w") as file:
            file.write("")
        with open(path + "edge_data" + str(i) + ".txt", "w") as file:
            file.write("")
        with open(path + "vertex_offsets" + str(i) + ".txt", "w") as file:
            file.write("")
        with open(path + "vertex_valences" + str(i) + ".txt", "w") as file:
            file.write("")
        with open(path + "vertex_data" + str(i) + ".txt", "w") as file:
            file.write("")


def export_to_txt(f_offsets, f_valences, f_data, e_data, v_offsets, v_valences, v_data, depth):
    path = "./output/"
    with open(path + "face_offsets" + str(depth) + ".txt", "a") as file:
        for i in f_offsets:
            file.write(str(i) + ", ")
    with open(path + "face_valences" + str(depth) + ".txt", "a") as file:
        for i in f_valences:
            file.write(str(i) + ", ")
    with open(path + "face_data" + str(depth) + ".txt", "a") as file:
        for i in f_data:
            file.write(str(i) + ", ")
    with open(path + "edge_data" + str(depth) + ".txt", "a") as file:
        for i in e_data:
            file.write(str(i) + ", ")
    with open(path + "vertex_offsets" + str(depth) + ".txt", "a") as file:
        for i in v_offsets:
            file.write(str(i) + ", ")
    with open(path + "vertex_valences" + str(depth) + ".txt", "a") as file:
        for i in v_valences:
            file.write(str(i) + ", ")
    with open(path + "vertex_data" + str(depth) + ".txt", "a") as file:
        for i in v_data:
            file.write(str(i) + ", ")
