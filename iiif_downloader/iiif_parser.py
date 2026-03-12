import json
import re
from urllib.parse import urlparse, urljoin

class IIIFParser:
    def __init__(self):
        pass
    
    def parse_from_url(self, url):
        """从IIIF URL解析信息"""
        # 检查是否是IIIF Image API URL
        if '/info.json' in url:
            # 已经是info.json URL
            info_url = url
        else:
            # 尝试构造info.json URL
            parsed = urlparse(url)
            path = parsed.path
            # 移除可能的参数和后缀
            path = re.sub(r'/(full|\d+,\d+|pct:\d+)/(\d+|max)/(0|180|270|90)/(default|gray|color|bitonal)(\.\w+)?$', '', path)
            info_url = urljoin(url, path + '/info.json')
        
        return info_url
    
    def parse_from_json(self, json_data):
        """从JSON数据解析IIIF信息"""
        if isinstance(json_data, str):
            json_data = json.loads(json_data)
        
        # 提取基本信息
        info = {
            'id': json_data.get('@id'),
            'width': json_data.get('width'),
            'height': json_data.get('height'),
            'profile': json_data.get('profile', []),
            'tiles': json_data.get('tiles', [])
        }
        
        return info
    
    def get_image_urls(self, info_json, region='full', size='max', rotation='0', quality='default', format='jpg'):
        """根据info.json生成图片URL"""
        base_url = info_json.get('@id')
        if not base_url:
            return []
        
        # 构建基本URL模板
        image_url = f"{base_url}/{region}/{size}/{rotation}/{quality}.{format}"
        
        return [image_url]
    
    def get_all_image_urls(self, iiif_json, format='jpg'):
        """从IIIF JSON中提取所有图片地址"""
        image_urls = []
        
        # 检查是否是Presentation API的manifest
        if '@type' in iiif_json and iiif_json['@type'] == 'sc:Manifest':
            # 处理Presentation API格式
            image_urls.extend(self._extract_from_manifest(iiif_json, format))
        else:
            # 处理Image API的info.json格式
            image_urls.extend(self._extract_from_info(iiif_json, format))
        
        return image_urls
    
    def _extract_from_manifest(self, manifest_json, format='jpg'):
        """从Presentation API manifest中提取图片地址"""
        image_urls = []
        
        # 遍历sequences
        sequences = manifest_json.get('sequences', [])
        for sequence in sequences:
            # 遍历canvases
            canvases = sequence.get('canvases', [])
            for canvas in canvases:
                # 遍历images
                images = canvas.get('images', [])
                for image in images:
                    # 获取resource
                    resource = image.get('resource', {})
                    # 获取service
                    service = resource.get('service', {})
                    if service and '@id' in service:
                        # 提取Image API基础URL
                        base_url = service['@id']
                        # 构建完整尺寸图片URL（高清图）
                        full_image_url = f"{base_url}/full/max/0/default.{format}"
                        image_urls.append(full_image_url)
        
        return image_urls
    
    def _extract_from_info(self, info_json, format='jpg'):
        """从Image API info.json中提取图片地址"""
        image_urls = []
        
        # 基本图片URL
        base_url = info_json.get('@id')
        if base_url:
            # 添加完整尺寸图片
            full_image_url = f"{base_url}/full/max/0/default.{format}"
            image_urls.append(full_image_url)
            
            # 从tiles中提取图片URL
            tiles = info_json.get('tiles', [])
            for tile in tiles:
                width = tile.get('width', 512)
                height = tile.get('height', 512)
                scale_factors = tile.get('scaleFactors', [1])
                
                for scale in scale_factors:
                    tile_url = f"{base_url}/full/{width * scale},{height * scale}/0/default.{format}"
                    image_urls.append(tile_url)
            
            # 从sizes中提取不同尺寸的图片
            sizes = info_json.get('sizes', [])
            for size in sizes:
                width = size.get('width')
                height = size.get('height')
                if width and height:
                    size_url = f"{base_url}/full/{width},{height}/0/default.{format}"
                    image_urls.append(size_url)
        
        return image_urls