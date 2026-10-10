import os
import sys
import subprocess
import threading
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ctypes
import tempfile

# ================= 终极原生拖拽类 =================
class DropTarget:
    def __init__(self, widget, callback):
        self.widget = widget
        self.callback = callback
        self.hwnd = widget.winfo_id()
        self._callback_ptr = ctypes.WINFUNCTYPE(
            ctypes.c_long, ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p, ctypes.c_void_p
        )(self._wnd_proc_callback)
        self._old_wnd_proc = ctypes.windll.user32.SetWindowLongPtrA(
            self.hwnd, -4, ctypes.cast(self._callback_ptr, ctypes.c_void_p)
        )
        ctypes.windll.shell32.DragAcceptFiles(self.hwnd, True)

    def _wnd_proc_callback(self, hwnd, msg, wparam, lparam):
        msg_int = msg if isinstance(msg, int) else ctypes.c_ulong(msg).value
        if msg_int == 0x0233:
            try:
                self._handle_drop(wparam)
            except Exception:
                pass
            return 0
        return ctypes.windll.user32.CallWindowProcA(
            self._old_wnd_proc, hwnd, msg, wparam, lparam
        )

    def _handle_drop(self, hdrop):
        try:
            count = ctypes.windll.shell32.DragQueryFileW(hdrop, 0xFFFFFFFF, None, 0)
            if count == 0: return
            files = []
            buf = ctypes.create_unicode_buffer(260)
            for i in range(count):
                ctypes.windll.shell32.DragQueryFileW(hdrop, i, buf, len(buf))
                path = buf.value
                if os.path.isfile(path) and path not in files:
                    files.append(path)
            if files:
                self.widget.after(0, lambda: self.callback(files))
        finally:
            ctypes.windll.shell32.DragFinish(hdrop)

