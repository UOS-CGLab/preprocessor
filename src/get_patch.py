import openmesh as om
"""
v0 v1 v2 v3
v4 v5 v6 v7
v8 v9 v10 v11
v12 v13 v14 v15
"""


def write_into_file(v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, idx):
    with open("patch.txt", "a") as file:
        file.write(str(v0 + idx) + ", " + str(v1 + idx) + ", " + str(v2 + idx) + ", " + str(v3 + idx) + ", " + str(v4 + idx) + ", " + str(v5 + idx) + ", " + str(v6 + idx) + ", " + str(v7 + idx) + ", " + str(v8 + idx) + ", " + str(v9 + idx) + ", " + str(v10 + idx) + ", " + str(v11 + idx) + ", " + str(v12 + idx) + ", " + str(v13 + idx) + ", " + str(v14 + idx) + ", " + str(v15 + idx) + ",\n")


def write_into_file2(v5, v6, v9, v10, idx):
    with open("triangle.txt", "a") as file:
        file.write(str(v5 + idx) + ", " + str(v6 + idx) + ", " + str(v9 + idx) + ", " + str(v9 + idx) + ", " + str(v6 + idx) + ", " + str(v10 + idx) + ",\n")


def get_patch(mesh, idx) -> int:

    # get vertex's valence
    count = 0
    for f in mesh.faces():
        if mesh.valence(f) == 4:
            # Check if all vertices of the face have valence 4
            all_valence_4 = all(mesh.valence(vh) == 4 for vh in mesh.fv(f))
            if all_valence_4:
                count += 1
                # Access vertices of the face without subscripting
                v_indices = [vh.idx() for vh in mesh.fv(f)]

                f0 = v_indices[0]
                f1 = v_indices[1]
                f2 = v_indices[2]
                f3 = v_indices[3]

                top = mesh.next_halfedge_handle(mesh.next_halfedge_handle(mesh.find_halfedge(mesh.vertex_handle(f0), mesh.vertex_handle(f3))))
                left = mesh.next_halfedge_handle(mesh.next_halfedge_handle(mesh.find_halfedge(mesh.vertex_handle(f1), mesh.vertex_handle(f0))))
                bottom = mesh.next_halfedge_handle(mesh.next_halfedge_handle(mesh.find_halfedge(mesh.vertex_handle(f2), mesh.vertex_handle(f1))))
                right = mesh.next_halfedge_handle(mesh.next_halfedge_handle(mesh.find_halfedge(mesh.vertex_handle(f3), mesh.vertex_handle(f2))))

                v0 = mesh.to_vertex_handle(mesh.next_halfedge_handle(mesh.opposite_halfedge_handle(mesh.next_halfedge_handle(top)))).idx()
                v1 = mesh.to_vertex_handle(top).idx()
                v2 = mesh.from_vertex_handle(top).idx()
                v3 = mesh.to_vertex_handle(mesh.next_halfedge_handle(mesh.opposite_halfedge_handle(mesh.next_halfedge_handle(right)))).idx()
                v4 = mesh.from_vertex_handle(left).idx()
                v5 = f0
                v6 = f3
                v7 = mesh.to_vertex_handle(right).idx()
                v8 = mesh.to_vertex_handle(left).idx()
                v9 = f1
                v10 = f2
                v11 = mesh.from_vertex_handle(right).idx()
                v12 = mesh.to_vertex_handle(mesh.next_halfedge_handle(mesh.opposite_halfedge_handle(mesh.next_halfedge_handle(left)))).idx()
                v13 = mesh.from_vertex_handle(bottom).idx()
                v14 = mesh.to_vertex_handle(bottom).idx()
                v15 = mesh.to_vertex_handle(mesh.next_halfedge_handle(mesh.opposite_halfedge_handle(mesh.next_halfedge_handle(bottom)))).idx()

                # print("v0: ", v0, "v1: ", v1, "v2: ", v2, "v3: ", v3, "v4: ", v4, "v5: ", v5, "v6: ", v6, "v7: ", v7, "v8: ", v8, "v9: ", v9, "v10: ", v10, "v11: ", v11, "v12: ", v12, "v13: ", v13, "v14: ", v14, "v15: ", v15)
                # print(v0, v1, v2, v3)
                # print(v4, v5, v6, v7)
                # print(v8, v9, v10, v11)
                # print(v12, v13, v14, v15)
                # print(str(v0) + ", " + str(v1) + ", " + str(v2) + ", " + str(v3) + ",")
                # print(str(v4) + ", " + str(v5) + ", " + str(v6) + ", " + str(v7) + ",")
                # print(str(v8) + ", " + str(v9) + ", " + str(v10) + ", " + str(v11) + ",")
                # print(str(v12) + ", " + str(v13) + ", " + str(v14) + ", " + str(v15) + ",")

                #print(str(v0 + idx) + ", " + str(v1 + idx) + ", " + str(v2 + idx) + ", " + str(v3 + idx) + "," + str(v4 + idx) + ", " + str(v5 + idx) + ", " + str(v6 + idx) + ", " + str(v7 + idx) + ", " + str(v8 + idx) + ", " + str(v9 + idx) + ", " + str(v10 + idx) + ", " + str(v11 + idx) + "," + str(v12 + idx) + ", " + str(v13 + idx) + ", " + str(v14 + idx) + ", " + str(v15 + idx) + ",")
                write_into_file(v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, idx)
                # print(str(v5) + ", " + str(v6) + ", " + str(v9) + ", " + str(v9) + ", " + str(v6) + ", " + str(v10) + ",")

                # print(str(v5 + idx) + ", " + str(v6 + idx) + ", " + str(v9 + idx) + ", " + str(v9 + idx) + ", " + str(v6 + idx) + ", " + str(v10 + idx) + ",")
                write_into_file2(v5, v6, v9, v10, idx)
                #print()
    print(count)
    return count
