import openmesh as om
import src.MeshData as MeshData


def obj_to_meshdata(input_file, meshdata=MeshData.MeshData()):
    polymesh = om.read_polymesh(input_file)

    vertices = [vh.idx() for vh in polymesh.vertices()]
    meshdata.vertices = vertices

    for fh in polymesh.faces():
        face_vertices = [vh.idx() for vh in polymesh.fv(fh)]
        meshdata.faces.append(face_vertices)

    for eh in polymesh.edges():
        heh = polymesh.halfedge_handle(eh, 0)
        v0 = polymesh.from_vertex_handle(heh).idx()
        v1 = polymesh.to_vertex_handle(heh).idx()
        f0 = polymesh.face_handle(heh).idx()
        heh2 = polymesh.halfedge_handle(eh, 1)
        f1 = polymesh.face_handle(heh2).idx()
        meshdata.edges.append(
            [[[v0, v1], f0], [[v1, v0], f1]]
        )

    return meshdata
