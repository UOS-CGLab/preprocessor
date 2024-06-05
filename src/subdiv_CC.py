import openmesh as om
import numpy as np
from src.to_json import to_json
from src.to_json import to_json2

def compute_CC_vertex(mesh, v):
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
    return p


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


def subdivision(mesh: om.PolyMesh, prev_idx: int) -> (om.PolyMesh, int):
    mesh_next = om.PolyMesh()
    faces = []

    idx = 0
    for v in mesh.vertices():
        p = compute_CC_vertex(mesh, v)
        mesh.set_vertex_property("id", v, idx)
        mesh.set_vertex_property("position", v, p)
        mesh_next.add_vertex(p)
        idx = idx + 1

    for f in mesh.faces():
        p = compute_CC_face(mesh, f)
        mesh.set_face_property("id", f, idx)
        mesh.set_face_property("position", f, p)
        mesh_next.add_vertex(p)
        faces = faces
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

    return mesh_next, idx + prev_idx


def subdivision2(mesh: om.PolyMesh, prev_idx: int, depth: int) -> (om.PolyMesh, int):
    if depth == 0:
        origin_verticies = prev_idx
        prev_idx = 0


    f_offsets = []
    f_valances = []
    f_indices = []
    f_data = []
    e_data = []
    e_indices = []
    v_offsets = []
    v_data = []
    v_index = []
    v_valances = []
    v_indices = []
    mesh_next = om.PolyMesh()

    if depth == 0:
        prev_idx2 = prev_idx + origin_verticies
    else:
        prev_idx2 = prev_idx

    offset = 0
    idx = 0

    for f in mesh.faces():
        val = 0
        # ----- subdivision part -------
        p = compute_CC_face(mesh, f) #p = np.array([0, 0, 0])
        mesh.set_face_property("id", f, idx)
        mesh.set_face_property("position", f, p)
        fidx = mesh.face_property("prev_idx", f)
        mesh.set_face_property("idx", f, prev_idx2 + fidx)
        mesh_next.add_vertex(p)

        # ---- table part -----

        for vert in mesh.fv(f):
            val += 1
            f_data.append(mesh.vertex_property("prev_idx", vert) + prev_idx)
            # f_data.append(vert.idx() + prev_idx)

        f_offsets.append(offset)
        f_valances.append(val)
        offset += val

        f_indices.append(prev_idx2 + idx)

        idx = idx + 1

        if mesh.is_boundary(f):
            continue

        for v in mesh.fv(f):
            mesh.set_vertex_property("valid", v, True)
        for e in mesh.fe(f):
            mesh.set_edge_property("valid", e, True)


    for e in mesh.edges():
        if mesh.edge_property("valid", e) is None:
            continue
        # ---- subdivision part ----
        p = compute_CC_edge(mesh, e)#p = np.array([0, 0, 0])
        mesh.set_edge_property("id", e, idx)
        mesh.set_edge_property("position", e, p)
        mesh_next.add_vertex(p)

        # ---- table part ----
        e0 = mesh.halfedge_handle(e, 0)
        e1 = mesh.halfedge_handle(e, 1)
        v0 = mesh.to_vertex_handle(e0)
        v1 = mesh.to_vertex_handle(e1)
        f0 = mesh.face_handle(e0)
        f1 = mesh.face_handle(e1)

        e_data.append(mesh.vertex_property("prev_idx", v0) + prev_idx)
        e_data.append(mesh.vertex_property("prev_idx", v1) + prev_idx)
        e_data.append(mesh.face_property("idx", f0)) #e_data.append(mesh.face_property("prev_idx", f0) + prev_idx2)
        e_data.append(mesh.face_property("idx", f1)) #e_data.append(mesh.face_property("prev_idx", f1) + prev_idx2)

        # e_data.append(v0.idx() + prev_idx)
        # e_data.append(v1.idx() + prev_idx)
        # e_data.append(f0.idx() + prev_idx2)
        # e_data.append(f1.idx() + prev_idx2)

        e_indices.append(idx + prev_idx2)

        idx = idx + 1

    offset = 0
    for v in mesh.vertices():
        if mesh.vertex_property("valid", v) is None:
            continue
        # ---- subdivision part ----
        p = compute_CC_vertex(mesh, v)# p = np.array([0, 0, 0])
        mesh.set_vertex_property("id", v, idx)
        mesh.set_vertex_property("position", v, p)
        mesh_next.add_vertex(p)

        # ---- table part ----
        val = 0
        for face in mesh.vf(v):
            val += 1
            v_data.append(mesh.face_property("idx", face)) # v_data.append(mesh.face_property("prev_idx", face) + prev_idx2)
            # v_data.append(face.idx() + prev_idx2)

        for edge in mesh.ve(v):
            v0 = mesh.to_vertex_handle(mesh.halfedge_handle(edge, 0))
            v1 = mesh.to_vertex_handle(mesh.halfedge_handle(edge, 1))
            if v0 != v:
                # v_data.append(v0.idx() + prev_idx)
                v_data.append(mesh.vertex_property("prev_idx", v0) + prev_idx)
            if v1 != v:
                # v_data.append(v1.idx() + prev_idx)
                v_data.append(mesh.vertex_property("prev_idx", v1) + prev_idx)
            val += 1

        v_offsets.append(offset)
        v_valances.append(val)
        offset += val

        v_index.append(mesh.vertex_property("prev_idx", v) + prev_idx)
        v_indices.append(idx + prev_idx2)
        idx = idx + 1

    for f in mesh.faces():
        if mesh.is_boundary(f):
            continue
        v0 = mesh.face_property("id", f)
        is_not_boundary = all(not mesh.is_boundary(v) for v in mesh.fv(f))
        if not is_not_boundary:
            continue
        for h in mesh.fh(f):
            v1 = mesh.edge_property("id", mesh.edge_handle(h))
            v2 = mesh.vertex_property("id", mesh.to_vertex_handle(h))
            v3 = mesh.edge_property("id", mesh.edge_handle(mesh.next_halfedge_handle(h)))
            mesh_next.add_faces([[v0, v1, v2, v3]])
            if mesh.face_property("patched", f) is True:
                mesh_next.set_face_property("patched", mesh_next.face_handle(mesh_next.faces().__len__() - 1), True)



    to_json(v_indices, v_offsets, v_valances, v_index, v_data, e_indices, e_data, f_indices, f_offsets, f_valances, f_data, depth)

    return mesh_next, prev_idx2 + idx




