# GRDC 数据获取细则

> 本文档供 Claude Code、GitHub Copilot 等 AI 工具参考，提供 GRDC 数据获取的完整技术细节。
> 最后更新: 2026-05-10

---

## 1. 背景概述

### 1.1 GRDC 是什么

GRDC（Global Runoff Data Centre，全球径流数据中心）是世界气象组织（WMO）下属的国际数据中心，由德国联邦水文研究所（BfG）运营。它维护着全球最全面的河流流量观测数据库，包含来自 160+ 个国家、超过 10,000 个水文站的历史径流数据。

### 1.2 数据需求

- **目标**: 获取 GRDC 所有水文站点对应的流域边界（catchment/watershed）多边形数据
- **格式**: Shapefile 或 GeoJSON
- **用途**: 水文建模、流域分析、径流归因等

### 1.3 关键发现

GRDC 流域边界数据**可免费公开下载**，但官网入口隐蔽，不在主门户（Data Portal）的筛选界面中，而是通过一个独立的产品页面提供直接下载链接。

---

## 2. GRDC 官网结构

### 2.1 两个独立系统

GRDC 的数据分布在两个不同的 Web 系统中：

| 系统 | URL | 用途 |
|------|-----|------|
| **GRDC Data Portal** | https://portal.grdc.bafg.de | 径流数据、站点元数据的筛选和下载（Dojo SPA 应用） |
| **GRDC 主站** | https://grdc.bafg.de | 数据产品文档、静态文件下载（Quarto 静态站点） |

### 2.2 官网导航路径

```
GRDC 主站 (grdc.bafg.de)
├── About (关于)
├── Discharge Data (径流数据)
│   └── Data Portal → 跳转到 portal.grdc.bafg.de
├── Special Data Products (特色数据产品)  ← 关键
│   ├── Basin Layers (流域图层)            ← 关键
│   │   ├── Major River Basins (主要河流流域)
│   │   ├── Watershed Boundaries (流域边界) ← 本项目目标
│   │   └── WMO Basins (WMO 流域分区)
│   ├── Freshwater Fluxes
│   ├── Runoff Fields
│   └── Packages
├── Collaboration
└── Resources
```

**到达目标页面的完整路径**:
```
https://grdc.bafg.de
  → Special Data Products
    → Basin Layers
      → Watershed Boundaries of GRDC Stations
        → https://grdc.bafg.de/products/basin_layers/watershed_boundaries/index.html
```

---

## 3. 数据清单

### 3.1 流域边界数据（核心数据）

| 文件 | 格式 | 大小 | URL | 说明 |
|------|------|------|-----|------|
| GRDC_Watersheds_shp.zip | Shapefile | ~112 MB | https://grdc.bafg.de/downloads/GRDC_Watersheds_shp.zip | 推荐，兼容性最好 |
| GRDC_Watersheds_geojson.zip | GeoJSON | ~110 MB | https://grdc.bafg.de/downloads/GRDC_Watersheds_geojson.zip | 适合 Web/可视化 |

**数据特征**:
- 覆盖约 10,000 个 GRDC 水文站
- 约 97% 的 GRDC 站点都有对应的流域多边形
- 每个多边形表示该站点上游的集水区边界
- 坐标系: WGS 84 (EPSG:4326)

**Shapefile 字段说明**:

| 字段名 | 类型 | 说明 |
|--------|------|------|
| GRDC_NO | Integer | GRDC 站点编号，**与站点元数据关联的关键字段** |
| area_calc | Float | 计算的流域面积 (km²) |
| geometry | Polygon | 流域边界多边形 |

### 3.2 其他流域数据

| 数据 | URL | 说明 |
|------|-----|------|
| 主要河流流域 (MRB) | https://grdc.bafg.de/downloads/GRDC_Major_River_Basins.zip | 520个全球主要流域 |
| WMO 流域分区 | https://grdc.bafg.de/downloads/GRDC_WMO_Basins.zip | WMO 标准流域划分 |

