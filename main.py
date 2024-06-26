from src.get_patch import get_patch
from src.get_extraordinary import get_extraordinary3
from src.subdiv_CC import subdivision3
from src.subdiv_CC import subdivision_2
from src.phrase import obj_to_json


import openmesh as om
import os
import shutil

def print_coord(mesh):
    with open("mesh_cord.txt", "w") as file:
        for v in mesh.vertices():
            coord = mesh.point(v)
            file.write(str(coord[0]) + ", " + str(coord[1]) + ", " + str(coord[2]) + "\n")


def add_dash(output_dir):
    with open(output_dir + "/patch.txt", "a") as file:
        file.write("-\n")


def remove_files(output_dir):
    with open(output_dir + "/patch.txt", "w") as file:
        file.write("")
    # with open("triangle.txt", "w") as file:
    #     file.write("")


def write_info_file(coord):
    with open("coord.txt", "a") as file:
        #coord 소수점 3자리까지만 출력
        file.write(str(round(coord[0], 3)) + ", " + str(round(coord[1], 3)) + ", " + str(round(coord[2], 3)) + ", 0,\n")
        #file.write(str(coord[0]) + ", " + str(coord[1]) + ", " + str(coord[2]) + ", 0,\n")


if __name__ == "__main__":
    print("input file: ", end="")
    # input_file = input()
    # input_file = "mesh_files/cone.obj"; print(input_file)
    # input_file = "mesh_files/untitled2.obj"; print(input_file)
    # input_file = "mesh_files/Car.obj"; print(input_file)
    # input_file = "mesh_files/monsterfrog_5copies.obj"; print(input_file)
    # input_file = "mesh_files/shuttle.obj"; print(input_file)
    # input_file = "mesh_files/hand.obj"; print(input_file)
    # input_file = "mesh_files/dog.obj"; print(input_file)
    # input_file = "mesh_files/donut.obj"; print(input_file)
    # input_file = "mesh_files/donut2.obj"; print(input_file)
    # input_file = "mesh_files/donut3.obj"; print(input_file)
    # input_file = "mesh_files/strange2.obj"; print(input_file)
    # input_file = "mesh_files/strange.obj"; print(input_file)
    input_file = "mesh_files/monsterfrog.obj"; print(input_file)
    # input_file = "mesh_files/cow-nonormals.obj"; print(input_file)
    # input_file = "mesh_files/monsterfrog_5copies.obj"; print(input_file)
    # input_file = "mesh_files/suzanne.obj"; print(input_file)

    #make base.json

    str_name = input_file.split("/")[-1].split(".")[0]

    output_dir = "output/" + str_name
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        shutil.rmtree(output_dir)
        os.makedirs(output_dir)

    obj_to_json(input_file, output_dir + "/base.json")

    mesh = om.read_polymesh(input_file)
    # print_coord(mesh)
    origin_verticies = mesh.vertices().__len__()

    print("depth of subdivision: ", end="")
    depth = int(input())

    remove_files(output_dir)

    idx = 0

    for i in range(depth + 1):
        print("depth: ", i)
        get_patch(mesh, idx, i, output_dir)

        get_extraordinary3(mesh, i)

        with open(output_dir + "/extra_ordinary" + str(i) + ".txt", "w") as file:
            for f in mesh.faces():
                verts = []
                var = 0
                for vert in mesh.fv(f):
                    var += mesh.valence(vert)
                    verts.append(vert.idx() + idx)
                if verts.__len__() == 16:
                    continue
                file.write(str(verts[0]) + ", " + str(verts[1]) + ", " + str(verts[3]) + ", "
                           + str(verts[3]) + ", " + str(verts[1]) + ", " + str(verts[2]) + ",\n")

        if i == depth + 1:
            break

        mesh, idx = subdivision3(mesh, idx, i, output_dir)

        # om.write_mesh(output_dir + "/subdiv_output_" + str_name + str(i) + ".obj", mesh)

        add_dash(output_dir)


    # om.write_mesh(output_dir + "/output.obj", mesh)
    # with open(output_dir + "/extra_ordinary.txt", "w") as file:
    #     for f in mesh.faces():
    #         verts = []
    #         for vert in mesh.fv(f):
    #             if mesh.valence(vert) != 4:
    #                 continue
    #             verts.append(vert.idx() + idx)
    #         if verts.__len__() <= 3:
    #             continue
    #         file.write(str(verts[0]) + ", " + str(verts[1]) + ", " + str(verts[3]) + ", "
    #                    + str(verts[3]) + ", " + str(verts[1]) + ", " + str(verts[2]) + ",\n")
    #
    # for v in mesh.vertices():
    #     coord = mesh.point(v)
    #     write_info_file(coord)
    # add_dash()