def subdivision3(mesh: om.PolyMesh, prev_idx: int, depth: int) -> (om.PolyMesh, int):

    f_offsets = []
    f_valances = []
    f_indices = []
    f_data = []
    e_data = []
    e_indices = []
    v_offsets = []
    v_data = []
    v_index = []
    v_valances = []
    v_indices = []
    mesh_next = om.PolyMesh()

    fidx = prev_idx + mesh.vertices().__len__()
    offset = 0
    idx = 0

    for f in mesh.faces():
        if mesh.face_property("visited") is None:
            continue
        val = 0
        # ----- subdivision part -------
        p = compute_CC_face(mesh, f) #p = np.array([0, 0, 0])
        mesh.set_face_property("id", f, idx)
        mesh.set_face_property("position", f, p)
        mesh_next.add_vertex(p)

        # ---- table part -----

        for vert in mesh.fv(f):
            val += 1
            f_data.append(vert.idx() + prev_idx)
            # f_data.append(vert.idx() + prev_idx)

        f_offsets.append(offset)
        f_valances.append(val)
        offset += val

        f_indices.append(idx + fidx)

        idx = idx + 1

        # if mesh.is_boundary(f):
        #     continue
        if mesh.face_property("interior", f) is None:
            continue

        for v in mesh.fv(f):
            mesh.set_vertex_property("valid", v, True)
        for e in mesh.fe(f):
            mesh.set_edge_property("valid", e, True)


    for e in mesh.edges():
        if mesh.edge_property("valid", e) is None:
            continue
        # ---- subdivision part ----
        p = compute_CC_edge(mesh, e)#p = np.array([0, 0, 0])
        mesh.set_edge_property("id", e, idx)
        mesh.set_edge_property("position", e, p)
        mesh_next.add_vertex(p)

        # ---- table part ----
        e0 = mesh.halfedge_handle(e, 0)
        e1 = mesh.halfedge_handle(e, 1)
        v0 = mesh.to_vertex_handle(e0)
        v1 = mesh.to_vertex_handle(e1)
        f0 = mesh.face_handle(e0)
        f1 = mesh.face_handle(e1)

        e_data.append(v0.idx() + prev_idx)
        e_data.append(v1.idx() + prev_idx)
        e_data.append(f0.idx() + fidx)
        e_data.append(f1.idx() + fidx)

        e_indices.append(idx + fidx)

        idx = idx + 1

    offset = 0
    for v in mesh.vertices():
        if mesh.vertex_property("valid", v) is None:
            continue
        # ---- subdivision part ----
        p = compute_CC_vertex(mesh, v)# p = np.array([0, 0, 0])
        mesh.set_vertex_property("id", v, idx)
        mesh.set_vertex_property("position", v, p)
        mesh_next.add_vertex(p)

        # ---- table part ----
        val = 0
        for face in mesh.vf(v):
            val += 1
            v_data.append(face.idx() + fidx)

        for edge in mesh.ve(v):
            v0 = mesh.to_vertex_handle(mesh.halfedge_handle(edge, 0))
            v1 = mesh.to_vertex_handle(mesh.halfedge_handle(edge, 1))
            if v0 != v:
                v_data.append(v0.idx() + prev_idx)
            if v1 != v:
                v_data.append(v1.idx() + prev_idx)
            val += 1

        v_offsets.append(offset)
        v_valances.append(val)
        offset += val

        v_index.append(v.idx() + prev_idx)
        v_indices.append(idx + fidx)
        idx = idx + 1

    for f in mesh.faces():
        if mesh.face_property("interior", f) is None:
            continue

        v0 = mesh.face_property("id", f)

        for h in mesh.fh(f):
            v1 = mesh.edge_property("id", mesh.edge_handle(h))
            v2 = mesh.vertex_property("id", mesh.to_vertex_handle(h))
            v3 = mesh.edge_property("id", mesh.edge_handle(mesh.next_halfedge_handle(h)))
            mesh_next.add_faces([[v0, v1, v2, v3]])
            if mesh.face_property("patched", f) is True:
                mesh_next.set_face_property("patched", mesh_next.face_handle(mesh_next.faces().__len__() - 1), True)
            else:
                mesh_next.set_face_property("patched", mesh_next.face_handle(mesh_next.faces().__len__() - 1), False)

    to_json(v_indices, v_offsets, v_valances, v_index, v_data, e_indices, e_data, f_indices, f_offsets, f_valances, f_data, depth)

    return mesh_next, fidx



