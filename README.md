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

### 环境要求

- Python 3.8+
- conda 环境 `common`（含 geopandas 等地理数据处理库）

### 下载数据

```powershell
# 激活环境
conda activate common

# 运行下载脚本
python download_grdc_watersheds.py
```

脚本功能：
- 下载流域边界 Shapefile / GeoJSON
- 自动解压
- 配置代理（默认 `http://127.0.0.1:7890`，可在脚本中关闭）

### 使用数据

```python
import geopandas as gpd

# 读取流域边界
gdf = gpd.read_file("GRDC_Watersheds.shp")

# 查看字段
print(gdf.columns)
# 预期字段: GRDC_NO, area_calc, geometry, ...

# 按站点编号筛选
station = gdf[gdf['GRDC_NO'] == 6340100]

# 保存为 GeoJSON
gdf.to_file("GRDC_Watersheds.geojson", driver="GeoJSON")
```

## 目录结构

```
全球径流数据中心/
├── README.md                          # 本文件
├── GRDC数据获取细则.md                  # 详细技术文档，供 AI 工具参考
├── download_grdc_watersheds.py         # 下载脚本
├── GRDC_Watersheds_shp.zip             # 下载后：流域边界 Shapefile 压缩包
└── GRDC_Watersheds/                    # 解压后：流域边界 Shapefile 文件
    ├── GRDC_Watersheds.shp
    ├── GRDC_Watersheds.shx
    ├── GRDC_Watersheds.dbf
    ├── GRDC_Watersheds.prj
    └── ...
```

## 常见问题

### Q: 官网筛选后找不到下载按钮？

GRDC 的流域边界数据**不在 Data Portal 的筛选界面下载**，而是直接提供 ZIP 包下载链接。详见 `GRDC数据获取细则.md` 中的「官网导航路径」章节。

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
