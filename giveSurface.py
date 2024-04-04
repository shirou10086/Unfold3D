import rhinoscriptsyntax as rs

def loft_surfaces():
    # 提示用户选择曲线
    curve_ids = rs.GetObjects("Select curves for loft", rs.filter.curve)
    if not curve_ids or len(curve_ids) < 2:
        rs.MessageBox("You must select at least two curves.")
        return

    # 使用选择的曲线进行loft
    lofted_surface_id = rs.AddLoftSrf(curve_ids)
    
    if lofted_surface_id:
        print("Lofted surface created.")
    else:
        print("Failed to create lofted surface.")
    
    return lofted_surface_id

# 调用函数
loft_surfaces()