### 3.3 站点元数据（需从 Portal 获取）

站点元数据**没有直接下载链接**，需要通过 Data Portal 的 Web 界面筛选下载：

**Portal 入口**: https://portal.grdc.bafg.de/applications/public.html?publicuser=PublicUser

**操作步骤**:
1. 打开上述 URL（无需登录，使用 PublicUser）
2. 页面自动加载，进入 Dojo SPA 应用
3. 左侧菜单选择 "Data Download" → "Stations"
4. 使用筛选条件（流域、国家等）选择站点
5. 点击下载按钮，获取 CSV 格式的站点列表

**站点元数据 CSV 字段**:

| 字段 | 说明 |
|------|------|
| grdc_no | GRDC 站点编号（与流域 Shapefile 的 GRDC_NO 关联） |
| river | 河流名称 |
| station | 站点名称 |
| country | 国家代码 |
| lat | 纬度 |
| long | 经度 |
| area | 流域面积 (km²)，报告值 |
| altitude | 海拔 (m) |
| d_start | 数据起始日期 |
| d_end | 数据结束日期 |

---

## 4. 下载方法

### 4.1 直接下载（推荐）

URL 是静态的，可直接用任何 HTTP 客户端下载：

```bash
# Shapefile 格式
curl -L -o GRDC_Watersheds_shp.zip "https://grdc.bafg.de/downloads/GRDC_Watersheds_shp.zip"

# GeoJSON 格式
curl -L -o GRDC_Watersheds_geojson.zip "https://grdc.bafg.de/downloads/GRDC_Watersheds_geojson.zip"
```

**注意**: 需要使用 GET 请求（HEAD 请求会返回 400 错误）。

### 4.2 Python 脚本

项目中已提供 `download_grdc_watersheds.py`，功能包括：
- 交互式选择下载格式
- 下载进度显示
- 自动解压
- 代理支持

```powershell
conda activate common
python download_grdc_watersheds.py
```

### 4.3 代理配置

GRDC 服务器位于德国（BfG Koblenz），在国内访问可能需要代理：

```python
# Python
import os
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
```

```powershell
# PowerShell
$env:HTTP_PROXY="http://127.0.0.1:7890"
$env:HTTPS_PROXY="http://127.0.0.1:7890"
```

---

## 5. 数据处理示例

### 5.1 读取流域 Shapefile

```python
import geopandas as gpd

# 读取
gdf = gpd.read_file("GRDC_Watersheds/GRDC_Watersheds.shp")

# 基本信息
print(f"站点数量: {len(gdf)}")
print(f"字段: {list(gdf.columns)}")
print(f"CRS: {gdf.crs}")

# 查看前几行
print(gdf[['GRDC_NO', 'area_calc']].head())
```

### 5.2 关联站点元数据

```python
import pandas as pd
import geopandas as gpd

# 读取流域边界
watersheds = gpd.read_file("GRDC_Watersheds/GRDC_Watersheds.shp")

# 读取站点元数据（从 Portal 下载的 CSV）
stations = pd.read_csv("station_catalogue.csv", sep=";")

# 关联
merged = watersheds.merge(stations, left_on='GRDC_NO', right_on='grdc_no', how='left')

# 检查匹配率
print(f"匹配站点数: {merged['river'].notna().sum()} / {len(merged)}")
```

### 5.3 按区域筛选

```python
import geopandas as gpd
from shapely.geometry import box

gdf = gpd.read_file("GRDC_Watersheds/GRDC_Watersheds.shp")

# 筛选中国站点（大致范围）
china_bbox = box(73, 18, 136, 54)
china_stations = gdf[gdf.geometry.centroid.within(china_bbox)]
print(f"中国区域站点数: {len(china_stations)}")

# 保存
china_stations.to_file("GRDC_Watersheds_China.shp")
```

