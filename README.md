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

- **Semantic Scholar**
  - 使用 Semantic Scholar API 搜索学术论文
  - 按引用次数降序排序
  - 支持时间筛选
  - 每次返回最相关的 10 篇论文
  - 显示引用次数、作者信息和发表年份

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

#### Semantic Scholar 搜索
- **API 端点**: `http://api.semanticscholar.org/graph/v1/paper/search`
- **搜索参数**:
  - `query`: 搜索关键词
  - `limit`: 返回结果数量
  - `fields`: 返回字段（标题、作者、年份、摘要等）
  - `sort`: 按引用次数降序排序
- **返回数据**: 包含论文标题、作者、发表年份、摘要、引用次数等信息

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
bash
pip install flask feedparser requests python-dateutil pytz scholarly

2. 运行项目：
bash
python app.py

3. 访问项目：
bash
http://localhost:5001

## 界面说明

- **关键词输入**: 支持多个关键词组合搜索
- **时间范围**: 下拉选择不同的时间范围
- **数据来源**: 可以选择搜索 arXiv、Semantic Scholar 或 GitHub
- **更新按钮**: 点击后实时获取最新数据

## 搜索结果展示

1. **GitHub 项目**:
   - 项目名称和链接
   - 项目描述
   - Stars 数量
   - 创建时间
   - 最后更新时间

2. **学术论文**:
   - 论文标题和链接
   - 摘要内容
   - 发布时间
   - 来源标记
   - 作者信息
   - 引用次数（仅 Semantic Scholar）

## 注意事项

1. GitHub API 可能有访问限制
2. 建议合理使用关键词以获得更精确的搜索结果
3. 时间筛选对不同来源的处理方式略有不同
4. Semantic Scholar API 有每秒一次的请求限制

## 未来改进方向

1. 添加更多数据源
2. 优化搜索结果的排序算法
3. 添加更多的筛选条件