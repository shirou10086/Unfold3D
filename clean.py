import rhinoscriptsyntax as rs

# 删除场景中的所有对象
rs.DeleteObjects(rs.AllObjects())

# 清空选择
rs.UnselectAllObjects()

print("场景已清空，所有模型已删除。")