### 5.4 格式转换

```python
import geopandas as gpd

gdf = gpd.read_file("GRDC_Watersheds/GRDC_Watersheds.shp")

# 转 GeoJSON
gdf.to_file("GRDC_Watersheds.geojson", driver="GeoJSON")

# 转 GeoPackage
gdf.to_file("GRDC_Watersheds.gpkg", driver="GPKG")
```

---

## 6. 技术细节

### 6.1 Portal 技术栈

- **前端框架**: Dojo Toolkit (JavaScript SPA)
- **渲染方式**: 客户端渲染，直接抓取 HTML 无法获取数据
- **API**: Portal 使用内部 REST API，但未公开文档
- **认证**: 支持 PublicUser（无需注册即可下载站点元数据）

### 6.2 已验证的下载 URL

经过探测，以下 URL 返回 200 且内容有效：

| URL | HTTP 方法 | 状态 |
|-----|----------|------|
| https://grdc.bafg.de/downloads/GRDC_Watersheds_shp.zip | GET | 200 ✓ |
| https://grdc.bafg.de/downloads/GRDC_Watersheds_geojson.zip | GET | 200 ✓ |
| https://portal.grdc.bafg.de/applications/public.html?publicuser=PublicUser | GET | 200 ✓ |

### 6.3 失败的 URL 探测记录

以下 URL 均返回 404 或 400，**不可用**：

```
https://grdc.bafg.de/downloads/GRDC_Stations.zip
https://grdc.bafg.de/downloads/grdc_stations.kml
https://grdc.bafg.de/downloads/GRDC_Stations.geojson
https://portal.grdc.bafg.de/api/stations
https://portal.grdc.bafg.de/rest/stations
https://portal.grdc.bafg.de/kml/grdc_stations.kml
https://portal.grdc.bafg.de/geoserver/wfs?...
```

---

## 7. 引用规范

使用 GRDC 数据时，请引用：

```
GRDC (2023): Watershed Boundaries of GRDC Stations.
Global Runoff Data Centre. Koblenz, Germany:
Federal Institute of Hydrology (BfG).
```

参考文献:
- Lehner, B., Verdin, K., Jarvis, A. (2008): New global hydrography derived from spaceborne elevation data. Eos, Transactions, AGU, 89(10): 93-94.
- GRDC Report Series No. 41 (2012): Algorithm Theoretical Basis Document - Catchment boundaries of GRDC gauging stations.

---

## 8. AI 工具使用指南

### 8.1 给 AI 的上下文提示

当需要 AI 工具帮助处理 GRDC 数据时，可使用以下提示：

```
工作目录: D:\文档类\瑾雯\全球径流数据中心

GRDC 数据信息:
- 流域边界 Shapefile 已下载到工作目录
- 数据来源: https://grdc.bafg.de/downloads/GRDC_Watersheds_shp.zip
- 包含约 10,000 个水文站的流域多边形
- 关键字段: GRDC_NO (站点编号), area_calc (流域面积), geometry (多边形)
- 坐标系: EPSG:4326 (WGS 84)
- 使用 geopandas 读取: gpd.read_file("GRDC_Watersheds/GRDC_Watersheds.shp")

Python 环境: conda activate common
```

### 8.2 常见任务提示词

**筛选特定区域站点**:
```
帮我从 GRDC 流域数据中筛选出 [区域名称] 范围内的站点，
并导出为新的 Shapefile
```

**关联站点元数据**:
```
我有 GRDC 流域 Shapefile 和站点元数据 CSV，
帮我通过 GRDC_NO 字段将它们关联，
并统计匹配率
```

**可视化**:
```
帮我用 matplotlib 绘制 GRDC 流域边界地图，
按流域面积着色
```

---

## 9. 更新记录

| 日期 | 内容 |
|------|------|
| 2026-05-10 | 初始版本，整理 GRDC 流域边界数据获取方法 |
