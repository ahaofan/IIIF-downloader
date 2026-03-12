#!/usr/bin/env python3
"""
测试从IIIF Presentation API manifest.json中提取图像地址
"""

import json
from iiif_downloader.iiif_parser import IIIFParser

def test_manifest_parsing():
    """测试解析manifest.json"""
    print("测试解析IIIF Presentation API manifest.json...")
    
    # 读取test.json文件
    with open('test.json', 'r', encoding='utf-8') as f:
        manifest_json = json.load(f)
    
    print(f"Manifest类型: {manifest_json.get('@type')}")
    print(f"Manifest ID: {manifest_json.get('@id')}")
    
    # 创建解析器
    parser = IIIFParser()
    
    # 提取所有图片地址
    image_urls = parser.get_all_image_urls(manifest_json)
    
    print(f"\n提取到的图片地址数量: {len(image_urls)}")
    print("提取到的图片地址:")
    for i, url in enumerate(image_urls, 1):
        print(f"{i}. {url}")
    
    # 验证是否提取到了正确的图片地址
    assert len(image_urls) > 0, "没有提取到图片地址"
    
    # 检查是否包含预期的图片地址
    expected_base_url = "https://emuseum.nich.go.jp/iiif/?IIIF=/100949001005.tif"
    expected_image_url = "https://emuseum.nich.go.jp/iiif/?IIIF=/100949001005.tif/full/max/0/default.jpg"
    
    assert any(expected_base_url in url for url in image_urls), f"没有找到预期的基础URL: {expected_base_url}"
    assert any(expected_image_url in url for url in image_urls), f"没有找到预期的图片URL: {expected_image_url}"
    
    print("\n✓ 测试通过！成功从manifest.json中提取到图片地址")

if __name__ == "__main__":
    test_manifest_parsing()