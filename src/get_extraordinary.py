import openmesh as om
import numpy as np


def add_vertex(mesh: om.PolyMesh, new_mesh: om.PolyMesh, v: om.VertexHandle, idx: int) -> int:
    if mesh.vertex_property("visited", v) is None:
        mesh.set_vertex_property("visited", v, True)
        mesh.set_vertex_property("id", v, idx)
        mesh.set_vertex_property("position", v, mesh.point(v))
        new_mesh.add_vertex(mesh.point(v))
        new_mesh.set_vertex_property("prev_idx", new_mesh.vertex_handle(idx), v.idx())
        idx += 1
    return idx


def add_face(mesh: om.PolyMesh, new_mesh: om.PolyMesh, v: om.VertexHandle, idx: int) -> int:

    for f in mesh.vf(v):
        if mesh.face_property("visited", f) is None:
            mesh.set_face_property("visited", f, True)
            mesh.set_face_property("prev_fidx", f, idx)

            for face_verts in mesh.fv(f):
                idx = add_vertex(mesh, new_mesh, face_verts, idx)

            new_mesh.add_faces([[
                mesh.vertex_property("id", face_verts) for face_verts in mesh.fv(f)
            ]])
            # face_idx = new_mesh.faces().__len__() - 1
            new_mesh.set_face_property("prev_idx", new_mesh.face_handle(new_mesh.faces().__len__() - 1), f.idx())
    return idx


def get_extraordinary(mesh: om.PolyMesh, depth: int) -> om.PolyMesh:
    new_mesh = om.PolyMesh()

    idx = 0
    for v in mesh.vertices():
        val = mesh.valence(v)
        if val > 2 and val != 4 and not mesh.is_boundary(v):
            idx = add_vertex(mesh, new_mesh, v, idx)
            idx = add_face(mesh, new_mesh, v, idx)

            # for f in mesh.vf(v):
            #     mesh.set_face_property("visited", f, True)

            v_corners = [mesh.to_vertex_handle(mesh.next_halfedge_handle(mesh.find_halfedge(v, _))) for _ in mesh.vv(v)]

            v_corners2 = [mesh.to_vertex_handle(mesh.next_halfedge_handle(mesh.opposite_halfedge_handle(mesh.prev_halfedge_handle(mesh.opposite_halfedge_handle(mesh.next_halfedge_handle(mesh.find_halfedge(v, _))))))) for _ in mesh.vv(v)]

            v_corners3 = [mesh.from_vertex_handle(mesh.prev_halfedge_handle(mesh.opposite_halfedge_handle(mesh.next_halfedge_handle(mesh.next_halfedge_handle(mesh.find_halfedge(v, _)))))).idx() for _ in mesh.vv(v)]

            # for corner in v_corners:
            #     idx = add_vertex(mesh, new_mesh, corner, idx)
            #     idx = add_face(mesh, new_mesh, corner, idx)

            for corner in v_corners2:
                idx = add_vertex(mesh, new_mesh, corner, idx)
                # new_mesh.set_vertex_property("prev_idx", new_mesh.vertex_handle(idx - 1), idx - 2)
                idx = add_face(mesh, new_mesh, corner, idx)
                # new_mesh.set_face_property("prev_idx", )

            for corner in v_corners3:
                idx = add_vertex(mesh, new_mesh, mesh.vertex_handle(corner), idx)
                # new_mesh.set_vertex_property("prev_idx", new_mesh.vertex_handle(idx - 1), idx - 2)
                idx = add_face(mesh, new_mesh, mesh.vertex_handle(corner), idx)

    return new_mesh


def add_vertex2(mesh: om.PolyMesh, new_mesh: om.PolyMesh, v: om.VertexHandle, idx: int) -> int:
    if mesh.vertex_property("visited", v) is None:
        mesh.set_vertex_property("visited", v, True)
        mesh.set_vertex_property("id", v, idx)
        mesh.set_vertex_property("position", v, mesh.point(v))
        new_mesh.add_vertex(mesh.point(v))
        new_mesh.set_vertex_property("prev_idx", new_mesh.vertex_handle(idx), v.idx())
        idx += 1
    return idx


def add_face2(mesh: om.PolyMesh, new_mesh: om.PolyMesh, f: om.FaceHandle, idx: int) -> int:
    if mesh.face_property("visited", f) is None:
        mesh.set_face_property("visited", f, True)

        for face_verts in mesh.fv(f):
            idx = add_vertex2(mesh, new_mesh, face_verts, idx)

        new_mesh.add_faces([[
            mesh.vertex_property("id", face_verts) for face_verts in mesh.fv(f)
        ]])
        # face_idx = new_mesh.faces().__len__() - 1
        new_mesh.set_face_property("prev_idx", new_mesh.face_handle(new_mesh.faces().__len__() - 1), f.idx())

        if mesh.face_property("patched", f) is True:
            new_mesh.set_face_property("patched", new_mesh.face_handle(new_mesh.faces().__len__() - 1), True)

    return idx

def get_extraordinary2(mesh: om.PolyMesh, depth: int) -> om.PolyMesh:
    new_mesh = om.PolyMesh()

    if depth >= 0:

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
                    idx = add_face2(mesh, new_mesh, f, idx)

        for v in mesh.vertices():
            if mesh.vertex_property("visited", v):
                mesh.set_vertex_property("visited2", v, True)

        for v in mesh.vertices():
            if mesh.vertex_property("visited2", v):
                for f in mesh.vf(v):
                    idx = add_face2(mesh, new_mesh, f, idx)
        for v in mesh.vertices():
            if mesh.vertex_property("visited", v):
                mesh.set_vertex_property("visited3", v, True)

        for v in mesh.vertices():
            if mesh.vertex_property("visited3", v):
                for f in mesh.vf(v):
                    idx = add_face2(mesh, new_mesh, f, idx)
    else:
        idx = 0

        for v in mesh.vertices():
            if mesh.is_boundary(v):
                continue




    return new_mesh



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


def get_extraordinary3(mesh: om.PolyMesh, depth: int) -> om.PolyMesh:
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

