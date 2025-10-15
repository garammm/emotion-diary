"""
감정 분석을 위한 데이터 수집 크롤러
- 소셜 미디어 텍스트 (Twitter, Instagram 등)
- 온라인 커뮤니티 글 (네이버 카페, 디시인사이드 등)
- 뉴스 댓글
- 블로그 포스트
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from loguru import logger
import re
from dataclasses import dataclass

@dataclass
class CrawlResult:
    text: str
    source: str
    url: str
    timestamp: datetime
    metadata: Dict

class BaseCrawler:
    def __init__(self, delay_range=(1, 3)):
        self.delay_range = delay_range
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def random_delay(self):
        """랜덤 지연으로 차단 방지"""
        delay = random.uniform(*self.delay_range)
        time.sleep(delay)
    
    def clean_text(self, text: str) -> str:
        """텍스트 정제"""
        if not text:
            return ""
        
        # HTML 태그 제거
        text = re.sub(r'<[^>]+>', '', text)
        # 특수문자 정규화
        text = re.sub(r'\s+', ' ', text)
        # 이모지 제거 (선택적)
        text = re.sub(r'[^\w\s가-힣ㄱ-ㅎㅏ-ㅣ]', ' ', text)
        
        return text.strip()

class NaverCafeCrawler(BaseCrawler):
    """네이버 카페 글 크롤링"""
    
    def crawl_cafe_posts(self, cafe_id: str, board_id: str, max_pages: int = 10) -> List[CrawlResult]:
        results = []
        
        for page in range(1, max_pages + 1):
            try:
                url = f"https://cafe.naver.com/ArticleList.nhn?search.clubid={cafe_id}&search.boardtype=L&search.menuid={board_id}&search.page={page}"
                
                response = self.session.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                articles = soup.find_all('tr', class_='board-list')
                
                for article in articles:
                    title_elem = article.find('a', class_='article')
                    if title_elem:
                        article_url = "https://cafe.naver.com" + title_elem.get('href')
                        title = title_elem.text.strip()
                        
                        # 개별 글 내용 가져오기
                        content = self._get_article_content(article_url)
                        
                        if content:
                            results.append(CrawlResult(
                                text=f"{title} {content}",
                                source="naver_cafe",
                                url=article_url,
                                timestamp=datetime.now(),
                                metadata={"cafe_id": cafe_id, "board_id": board_id}
                            ))
                
                self.random_delay()
                logger.info(f"네이버 카페 {page}페이지 크롤링 완료")
                
            except Exception as e:
                logger.error(f"네이버 카페 크롤링 오류: {e}")
                continue
        
        return results
    
    def _get_article_content(self, url: str) -> str:
        try:
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            content_elem = soup.find('div', class_='se-main-container')
            if content_elem:
                return self.clean_text(content_elem.get_text())
            
            return ""
        except:
            return ""

class DCInsideCrawler(BaseCrawler):
    """디시인사이드 갤러리 크롤링"""
    
    def crawl_gallery(self, gallery_id: str, max_pages: int = 10) -> List[CrawlResult]:
        results = []
        
        for page in range(1, max_pages + 1):
            try:
                url = f"https://gall.dcinside.com/board/lists/?id={gallery_id}&page={page}"
                
                response = self.session.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                posts = soup.find_all('tr', class_='ub-content')
                
                for post in posts:
                    title_elem = post.find('a')
                    if title_elem:
                        post_url = "https://gall.dcinside.com" + title_elem.get('href')
                        title = title_elem.text.strip()
                        
                        content = self._get_post_content(post_url)
                        
                        if content:
                            results.append(CrawlResult(
                                text=f"{title} {content}",
                                source="dcinside",
                                url=post_url,
                                timestamp=datetime.now(),
                                metadata={"gallery_id": gallery_id}
                            ))
                
                self.random_delay()
                logger.info(f"디시인사이드 {gallery_id} {page}페이지 크롤링 완료")
                
            except Exception as e:
                logger.error(f"디시인사이드 크롤링 오류: {e}")
                continue
        
        return results
    
    def _get_post_content(self, url: str) -> str:
        try:
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            content_elem = soup.find('div', class_='writing_view_box')
            if content_elem:
                return self.clean_text(content_elem.get_text())
            
            return ""
        except:
            return ""

class NewsCrawler(BaseCrawler):
    """뉴스 기사 및 댓글 크롤링"""
    
    def crawl_news_comments(self, news_urls: List[str]) -> List[CrawlResult]:
        results = []
        
        for url in news_urls:
            try:
                # 네이버 뉴스 댓글 API 호출 (실제로는 더 복잡함)
                comments = self._get_news_comments(url)
                
                for comment in comments:
                    results.append(CrawlResult(
                        text=comment['content'],
                        source="news_comment",
                        url=url,
                        timestamp=datetime.now(),
                        metadata={"news_url": url}
                    ))
                
                self.random_delay()
                logger.info(f"뉴스 댓글 크롤링 완료: {url}")
                
            except Exception as e:
                logger.error(f"뉴스 댓글 크롤링 오류: {e}")
                continue
        
        return results
    
    def _get_news_comments(self, url: str) -> List[Dict]:
        # 실제 구현에서는 네이버 뉴스 API나 Selenium을 사용
        return []

class BlogCrawler(BaseCrawler):
    """블로그 포스트 크롤링"""
    
    def crawl_blog_posts(self, keywords: List[str], max_posts: int = 100) -> List[CrawlResult]:
        results = []
        
        for keyword in keywords:
            try:
                # 네이버 블로그 검색 결과 크롤링
                search_url = f"https://search.naver.com/search.naver?where=post&query={keyword}"
                
                response = self.session.get(search_url)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                blog_links = soup.find_all('a', class_='api_txt_lines')[:max_posts//len(keywords)]
                
                for link in blog_links:
                    blog_url = link.get('href')
                    title = link.text.strip()
                    
                    content = self._get_blog_content(blog_url)
                    
                    if content and len(content) > 50:  # 충분한 길이의 내용만
                        results.append(CrawlResult(
                            text=f"{title} {content}",
                            source="blog",
                            url=blog_url,
                            timestamp=datetime.now(),
                            metadata={"keyword": keyword}
                        ))
                
                self.random_delay()
                logger.info(f"블로그 크롤링 완료: {keyword}")
                
            except Exception as e:
                logger.error(f"블로그 크롤링 오류: {e}")
                continue
        
        return results
    
    def _get_blog_content(self, url: str) -> str:
        try:
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 블로그 플랫폼별로 다른 선택자 사용
            content_selectors = [
                'div.se-main-container',  # 네이버 블로그
                'div.entry-content',      # 티스토리
                'div.post-content',       # 일반적인 블로그
                'div.content',
                'article'
            ]
            
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    return self.clean_text(content_elem.get_text())
            
            return ""
        except:
            return ""

class DataCollector:
    """데이터 수집 관리자"""
    
    def __init__(self, output_dir: str = "data/raw"):
        self.output_dir = output_dir
        self.crawlers = {
            'naver_cafe': NaverCafeCrawler(),
            'dcinside': DCInsideCrawler(),
            'news': NewsCrawler(),
            'blog': BlogCrawler()
        }
    
    def collect_all(self, config: Dict) -> pd.DataFrame:
        """모든 소스에서 데이터 수집"""
        all_results = []
        
        # 네이버 카페
        if 'naver_cafe' in config:
            for cafe_config in config['naver_cafe']:
                results = self.crawlers['naver_cafe'].crawl_cafe_posts(
                    cafe_config['cafe_id'],
                    cafe_config['board_id'],
                    cafe_config.get('max_pages', 10)
                )
                all_results.extend(results)
        
        # 디시인사이드
        if 'dcinside' in config:
            for gallery_id in config['dcinside']['galleries']:
                results = self.crawlers['dcinside'].crawl_gallery(
                    gallery_id,
                    config['dcinside'].get('max_pages', 10)
                )
                all_results.extend(results)
        
        # 블로그
        if 'blog' in config:
            results = self.crawlers['blog'].crawl_blog_posts(
                config['blog']['keywords'],
                config['blog'].get('max_posts', 100)
            )
            all_results.extend(results)
        
        # DataFrame으로 변환
        df = pd.DataFrame([
            {
                'text': result.text,
                'source': result.source,
                'url': result.url,
                'timestamp': result.timestamp,
                'metadata': json.dumps(result.metadata, ensure_ascii=False)
            }
            for result in all_results
        ])
        
        # 중복 제거
        df = df.drop_duplicates(subset=['text'])
        
        # 저장
        output_file = f"{self.output_dir}/crawled_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        logger.info(f"총 {len(df)}개 데이터 수집 완료: {output_file}")
        
        return df

if __name__ == "__main__":
    # 사용 예시
    config = {
        "naver_cafe": [
            {"cafe_id": "29842958", "board_id": "1", "max_pages": 5}  # 예시 카페
        ],
        "dcinside": {
            "galleries": ["humor", "hit"],
            "max_pages": 5
        },
        "blog": {
            "keywords": ["우울", "기쁨", "화남", "슬픔", "행복", "스트레스"],
            "max_posts": 50
        }
    }
    
    collector = DataCollector()
    df = collector.collect_all(config)