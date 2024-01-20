import os
import rhinoscriptsyntax as rs
import time
def delete_unsupported_objects(imported_geometry):
    for geometry in imported_geometry:
        if not is_geometry_supported_for_unroll(geometry):
            rs.DeleteObject(geometry)

def is_geometry_supported_for_unroll(geometry):
    # 检查几何体是否支持展开
    return rs.IsSurface(geometry) or rs.IsPolysurface(geometry)

def create_directory(base_path, subfolder_name):
    path = os.path.join(base_path, subfolder_name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def flatten_and_save(geometry, folder_path, model_name, thickness):
    if not is_geometry_supported_for_unroll(geometry):
        print(f"模型 {model_name} - {geometry} 不支持展开。")
        return None
    
    # 展开几何体
    flattened = rs.UnrollSurface(geometry, True)  # True表示保留属性
    if not flattened:
        print(f"无法展开几何体: {geometry}")
        return None

    unrolled_surfaces = rs.LastCreatedObjects()
    if not unrolled_surfaces:
        print(f"未找到展开的表面: {model_name}")
        return None
    
    # 给展开图增加厚度，即挤出
    valid_extrusions = []
    for unrolled in unrolled_surfaces:
        if rs.IsSurface(unrolled):
            try:
                extrusion = rs.ExtrudeSurface(unrolled, (0, 0, 1), thickness)
                if extrusion:
                    valid_extrusions.extend(extrusion)
            except Exception as e:
                print(f"无法挤出表面: {unrolled}. 错误: {e}")
            finally:
                rs.DeleteObject(unrolled)
        else:
            print(f"无效的展开表面对象: {unrolled}")
    
    if not valid_extrusions:
        print(f"无法创建挤出体: {model_name}")
        return None

    # 保存挤出体为STEP文件
    step_file_path = os.path.join(folder_path, f"{model_name}.step")
    rs.SelectObjects(extrusions)
    rs.Command(f"_-Export \"{step_file_path}\" _Enter")
    rs.DeleteObjects(extrusions)

    # 保存顶视图图片
    image_file_path = os.path.join(folder_path, f"{model_name}_topview.png")
    rs.Command("_-SetView _World _Top _Enter")
    rs.Command("_-Zoom _All _Extents _Enter")
    time.sleep(1)
    rs.Command(f"_-ViewCaptureToFile \"{image_file_path}\" _Width 800 _Height 600 _Enter")
    time.sleep(1)

def import_and_unroll_models(folder_path, save_folder, thickness):
    # 获取文件夹中的所有 STEP 文件
    step_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".step")]

    for index, step_file in enumerate(step_files, start=1):
        rs.DeleteObjects(rs.AllObjects())
        subfolder_name = str(index).zfill(6)
        model_folder = create_directory(save_folder, subfolder_name)

        full_path = os.path.join(folder_path, step_file)
        model_name = os.path.splitext(step_file)[0]
        
        rs.Command(f"_-Import \"{full_path}\" _Enter")
        imported_geometry = rs.LastCreatedObjects()

        if imported_geometry:
            delete_unsupported_objects(imported_geometry)
            for geometry in imported_geometry:
                if is_geometry_supported_for_unroll(geometry):
                    flatten_and_save(geometry, model_folder, model_name, thickness)
                    # 删除处理过的几何体
                    rs.DeleteObject(geometry)
                else:
                    print(f"模型 {model_name} 不支持展开。")
            # 在处理下一个文件前，确保场景中没有残余的几何体
            rs.DeleteObjects(imported_geometry)
            time.sleep(1)
        else:
            print(f"无法导入模型 {step_file}")

        # 清除屏幕上所有残余对象
        rs.DeleteObjects(rs.AllObjects())

def main():
    folder_path = "C:/Users/frank/Documents/GitHub/Unfold3D/test"
    save_folder = "C:/Users/frank/Documents/GitHub/Unfold3D/Unrolled_results"
    thickness = 0.1

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    import_and_unroll_models(folder_path, save_folder, thickness)

if __name__ == "__main__":
    main()
