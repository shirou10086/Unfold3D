import rhinoscriptsyntax as rs

def unroll_current_geometry():
    # 获取当前Rhino场景中的所有对象
    all_objects = rs.AllObjects()

    if all_objects and len(all_objects) == 1:
        # 获取场景中唯一的几何体
        geometry_id = all_objects[0]

        # 检查几何体是否是有效的曲面
        if rs.IsSurface(geometry_id):
            # 创建展开图
            unrolled_surface = rs.UnrollSurface(geometry_id)

            if unrolled_surface:
                print("成功展开当前几何体。")
                # 在Rhino中显示展开图
                rs.SelectObjects([unrolled_surface])
            else:
                print("无法展开当前几何体。")
        else:
            print("当前几何体不是有效的曲面。")
    else:
        print("Rhino场景中应只包含一个几何体，但包含了多个几何体或没有几何体。")

def main():
    # 展开当前Rhino场景中的几何体
    unroll_current_geometry()

if __name__ == "__main__":
    main()
