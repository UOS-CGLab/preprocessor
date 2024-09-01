import numpy as np
import openmesh as om
import json
import os
def clear_json(output_dir):
    with open(output_dir + "/limit_point.json", "w") as f:
        f.write("[]")

def append_to_json(data, output_dir):
    with open(output_dir + "/limit_point.json", "r+") as f:
        json_data = json.load(f)
        f.seek(0)
        if json_data:
            f.truncate(0)
            f.seek(0)
            json_data.append(data)
            json.dump(json_data, f, separators=(', ', ':'))
        else:
            json.dump([data], f, separators=(', ', ':'))

def find_vertex(mesh: om.PolyMesh, v: om.VertexHandle) -> []:
    ret = [v.idx()]
    for e in mesh.voh(v):
        ret.append(mesh.to_vertex_handle(e).idx())
        ret.append(mesh.to_vertex_handle(mesh.next_halfedge_handle(e)).idx())
    return ret


def add_vertex3(mesh: om.PolyMesh, v: om.VertexHandle, idx: int) -> int:
    if mesh.vertex_property("visited", v) is None:
        mesh.set_vertex_property("visited", v, True)
        # mesh.set_vertex_property("id", v, idx)
        # mesh.set_vertex_property("position", v, mesh.point(v))
        idx += 1
    return idx

def add_face3(mesh: om.PolyMesh, f: om.FaceHandle, idx: int) -> int:
    if mesh.face_property("visited", f) is None:
        mesh.set_face_property("visited", f, True)

        for face_verts in mesh.fv(f):
            idx = add_vertex3(mesh, face_verts, idx)
    return idx

def get_limit_point(mesh: om.PolyMesh, output_dir: str, depth: int, idx: int) -> None:
    outputs = []
    for v in mesh.vertices():
        if mesh.valence(v) != 4:
            if mesh.is_boundary(v):
                continue
            for voh in mesh.voh(v):
                ve = mesh.to_vertex_handle(voh)
                vv = mesh.to_vertex_handle(mesh.next_halfedge_handle(voh))

                output = []
                output.append(ve.idx() + idx)
                for veoh in mesh.voh(ve):
                    output.append(mesh.to_vertex_handle(veoh).idx() + idx)
                    output.append(mesh.to_vertex_handle(mesh.next_halfedge_handle(veoh)).idx() + idx)
                outputs.append(output)

                output = []
                output.append(vv.idx() + idx)
                for vvoh in mesh.voh(vv):
                    output.append(mesh.to_vertex_handle(vvoh).idx() + idx)
                    output.append(mesh.to_vertex_handle(mesh.next_halfedge_handle(vvoh)).idx() + idx)
                outputs.append(output)

    data = {
        "depth": depth,
        "data": outputs
    }
    # print(data)

    if depth <= 1:
        clear_json(output_dir)
    append_to_json(data, output_dir)

    # if depth > 0:
    #     for v in mesh.vertices():
    #         if mesh.valence(v) != 4:
    #             if mesh.is_boundary(v):
    #                 continue
    #             n = mesh.valence(v)
    #             e = np.array([0.0, 0.0, 0.0])
    #             f = np.array([0.0, 0.0, 0.0])
    #             # for voh in mesh.voh(v):
    #             #     ve = mesh.to_vertex_handle(voh)
    #             #     vv = mesh.to_vertex_handle(mesh.next_halfedge_handle(voh))
    #             #
    #             #     e += mesh.point(ve)
    #             #     f += mesh.point(vv)
    #
    #             limitpoint = (n * n * mesh.point(v) + 4 * e + f) / (n * (n+5))
    #             mesh.set_point(v, limitpoint)
    #
    #
    #     # export mesh to obj
    #     om.write_mesh(output_dir + "/limit_point" + str(depth) + ".obj", mesh)
    #     exit(0)



def get_extraordinary3(mesh: om.PolyMesh, output_dir: str, depth: int) -> om.PolyMesh:
    idx = 0
    for f in mesh.faces():
        if mesh.valence(f) != 4:
            for v in mesh.fv(f):
                if mesh.vertex_property("todo", v) is None:
                    mesh.set_vertex_property("todo", v, True)

    for v in mesh.vertices():
        if mesh.is_boundary(v):
            continue
        if mesh.valence(v) != 4 or mesh.vertex_property("todo", v):
            for f in mesh.vf(v):
                idx = add_face3(mesh, f, idx)

    for v in mesh.vertices():
        if mesh.vertex_property("visited", v):
            mesh.set_vertex_property("visited2", v, True)

    for v in mesh.vertices():
        if mesh.vertex_property("visited2", v):
            for f in mesh.vf(v):
                idx = add_face3(mesh, f, idx)

    for v in mesh.vertices():
        if mesh.vertex_property("visited", v):
            mesh.set_vertex_property("visited3", v, True)
            mesh.set_vertex_property("interior", v, True)

    for v in mesh.faces():
        if mesh.face_property("visited", v):
            mesh.set_face_property("interior", v, True)

    for v in mesh.vertices():
        if mesh.vertex_property("visited3", v):
            for f in mesh.vf(v):
                idx = add_face3(mesh, f, idx)
    return mesh

def get_extraordinary_2(mesh: om.PolyMesh, depth: int) -> (om.PolyMesh, []):
    new_mesh = om.PolyMesh()

    face_index = []
    edge_index = []
    vert_index = []

    for faces in mesh.faces():
        verts = []
        for v in mesh.fv(faces):
            verts.append(v.idx())
            new_mesh.add_vertex(mesh.point(v))
            new_mesh.set_vertex_property("prev_idx", new_mesh.vertex_handle(v.idx()), v.idx())
            vert_index.append(v.idx())
        new_mesh.add
    return new_mesh

