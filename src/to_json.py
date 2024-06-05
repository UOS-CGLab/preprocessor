import json
import os


def clear_json():
    with open("topology.json", "w") as f:
        f.write("[]")  # 빈 배열로 초기화


def append_to_json(data):
    with open("topology.json", "r+") as f:
        json_data = json.load(f)
        f.seek(0)
        if json_data:  # 기존에 데이터가 있는 경우
            f.truncate(0)  # 파일 내용을 비움
            f.seek(0)
            json_data.append(data)  # 새 데이터 추가
            # json.dump(json_data, f, indent=4)
            json.dump(json_data, f, separators=(', ', ':'))
        else:  # 파일이 비어있는 경우
            # json.dump([data], f, indent=4)
            json.dump([data], f, separators=(', ', ':'))



def to_json(v_indices, v_offsets, v_valances, v_index, v_data, e_indices, e_data, f_indices, f_offsets, f_valances,
            f_data, depth):
    if depth == 0:
        clear_json()

    data = {
        "depth": depth,
        "data": {
            "v_indices": v_indices,
            "v_offsets": v_offsets,
            "v_valances": v_valances,
            "v_index": v_index,
            "v_data": v_data,
            "e_indices": e_indices,
            "e_data": e_data,
            "f_indices": f_indices,
            "f_offsets": f_offsets,
            "f_valances": f_valances,
            "f_data": f_data
        }
    }

    append_to_json(data)


def add_offset(array, offset):
    return [x + offset for x in array]
def to_json2(v_indices, v_offsets, v_valances, v_index, v_data, e_indices, e_data, f_indices, f_offsets, f_valances,
            f_data, depth, offest):

    data = {
        "depth": depth,
        "data": {
            "v_indices": add_offset(v_indices, offest),
            "v_offsets": add_offset(v_offsets, offest),
            "v_valances": v_valances,
            "v_index": add_offset(v_index, offest),
            "v_data": add_offset(v_data, offest),
            "e_indices": add_offset(e_indices, offest),
            "e_data": add_offset(e_data, offest),
            "f_indices": add_offset(f_indices, offest),
            "f_offsets": add_offset(f_offsets, offest),
            "f_valances": f_valances,
            "f_data": add_offset(f_data, offest)
        }
    }

    append_to_json(data)


