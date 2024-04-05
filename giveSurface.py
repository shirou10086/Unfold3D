import rhinoscriptsyntax as rs

def cap_open_breps():
    # 获取所有Brep对象
    all_object_ids = rs.AllObjects()
    if not all_object_ids:
        print("No objects found in the document.")
        return
    
    brep_ids = [obj_id for obj_id in all_object_ids if rs.IsBrep(obj_id)]
    if not brep_ids:
        print("No Brep objects found.")
        return
    
    # 检查每个 Brep 是否封闭，如果不是，则尝试封闭它
    for brep_id in brep_ids:
        if not rs.IsObjectSolid(brep_id):
            print(f"Brep Object ID {brep_id} is not solid. Attempting to cap...")
            if rs.CapPlanarHoles(brep_id):
                print("Brep was successfully capped.")
            else:
                print("Failed to cap Brep.")
        else:
            print(f"Brep Object ID {brep_id} is already solid.")
            
cap_open_breps()

def make_breps_solid():
    # 获取所有Brep对象
    brep_ids = rs.ObjectsByType(16) # Type ID for Breps is 16
    if not brep_ids:
        print("No Brep objects found.")
        return
    
    # 尝试将每个Brep对象转换为封闭的实体
    for brep_id in brep_ids:
        # 选择Brep对象
        rs.SelectObject(brep_id)
        # 使用Rhino命令MakeSolid来尝试将Brep变成实体
        rs.Command("MakeSolid")
        rs.UnselectObject(brep_id)

# 调用函数
make_breps_solid()