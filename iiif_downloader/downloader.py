import os
import requests
from tqdm import tqdm

class IIIFDownloader:
    def __init__(self):
        self._cancel = False
    
    def cancel_download(self):
        """取消下载"""
        self._cancel = True
    
    def reset_cancel(self):
        """重置取消状态"""
        self._cancel = False
    
    def download_image(self, url, save_path, progress_callback=None, current=0, total=1):
        """下载单个图片"""
        try:
            import time
            # 添加浏览器头信息，伪装为浏览器
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            # 打印调试信息
            print(f"开始下载: {url}")
            print(f"保存路径: {save_path}")
            
            response = requests.get(url, stream=True, timeout=30, headers=headers)
            response.raise_for_status()
            
            # 确保目录存在
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # 下载并显示进度
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0
            start_time = time.time()
            
            # 控制进度回调频率
            callback_interval = 100  # 每100个chunk回调一次
            chunk_count = 0
            
            # 移除tqdm，因为它在非控制台环境中可能有问题
            with open(save_path, 'wb') as f:
                for data in response.iter_content(chunk_size=1024):
                    # 检查是否取消下载
                    if self._cancel:
                        print("下载已取消")
                        return False
                    
                    size = f.write(data)
                    downloaded_size += size
                    chunk_count += 1
                    
                    # 计算下载速度并更新进度，控制回调频率
                    if progress_callback and chunk_count % callback_interval == 0:
                        elapsed_time = time.time() - start_time
                        if elapsed_time > 0:
                            speed = downloaded_size / elapsed_time / 1024  # KB/s
                            progress_callback(current, total, speed)
            
            # 打印下载完成信息
            print(f"下载完成: {url}")
            print(f"文件大小: {os.path.getsize(save_path)} 字节")
            
            return True
        except Exception as e:
            print(f"下载失败: {str(e)}")
            # 确保文件被删除，避免生成0字节文件
            if os.path.exists(save_path):
                os.remove(save_path)
                print(f"已删除0字节文件: {save_path}")
            return False
    
    def download_images(self, urls, save_dir, filenames=None, progress_callback=None):
        """批量下载图片"""
        if filenames is None:
            filenames = [f"image_{i}.jpg" for i in range(len(urls))]
        
        results = []
        total = len(urls)
        for i, (url, filename) in enumerate(zip(urls, filenames)):
            save_path = os.path.join(save_dir, filename)
            success = self.download_image(url, save_path, progress_callback, i + 1, total)
            results.append((url, save_path, success))
        
        return results
    
    def download_from_info(self, info_json, save_dir, region='full', size='max', rotation='0', quality='default', format='jpg'):
        """从info.json下载图片"""
        from .iiif_parser import IIIFParser
        parser = IIIFParser()
        
        image_urls = parser.get_image_urls(info_json, region, size, rotation, quality, format)
        filenames = [f"image.{format}"]
        
        return self.download_images(image_urls, save_dir, filenames)
    
    def download_all_images(self, info_json, save_dir, format='jpg', progress_callback=None):
        """下载所有图片"""
        from .iiif_parser import IIIFParser
        parser = IIIFParser()
        
        image_urls = parser.get_all_image_urls(info_json, format)
        filenames = [f"image_{i}.{format}" for i in range(len(image_urls))]
        
        return self.download_images(image_urls, save_dir, filenames, progress_callback)