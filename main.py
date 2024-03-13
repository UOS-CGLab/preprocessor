from src.obj_to_meshdata import obj_to_meshdata
from src.generate_lookup_table import generate_lookup_table


if __name__ == "__main__":
    print("input file: ", end="")
    # input_file = input()
    input_file = "mesh_files/untitled2.obj"; print(input_file)



    mesh = obj_to_meshdata(input_file)

    print("depth of subdivision: ", end="")
    depth = int(input())

    for i in range(depth):
        mesh = generate_lookup_table(mesh)
        print("depth: ", i+1)

    # draw
