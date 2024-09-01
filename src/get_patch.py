import openmesh as om
"""
v0 v1 v2 v3
v4 v5 v6 v7
v8 v9 v10 v11
v12 v13 v14 v15
"""


def write_into_file(v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, idx, v5_texcoord, v6_texcoord, v9_texcoord, v10_texcoord, output_dir):
    with open(output_dir + "/patch.txt", "a") as file:
        file.write(str(v0 + idx) + ", " + str(v1 + idx) + ", " + str(v2 + idx) + ", " + str(v3 + idx) + ", "
                   + str(v4 + idx) + ", "+ str(v5 + idx) + ", " + str(v6 + idx) + ", " + str(v7 + idx) + ", "
                   + str(v8 + idx) + ", " + str(v9 + idx) + ", " + str(v10 + idx) + ", " + str(v11 + idx) + ", "
                   + str(v12 + idx) + ", " + str(v13 + idx) + ", " + str(v14 + idx) + ", " + str(v15 + idx) + ", "
                   + str(v5_texcoord[0]) + ", " + str(v5_texcoord[1]) + ", "
                   + str(v6_texcoord[0]) + ", " + str(v6_texcoord[1]) + ", "
                   + str(v9_texcoord[0]) + ", " + str(v9_texcoord[1]) + ", "
                   + str(v10_texcoord[0]) + ", " + str(v10_texcoord[1]) + ",\n")


def write_into_file2(v5, v6, v9, v10, idx):
    with open("triangle.txt", "a") as file:
        file.write(str(v5 + idx) + ", " + str(v6 + idx) + ", " + str(v9 + idx) + ", " + str(v9 + idx) + ", " + str(v6 + idx) + ", " + str(v10 + idx) + ",\n")


def get_patch(mesh, idx, depth, output_dir) -> int:

    # get vertex's valence
    count = 0
    for f in mesh.faces():
        if mesh.face_property("patched", f) is True:
            continue
        if mesh.valence(f) == 4 and not mesh.is_boundary(f):
            # Check if all vertices of the face have valence 4
            neighbors = [face for vh in mesh.fv(f) for face in mesh.vf(vh)]
            all_valence_4 = all(mesh.valence(face) == 4 for face in neighbors)

            if depth != 0:
                all_valence_4 = all(mesh.valence(face) == 4 and not mesh.is_boundary(face) for face in neighbors)

            if all_valence_4:
                count += 1
                # Access vertices of the face without subscripting
                v_indices = [vh.idx() for vh in mesh.fv(f)]

                not_extraordinary = all((mesh.valence(vh) == 4) for vh in mesh.fv(f))
                if not not_extraordinary:
                    continue


                f0 = v_indices[0]
                f1 = v_indices[1]
                f2 = v_indices[2]
                f3 = v_indices[3]

                top = mesh.next_halfedge_handle(mesh.next_halfedge_handle(mesh.find_halfedge(mesh.vertex_handle(f0), mesh.vertex_handle(f3))))
                left = mesh.next_halfedge_handle(mesh.next_halfedge_handle(mesh.find_halfedge(mesh.vertex_handle(f1), mesh.vertex_handle(f0))))
                bottom = mesh.next_halfedge_handle(mesh.next_halfedge_handle(mesh.find_halfedge(mesh.vertex_handle(f2), mesh.vertex_handle(f1))))
                right = mesh.next_halfedge_handle(mesh.next_halfedge_handle(mesh.find_halfedge(mesh.vertex_handle(f3), mesh.vertex_handle(f2))))

                if depth != 0:
                    if mesh.is_boundary(mesh.to_vertex_handle(mesh.next_halfedge_handle(mesh.opposite_halfedge_handle(mesh.next_halfedge_handle(top))))):
                        continue
                    if mesh.is_boundary(mesh.to_vertex_handle(mesh.next_halfedge_handle(mesh.opposite_halfedge_handle(mesh.next_halfedge_handle(right))))):
                        continue
                    if mesh.is_boundary(mesh.to_vertex_handle(mesh.next_halfedge_handle(mesh.opposite_halfedge_handle(mesh.next_halfedge_handle(left))))):
                        continue
                    if mesh.is_boundary(mesh.to_vertex_handle(mesh.next_halfedge_handle(mesh.opposite_halfedge_handle(mesh.next_halfedge_handle(bottom))))):
                        continue



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

                mesh.set_face_property("patched", f, True)

                v5_texcoord = mesh.texcoord2D(mesh.find_halfedge(mesh.vertex_handle(f3), mesh.vertex_handle(f0)))
                v6_texcoord = mesh.texcoord2D(mesh.find_halfedge(mesh.vertex_handle(f2), mesh.vertex_handle(f3)))
                v9_texcoord = mesh.texcoord2D(mesh.find_halfedge(mesh.vertex_handle(f0), mesh.vertex_handle(f1)))
                v10_texcoord = mesh.texcoord2D(mesh.find_halfedge(mesh.vertex_handle(f1), mesh.vertex_handle(f2)))

                write_into_file(v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, idx, v5_texcoord, v6_texcoord, v9_texcoord, v10_texcoord, output_dir)

    # print(count)
    return count