def subdivision_2(mesh: om.PolyMesh, prev_idx: int, current_depth: int, depth: int):
    f_offsets = []
    f_valances = []
    f_indices = []
    f_data = []
    e_data = []
    e_indices = []
    v_offsets = []
    v_data = []
    v_index = []
    v_valances = []
    v_indices = []
    mesh_next = om.PolyMesh()

    fidx = prev_idx + mesh.vertices().__len__()
    offset = 0
    idx = 0

    for f in mesh.faces():
        if mesh.face_property("visited") is None:
            continue
        val = 0
        # ----- subdivision part -------
        p = compute_CC_face(mesh, f)  # p = np.array([0, 0, 0])
        mesh.set_face_property("id", f, idx)
        mesh.set_face_property("position", f, p)
        mesh_next.add_vertex(p)

        # ---- table part -----

        for vert in mesh.fv(f):
            val += 1
            f_data.append(vert.idx() + prev_idx)
            # f_data.append(vert.idx() + prev_idx)

        f_offsets.append(offset)
        f_valances.append(val)
        offset += val

        f_indices.append(idx + fidx)

        idx = idx + 1

        # if mesh.is_boundary(f):
        #     continue
        if mesh.face_property("interior", f) is None:
            continue

        for v in mesh.fv(f):
            mesh.set_vertex_property("valid", v, True)
        for e in mesh.fe(f):
            mesh.set_edge_property("valid", e, True)

    for e in mesh.edges():
        if mesh.edge_property("valid", e) is None:
            continue
        # ---- subdivision part ----
        p = compute_CC_edge(mesh, e)  # p = np.array([0, 0, 0])
        mesh.set_edge_property("id", e, idx)
        mesh.set_edge_property("position", e, p)
        mesh_next.add_vertex(p)

        # ---- table part ----
        e0 = mesh.halfedge_handle(e, 0)
        e1 = mesh.halfedge_handle(e, 1)
        v0 = mesh.to_vertex_handle(e0)
        v1 = mesh.to_vertex_handle(e1)
        f0 = mesh.face_handle(e0)
        f1 = mesh.face_handle(e1)

        e_data.append(v0.idx() + prev_idx)
        e_data.append(v1.idx() + prev_idx)
        e_data.append(f0.idx() + fidx)
        e_data.append(f1.idx() + fidx)

        e_indices.append(idx + fidx)

        idx = idx + 1

    offset = 0
    for v in mesh.vertices():
        if mesh.vertex_property("valid", v) is None:
            continue
        # ---- subdivision part ----
        p = compute_CC_vertex(mesh, v)  # p = np.array([0, 0, 0])
        mesh.set_vertex_property("id", v, idx)
        mesh.set_vertex_property("position", v, p)
        mesh_next.add_vertex(p)

        # ---- table part ----
        val = 0
        for face in mesh.vf(v):
            val += 1
            v_data.append(face.idx() + fidx)

        for edge in mesh.ve(v):
            v0 = mesh.to_vertex_handle(mesh.halfedge_handle(edge, 0))
            v1 = mesh.to_vertex_handle(mesh.halfedge_handle(edge, 1))
            if v0 != v:
                v_data.append(v0.idx() + prev_idx)
            if v1 != v:
                v_data.append(v1.idx() + prev_idx)
            val += 1

        v_offsets.append(offset)
        v_valances.append(val)
        offset += val

        v_index.append(v.idx() + prev_idx)
        v_indices.append(idx + fidx)
        idx = idx + 1

    for f in mesh.faces():
        if mesh.face_property("interior", f) is None:
            continue

        v0 = mesh.face_property("id", f)

        for h in mesh.fh(f):
            v1 = mesh.edge_property("id", mesh.edge_handle(h))
            v2 = mesh.vertex_property("id", mesh.to_vertex_handle(h))
            v3 = mesh.edge_property("id", mesh.edge_handle(mesh.next_halfedge_handle(h)))
            mesh_next.add_faces([[v0, v1, v2, v3]])
            if mesh.face_property("patched", f) is True:
                mesh_next.set_face_property("patched", mesh_next.face_handle(mesh_next.faces().__len__() - 1), True)
            else:
                mesh_next.set_face_property("patched", mesh_next.face_handle(mesh_next.faces().__len__() - 1), False)

    # to_json(v_indices, v_offsets, v_valances, v_index, v_data, e_indices, e_data, f_indices, f_offsets, f_valances,
    #         f_data, current_depth)


    add = mesh_next.vertices().__len__()
    offset = 0
    for i in range(current_depth, depth + 1):
        print("depth: ", i)
        to_json2(v_indices, v_offsets, v_valances, v_index, v_data, e_indices, e_data, f_indices, f_offsets, f_valances,
                f_data, i, offset)
        offset = offset + add
