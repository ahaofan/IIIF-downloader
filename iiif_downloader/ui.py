import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import requests
import threading
import os
from .iiif_parser import IIIFParser
from .downloader import IIIFDownloader

class IIIFDownloaderUI:
    def __init__(self, root):
        self.root = root
        self.root.title("IIIF Image Downloader")
        self.root.geometry("800x750")
        
        self.parser = IIIFParser()
        self.downloader = IIIFDownloader()
        
        self.save_dir = ""
        
        self.create_widgets()
    
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 输入区域 - 只接受JSON输入
        input_area_frame = ttk.LabelFrame(main_frame, text="输入JSON数据", padding="10")
        input_area_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 创建文本框和滚动条
        input_frame = ttk.Frame(input_area_frame)
        input_frame.pack(fill=tk.BOTH, expand=True)
        
        self.input_text = tk.Text(input_frame, height=10, wrap=tk.WORD)
        self.input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 添加滚动条
        input_scrollbar = ttk.Scrollbar(input_frame, orient=tk.VERTICAL, command=self.input_text.yview)
        input_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.input_text.config(yscrollcommand=input_scrollbar.set)
        
        # 输入框控制 - 放在输入框下面
        input_control_frame = ttk.Frame(input_area_frame)
        input_control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(input_control_frame, text="重置", command=self.clear_input).pack(side=tk.RIGHT, padx=5)
        
        # 保存路径选择
        path_frame = ttk.LabelFrame(main_frame, text="保存路径", padding="10")
        path_frame.pack(fill=tk.X, pady=5)
        
        # 设置默认保存路径为系统下载路径
        import os
        default_download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        self.path_var = tk.StringVar(value=default_download_path)
        ttk.Entry(path_frame, textvariable=self.path_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(path_frame, text="浏览", command=self.browse_path).pack(side=tk.RIGHT, padx=5)
        
        # 下载按钮 - 放在保存路径下面
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="下载全部图片", command=self.download_all).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(button_frame, text="取消下载", command=self.cancel_download).pack(side=tk.RIGHT, padx=5)
        
        # 下载进度条
        progress_frame = ttk.LabelFrame(main_frame, text="下载进度", padding="10")
        progress_frame.pack(fill=tk.X, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # 下载速度和状态显示
        self.status_details_var = tk.StringVar(value="准备就绪")
        ttk.Label(progress_frame, textvariable=self.status_details_var).pack(anchor=tk.W)
        
        # 图片地址显示区域 - 放在进度条下面
        urls_frame = ttk.LabelFrame(main_frame, text="图片地址", padding="10")
        urls_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 创建文本框和滚动条
        urls_inner_frame = ttk.Frame(urls_frame)
        urls_inner_frame.pack(fill=tk.BOTH, expand=True)
        
        self.urls_text = tk.Text(urls_inner_frame, height=5, wrap=tk.WORD, state=tk.DISABLED)
        self.urls_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 添加滚动条
        urls_scrollbar = ttk.Scrollbar(urls_inner_frame, orient=tk.VERTICAL, command=self.urls_text.yview)
        urls_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.urls_text.config(yscrollcommand=urls_scrollbar.set)
        
        # 状态区域
        self.status_var = tk.StringVar(value="就绪")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_label.pack(fill=tk.X, pady=5)
        # 确保状态标签可见
        status_label.update_idletasks()
    
    def browse_path(self):
        """浏览保存路径"""
        directory = filedialog.askdirectory()
        if directory:
            self.path_var.set(directory)
            self.save_dir = directory
    
    def clear_input(self):
        """清空输入框"""
        self.input_text.delete(1.0, tk.END)
        self.urls_text.config(state=tk.NORMAL)
        self.urls_text.delete(1.0, tk.END)
        self.urls_text.config(state=tk.DISABLED)
        self.status_var.set("就绪")
        self.status_details_var.set("准备就绪")
    
    def cancel_download(self):
        """取消下载"""
        self.downloader.cancel_download()
        self.status_var.set("下载已取消")
        self.status_details_var.set("准备就绪")

    def download(self):
        """开始下载"""
        input_content = self.input_text.get(1.0, tk.END).strip()
        save_dir = self.path_var.get()
        
        if not input_content:
            messagebox.showerror("错误", "请输入JSON数据")
            return
        
        if not save_dir:
            messagebox.showerror("错误", "请选择保存路径")
            return
        
        # 使用线程处理下载，避免UI卡死
        def download_thread():
            try:
                # 尝试解析为JSON
                try:
                    info_json = json.loads(input_content)
                    self.status_var.set("检测到JSON数据")
                    self.root.update()
                except json.JSONDecodeError:
                    # 不是JSON，视为URL
                    info_url = self.parser.parse_from_url(input_content)
                    response = requests.get(info_url)
                    response.raise_for_status()
                    info_json = response.json()
                    self.status_var.set("检测到URL，正在获取info.json")
                    self.root.update()
                
                # 提取并显示所有图片地址
                image_urls = self.parser.get_all_image_urls(info_json, self.format_var.get())
                self.urls_text.delete(1.0, tk.END)
                for url in image_urls:
                    self.urls_text.insert(tk.END, url + "\n")
                self.status_var.set(f"提取到 {len(image_urls)} 个图片地址")
                self.root.update()
                
                # 获取下载参数
                region = self.region_var.get()
                size = self.size_var.get()
                rotation = self.rotation_var.get()
                quality = self.quality_var.get()
                format = self.format_var.get()
                
                # 下载图片
                results = self.downloader.download_from_info(
                    info_json, save_dir, region, size, rotation, quality, format
                )
                
                # 显示结果
                success_count = sum(1 for _, _, success in results if success)
                if success_count > 0:
                    self.root.after(0, lambda: messagebox.showinfo("成功", f"成功下载 {success_count} 张图片"))
                    self.status_var.set("下载完成")
                else:
                    self.root.after(0, lambda: messagebox.showerror("错误", "下载失败"))
                    self.status_var.set("下载失败")
                    
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("错误", f"处理失败: {str(e)}"))
                self.status_var.set("处理失败")
        
        # 启动下载线程
        self.status_var.set("正在处理...")
        thread = threading.Thread(target=download_thread)
        thread.daemon = True
        thread.start()
    
    def download_all(self):
        """下载所有图片"""
        input_content = self.input_text.get(1.0, tk.END).strip()
        save_dir = self.path_var.get()
        
        if not input_content:
            messagebox.showerror("错误", "请输入JSON数据")
            return
        
        if not save_dir:
            messagebox.showerror("错误", "请选择保存路径")
            return
        
        # 使用线程处理下载，避免UI卡死
        def download_all_thread():
            try:
                # 直接解析为JSON
                info_json = json.loads(input_content)
                self.root.after(0, lambda: self.status_var.set("解析JSON数据"))
                
                # 提取作品名称
                work_name = self._extract_work_name(info_json)
                
                # 创建作品文件夹
                work_dir = os.path.join(save_dir, work_name)
                os.makedirs(work_dir, exist_ok=True)
                
                # 提取并显示所有图片地址
                image_urls = self.parser.get_all_image_urls(info_json, "jpg")
                self.root.after(0, lambda: self.urls_text.config(state=tk.NORMAL))
                self.root.after(0, lambda: self.urls_text.delete(1.0, tk.END))
                for url in image_urls:
                    self.root.after(0, lambda u=url: self.urls_text.insert(tk.END, u + "\n"))
                self.root.after(0, lambda: self.urls_text.config(state=tk.DISABLED))
                self.root.after(0, lambda: self.status_var.set(f"提取到 {len(image_urls)} 个图片地址，开始下载"))
                
                # 下载所有图片
                total_images = len(image_urls)
                self.root.after(0, lambda: self.progress_var.set(0))
                
                # 定义进度更新函数
                def update_progress(current, total, speed):
                    progress = (current / total) * 100
                    self.root.after(0, lambda: self.progress_var.set(progress))
                    self.root.after(0, lambda: self.status_details_var.set(f"正在下载 {current}/{total} 张图片，速度: {speed:.2f} KB/s"))
                
                # 下载所有图片（使用默认格式jpg）
                results = self.downloader.download_all_images(info_json, work_dir, "jpg", update_progress)
                
                # 显示结果
                success_count = sum(1 for _, _, success in results if success)
                if success_count > 0:
                    self.root.after(0, lambda: messagebox.showinfo("成功", f"成功下载 {success_count} 张图片到 {work_dir}"))
                    self.root.after(0, lambda: self.status_var.set("下载完成"))
                    self.root.after(0, lambda: self.status_details_var.set("准备就绪"))
                else:
                    self.root.after(0, lambda: messagebox.showerror("错误", "下载失败"))
                    self.root.after(0, lambda: self.status_var.set("下载失败"))
                    self.root.after(0, lambda: self.status_details_var.set("准备就绪"))
                    
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("错误", f"处理失败: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("处理失败"))
                self.root.after(0, lambda: self.status_details_var.set("准备就绪"))
        
        # 重置取消状态
        self.downloader.reset_cancel()
        
        # 启动下载线程
        self.status_var.set("正在处理...")
        self.status_details_var.set("正在处理...")
        thread = threading.Thread(target=download_all_thread)
        thread.daemon = True
        thread.start()
    
    def _extract_work_name(self, iiif_json):
        """提取作品名称"""
        # 从manifest中提取label
        if '@type' in iiif_json and iiif_json['@type'] == 'sc:Manifest':
            # 尝试从metadata中获取标题
            metadata = iiif_json.get('metadata', [])
            for item in metadata:
                if item.get('label') in ['标题', 'title', '名称', 'name']:
                    return str(item.get('value', 'untitled')).replace('/', '').replace('\\', '')
            
            # 尝试从label中获取
            if 'label' in iiif_json:
                label = iiif_json['label']
                if isinstance(label, list):
                    for item in label:
                        if '@value' in item:
                            return str(item['@value']).replace('/', '').replace('\\', '')
                else:
                    return str(label).replace('/', '').replace('\\', '')
            
            # 从within中获取
            within = iiif_json.get('within', {})
            if 'label' in within:
                label = within['label']
                if isinstance(label, list):
                    for item in label:
                        if '@value' in item:
                            return str(item['@value']).replace('/', '').replace('\\', '')
                else:
                    return str(label).replace('/', '').replace('\\', '')
        
        # 默认名称
        return 'untitled'
    
    def run(self):
        """运行UI"""
        self.root.mainloop()