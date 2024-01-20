import os
import rhinoscriptsyntax as rs
import time

def is_geometry_supported_for_unroll(geometry):
    # 检查几何体是否支持展开
    return rs.IsSurface(geometry) or rs.IsPolysurface(geometry)

def flatten_and_save(geometry, save_folder, model_name, index):
    if not is_geometry_supported_for_unroll(geometry):
        rs.DeleteObjects([geometry])
        print("模型 {} - {} 不支持展开。".format(model_name, index))
        return None, None
    
    # 创建展开图
    flattened = rs.UnrollSurface(geometry)
    if flattened:
        unrolled_surfaces = rs.LastCreatedObjects()
        
        if unrolled_surfaces:
            # 停顿2秒
            rs.DeleteObjects([geometry])
            # 构造展开图的文件名
            step_file_name = "{}_{}.step".format(model_name, index)
            image_file_name = "{}_{}.png".format(model_name, index)
            
            # 保存展开图为STEP文件
            step_file_path = os.path.join(save_folder, step_file_name)
            rs.Command("_-Export \"" + step_file_path + "\" _Enter", False)
            
            # 保存展开图为图片（PNG格式）
            image_file_path = os.path.join(save_folder, image_file_name)
            rs.Command("_-ViewCaptureToFile \"" + image_file_path + "\" _Enter", False)
            time.sleep(1)
            
            # 删除原模型
            rs.DeleteObjects(rs.AllObjects())
            return step_file_path, image_file_path
    
    return None, None

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
            index = 1
            
            while True:
                # 展开导入的模型并保存展开图
                step_file_path, image_file_path = flatten_and_save(imported_geometry[0], save_folder, model_name, index)
                
                if step_file_path and image_file_path:
                    print("成功导入、展开并保存模型：{} - {}".format(model_name, index))
                    print("STEP文件保存为：{}".format(step_file_path))
                    print("图片保存为：{}".format(image_file_path))
                    
                    index += 1
                else:
                    print("无法展开模型：{} - {}".format(model_name, index))
                    break
        else:
            print("无法导入模型：{}".format(step_file))
        time.sleep(1)
        rs.DeleteObjects(rs.AllObjects())

            
def main():
    # 指定模型文件夹路径
    folder_path = "C:/Users/frank/Documents/GitHub/Unfold3D/test"

    # 指定保存展开结果的文件夹路径
    save_folder = "C:/Users/frank/Documents/GitHub/Unfold3D/Unrolled_results"

    # 确保保存文件夹存在，如果不存在则创建它
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # 导入、展开、保存和删除原始模型
    import_and_unroll_models(folder_path, save_folder)

if __name__ == "__main__":
    main()
