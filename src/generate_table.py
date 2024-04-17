import openmesh as om
from src.export import export_to_txt

def generate_table(mesh: om.PolyMesh, idx: int, prev_idx: int,depth: int) -> int:

    #print("f points", idx) # get vertex idx for each face

    f_offsets = []
    f_valences = []
    f_data = []

    offset = 0
    for f in mesh.faces():
        val = 0
        for vert in mesh.fv(f):
            #print(vert.idx() + idx, end=" ")
            val += 1
            f_data.append(vert.idx() + idx)
        #print()
        f_offsets.append(offset)
        f_valences.append(val)
        offset += val


    if depth == 0:
        fidx = mesh.vertices().__len__()
    else:
        fidx = idx
        idx = 0

    #print("e points") # get vertex idx for each edge and get linked faces idx

    e_data = []

    for e in mesh.edges():
        e0 = mesh.halfedge_handle(e, 0)
        e1 = mesh.halfedge_handle(e, 1)
        v0 = mesh.to_vertex_handle(e0)
        v1 = mesh.to_vertex_handle(e1)
        f0 = mesh.face_handle(e0)
        f1 = mesh.face_handle(e1)
        #print(v0.idx() + idx, v1.idx() + idx, f0.idx() + fidx, f1.idx() + fidx)
        e_data.append(v0.idx() + idx)
        e_data.append(v1.idx() + idx)
        e_data.append(f0.idx() + fidx)
        e_data.append(f1.idx() + fidx)

    #print("v points") # get linked faces idx get linked edges other vert idx

    v_offsets = []
    v_valences = []
    v_indices = []
    v_data = []

    offset = 0
    for v in mesh.vertices():
        val = 0
        for face in mesh.vf(v):
            #print(face.idx() + fidx, end=" ")
            val += 1
            v_data.append(face.idx() + fidx)
        for edge in mesh.ve(v):
            v0 = mesh.to_vertex_handle(mesh.halfedge_handle(edge, 0))
            v1 = mesh.to_vertex_handle(mesh.halfedge_handle(edge, 1))
            # Ensure v0 and v1 are not the same as v
            if v0 != v:
                #print(v0.idx() + idx, end=" ")
                v_data.append(v0.idx() + idx)
            if v1 != v:
                #print(v1.idx() + idx, end=" ")
                v_data.append(v1.idx() + idx)
            val += 1
        #print()

        v_offsets.append(offset)
        v_valences.append(val)
        v_indices.append(v.idx() + idx)
        offset += 2 * val

    # print("face")
    # print("f_offsets", f_offsets)
    # print("f_valences", f_valences)
    # print("f_data", f_data)
    #
    # print("edge")
    # print("e_data", e_data)
    #
    # print("vertex")
    # print("v_offsets", v_offsets)
    # print("v_valences", v_valences)
    # print("v_indices", v_indices)
    # print("v_data", v_data)

    export_to_txt(f_offsets.copy(), f_valences.copy(), f_data.copy(),
                  e_data.copy(), v_offsets.copy(),
                  v_valences.copy(), v_data.copy(), depth)

    return 0
