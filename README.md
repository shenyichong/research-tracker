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
bash
pip install flask feedparser requests python-dateutil pytz

2. 运行项目：
bash
python app.py

3. 访问项目：
bash
http://localhost:5001

## 界面说明

- **关键词输入**: 支持多个关键词组合搜索
- **时间范围**: 下拉选择不同的时间范围
- **数据来源**: 可以选择搜索 arXiv、GitHub 或两者都搜索
- **更新按钮**: 点击后实时获取最新数据

## 搜索结果展示

1. **GitHub 项目**:
   - 项目名称和链接
   - 项目描述
   - Stars 数量
   - 创建时间
   - 最后更新时间

2. **arXiv 论文**:
   - 论文标题和链接
   - 摘要内容
   - 发布时间
   - 来源标记

## 注意事项

1. GitHub API 可能有访问限制
2. 建议合理使用关键词以获得更精确的搜索结果
3. 时间筛选对不同来源的处理方式略有不同

## 未来改进方向

1. 添加更多数据源
2. 实现高级搜索功能
3. 添加结果导出功能
4. 支持用户收藏
5. 添加搜索历史记录