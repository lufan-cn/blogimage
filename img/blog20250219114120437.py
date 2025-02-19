# main.py (更新版)
import sys
import os
import subprocess
import tkinter as tk
from tkinter import filedialog

def select_input_path():
    """选择文件或文件夹"""
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename(
        title="选择H5文件或文件夹",
        filetypes=[("HDF5 files", "*.h5")],
    ) or filedialog.askdirectory(title="选择包含H5文件的文件夹")
    return path

def get_h5_files(path):
    """获取H5文件列表"""
    if os.path.isfile(path) and path.endswith(".h5"):
        return [path]
    elif os.path.isdir(path):
        return [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".h5")]
    return []

def run_script(script_name, excel_path, success_keyword):
    """通用脚本运行函数"""
    print(f"\n========== 开始执行 {script_name} ==========")
    result = subprocess.run(
        [sys.executable, script_name, excel_path],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print(f"错误信息：{result.stderr}")
    return success_keyword in result.stdout

def process_single_h5(h5_path):
    """处理单个H5文件"""
    try:
        # 第一阶段：h5转Excel
        print(f"\n处理文件: {h5_path}")
        result = subprocess.run(
            [sys.executable, "1_2.py", h5_path],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if "成功导出数据到" not in result.stdout:
            return False
        
        current_excel = result.stdout.split("成功导出数据到：")[1].splitlines()[0].strip()

        # 后续处理阶段
        scripts = [
            ("2_4.py", "筛选后的数据已成功保存到"),
            ("3_3.py", "数据已保存到"),
            ("4_1.py", "处理完成，数据已保存到"),
            ("5_1.py", "δF/F 计算完成"),
            ("6_1.py", "校正数据已保存"),
            ("7_1.py", "成功处理"),
            ("8_1.py", "图表已生成")
        ]

        for script, keyword in scripts:
            if not run_script(script, current_excel, keyword):
                return False
        return True

    except Exception as e:
        print(f"处理失败: {str(e)}")
        return False

if __name__ == "__main__":
    # 设置工作目录
    base_dir = r"Z:\A- Science\workspace\code\fiberphotometry data analysis\fibermetry"
    os.chdir(base_dir)

    # 获取输入路径
    input_path = select_input_path()
    if not input_path:
        print("未选择文件或文件夹，程序退出。")
        sys.exit()

    # 获取所有H5文件
    h5_files = get_h5_files(input_path)
    if not h5_files:
        print("未找到H5文件，程序退出。")
        sys.exit()

    # 按顺序处理文件
    for h5_file in h5_files:
        if process_single_h5(h5_file):
            print(f"\n文件 {h5_file} 处理完成！")
        else:
            print(f"\n文件 {h5_file} 处理失败！")

    input("\n按Enter键退出...")