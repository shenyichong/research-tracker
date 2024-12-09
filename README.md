# Research Tracker (研究热点追踪)

一个简单而强大的研究热点追踪工具，可以同时搜索学术论文和开源项目。

## 功能特点

### 1. 多源数据搜索
- **arXiv 论文**
  - 使用 arXiv API 进行全文搜索
  - 搜索范围包括标题、摘要等所有字段
  - 结果按相关性排序（relevance）
  - 每次返回最相关的 10 篇论文

- **GitHub 项目**
  - 使用 GitHub REST API 搜索仓库
  - 按照 stars 数量降序排序
  - 每次返回最受欢迎的 10 个项目

### 2. 时间筛选
支持多个时间范围的筛选：
- 一周内
- 一个月内
- 半年内
- 一年内
- 所有时间

### 3. 搜索实现细节

#### arXiv 搜索
- **API 端点**: `http://export.arxiv.org/api/query`
- **搜索语法**: 
  - 使用 `all:` 前缀进行全文搜索
  - 多个关键词使用 `AND` 连接
  - 示例: `all:PLM+AND+all:Interpretability`
- **排序方式**: 
  - 使用 `sortBy=relevance` 按相关性排序
  - `sortOrder=descending` 降序排列

#### GitHub 搜索
- **API 端点**: `https://api.github.com/search/repositories`
- **搜索参数**:
  - `q`: 搜索关键词
  - `sort=stars`: 按 star 数量排序
  - `order=desc`: 降序排列
- **时间过滤**: 基于仓库的创建时间（created_at）

## 技术栈

### 后端
- Flask: Web 框架
- feedparser: 解析 arXiv RSS feed
- requests: HTTP 请求
- python-dateutil: 日期处理
- pytz: 时区处理

### 前端
- 原生 JavaScript
- HTML5
- CSS3

## 使用方法

1. 安装依赖： 