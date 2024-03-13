from dataclasses import dataclass


@dataclass
class MeshData:
    faces: list
    edges: list
    vertices: list

    def __init__(self):
        self.faces = []
        self.edges = []
        self.vertices = []

"""
faces = [
    [vertices.idx],
]

edges = [
    [vertices.idx],
]

vertices = [
    [vertices.idx],
]


"""