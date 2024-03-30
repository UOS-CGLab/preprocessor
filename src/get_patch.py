import openmesh as om
"""
v0 v1 v2 v3
v4 v5 v6 v7
v8 v9 v10 v11
v12 v13 v14 v15
"""




def get_patch(mesh):

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
                v8 = mesh.to_vertex_handle(mesh.next_halfedge_handle(mesh.opposite_halfedge_handle(left))).idx()
                v9 = f1
                v10 = f2
                v11 = mesh.from_vertex_handle(right).idx()
                v12 = mesh.to_vertex_handle(mesh.next_halfedge_handle(mesh.opposite_halfedge_handle(mesh.next_halfedge_handle(left)))).idx()
                v13 = mesh.from_vertex_handle(bottom).idx()
                v14 = mesh.to_vertex_handle(bottom).idx()
                v15 = mesh.to_vertex_handle(mesh.next_halfedge_handle(mesh.opposite_halfedge_handle(mesh.next_halfedge_handle(bottom)))).idx()

                # print("v0: ", v0, "v1: ", v1, "v2: ", v2, "v3: ", v3, "v4: ", v4, "v5: ", v5, "v6: ", v6, "v7: ", v7, "v8: ", v8, "v9: ", v9, "v10: ", v10, "v11: ", v11, "v12: ", v12, "v13: ", v13, "v14: ", v14, "v15: ", v15)
                print(v0, v1, v2, v3)
                print(v4, v5, v6, v7)
                print(v8, v9, v10, v11)
                print(v12, v13, v14, v15)
                print()
    print(count)
    return
