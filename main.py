from src.get_patch import get_patch
from src.get_extraordinary import get_extraordinary
from src.subdiv_CC import subdivision

import openmesh as om


if __name__ == "__main__":
    print("input file: ", end="")
    # input_file = input()
    # input_file = "mesh_files/untitled2.obj"; print(input_file)
    # input_file = "mesh_files/Car.obj"; print(input_file)
    input_file = "mesh_files/suzanne.obj"; print(input_file)
    str_name = input_file.split("/")[-1].split(".")[0]


    mesh = om.read_polymesh(input_file)

    print("depth of subdivision: ", end="")
    depth = int(input())

    # idx = 0
    # for i in range(depth):
    #     print("depth: ", i + 1)
    #     generate_table(mesh, idx)
    #     idx += mesh.vertices().__len__()
    #     mesh = subdivision_cc(mesh)
    #
    #     _ = get_patch(mesh)
    #     if _ != 0:
    #         new_mesh = get_extraordinary(mesh)
    #         om.write_mesh("output_extraordinary_" + str_name + str(i+1) + ".obj", new_mesh)
    #         # new_mesh = subdivision_cc(new_mesh)


    for i in range(depth + 1):
        print("depth: ", i)
        get_patch(mesh)
        mesh = get_extraordinary(mesh)
        om.write_mesh("output_2_" + str_name + str(i + 1) + ".obj", mesh)
        # mesh = subdivision_cc(mesh)
        mesh = subdivision(mesh)

    om.write_mesh("output.obj", mesh)
