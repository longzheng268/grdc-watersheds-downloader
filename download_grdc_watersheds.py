"""
GRDC 站点流域边界数据下载脚本
=================================
下载 GRDC 所有站点的流域边界 (catchment/watershed) 数据

数据来源: https://grdc.bafg.de/products/basin_layers/watershed_boundaries/index.html
包含约 10,000 个水文站点的流域多边形

数据说明:
- GRDC_Watersheds_shp.zip  : Shapefile 格式 (112MB)
- GRDC_Watersheds_geojson.zip : GeoJSON 格式 (110MB)
"""

import os
import zipfile
import urllib.request
import ssl

# ============================================================
# 配置
# ============================================================
DOWNLOAD_DIR = os.path.dirname(os.path.abspath(__file__))

# GRDC 流域边界直接下载链接 (无需登录)
DOWNLOAD_URLS = {
    "watershed_shp": "https://grdc.bafg.de/downloads/GRDC_Watersheds_shp.zip",
    "watershed_geojson": "https://grdc.bafg.de/downloads/GRDC_Watersheds_geojson.zip",
}

# GRDC 主要河流流域 (520个主要流域)
MRB_URL = "https://grdc.bafg.de/downloads/GRDC_Major_River_Basins.zip"

# GRDC 站点元数据 (需要从 Data Portal 手动下载)
# 官网: https://portal.grdc.bafg.de/applications/public.html?publicuser=PublicUser
# 在 Data Download > Stations 页面筛选后点击下载


def download_file(url, save_path, proxy=None):
    """下载文件并显示进度"""
    print(f"\n{'='*60}")
    print(f"下载: {url}")
    print(f"保存到: {save_path}")
    print(f"{'='*60}")

    # 设置代理 (如果需要)
    if proxy:
        os.environ['HTTP_PROXY'] = proxy
        os.environ['HTTPS_PROXY'] = proxy

    # 忽略 SSL 验证 (某些网络环境需要)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    def progress_hook(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            percent = min(100, downloaded * 100 / total_size)
            mb_downloaded = downloaded / (1024 * 1024)
            mb_total = total_size / (1024 * 1024)
            print(f"\r  进度: {percent:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)", end="", flush=True)
        else:
            mb_downloaded = downloaded / (1024 * 1024)
            print(f"\r  已下载: {mb_downloaded:.1f} MB", end="", flush=True)

    try:
        urllib.request.urlretrieve(url, save_path, reporthook=progress_hook)
        print(f"\n  下载完成!")
        return True
    except Exception as e:
        print(f"\n  下载失败: {e}")
        return False


def unzip_file(zip_path, extract_dir):
    """解压 ZIP 文件"""
    print(f"\n解压: {zip_path}")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(extract_dir)
            print(f"  解压完成, 文件列表:")
            for name in zf.namelist():
                print(f"    - {name}")
        return True
    except Exception as e:
        print(f"  解压失败: {e}")
        return False


def main():
    # 代理设置 (如果需要)
    proxy = "http://127.0.0.1:7890"  # 设置为 None 如果不需要代理
    # proxy = None

    if proxy:
        os.environ['HTTP_PROXY'] = proxy
        os.environ['HTTPS_PROXY'] = proxy
        print(f"使用代理: {proxy}")

    print("\n" + "="*60)
    print("GRDC 流域边界数据下载工具")
    print("="*60)
    print("\n数据说明:")
    print("  - 流域边界包含约 10,000 个 GRDC 水文站的 catchment 多边形")
    print("  - Shapefile 格式 (~112MB)")
    print("  - GeoJSON 格式 (~110MB)")
    print("\n选择下载内容:")
    print("  1. 流域边界 Shapefile (推荐)")
    print("  2. 流域边界 GeoJSON")
    print("  3. 全部下载")
    print("  4. 主要河流流域 (Major River Basins, 520个)")

    choice = input("\n请选择 [1/2/3/4]: ").strip()

    downloads = []
    if choice in ("1", "3"):
        downloads.append(("watershed_shp", "GRDC_Watersheds_shp.zip"))
    if choice in ("2", "3"):
        downloads.append(("watershed_geojson", "GRDC_Watersheds_geojson.zip"))
    if choice == "4":
        downloads.append(("major_basins", "GRDC_Major_River_Basins.zip"))

    if not downloads:
        print("无效选择, 默认下载 Shapefile 格式")
        downloads.append(("watershed_shp", "GRDC_Watersheds_shp.zip"))

    for key, filename in downloads:
        if key == "major_basins":
            url = MRB_URL
        else:
            url = DOWNLOAD_URLS[key]

        save_path = os.path.join(DOWNLOAD_DIR, filename)

        if os.path.exists(save_path):
            print(f"\n文件已存在: {save_path}")
            re_download = input("是否重新下载? [y/N]: ").strip().lower()
            if re_download != 'y':
                print("跳过下载, 直接解压...")
                unzip_file(save_path, DOWNLOAD_DIR)
                continue

        if download_file(url, save_path, proxy):
            unzip_file(save_path, DOWNLOAD_DIR)

    # 打印站点元数据获取说明
    print("\n" + "="*60)
    print("站点元数据获取方式:")
    print("="*60)
    print("""
  GRDC 站点元数据 (站点名称、坐标、流域面积等) 需要从 Data Portal 获取:

  1. 访问: https://portal.grdc.bafg.de/applications/public.html?publicuser=PublicUser
  2. 点击左侧 "Data Download" > "Stations"
  3. 使用筛选条件选择需要的站点
  4. 点击下载按钮获取站点列表 (CSV 格式)

  注意: 下载的流域 Shapefile 中已包含 GRDC_NO (站点编号) 字段,
       可以与站点元数据通过该字段关联

  流域 Shapefile 主要字段:
    - GRDC_NO    : GRDC 站点编号 (与站点元数据关联的 key)
    - area_calc  : 计算的流域面积 (km²)
    - geometry   : 流域多边形边界
""")

    print("完成! 数据保存在:", DOWNLOAD_DIR)


if __name__ == "__main__":
    main()
