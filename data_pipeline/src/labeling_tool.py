"""
반자동 라벨링 도구
- 크롤링된 데이터에 감정 라벨 자동 부여
- 사람이 검수하고 수정할 수 있는 웹 인터페이스
- 능동학습(Active Learning)으로 효율적인 라벨링
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
import json
from pathlib import Path
import sqlite3
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import re
from loguru import logger

class EmotionLabeler:
    """감정 라벨링 클래스"""
    
    EMOTIONS = {
        0: "중립",
        1: "기쁨", 
        2: "슬픔",
        3: "분노",
        4: "두려움",
        5: "놀라움",
        6: "혐오"
    }
    
    EMOTION_KEYWORDS = {
        "기쁨": ["기쁘", "행복", "좋", "웃", "즐거", "신나", "만족", "성공", "사랑", "고마워", "최고", "대단"],
        "슬픔": ["슬프", "우울", "힘들", "아프", "괴로", "눈물", "울", "실망", "좌절", "외로", "그리워"],
        "분노": ["화", "짜증", "분노", "열받", "빡치", "싫", "미워", "증오", "억울", "불만", "욕"],
        "두려움": ["무서", "두려", "걱정", "불안", "긴장", "떨", "공포", "위험", "조심", "피하"],
        "놀라움": ["놀라", "깜짝", "의외", "갑자기", "예상외", "충격", "발견", "처음", "새로"],
        "혐오": ["더러", "역겨", "싫", "혐오", "구역", "토", "못참", "지겨", "답답"],
        "중립": ["그냥", "평범", "보통", "일반", "무난", "평소", "항상", "매일"]
    }
    
    def __init__(self):
        self.db_path = "data/labels.db"
        self.init_database()
    
    def init_database(self):
        """라벨링 결과 저장용 데이터베이스 초기화"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS labeled_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                source TEXT,
                auto_label INTEGER,
                auto_confidence REAL,
                human_label INTEGER,
                is_verified BOOLEAN DEFAULT FALSE,
                labeler_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def auto_label_batch(self, texts: List[str]) -> List[Tuple[int, float]]:
        """키워드 기반 자동 라벨링"""
        results = []
        
        for text in texts:
            emotion_scores = {}
            text_lower = text.lower()
            
            for emotion, keywords in self.EMOTION_KEYWORDS.items():
                score = 0
                for keyword in keywords:
                    score += text_lower.count(keyword)
                
                if emotion in self.EMOTIONS.values():
                    emotion_id = list(self.EMOTIONS.keys())[list(self.EMOTIONS.values()).index(emotion)]
                    emotion_scores[emotion_id] = score
            
            if not emotion_scores or max(emotion_scores.values()) == 0:
                # 모든 점수가 0이면 중립
                results.append((0, 0.5))
            else:
                # 가장 높은 점수의 감정
                best_emotion = max(emotion_scores, key=emotion_scores.get)
                max_score = emotion_scores[best_emotion]
                total_score = sum(emotion_scores.values())
                confidence = (max_score / total_score) if total_score > 0 else 0.5
                results.append((best_emotion, confidence))
        
        return results
    
    def save_labels(self, data: List[Dict]):
        """라벨링 결과 저장"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for item in data:
            cursor.execute('''
                INSERT INTO labeled_data 
                (text, source, auto_label, auto_confidence, human_label, is_verified, labeler_name)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                item['text'],
                item['source'],
                item['auto_label'],
                item['auto_confidence'],
                item.get('human_label'),
                item.get('is_verified', False),
                item.get('labeler_name', 'unknown')
            ))
        
        conn.commit()
        conn.close()
    
    def get_unlabeled_data(self, limit: int = 50) -> pd.DataFrame:
        """검수가 필요한 데이터 가져오기"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT * FROM labeled_data 
            WHERE is_verified = FALSE 
            ORDER BY auto_confidence ASC, created_at DESC
            LIMIT ?
        '''
        
        df = pd.read_sql_query(query, conn, params=[limit])
        conn.close()
        
        return df
    
    def update_human_label(self, data_id: int, human_label: int, labeler_name: str):
        """사람이 수정한 라벨 업데이트"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE labeled_data 
            SET human_label = ?, is_verified = TRUE, labeler_name = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (human_label, labeler_name, data_id))
        
        conn.commit()
        conn.close()

def create_labeling_interface():
    """Streamlit 라벨링 인터페이스"""
    st.set_page_config(page_title="감정 라벨링 도구", layout="wide")
    
    st.title("🏷️ 감정 라벨링 도구")
    st.write("크롤링된 텍스트에 감정 라벨을 부여하고 검수하는 도구입니다.")
    
    labeler = EmotionLabeler()
    
    # 사이드바 - 작업자 정보
    st.sidebar.header("작업자 정보")
    labeler_name = st.sidebar.text_input("작업자 이름", value="labeler1")
    
    # 메인 탭
    tab1, tab2, tab3, tab4 = st.tabs(["📝 라벨링", "📊 통계", "📁 데이터 관리", "🔄 배치 처리"])
    
    with tab1:
        st.header("감정 라벨링")
        
        # 검수할 데이터 로드
        if st.button("새 데이터 로드"):
            st.session_state.current_data = labeler.get_unlabeled_data(20)
        
        if 'current_data' not in st.session_state:
            st.session_state.current_data = labeler.get_unlabeled_data(20)
        
        if not st.session_state.current_data.empty:
            current_idx = st.session_state.get('current_idx', 0)
            
            if current_idx < len(st.session_state.current_data):
                row = st.session_state.current_data.iloc[current_idx]
                
                st.subheader(f"텍스트 {current_idx + 1}/{len(st.session_state.current_data)}")
                
                # 텍스트 표시
                st.text_area("텍스트 내용", value=row['text'], height=150, disabled=True)
                
                # 현재 자동 라벨
                auto_emotion = labeler.EMOTIONS.get(row['auto_label'], '알 수 없음')
                st.info(f"자동 라벨: {auto_emotion} (신뢰도: {row['auto_confidence']:.3f})")
                
                # 사람이 수정할 라벨 선택
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    human_label = st.selectbox(
                        "올바른 감정 라벨을 선택하세요:",
                        options=list(labeler.EMOTIONS.keys()),
                        format_func=lambda x: labeler.EMOTIONS[x],
                        index=row['auto_label']
                    )
                
                with col2:
                    if st.button("확인 ✅"):
                        labeler.update_human_label(row['id'], human_label, labeler_name)
                        st.session_state.current_idx = current_idx + 1
                        st.rerun()
                
                # 진행률
                progress = (current_idx + 1) / len(st.session_state.current_data)
                st.progress(progress)
                
                # 네비게이션
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("⬅️ 이전") and current_idx > 0:
                        st.session_state.current_idx = current_idx - 1
                        st.rerun()
                
                with col3:
                    if st.button("다음 ➡️") and current_idx < len(st.session_state.current_data) - 1:
                        st.session_state.current_idx = current_idx + 1
                        st.rerun()
        
        else:
            st.info("검수할 데이터가 없습니다.")
    
    with tab2:
        st.header("라벨링 통계")
        
        # 통계 쿼리
        conn = sqlite3.connect(labeler.db_path)
        
        # 전체 통계
        total_data = pd.read_sql_query("SELECT COUNT(*) as count FROM labeled_data", conn)
        verified_data = pd.read_sql_query("SELECT COUNT(*) as count FROM labeled_data WHERE is_verified = TRUE", conn)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("전체 데이터", total_data['count'].iloc[0])
        with col2:
            st.metric("검수 완료", verified_data['count'].iloc[0])
        with col3:
            progress_pct = (verified_data['count'].iloc[0] / total_data['count'].iloc[0] * 100) if total_data['count'].iloc[0] > 0 else 0
            st.metric("진행률", f"{progress_pct:.1f}%")
        
        # 감정별 분포
        emotion_dist = pd.read_sql_query('''
            SELECT human_label, COUNT(*) as count 
            FROM labeled_data 
            WHERE is_verified = TRUE 
            GROUP BY human_label
        ''', conn)
        
        if not emotion_dist.empty:
            emotion_dist['emotion_name'] = emotion_dist['human_label'].map(labeler.EMOTIONS)
            st.bar_chart(emotion_dist.set_index('emotion_name')['count'])
        
        conn.close()
    
    with tab3:
        st.header("데이터 관리")
        
        # 파일 업로드
        uploaded_file = st.file_uploader("CSV 파일 업로드", type=['csv'])
        
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write("업로드된 데이터 미리보기:")
            st.dataframe(df.head())
            
            if st.button("자동 라벨링 실행"):
                with st.spinner("자동 라벨링 중..."):
                    texts = df['text'].tolist()
                    labels = labeler.auto_label_batch(texts)
                    
                    # 데이터 준비
                    labeled_data = []
                    for i, (text, source) in enumerate(zip(df['text'], df.get('source', ['unknown'] * len(df)))):
                        label, confidence = labels[i]
                        labeled_data.append({
                            'text': text,
                            'source': source,
                            'auto_label': label,
                            'auto_confidence': confidence
                        })
                    
                    # 저장
                    labeler.save_labels(labeled_data)
                    st.success(f"{len(labeled_data)}개 데이터에 자동 라벨링 완료!")
        
        # 데이터 내보내기
        if st.button("검수 완료 데이터 다운로드"):
            conn = sqlite3.connect(labeler.db_path)
            verified_df = pd.read_sql_query('''
                SELECT text, source, human_label as label, labeler_name, updated_at
                FROM labeled_data 
                WHERE is_verified = TRUE
            ''', conn)
            conn.close()
            
            if not verified_df.empty:
                csv = verified_df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="CSV 다운로드",
                    data=csv,
                    file_name=f"labeled_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    
    with tab4:
        st.header("배치 처리")
        
        st.write("대량의 데이터를 일괄 처리합니다.")
        
        # 배치 자동 라벨링
        if st.button("모든 미라벨 데이터 자동 라벨링"):
            with st.spinner("배치 처리 중..."):
                conn = sqlite3.connect(labeler.db_path)
                unlabeled_df = pd.read_sql_query('''
                    SELECT * FROM labeled_data WHERE auto_label IS NULL
                ''', conn)
                conn.close()
                
                if not unlabeled_df.empty:
                    texts = unlabeled_df['text'].tolist()
                    labels = labeler.auto_label_batch(texts)
                    
                    # 업데이트
                    conn = sqlite3.connect(labeler.db_path)
                    cursor = conn.cursor()
                    
                    for i, (label, confidence) in enumerate(labels):
                        data_id = unlabeled_df.iloc[i]['id']
                        cursor.execute('''
                            UPDATE labeled_data 
                            SET auto_label = ?, auto_confidence = ?
                            WHERE id = ?
                        ''', (label, confidence, data_id))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success(f"{len(labels)}개 데이터 자동 라벨링 완료!")

if __name__ == "__main__":
    create_labeling_interface()