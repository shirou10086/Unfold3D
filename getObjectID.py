import rhinoscriptsyntax as rs

def print_all_object_ids_and_types():
    # 获取所有对象的ID
    object_ids = rs.AllObjects()
    if not object_ids:
        print("No objects found in the document.")
        return
    
    # 遍历对象并输出它们的ID和类型
    for obj_id in object_ids:
        obj_type = rs.ObjectType(obj_id)
        print(f"Object ID: {obj_id}, Object Type ID: {obj_type}")

# 执行函数
print_all_object_ids_and_types()