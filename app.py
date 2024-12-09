from flask import Flask, render_template, jsonify
import feedparser
import requests
from datetime import datetime, timedelta
import json
import urllib.parse
import re
from dateutil import parser as date_parser
import pytz
import logging
import time

app = Flask(__name__)
app.logger.setLevel(logging.CRITICAL)  # 只显示严重错误

class DataFetcher:
    def _get_published_date(self, entry):
        """统一获取发布日期的方法"""
        # 尝试常见日期字段
        for date_field in ['published', 'updated', 'pubDate', 'date']:
            if hasattr(entry, date_field):
                try:
                    date_str = getattr(entry, date_field)
                    return date_parser.parse(date_str)
                except Exception as e:
                    app.logger.error(f"Error parsing {date_field}: {str(e)}")
                    continue

        # 如果所有方法都失败，返回 None
        app.logger.warning(f"No valid date found for entry: {entry.get('title', 'Unknown title')}")
        return None

    def _filter_by_date(self, papers, time_filter):
        """按时间筛选论文"""
        if time_filter == 'all':
            return papers
        
        now = datetime.now()
        filter_dates = {
            'week': now - timedelta(days=7),
            'month': now - timedelta(days=30),
            'half_year': now - timedelta(days=183),
            'year': now - timedelta(days=365),
        }
        
        cutoff_date = filter_dates.get(time_filter)
        if not cutoff_date:
            return papers
        
        return [paper for paper in papers 
                if paper['published'] != '发布时间未知' 
                and date_parser.parse(paper['published']) > cutoff_date]

    def fetch_arxiv(self, keyword):
        """获取 arXiv 最新论文"""
        # 使用 all: 进行全文搜索，支持多个词的组合搜索
        # 将关键词用 AND 连接，确保所有词都出现
        keywords = keyword.strip().split()
        search_terms = [f'all:{kw}' for kw in keywords]
        search_query = '+AND+'.join(search_terms)
        
        base_url = (
            f'http://export.arxiv.org/api/query?'
            f'search_query={search_query}'  # 不需要额外的 URL 编码，因为关键词已经正确格式化
            f'&start=0'
            f'&max_results=10'
            f'&sortBy=relevance'
            f'&sortOrder=descending'
        )
        
        response = feedparser.parse(base_url)
        return [{
            'title': entry.title,
            'link': entry.link,
            'published': self._get_published_date(entry).strftime('%Y-%m-%d %H:%M:%S') if self._get_published_date(entry) else '发布时间未知',
            'summary': entry.summary,
            'source': 'arXiv'
        } for entry in response.entries]

    def fetch_github(self, keyword, time_filter):
        """获取 GitHub 相关项目"""
        url = f'https://api.github.com/search/repositories?q={keyword}&sort=stars&order=desc'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                repos = response.json()['items']
                
                # 处理时间过滤
                now = datetime.now(pytz.UTC)
                filter_dates = {
                    'week': now - timedelta(days=7),
                    'month': now - timedelta(days=30),
                    'half_year': now - timedelta(days=183),
                    'year': now - timedelta(days=365),
                }
                
                cutoff_date = filter_dates.get(time_filter)
                
                filtered_repos = []
                for repo in repos:
                    created_date = date_parser.parse(repo['created_at'])
                    if time_filter == 'all' or (cutoff_date and created_date > cutoff_date):
                        filtered_repos.append({
                            'name': repo['name'],
                            'description': repo['description'],
                            'url': repo['html_url'],
                            'stars': repo['stargazers_count'],
                            'updated_at': date_parser.parse(repo['updated_at']).strftime('%Y-%m-%d %H:%M:%S'),
                            'created_at': created_date.strftime('%Y-%m-%d %H:%M:%S')
                        })
                
                return filtered_repos[:10]  # 返回前10个结果
        except Exception as e:
            app.logger.error(f"Error fetching GitHub data: {str(e)}")
        return []

def fetch_from_semantic_scholar(query):
    try:
        base_url = "http://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": query,
            "limit": 10,
            "fields": "title,authors,year,abstract,url,venue,citationCount",
            "sort": "citationCount:desc"
        }
        
        headers = {
            'Accept': 'application/json'
        }
        
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        
        if response.status_code != 200:
            app.logger.error(f"Semantic Scholar API error: {response.status_code}")
            app.logger.error(f"Response content: {response.text}")
            return []
            
        data = response.json()
        papers = []
        
        if 'data' not in data:
            app.logger.error(f"Unexpected API response: {data}")
            return []
            
        for paper in data['data']:
            try:
                # 确保所有必需的字段都存在
                paper_data = {
                    'title': paper.get('title', 'Untitled'),
                    'link': paper.get('url', ''),  # 使用 url 作为 link
                    'published': str(paper.get('year', '')),  # 年份作为发布时间
                    'summary': paper.get('abstract', 'No abstract available'),  # 使用 abstract 作为 summary
                    'source': 'Semantic Scholar',
                    'citations': paper.get('citationCount', 0),
                    'authors': ', '.join([author.get('name', '') for author in paper.get('authors', [])])
                }
                
                papers.append(paper_data)
            except Exception as e:
                app.logger.error(f"Error processing paper: {e}")
                continue
                
        return papers
        
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Request failed: {e}")
        return []
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return []

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        app.logger.error(f"Error rendering index: {str(e)}")
        return str(e), 500

@app.route('/update/<keyword>/<time_filter>/<sources>')
def update(keyword, time_filter, sources):
    try:
        decoded_keyword = urllib.parse.unquote(keyword)
        fetcher = DataFetcher()
        selected_sources = sources.split(',')
        
        all_papers = []
        github_results = []
        
        if 'semantic_scholar' in selected_sources:
            scholar_papers = fetch_from_semantic_scholar(decoded_keyword)
            all_papers.extend(scholar_papers)
            
        if 'arxiv' in selected_sources:
            arxiv_papers = fetcher.fetch_arxiv(decoded_keyword)
            all_papers.extend(arxiv_papers)
            
        if 'github' in selected_sources:
            github_results = fetcher.fetch_github(decoded_keyword, time_filter)
        
        # 按时间筛选
        filtered_papers = fetcher._filter_by_date(all_papers, time_filter)
        filtered_papers.sort(key=lambda x: x.get('citations', 0), reverse=True)
        
        results = {
            'papers': filtered_papers,
            'github': github_results
        }
        
        return jsonify(results)
    except Exception as e:
        app.logger.error(f"Error in update: {str(e)}")
        return jsonify({'error': str(e), 'papers': [], 'github': []}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 