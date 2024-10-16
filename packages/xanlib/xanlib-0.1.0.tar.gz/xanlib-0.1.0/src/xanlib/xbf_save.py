from struct import pack
from .xbf_base import NodeFlags

def convert_to_5bit_signed(v):
    v_clamped = max(-15, min(15, int(round(v))))

    if v_clamped < 0:
        return v_clamped + 32
    else:
        return v_clamped

def write_Int32sl(buffer, v):
	buffer.write(pack('<i', v))
	
def write_Int32ul(buffer, v):
	buffer.write(pack('<I', v))
	
def write_Int16sl(buffer, v):
	buffer.write(pack('<h', v))
	
def write_Int16ul(buffer, v):
	buffer.write(pack('<H', v))
	
def write_Int8ul(buffer, v):
	buffer.write(pack('<B', v))
	
def write_matrix44dl(buffer, v):
    buffer.write(pack('<16d', *v))
    
def write_vertex(buffer, vertex):
    buffer.write(pack('<3f', *vertex.position))
    buffer.write(pack('<3f', *vertex.normal))

def write_vertex_for_vertex_animation(buffer, vertex_animation_frame_datum):
    buffer.write(pack('<3hH', *vertex_animation_frame_datum))
    
def write_face(buffer, face):
    buffer.write(pack('<3i', *face.vertex_indices))
    buffer.write(pack('<1i', face.texture_index))
    buffer.write(pack('<1i', face.flags))
    for uv in face.uv_coords:
        buffer.write(pack('2f', *uv))
        
def write_vertex_animation(buffer, va):
    write_Int32sl(buffer, va.frame_count)
    write_Int32sl(buffer, va.count)
    write_Int32sl(buffer, va.actual)
    for key in va.keys:
        write_Int32ul(buffer, key)
    
    if va.count<0:
        write_Int32ul(buffer, va.scale)
        write_Int32ul(buffer, va.base_count)
        for frame in va.frames:
            for vertex_flagged in frame:
                write_vertex_for_vertex_animation(buffer, vertex_flagged)
        if (va.scale & 0x80000000):
            for v in va.interpolation_data:
                write_Int32ul(buffer, v)
                
def write_key_animation(buffer, ka):
    write_Int32sl(buffer, ka.frame_count)
    write_Int32sl(buffer, ka.flags)
    if ka.flags==-1:
        for matrix in ka.matrices:
            buffer.write(pack('<16f', *matrix))
    elif ka.flags==-2:
        for matrix in ka.matrices:
            buffer.write(pack('<12f', *matrix))
    elif ka.flags==-3:
        write_Int32sl(buffer, ka.actual)
        for extra_datum in ka.extra_data:
            write_Int16sl(buffer, extra_datum)
        for matrix in ka.matrices:
            buffer.write(pack('<12f', *matrix))
    else:
        for frame in ka.frames:
            write_Int16sl(buffer, frame.frame_id)
            write_Int16sl(buffer, frame.flag)
            if frame.rotation is not None:
                buffer.write(pack('<4f', *frame.rotation))
            if frame.scale is not None:
                buffer.write(pack('<3f', *frame.scale))
            if frame.translation is not None:
                buffer.write(pack('<3f', *frame.translation))
	
def write_node(buffer, node):
    write_Int32sl(buffer, len(node.vertices))
    write_Int32sl(buffer, node.flags)
    write_Int32sl(buffer, len(node.faces))
    write_Int32sl(buffer, len(node.children))
    write_matrix44dl(buffer, node.transform)
    write_Int32sl(buffer, len(node.name))
    buffer.write(node.name.encode())
    
    for child in node.children:
        write_node(buffer, child)
        
    for vertex in node.vertices:
        write_vertex(buffer, vertex)
        
    for face in node.faces:
        write_face(buffer, face)
        
    if NodeFlags.PRELIGHT in node.flags:
        for j, vertex in enumerate(node.vertices):
            for i in range(3):
                write_Int8ul(buffer, node.rgb[j][i])

    if NodeFlags.FACE_DATA in node.flags:
        for faceDatum in node.faceData:
            write_Int32sl(buffer, faceDatum)

    if NodeFlags.VERTEX_ANIMATION in node.flags:
        write_vertex_animation(buffer, node.vertex_animation)
        
    if NodeFlags.KEY_ANIMATION in node.flags:
        write_key_animation(buffer, node.key_animation)
        

def save_xbf(scene, filename):
    with open(filename, 'wb') as f:
        write_Int32sl(f, scene.version)
        write_Int32sl(f, len(scene.FXData))
        f.write(scene.FXData)
        write_Int32sl(f, len(scene.textureNameData))
        f.write(scene.textureNameData)
        for node in scene.nodes:
            write_node(f, node)
        if scene.unparsed is not None:
            f.write(scene.unparsed)
        else:
            write_Int32sl(f, -1)
