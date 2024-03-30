from src.subdivison import subdivision_cc
from src.generate_table import generate_table
from src.get_patch import get_patch

import openmesh as om


if __name__ == "__main__":
    print("input file: ", end="")
    # input_file = input()
    input_file = "mesh_files/untitled2.obj"; print(input_file)

    mesh = om.read_polymesh(input_file)

    print("depth of subdivision: ", end="")
    depth = int(input())

    idx = 0
    for i in range(depth):
        print("depth: ", i + 1)
        generate_table(mesh, idx)
        idx += mesh.vertices().__len__()
        mesh = subdivision_cc(mesh)
        get_patch(mesh)
