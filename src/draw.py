import src.MeshData as MeshData
import openmesh as om

from wgpu.gui.auto import WgpuCanvas, run
import wgpu


def draw(MeshData: MeshData):
    canvas = WgpuCanvas(title="Subdivision Surface", width=800, height=800)

    # Create a wgpu device
    adapter = wgpu.gpu.request_adapter(power_preference="high-performance")
    device = adapter.request_device()

    # Prepare present context
    present_context = canvas.get_context()
    render_texture_format = present_context.get_preferred_format(device.adapter)
    present_context.configure(device=device, format=render_texture_format)

    # Shader code
    shader_src = """
    @group(0) @binding(0)
    var<storage, buffer> vertices: [[f32; 3]];
    
    
    
    """