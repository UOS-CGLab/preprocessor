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

    """
    v1 v2 v3
    v4 v5 v6
    x  x  init
    
    """

    idx = 0

    for v in mesh.vertices():
        val = mesh.valence(v)
        if val > 2 and val != 4 and not mesh.is_boundary(v):
            idx = add_vertex(mesh, new_mesh, v, idx)

            v_verts = [i for i in mesh.vv(v)]

            # for f in mesh.vf(v):
            #     mesh.set_face_property("visited", f, True)


            v_corners = [mesh.to_vertex_handle(mesh.next_halfedge_handle(mesh.find_halfedge(v, _))) for _ in mesh.vv(v)]

            for corner in v_corners:
                idx = add_vertex(mesh, new_mesh, corner, idx)
                idx = add_face(mesh, new_mesh, corner, idx)







            # for _ in v_verts:
            #     # v -> _
            #     edge = mesh.find_halfedge(v, _)
            #
            #     v1 = mesh.to_vertex_handle(edge)
            #     mesh.set_vertex_property("id", v1, idx)
            #     mesh.set_vertex_property("position", v1, mesh.point(v1))
            #     new_mesh.add_vertex(mesh.point(v1));
            #     idx += 1
            #
            #     v2 = mesh.to_vertex_handle(mesh.next_halfedge_handle(edge))
            #     mesh.set_vertex_property("id", v2, idx)
            #     mesh.set_vertex_property("position", v2, mesh.point(v2))
            #     new_mesh.add_vertex(mesh.point(v2));
            #     idx += 1
            #
            #     v3 = mesh.to_vertex_handle(mesh.next_halfedge_handle(mesh.next_halfedge_handle(edge)))
            #     mesh.set_vertex_property("id", v3, idx)
            #     mesh.set_vertex_property("position", v3, mesh.point(v3))
            #     new_mesh.add_vertex(mesh.point(v3));
            #     idx += 1
            #
            #     new_mesh.add_faces([[
            #         mesh.vertex_property("id", v),
            #         mesh.vertex_property("id", v1),
            #         mesh.vertex_property("id", v2),
            #         mesh.vertex_property("id", v3)
            #     ]])

    return new_mesh
