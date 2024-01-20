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

def flatten_and_save(geometry, save_folder, model_name, index):
    if not is_geometry_supported_for_unroll(geometry):
        print("模型 {} - {} 不支持展开。".format(model_name, index))
        return None
    
    # 展开几何体
    flattened = rs.UnrollSurface(geometry)
    if flattened:
        unrolled_surfaces = rs.LastCreatedObjects()
        if unrolled_surfaces:
            # 切换到顶视图
            rs.Command("_-SetView _World _Top", False)
            time.sleep(1)  # 等待视图切换
            
            # Zoom Extents All，以确保展开图在视图中居中且完整显示
            rs.Command("_-Zoom _All _Extents", False)
            time.sleep(1)  # 等待视图更新
            # 删除展开的对象
            rs.DeleteObjects(unrolled_surfaces)
            # 构造图片文件名
            image_file_name = "{}_topview.png".format(model_name)
            
            # 保存图片
            image_file_path = os.path.join(save_folder, image_file_name)
            rs.Command("_-ViewCaptureToFile \"" + image_file_path + "\" _Width 800 _Height 600 _Enter", False)
            time.sleep(1)  # 等待图片保存完成
            

            
            return image_file_path
    
    return None


def import_and_unroll_models(folder_path, save_folder):
    # 获取文件夹中的所有 STEP 文件
    step_files = [f for f in os.listdir(folder_path) if f.endswith(".step")]

    for step_file in step_files:
        full_path = os.path.join(folder_path, step_file)
        model_name = os.path.splitext(step_file)[0]  # 获取模型名称
        
        rs.Command("_-Import \"" + full_path + "\" Enter")
        
        # 获取导入的几何体
        imported_geometry = rs.LastCreatedObjects()
        
        if imported_geometry:
            delete_unsupported_objects(imported_geometry)
            index = 1
            for geometry in imported_geometry:
                # 展开导入的模型并保存展开图
                image_file_path = flatten_and_save(geometry, save_folder, model_name, index)
                rs.DeleteObjects(imported_geometry)
                if image_file_path:
                    print("成功导入、展开并保存模型的展开图：{} - {}".format(model_name, index))
                    print("展开图图片保存为：{}".format(image_file_path))
                    index += 1
                else:
                    print("无法展开模型：{} - {}".format(model_name, index))
                    break
            

            time.sleep(1)
        else:
            print("无法导入模型：{}".format(step_file))
        
        # 清除屏幕上所有残余对象
        rs.DeleteObjects(rs.AllObjects())
        time.sleep(1)

def main():
    # 指定模型文件夹路径
    folder_path = "C:/Users/frank/Documents/GitHub/Unfold3D/test"

    # 指定保存展开结果的文件夹路径
    save_folder = "C:/Users/frank/Documents/GitHub/Unfold3D/Unrolled_results"

    # 确保保存文件夹存在，如果不存在则创建它
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # 导入、展开、保存展开图并删除原始模型
    import_and_unroll_models(folder_path, save_folder)

if __name__ == "__main__":
    main()
