import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
from imageCompression import imageCompress, dirOfImageCompress

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("图片压缩工具")
        self.root.geometry("600x450")

        # --- Input Selection ---
        self.input_path_label = tk.Label(root, text="输入路径: (请选择图片或文件夹)")
        self.input_path_label.pack(pady=5)
        self.input_path_var = tk.StringVar()
        self.input_path_entry = tk.Entry(root, textvariable=self.input_path_var, width=70, state='readonly')
        self.input_path_entry.pack(pady=5, padx=10)

        self.select_frame = tk.Frame(root)
        self.select_frame.pack(pady=5)
        self.select_file_btn = tk.Button(self.select_frame, text="选择图片", command=self.select_file)
        self.select_file_btn.pack(side=tk.LEFT, padx=10)
        self.select_folder_btn = tk.Button(self.select_frame, text="选择文件夹", command=self.select_folder)
        self.select_folder_btn.pack(side=tk.LEFT, padx=10)

        # --- Output Selection ---
        self.output_path_label = tk.Label(root, text="输出文件夹:")
        self.output_path_label.pack(pady=5)
        self.output_path_var = tk.StringVar()
        self.output_path_entry = tk.Entry(root, textvariable=self.output_path_var, width=70, state='readonly')
        self.output_path_entry.pack(pady=5, padx=10)
        self.select_output_btn = tk.Button(root, text="选择输出文件夹", command=self.select_output_folder)
        self.select_output_btn.pack(pady=5)

        # --- Compression Settings ---
        self.settings_frame = tk.Frame(root)
        self.settings_frame.pack(pady=10)
        
        self.min_size_label = tk.Label(self.settings_frame, text="最小大小 (KB):")
        self.min_size_label.pack(side=tk.LEFT, padx=5)
        self.min_size_var = tk.StringVar(value="2048")
        self.min_size_entry = tk.Entry(self.settings_frame, textvariable=self.min_size_var, width=10)
        self.min_size_entry.pack(side=tk.LEFT)

        self.max_size_label = tk.Label(self.settings_frame, text="最大大小 (KB):")
        self.max_size_label.pack(side=tk.LEFT, padx=5)
        self.max_size_var = tk.StringVar(value="4096")
        self.max_size_entry = tk.Entry(self.settings_frame, textvariable=self.max_size_var, width=10)
        self.max_size_entry.pack(side=tk.LEFT)

        # --- Action Button ---
        self.compress_btn = tk.Button(root, text="开始压缩", command=self.start_compression, font=("Helvetica", 12, "bold"), bg="lightblue")
        self.compress_btn.pack(pady=20)

        # --- Status Log ---
        self.log_label = tk.Label(root, text="日志:")
        self.log_label.pack()
        self.log_text = tk.Text(root, height=8, width=70, state='disabled')
        self.log_text.pack(pady=10, padx=10)

    def select_file(self):
        path = filedialog.askopenfilename(
            title="选择一个图片文件",
            filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*"))
        )
        if path:
            self.input_path_var.set(path)
            self.log("已选择图片: " + path)

    def select_folder(self):
        path = filedialog.askdirectory(title="选择一个文件夹")
        if path:
            self.input_path_var.set(path)
            self.log("已选择文件夹: " + path)

    def select_output_folder(self):
        path = filedialog.askdirectory(title="选择输出文件夹")
        if path:
            self.output_path_var.set(path)
            self.log("已选择输出文件夹: " + path)

    def log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def start_compression(self):
        input_path = self.input_path_var.get()
        output_path = self.output_path_var.get()
        min_size_str = self.min_size_var.get()
        max_size_str = self.max_size_var.get()

        if not input_path or not output_path:
            messagebox.showerror("错误", "请输入输入路径和输出文件夹。")
            return
        
        try:
            min_size = int(min_size_str)
            max_size = int(max_size_str)
        except ValueError:
            messagebox.showerror("错误", "最小/最大大小必须是有效的数字。")
            return

        self.compress_btn.config(state='disabled', text="压缩中...")
        self.log("开始压缩...")
        
        # Run compression in a separate thread to avoid freezing the GUI
        thread = threading.Thread(
            target=self.run_compression_thread,
            args=(input_path, output_path, min_size, max_size)
        )
        thread.start()

    def run_compression_thread(self, input_path, output_path, min_size, max_size):
        # A wrapper for the log method to ensure it's called on the main GUI thread
        def gui_logger(message):
            self.root.after(0, self.log, message)

        try:
            if os.path.isfile(input_path):
                # Single file compression
                gui_logger(f"正在处理文件: {input_path}")
                imageCompress(
                    quality=95,  # Initial quality, will be overridden by search
                    subsampling=-1, # Not used in new logic
                    img_item=input_path,
                    notfound_imgs=[],
                    jpga=0,
                    output=output_path,
                    min_size_kb=min_size,
                    max_size_kb=max_size,
                    logger=gui_logger
                )
            elif os.path.isdir(input_path):
                # Directory compression
                gui_logger(f"正在处理文件夹: {input_path}")
                dirOfImageCompress(
                    dir=input_path,
                    quality=95,
                    subsampling=-1,
                    notfound_imgs=[],
                    jpga=0,
                    output=output_path,
                    min_size=min_size,
                    max_size=max_size,
                    logger=gui_logger
                )
            gui_logger("压缩完成！")
        except Exception as e:
            self.log(f"发生错误: {e}")
            messagebox.showerror("错误", f"压缩过程中发生错误: {e}")
        finally:
            self.compress_btn.config(state='normal', text="开始压缩")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
