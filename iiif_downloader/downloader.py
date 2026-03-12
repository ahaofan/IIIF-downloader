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
            response = requests.get(url, stream=True, timeout=30)
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
            
            with open(save_path, 'wb') as f, tqdm(
                desc=os.path.basename(save_path),
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                ncols=80,  # 设置进度条宽度
                leave=False,  # 下载完成后不保留进度条
                dynamic_ncols=True  # 动态调整宽度
            ) as bar:
                for data in response.iter_content(chunk_size=1024):
                    # 检查是否取消下载
                    if self._cancel:
                        print("下载已取消")
                        return False
                    
                    size = f.write(data)
                    downloaded_size += size
                    bar.update(size)
                    chunk_count += 1
                    
                    # 计算下载速度并更新进度，控制回调频率
                    if progress_callback and chunk_count % callback_interval == 0:
                        elapsed_time = time.time() - start_time
                        if elapsed_time > 0:
                            speed = downloaded_size / elapsed_time / 1024  # KB/s
                            progress_callback(current, total, speed)
            
            return True
        except Exception as e:
            print(f"下载失败: {e}")
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