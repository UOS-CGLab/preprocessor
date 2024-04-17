import openmesh as om
import numpy as np


def add_vertex(mesh: om.PolyMesh, new_mesh: om.PolyMesh, v: om.VertexHandle, idx: int) -> int:
    if mesh.vertex_property("visited", v) is None:
        mesh.set_vertex_property("visited", v, True)
        mesh.set_vertex_property("id", v, idx)
        mesh.set_vertex_property("position", v, mesh.point(v))
        new_mesh.add_vertex(mesh.point(v))
        idx += 1
    return idx


def add_face(mesh: om.PolyMesh, new_mesh: om.PolyMesh, v: om.VertexHandle, idx: int) -> int:

    for f in mesh.vf(v):
        if mesh.face_property("visited", f) is None:
            mesh.set_face_property("visited", f, True)

            for face_verts in mesh.fv(f):
                idx = add_vertex(mesh, new_mesh, face_verts, idx)

            new_mesh.add_faces([[
                mesh.vertex_property("id", face_verts) for face_verts in mesh.fv(f)
            ]])
    return idx


def get_extraordinary(mesh: om.PolyMesh) -> om.PolyMesh:
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
                new_mesh.set_vertex_property("prev_idx", new_mesh.vertex_handle(idx - 1), idx - 2)
                idx = add_face(mesh, new_mesh, corner, idx)

            for corner in v_corners3:
                idx = add_vertex(mesh, new_mesh, mesh.vertex_handle(corner), idx)
                new_mesh.set_vertex_property("prev_idx", new_mesh.vertex_handle(idx - 1), idx - 2)
                idx = add_face(mesh, new_mesh, mesh.vertex_handle(corner), idx)

    return new_mesh
