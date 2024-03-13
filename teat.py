import openmesh as om
import numpy as np




# print("input file: ")
# input_file = input()
# polymesh = om.read_polymesh(input_file)
polymesh = om.read_polymesh("mesh_files/cone.obj")

# print("depth of subdivisoin: ")
# depth = int(input())
depth = 3


# make vertices index array
vertices = [vh.idx() for vh in polymesh.vertices()]
print(vertices)


# calc f points
t = 0
for fh in polymesh.faces():
    face_vertices = [vh.idx() for vh in polymesh.fv(fh)]
    val = len(face_vertices)
    print(t, val, face_vertices)
    t += val

# calc e points
for eh in polymesh.edges():
    heh = polymesh.halfedge_handle(eh, 0)  # Get one of the halfedges of the edge
    heh2 = polymesh.halfedge_handle(eh, 1)  # Get the other halfedge of the edge
    v0 = polymesh.from_vertex_handle(heh).idx()  # Add the first vertex
    v1 = polymesh.to_vertex_handle(heh).idx()    # Add the second vertex
    #print(v0, v1)
    # get the face that includes the v0, v1
    face1 = polymesh.face_handle(heh).idx()
    face2 = polymesh.face_handle(heh2).idx()
    #print(face.idx())
    e_vertices = [v0, v1, face1 + len(vertices), face2 + len(vertices)]
    print(e_vertices)



# calc v points
off = 0
for vh in polymesh.vertices():
    v_vertices = []
    # get the linked faces
    for fh in polymesh.vf(vh):
        v_vertices.append(fh.idx() + len(vertices))

    # get the linked edges and their other vertex
    for eh in polymesh.ve(vh):
        v1 = polymesh.halfedge_handle(eh, 0)
        v2 = polymesh.halfedge_handle(eh, 1)

        if polymesh.from_vertex_handle(v1) == vh:
            v = polymesh.to_vertex_handle(v1).idx()
        else:
            v = polymesh.from_vertex_handle(v1).idx()
        v_vertices.append(v)

    val = len(v_vertices)
    print(vh.idx(),off, int(val/2),v_vertices)
    off += val


# create new faces


