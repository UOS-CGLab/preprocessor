from src.get_patch import get_patch
from src.get_extraordinary import get_extraordinary3, get_limit_point
from src.subdiv_CC import subdivision3
from src.phrase import obj_to_json

import openmesh as om
import os
import shutil

def add_dash(output_dir):
    with open(output_dir + "/patch.txt", "a") as file:
        file.write("-\n")

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
    # input_file = "mesh_files/Grass_Block.obj"; print(input_file)
    # input_file = "mesh_files/grass_block2.obj"; print(input_file)
    # input_file = "mesh_files/chest.obj"; print(input_file)
    # input_file = "mesh_files/chest2.obj"; print(input_file)
    #make base.json

    str_name = input_file.split("/")[-1].split(".")[0]

    output_dir = "output/" + str_name
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        shutil.rmtree(output_dir)
        os.makedirs(output_dir)

    obj_to_json(input_file, output_dir + "/base.json")
    mesh = om.read_polymesh(input_file, halfedge_tex_coord=True, vertex_tex_coord=True)

    origin_verticies = mesh.vertices().__len__()

    print("depth of subdivision: ", end="")
    depth = int(input())

    idx = 0
    for i in range(depth + 1):
        print("depth: ", i)
        get_patch(mesh, idx, i, output_dir)

        # with open(output_dir + "/tex_coord.txt", "a") as file:
        #     # for h in mesh.halfedges():
        #     #     v = mesh.to_vertex_handle(h)
        #     for v in mesh.vertices():
        #         tex_coord = mesh.texcoord2D(v)
        #         file.write(str(v.idx() + idx) + ", " + str(round(tex_coord[0], 4)) + ", " + str(round(tex_coord[1], 4)) + ",\n")

        get_extraordinary3(mesh, output_dir, i)

        if i > 0:
            with open(output_dir + "/extra_ordinary" + str(i) + ".txt", "w") as file:
                for f in mesh.faces():
                    if mesh.face_property("patched", f) is True:
                        continue
                    verts = []
                    texcoords = []

                    for vert in mesh.fv(f):
                        verts.append(vert.idx() + idx)
                        texcoord = []
                        for voh in mesh.voh(vert):
                            texcoord.append(mesh.texcoord2D(mesh.opposite_halfedge_handle(voh)))
                        texcoords.append(texcoord)

                    var = []
                    for vert in mesh.fv(f):
                        var.append(mesh.valence(vert))


                    v0_texcoords_data = ""
                    for texcoord in texcoords[0]:
                        v0_texcoords_data += str(texcoord[0]) + ", " + str(texcoord[1]) + ", "
                    v0_texcoords_data = v0_texcoords_data[:-2]

                    v1_texcoords_data = ""
                    for texcoord in texcoords[1]:
                        v1_texcoords_data += str(texcoord[0]) + ", " + str(texcoord[1]) + ", "
                    v1_texcoords_data = v1_texcoords_data[:-2]

                    v2_texcoords_data = ""
                    for texcoord in texcoords[2]:
                        v2_texcoords_data += str(texcoord[0]) + ", " + str(texcoord[1]) + ", "
                    v2_texcoords_data = v2_texcoords_data[:-2]

                    v3_texcoords_data = ""
                    for texcoord in texcoords[3]:
                        v3_texcoords_data += str(texcoord[0]) + ", " + str(texcoord[1]) + ", "
                    v3_texcoords_data = v3_texcoords_data[:-2]

                    v0_len = str(len(texcoords[2]))


                    file.write(str(verts[0]) + ", " + str(verts[1]) + ", " + str(verts[3]) + ", "
                            + str(verts[3]) + ", " + str(verts[1]) + ", " + str(verts[2]) + ", " # check the order
                            + v0_len + ", "
                            + v0_texcoords_data + ", " + v1_texcoords_data + ", " + v3_texcoords_data + ", "
                            + v3_texcoords_data + ", " + v1_texcoords_data + ", " + v2_texcoords_data + "\n")

        if i == depth + 1:
            break

        mesh, idx = subdivision3(mesh, idx, i, output_dir)

        # std::string output_file = output_dir + "/subdivision" + std::to_string(i) + ".obj";
        om.write_mesh(
            filename=output_dir + "/subdivision" + str(i) + ".obj",
            mesh=mesh,
        )

        get_limit_point(mesh, output_dir, i, idx)

        add_dash(output_dir)

        #write mesh with texture
        # filename = "subdiv_" + str(i) + ".obj"
        #
        # om.write_mesh(
        #     filename=filename,
        #     mesh=mesh,
        #     halfedge_tex_coord = True,
        # )
