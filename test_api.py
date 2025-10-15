"""
간단한 API 테스트 스크립트
"""
import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    print("🧪 FastAPI 서버 테스트 시작...\n")
    
    # 1. Health Check
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"✅ Health Check: {response.status_code}")
        print(f"   Response: {response.json()}\n")
    except Exception as e:
        print(f"❌ Health Check 실패: {e}\n")
        return
    
    # 2. Root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Root endpoint: {response.status_code}")
        print(f"   Response: {response.json()}\n")
    except Exception as e:
        print(f"❌ Root endpoint 실패: {e}\n")
    
    # 3. 감정 분석 테스트 (인증 불필요)
    try:
        test_text = "오늘 정말 기뻤어요! 좋은 일이 많이 생겼네요."
        data = {"text": test_text}
        response = requests.post(f"{base_url}/api/emotions/test", json=data)
        print(f"✅ 감정 분석 테스트: {response.status_code}")
        print(f"   Input: {test_text}")
        print(f"   Response: {response.json()}\n")
    except Exception as e:
        print(f"❌ 감정 분석 테스트 실패: {e}\n")
    
    # 4. OpenAPI 문서 확인
    try:
        response = requests.get(f"{base_url}/api/docs")
        print(f"✅ OpenAPI Docs: {response.status_code}")
        print(f"   문서는 http://localhost:8000/api/docs 에서 확인 가능\n")
    except Exception as e:
        print(f"❌ OpenAPI Docs 실패: {e}\n")

if __name__ == "__main__":
    test_api()