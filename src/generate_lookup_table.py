import src.MeshData as MeshData
import json


def find_index(list, value):
    for i, sub_lst in enumerate(list):
        if sub_lst[0][0] == value:
            return i
    return -1


def generate_lookup_table(meshdata: MeshData) -> MeshData:
    faces = meshdata.faces
    vertices = meshdata.vertices.copy()
    edges = meshdata.edges.copy()

    faces_next = []
    edges_next = []
    vertices_next = []  #= meshdata.vertices.copy()

    face_points = {}
    edge_points = {}
    vertex_points = {}

    vert_idx = vertices[-1] + 1

    # f_points
    print("F points")
    off = 0
    for face in faces:
        val = len(face)

        idx = vert_idx if vertices_next == [] else vertices_next[-1] + 1

        vertices_next.append(idx)

        face_points[tuple(face)] = idx

        print(idx, ':', off, val, face)

        off += val

    # e_points
    print("E points")
    for edge in edges:
        # print(edge)
        idx = vertices_next[-1] + 1
        vertices_next.append(idx)

        edge_points[tuple(edge[0][0])] = idx
        edge_points[tuple(edge[1][0])] = idx

        f0 = face_points[tuple(faces[edge[0][1]])]
        f1 = face_points[tuple(faces[edge[1][1]])]

        print(idx, ':', edge[0][0][0], edge[1][0][0], f0, f1)

    # v_points
    print("V points")
    off = 0
    for vertex in vertices:
        # print(vertex)
        idx = vertices_next[-1] + 1
        vertices_next.append(idx)

        vertex_points[vertex] = idx

        v_faces = []
        v_edges = []

        for face in faces:
            if vertex in face:
                f = face_points[tuple(face)]
                v_faces.append(f)

        for edge in edges:
            if vertex == edge[0][0][0]:
                e = edge[0][0][1]
                v_edges.append(e)
            if vertex == edge[0][0][1]:
                e = edge[0][0][0]
                v_edges.append(e)

        val = len(v_faces) + len(v_edges)

        print(idx, ':', off, (len(v_faces) + len(v_edges)), v_faces + v_edges)

        off += val

    # create new faces, edges

    for face in faces:
        f = face_points[tuple(face)]

        l = len(face)
        for i in range(l):
            e0 = edge_points[(face[i], face[(i + 1) % l])]
            v0 = vertex_points[face[(i + 1) % l]]
            e1 = edge_points[(face[(i + 1) % l], face[(i + 2) % l])]

            faces_next.append([f, e0, v0, e1])

            idx = find_index(edges_next, [e0, f])
            if idx != -1:  # if the edge is already in the list
                edges_next[idx].append([[f, e0], len(faces_next) - 1])
            else:
                edges_next.append([[[f, e0], len(faces_next) - 1]])

            idx = find_index(edges_next, [v0, e0])
            if idx != -1:
                edges_next[idx].append([[e0, v0], len(faces_next) - 1])
            else:
                edges_next.append([[[e0, v0], len(faces_next) - 1]])

            idx = find_index(edges_next, [e1, v0])
            if idx != -1:
                edges_next[idx].append([[v0, e1], len(faces_next) - 1])
            else:
                edges_next.append([[[v0, e1], len(faces_next) - 1]])

            idx = find_index(edges_next, [f, e1])
            if idx != -1:
                edges_next[idx].append([[e1, f], len(faces_next) - 1])
            else:
                edges_next.append([[[e1, f], len(faces_next) - 1]])

    print("faces", len(faces_next), faces_next)
    print("edges", len(edges_next), edges_next)
    print("vertices", len(vertices_next), vertices_next)

    meshdata.faces = faces_next
    meshdata.edges = edges_next
    meshdata.vertices = vertices_next

    return meshdata
