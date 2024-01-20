import os

def main():
    test_dir = './test'
    unrolled_results_dir = './Unrolled_results'

    # 获取 test 目录中所有的 .step 文件名（不包含扩展名）
    step_filenames = {os.path.splitext(f)[0] for f in os.listdir(test_dir) if f.endswith('.step')}

    # 获取 Unrolled_results 目录中所有的 _topview.png 文件名（不包含扩展名和后缀）
    topview_png_filenames = {f.split('_topview')[0] for f in os.listdir(unrolled_results_dir) if f.endswith('_topview.png')}

    # 找出 test 目录中有，但 Unrolled_results 目录中没有对应 PNG 文件的 STEP 文件
    step_files_to_delete = step_filenames - topview_png_filenames

    # 删除这些没有对应 PNG 文件的 STEP 文件
    for file in step_files_to_delete:
        step_file_path = os.path.join(test_dir, file + '.step')
        if os.path.isfile(step_file_path):  # 确保文件存在
            os.remove(step_file_path)
            print(f"Deleted: {file}.step")

if __name__ == "__main__":
    main()