# ================= 核心工具与业务逻辑 =================
def find_7z():
    candidates = [r"C:\Program Files\7-Zip\7z.exe", r"C:\Program Files (x86)\7-Zip\7z.exe"]
    for p in candidates:
        if os.path.isfile(p): return p
    try:
        result = subprocess.run(["where", "7z"], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip().split("\n")[0].strip()
    except Exception: pass
    return None

def format_size(size_bytes):
    if size_bytes >= 1024**3: return f"{size_bytes / 1024**3:.2f} GB"
    if size_bytes >= 1024**2: return f"{size_bytes / 1024**2:.2f} MB"
    return f"{size_bytes} B"

# ================= 界面与事件处理 =================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("文件分卷与合并工具 (彻底修复版V4)")
        self.root.geometry("700x600")
        self.files_list = []
        self._build_ui()

    def _build_ui(self):
        ttk.Label(self.root, text="将文件拖拽到下方，或点击手动添加：", font=("微软雅黑", 11)).pack(pady=15)
        self.listbox = tk.Listbox(self.root, height=6, font=("微软雅黑", 9))
        self.listbox.pack(fill="both", expand=True, padx=20)
        DropTarget(self.listbox, self._on_drop)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="手动添加文件", command=self.on_add_files, width=12).pack(side="left", padx=5)
        self.start_btn = ttk.Button(btn_frame, text="🚀 开始执行", command=self.start_process, width=12)
        self.start_btn.pack(side="left", padx=5)
        ttk.Button(btn_frame, text="清空列表", command=self.clear_files, width=12).pack(side="left", padx=5)

        log_frame = ttk.LabelFrame(self.root, text="执行日志", padding=10)
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.log_text = tk.Text(log_frame, height=6, state="disabled", font=("Consolas", 9))
        self.log_text.pack(fill="both", expand=True)

    def _on_drop(self, files):
        for f in files:
            if f not in self.files_list:
                self.files_list.append(f)
        self._refresh_list()

    def on_add_files(self):
        paths = filedialog.askopenfilenames(title="选择文件")
        if paths:
            for p in paths:
                if p not in self.files_list:
                    self.files_list.append(p)
            self._refresh_list()

    def clear_files(self):
        self.files_list.clear()
        self._refresh_list()

    def _refresh_list(self):
        self.listbox.delete(0, "end")
        for f in self.files_list:
            self.listbox.insert("end", os.path.basename(f))

    def log(self, text):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", text + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def start_process(self):
        if not self.files_list:
            messagebox.showwarning("提示", "请先拖入或添加文件！")
            return
        
        output_dir = filedialog.askdirectory(title="选择保存目录")
        if not output_dir:
            return
            
        self.start_btn.config(state="disabled")
        self.log_text.configure(state="normal"); self.log_text.delete("1.0", "end"); self.log_text.configure(state="disabled")
        self.log(f"开始处理... 输出目录: {output_dir}")
        
        t = threading.Thread(target=self.process_files, args=(self.files_list, output_dir), daemon=True)
        t.start()

    # ---------- 核心业务处理逻辑 (终极无死循环版) ----------
    def process_files(self, files, output_dir):
        seven_zip = find_7z()
        if not seven_zip:
            self.log("错误：未在电脑中找到 7-Zip 软件，请先安装！")
            self.root.after(0, lambda: self.start_btn.config(state="normal"))
            return

        self.log(">>> 正在扫描拖入的文件...")
        info_path = None
        complete_files = []
        for f in files:
            if f.endswith(".split_info.txt"):
                info_path = f
            else:
                complete_files.append(f)

        merge_path = ""
        original_name = ""
        
        # 【逻辑一：处理分卷零件】
        if info_path:
            self.log("[识别为分卷零件] 正在自动合并...")
            info = {}
            try:
                with open(info_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if "=" in line:
                            k, v = line.strip().split("=", 1)
                            info[k] = v
                original_name = info.get("original_name", "merged_file")
                info_dir = os.path.dirname(info_path)
                merge_path = os.path.join(output_dir, original_name)
                
                with open(merge_path, "wb") as fout:
                    total_parts = int(info.get("total_parts", 0))
                    for i in range(1, total_parts + 1):
                        part_name = f"{original_name}.part{i:04d}"
                        _, ext = os.path.splitext(original_name)
                        if ext: part_name += ext
                        part_path = os.path.join(info_dir, part_name)
                        if not os.path.exists(part_path): 
                            raise FileNotFoundError(f"缺少分卷文件: {part_path}")
                        with open(part_path, "rb") as fin: 
                            fout.write(fin.read())
                self.log("合并完成，准备打包...")
            except Exception as e:
                self.log(f"合并失败: {str(e)}")
                self.root.after(0, lambda: self.start_btn.config(state="normal"))
                return
        # 【逻辑二：处理完整文件】
        elif complete_files:
            original_name = os.path.basename(complete_files[0])
            merge_path = complete_files[0]
            self.log(f"[识别为完整文件] 准备直接打包...")
        else:
            self.log("未识别到有效文件，请拖入 .part 或 .split_info.txt 文件。")
            self.root.after(0, lambda: self.start_btn.config(state="normal"))
            return

        # 【第一步】打包成 ZIP
        zip_name = original_name + ".zip"
        zip_path = os.path.join(output_dir, zip_name)
        
        self.log(f"正在打包 {zip_name} ...")
        cmd = [seven_zip, "a", "-tzip", zip_path, merge_path, "-r"]
        result = subprocess.run(cmd, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        if result.returncode != 0: 
            self.log(f"打包失败: {result.stderr}")
            self.root.after(0, lambda: self.start_btn.config(state="normal"))
            return

        zip_size = os.path.getsize(zip_path)
        self.log(f"打包成功，大小: {format_size(zip_size)}")

        # 【第二步】终极安全的自动分卷逻辑
        if zip_size > 100 * 1024 * 1024:
            self.log("超过 100MB，正在执行 80MB 绝对安全分卷...")
            
            try:
                # 1. 创建一个系统临时文件夹，作为 7-Zip 的绝对隔离操作区
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_zip_path = os.path.join(temp_dir, zip_name)
                    
                    # 2. 将打包好的 ZIP 安全地复制到这个临时文件夹里
                    self.log("正在转移文件至安全隔离区...")
                    shutil.copy2(zip_path, temp_zip_path)
                    
                    # 3. 让 7-Zip 在这个绝对干净的临时文件夹里切分文件
                    # 输出到当前目录 (.), 也就是 temp_dir
                    cmd_split = [seven_zip, "a", "-v83886080b", ".", zip_name]
                    result = subprocess.run(cmd_split, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW, cwd=temp_dir)
                    
                    if result.returncode != 0:
                        self.log(f"分卷失败: {result.stderr}")
                        self.root.after(0, lambda: self.start_btn.config(state="normal"))
                        return
                    
                    # 4. 把切好的分卷包 (.zip, .z001 等) 复制回你选择的输出文件夹
                    for f_name in os.listdir(temp_dir):
                        shutil.copy2(os.path.join(temp_dir, f_name), output_dir)
                        
            except Exception as e:
                self.log(f"分卷过程出现致命错误: {str(e)}")
                self.root.after(0, lambda: self.start_btn.config(state="normal"))
                return

            # 5. 删除原始未切割的大 ZIP 包
            if os.path.exists(zip_path):
                os.remove(zip_path)
            self.log("分卷完成，已清理临时大文件。")
        else:
            self.log("未超过 100MB，无需分卷。")

        self.log("🎉 任务圆满完成！")
        os.startfile(output_dir)
        self.root.after(0, lambda: messagebox.showinfo("🎉 成功", "分卷压缩已完成！\n\n文件夹已自动为您打开。"))
        self.root.after(0, lambda: self.start_btn.config(state="normal"))

# ================= 程序入口 =================
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()