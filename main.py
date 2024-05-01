from src.get_patch import get_patch
from src.get_extraordinary import get_extraordinary
from src.subdiv_CC import subdivision
from src.generate_table import generate_table
from src.export import remove_all_files

import openmesh as om


def print_coord(mesh):
    with open("mesh_cord.txt", "w") as file:
        for v in mesh.vertices():
            coord = mesh.point(v)
            file.write(str(coord[0]) + ", " + str(coord[1]) + ", " + str(coord[2]) + "\n")


def add_dash():
    with open("triangle.txt", "a") as file:
        file.write("-\n")


def remove_files():
    with open("coord.txt", "w") as file:
        file.write("")
    with open("patch.txt", "w") as file:
        file.write("")
    with open("triangle.txt", "w") as file:
        file.write("")


def write_info_file(coord):
    with open("coord.txt", "a") as file:
        #coord 소수점 3자리까지만 출력
        file.write(str(round(coord[0], 3)) + ", " + str(round(coord[1], 3)) + ", " + str(round(coord[2], 3)) + ", 0,\n")
        #file.write(str(coord[0]) + ", " + str(coord[1]) + ", " + str(coord[2]) + ", 0,\n")


if __name__ == "__main__":
    print("input file: ", end="")
    # input_file = input()
    input_file = "mesh_files/cone.obj"; print(input_file)
    # input_file = "mesh_files/untitled2.obj"; print(input_file)
    # input_file = "mesh_files/Car.obj"; print(input_file)
    # input_file = "mesh_files/suzanne.obj";
    # input_file = "mesh_files/shuttle.obj"; print(input_file)
    # input_file = "mesh_files/hand.obj"; print(input_file)
    # input_file = "mesh_files/dog.obj"; print(input_file)
    # input_file = "mesh_files/donut.obj"; print(input_file)
    # input_file = "mesh_files/donut2.obj"; print(input_file)
    # input_file = "mesh_files/donut3.obj"; print(input_file)
    str_name = input_file.split("/")[-1].split(".")[0]

    mesh = om.read_polymesh(input_file)
    print_coord(mesh)

    print("depth of subdivision: ", end="")
    depth = int(input())

    remove_files()
    remove_all_files(depth)

    idx = 0
    # idx2 = 0
    for i in range(depth + 1):
        print("depth: ", i)
        get_patch(mesh, idx)
        # # print all vertex coordinates
        # for v in mesh.vertices():
        #     coord = mesh.point(v)
        #     write_info_file(coord)
        # idx += mesh.vertices().__len__()
        mesh = get_extraordinary(mesh)
        # if i == 0: print_coord(mesh)
        om.write_mesh("output_2_" + str_name + str(i) + ".obj", mesh)
        # mesh = subdivision_cc(mesh)

        if i == depth:
            break

        generate_table(mesh, idx, 0, i)
        idx += mesh.vertices().__len__()
        mesh, _ = subdivision(mesh, idx)

        # idx2 = idx
        add_dash()

    om.write_mesh("output.obj", mesh)
    with open("extra_ordinary.txt", "w") as file:
        for f in mesh.faces():
            verts = []
            for vert in mesh.fv(f):
                verts.append(vert.idx() + idx)
            file.write(str(verts[0]) + ", " + str(verts[1]) + ", " + str(verts[2]) + ", "
                       + str(verts[2]) + ", " + str(verts[1]) + ", " + str(verts[3]) + ",\n")

    for v in mesh.vertices():
        coord = mesh.point(v)
        write_info_file(coord)
    add_dash()
