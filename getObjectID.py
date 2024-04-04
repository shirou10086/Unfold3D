import rhinoscriptsyntax as rs

def print_object_types():
    # 获取所有对象的ID
    object_ids = rs.AllObjects()
    if not object_ids:
        print("No objects found in the model.")
        return
    
    # 遍历对象并输出它们的类型
    for obj_id in object_ids:
        obj_type = rs.ObjectType(obj_id)
        obj_type_name = object_type_to_string(obj_type)
        print(f"Object ID: {obj_id}, Object Type: {obj_type_name}")

def object_type_to_string(object_type):
    # 将对象类型编号转换为字符串
    types = {
        0 : "Unknown",
        1 : "Point",
        2 : "Point cloud",
        4 : "Curve",
        8 : "Surface",
        16 : "Polysurface",
        32 : "Mesh",
        256 : "Light",
        512 : "Annotation",
        4096 : "Instance definition",
        8192 : "Instance reference",
        16384 : "Text dot",
        32768 : "Grip",
        65536 : "Detail",
        131072 : "Hatch",
        262144 : "Morph control",
        524288 : "SubD",
        1048576 : "Brep",
        2097152 : "Clip plane",
        4194304 : "Extrusion",
        8388608 : "Edge softening",
    }
    return types.get(object_type, "Unknown")

# 执行函数
print_object_types()