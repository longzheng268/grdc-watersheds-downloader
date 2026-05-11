# GRDC 全球径流数据中心 - 流域边界数据

## 项目目标

获取 **GRDC（Global Runoff Data Centre）所有水文站点**对应的**流域边界数据**（catchment/watershed shapefile），用于水文建模、径流分析等研究。

## 数据来源

- **官方机构**: GRDC，隶属世界气象组织（WMO），由德国联邦水文研究所（BfG）运营
- **数据官网**: https://portal.grdc.bafg.de
- **流域边界产品页**: https://grdc.bafg.de/products/basin_layers/watershed_boundaries/index.html

## 核心数据下载链接

### 流域边界（Station Catchments）—— 本项目主要目标

| 格式 | 大小 | 直接下载链接 |
|------|------|-------------|
| Shapefile (.zip) | ~112 MB | https://grdc.bafg.de/downloads/GRDC_Watersheds_shp.zip |
| GeoJSON (.zip) | ~110 MB | https://grdc.bafg.de/downloads/GRDC_Watersheds_geojson.zip |

- 覆盖约 **10,000 个** GRDC 水文站
- 每个站点对应一个多边形，表示该站点上游的集水区边界
- Shapefile 中包含 `GRDC_NO` 字段，可与站点元数据关联

### 其他相关数据

| 数据 | 说明 | 链接 |
|------|------|------|
| 主要河流流域 (MRB) | 520个全球主要流域 | https://grdc.bafg.de/downloads/GRDC_Major_River_Basins.zip |
| WMO 流域分区 | WMO 标准流域划分 | https://grdc.bafg.de/downloads/GRDC_WMO_Basins.zip |

### 站点元数据（需手动从 Portal 下载）

- **入口**: https://portal.grdc.bafg.de/applications/public.html?publicuser=PublicUser
- **路径**: 左侧菜单 → Data Download → Stations → 筛选 → 下载
- **无需注册**，PublicUser 即可访问

## 快速开始

### 1. 创建虚拟环境

```bash
# 使用 conda
conda create -n grdc python=3.11 -y
conda activate grdc

# 或使用 venv
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate
```

### 2. 安装依赖

下载脚本本身只用标准库，**不装依赖也能跑**。如果后续要读取/分析数据：

```bash
pip install -r requirements.txt
```

`requirements.txt` 内容：

```
geopandas>=0.14
matplotlib>=3.8
```

### 3. 下载数据

```bash
python download_grdc_watersheds.py
```

脚本功能：
- 交互式选择格式（Shapefile / GeoJSON / 全部）
- 下载进度显示
- 自动解压
- 需要代理时在脚本顶部修改 `proxy` 变量

### 4. 使用数据

```python
import geopandas as gpd

# 读取流域边界（文件名是时间戳格式，按实际解压结果填写）
gdf = gpd.read_file("2025-09-18 09-42-59.shp")

# 查看字段
print(gdf.columns)
# 字段: grdc_no, river, station, area, area_calc, lat_org, long_org, ...

# 按站点编号筛选
station = gdf[gdf['grdc_no'] == 6340100]

# 保存为 GeoJSON
gdf.to_file("GRDC_Watersheds.geojson", driver="GeoJSON")
```

## 项目结构

```
grdc-watersheds-downloader/
├── README.md                      # 本文件
├── GRDC数据获取细则.md             # 详细技术文档（供 AI 工具 / Claude Code 参考）
├── download_grdc_watersheds.py    # 下载脚本（仅依赖标准库）
├── requirements.txt               # 数据分析依赖（可选）
├── LICENSE                        # GPL-2.0
│
│  --- 以下为下载后生成，已 .gitignore 排除 ---
├── GRDC_Watersheds_shp.zip        # 流域边界 Shapefile 压缩包 (~112MB)
└── 2025-xx-xx xx-xx-xx.shp/.dbf/.prj/.shx  # 解压后的 Shapefile
```

## 常见问题

### Q: 解压后的文件名是时间戳（如 `2025-09-18 09-42-59.shp`）？

这是 GRDC 官方打包时的命名。文件内容是完整的全球流域边界，可用 `gpd.read_file()` 正常读取。如需重命名：

```bash
# Windows PowerShell
Rename-Item "2025-09-18 09-42-59.shp" "GRDC_Watersheds.shp"
Rename-Item "2025-09-18 09-42-59.dbf" "GRDC_Watersheds.dbf"
Rename-Item "2025-09-18 09-42-59.shx" "GRDC_Watersheds.shx"
Rename-Item "2025-09-18 09-42-59.prj" "GRDC_Watersheds.prj"
```

同一组文件的 `.shp` `.shx` `.dbf` `.prj` 必须保持**相同前缀名**。

### Q: Shapefile 里已有站点元数据，还需要从 Portal 下载吗？

**基本不需要**。下载的 Shapefile 已包含 `grdc_no`（站点编号）、`river`（河流名）、`station`（站名）、`lat_org`/`long_org`（坐标）、`area`（报告面积）、`area_calc`（计算面积）等字段。仅在需要更多字段（如数据起止年份）时才去 Portal 补充。

### Q: 需要代理吗？

GRDC 服务器位于德国，在国内访问可能较慢。脚本默认使用代理 `http://127.0.0.1:7890`，如不需要可在脚本中设置 `proxy = None`。

### Q: 如何关联站点元数据和流域边界？

两个数据集通过 `GRDC_NO`（GRDC 站点编号）字段关联。流域 Shapefile 中有 `GRDC_NO`，站点元数据 CSV 中也有对应字段。

## 引用

```
GRDC (2023): Watershed Boundaries of GRDC Stations. Global Runoff Data Centre.
Koblenz, Germany: Federal Institute of Hydrology (BfG).
```

## 许可

数据为 GRDC 公开数据，使用时请遵循 GRDC 数据政策并进行适当引用。
