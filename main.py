from modelscope import snapshot_download
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os

class ModelDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ModelScope 模型下载器")
        self.root.geometry("600x400")
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 模型ID输入
        ttk.Label(main_frame, text="模型ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.model_id_var = tk.StringVar()
        self.model_id_entry = ttk.Entry(main_frame, textvariable=self.model_id_var, width=50)
        self.model_id_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # 下载目录选择
        ttk.Label(main_frame, text="下载目录:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        dir_frame = ttk.Frame(main_frame)
        dir_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        dir_frame.columnconfigure(0, weight=1)
        
        self.download_dir_var = tk.StringVar()
        self.download_dir_entry = ttk.Entry(dir_frame, textvariable=self.download_dir_var)
        self.download_dir_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        self.browse_button = ttk.Button(dir_frame, text="浏览", command=self.browse_directory)
        self.browse_button.grid(row=0, column=1)
        
        # 下载按钮
        self.download_button = ttk.Button(main_frame, text="开始下载", command=self.start_download)
        self.download_button.grid(row=2, column=0, columnspan=2, pady=20)
        
        # 进度条
        self.progress_var = tk.StringVar()
        self.progress_var.set("准备就绪")
        ttk.Label(main_frame, text="状态:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.progress_label = ttk.Label(main_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # 日志文本框
        ttk.Label(main_frame, text="下载日志:").grid(row=4, column=0, sticky=(tk.W, tk.N), pady=5)
        
        log_frame = ttk.Frame(main_frame)
        log_frame.grid(row=4, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        self.log_text = tk.Text(log_frame, height=10, width=50)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 设置默认下载目录为当前目录下的models文件夹
        default_dir = os.path.join(os.getcwd(), "models")
        self.download_dir_var.set(default_dir)
        
    def browse_directory(self):
        """浏览并选择下载目录"""
        directory = filedialog.askdirectory()
        if directory:
            self.download_dir_var.set(directory)
    
    def log_message(self, message):
        """在日志文本框中添加消息"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def start_download(self):
        """开始下载模型"""
        model_id = self.model_id_var.get().strip()
        download_dir = self.download_dir_var.get().strip()
        
        if not model_id:
            messagebox.showerror("错误", "请输入模型ID")
            return
        
        if not download_dir:
            messagebox.showerror("错误", "请选择下载目录")
            return
        
        # 禁用下载按钮
        self.download_button.config(state="disabled")
        self.progress_var.set("正在下载...")
        
        # 清空日志
        self.log_text.delete(1.0, tk.END)
        
        # 在新线程中执行下载
        download_thread = threading.Thread(target=self.download_model, args=(model_id, download_dir))
        download_thread.daemon = True
        download_thread.start()
    
    def download_model(self, model_id, download_dir):
        """下载模型的实际函数"""
        try:
            self.log_message(f"开始下载模型: {model_id}")
            self.log_message(f"下载目录: {download_dir}")
            
            # 确保下载目录存在
            os.makedirs(download_dir, exist_ok=True)
            
            # 使用snapshot_download下载模型
            model_path = snapshot_download(
                model_id=model_id,
                cache_dir=download_dir
            )
            
            self.log_message(f"模型下载成功!")
            self.log_message(f"模型路径: {model_path}")
            self.progress_var.set("下载完成")
            
            # 显示成功消息
            self.root.after(0, lambda: messagebox.showinfo("成功", f"模型下载完成!\n路径: {model_path}"))
            
        except Exception as e:
            error_msg = f"下载失败: {str(e)}"
            self.log_message(error_msg)
            self.progress_var.set("下载失败")
            
            # 显示错误消息
            self.root.after(0, lambda: messagebox.showerror("错误", error_msg))
        
        finally:
            # 重新启用下载按钮
            self.root.after(0, lambda: self.download_button.config(state="normal"))

def main():
    """主函数 - 启动GUI应用"""
    root = tk.Tk()
    app = ModelDownloaderGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()