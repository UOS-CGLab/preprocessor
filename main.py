from src.get_patch import get_patch
from src.get_extraordinary import get_extraordinary3, get_limit_point
from src.subdiv_CC import subdivision3
from src.subdiv_CC import subdivision_2
from src.phrase import obj_to_json

import openmesh as om
import os
import shutil
from PIL import Image
import numpy as np


def get_tex_coord(file_path):
    tex_coords = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            if line.startswith('vt '):
                parts = line.split()
                u = float(parts[1])
                v = float(parts[2])
                tex_coords.append((u, v))

    return tex_coords

def add_dash(output_dir):
    with open(output_dir + "/patch.txt", "a") as file:
        file.write("-\n")


def convert_coord(mesh: om.PolyMesh, str_name: str):
    texture_image = Image.open("./mesh_files/" + str_name + ".png")
    texture_image = texture_image.convert('RGB')
    width, height = texture_image.size
    default_color = (0, 0, 0)  # Default color, e.g., black

    for v in mesh.vertices():
        tex_coord = mesh.texcoord2D(v)
        if np.isnan(tex_coord).any() or tex_coord[0] < 0 or tex_coord[0] > 1 or tex_coord[1] < 0 or tex_coord[1] > 1:
            color = default_color
        else:
            x = int(tex_coord[0] * width)
            y = int(tex_coord[1] * height)
            # Ensure x and y are within the image bounds
            x = max(0, min(x, width - 1))
            y = max(0, min(y, height - 1))
            color = texture_image.getpixel((x, y))
        mesh.set_point(v, np.array([color[0], color[1], color[2]]))


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
    # input_file = "mesh_files/bigguy.obj"; print(input_file)
    # input_file = "mesh_files/teapot.obj"; print(input_file)
    # input_file = "mesh_files/lamp.obj"; print(input_file)
    # input_file = "mesh_files/homer.obj"; print(input_file)

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
    tex_coord = get_tex_coord(input_file)
    for h in mesh.halfedges():
        v = mesh.to_vertex_handle(h)
        mesh.set_texcoord2D(h, tex_coord[v.idx()])
    for v in mesh.vertices():
        mesh.set_texcoord2D(v, tex_coord[v.idx()])

    origin_verticies = mesh.vertices().__len__()

    print("depth of subdivision: ", end="")
    depth = int(input())

    # convert_coord(mesh, str_name)


    idx = 0
    for i in range(depth + 1):
        print("depth: ", i)
        get_patch(mesh, idx, i, output_dir)

        if i != 0:
            for h in mesh.halfedges():
                v = mesh.to_vertex_handle(h)
                mesh.set_texcoord2D(h, mesh.texcoord2D(v))

        with open(output_dir + "/tex_coord.txt", "a") as file:
            # for h in mesh.halfedges():
            #     v = mesh.to_vertex_handle(h)
            for v in mesh.vertices():
                tex_coord = mesh.texcoord2D(v)
                file.write(str(v.idx() + idx) + ", " + str(round(tex_coord[0], 4)) + ", " + str(round(tex_coord[1], 4)) + ",\n")

        get_extraordinary3(mesh, output_dir, i)

        if i != 0:
            with open(output_dir + "/extra_ordinary" + str(i) + ".txt", "w") as file:
                for f in mesh.faces():
                    if mesh.face_property("patched", f) is True:
                        continue
                    verts = []
                    for vert in mesh.fv(f):
                        verts.append(vert.idx() + idx)
                    file.write(str(verts[0]) + ", " + str(verts[1]) + ", " + str(verts[3]) + ", "
                               + str(verts[3]) + ", " + str(verts[1]) + ", " + str(verts[2]) + ",\n")

        if i == depth + 1:
            break

        mesh, idx = subdivision3(mesh, idx, i, output_dir)

        get_limit_point(mesh, output_dir, i)

        add_dash(output_dir)
