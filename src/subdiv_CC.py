import openmesh
import numpy as np


def compute_CC_vertex(mesh, v):
    idx_set = []
    k = mesh.valence(v)
    alpha = 1.0 / (4.0 * k)
    beta = 6.0 / (4.0 * k)
    p = (1 - alpha - beta) * mesh.point(v)
    for vv in mesh.vv(v):
        p = p + (beta / k) * mesh.point(vv)
    for h in mesh.voh(v):
        p = p + (alpha / k) * mesh.point(mesh.to_vertex_handle(mesh.next_halfedge_handle(h)))
    return p


def compute_CC_face(mesh, f):
    idx_set = []
    p = np.array([0, 0, 0])
    for v in mesh.fv(f):
        p = p + mesh.point(v)
        idx_set.append(v.idx())
    p = p / mesh.valence(f)
    return p, idx_set


def compute_CC_edge(mesh, e):
    p = np.array([0, 0, 0])

    h = mesh.halfedge_handle(e, 0)
    p = p + 6.0 * mesh.point(mesh.to_vertex_handle(h))
    h = mesh.next_halfedge_handle(h)
    p = p + 1.0 * mesh.point(mesh.to_vertex_handle(h))
    h = mesh.next_halfedge_handle(h)
    p = p + 1.0 * mesh.point(mesh.to_vertex_handle(h))

    h = mesh.halfedge_handle(e, 1)
    p = p + 6.0 * mesh.point(mesh.to_vertex_handle(h))
    h = mesh.next_halfedge_handle(h)
    p = p + 1.0 * mesh.point(mesh.to_vertex_handle(h))
    h = mesh.next_halfedge_handle(h)
    p = p + 1.0 * mesh.point(mesh.to_vertex_handle(h))

    p = p / 16.0
    return p


def subdivision(mesh: openmesh.PolyMesh, idx: int) -> (openmesh.PolyMesh, int):
    mesh_next = openmesh.PolyMesh()
    faces = []
    edges = []
    vertices = []

    idx = 0
    for v in mesh.vertices():
        p = compute_CC_vertex(mesh, v)
        mesh.set_vertex_property("id", v, idx)
        mesh.set_vertex_property("position", v, p)
        mesh_next.add_vertex(p)
        idx = idx + 1

    for f in mesh.faces():
        p, face_set = compute_CC_face(mesh, f)
        mesh.set_face_property("id", f, idx)
        mesh.set_face_property("position", f, p)
        mesh_next.add_vertex(p)
        faces = faces + face_set
        idx = idx + 1

    for e in mesh.edges():
        p = compute_CC_edge(mesh, e)
        mesh.set_edge_property("id", e, idx)
        mesh.set_edge_property("position", e, p)
        mesh_next.add_vertex(p)
        idx = idx + 1

    for f in mesh.faces():
        v0 = mesh.face_property("id", f)
        for h in mesh.fh(f):
            v1 = mesh.edge_property("id", mesh.edge_handle(h))
            v2 = mesh.vertex_property("id", mesh.to_vertex_handle(h))
            v3 = mesh.edge_property("id", mesh.edge_handle(mesh.next_halfedge_handle(h)))
            mesh_next.add_faces([[v0, v1, v2, v3]])

    return mesh_next, idx
