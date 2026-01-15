# Amazon Product Crawler API with AI 🧠✨

이 프로젝트는 **FastAPI**, **LangGraph**, **Playwright**, 그리고 **AWS Bedrock (Claude 3 Haiku)**을 활용하여 아마존(Amazon) 상품 정보를 지능적으로 수집하고 분석하는 강력한 API입니다.

단순한 크롤링을 넘어, **고화질 이미지 추출**, **이미지 3단 분류**, 그리고 **자연스러운 한국어 리라이팅(Rewriting)** 기능을 제공하여 즉시 상용 가능한 수준의 데이터를 반환합니다.

---

## 🌟 핵심 기능 (Key Features)

1.  **초정밀 이미지 추출 (Advanced Image Extraction)** 🖼️
    *   **고화질 원본 확보**: 아마존의 썸네일 리사이징 파라미터(`._AC_US100_` 등)를 자동 제거하여 원본 해상도 이미지를 확보합니다.
    *   **3단 자동 분류**: 이미지를 목적에 따라 정확히 분류하여 제공합니다.
        *   `images`: 메인 갤러리 이미지
        *   `brand_story_images`: 브랜드 스토리(Brand Story) 섹션 이미지
        *   `manufacturer_images`: 제조사 상세(From the manufacturer) 섹션 이미지
    *   **중복 제거**: 중복된 이미지를 자동으로 필터링하여 깔끔한 목록을 제공합니다.

2.  **자연스러운 한국어화 (Natural Korean Polish)** 🇰🇷
    *   **번역투 제거**: LLM이 기계 번역된 텍스트를 "사람이 쓴 듯한 자연스러운 한국어"로 재작성합니다.
    *   **요약 및 정제**: 긴 설명글을 핵심만 요약하여 가독성을 높입니다.

3.  **다중 URL 동시 처리 (Multi-URL Support)** ⚡
    *   **병렬 처리**: 여러 개의 아마존 URL을 동시에 입력받아 병렬적으로 크롤링을 수행합니다.
    *   **고속 실행**: `asyncio.gather`를 활용하여 다수의 상품 정보를 매우 빠른 속도로 한 번에 수집합니다.

4.  **초저비용 고효율 (Cost Effective)** 💰
    *   **Claude 3 Haiku** 모델을 최적화하여 사용.
    *   **1회 요청 당 약 7원 미만** ($0.005 USD)의 압도적인 가성비를 자랑합니다.
    *   불필요한 HTML 노이즈를 제거하여 토큰 비용을 최소화했습니다.

---

## 🚀 시작 가이드 (Quick Start)

이 프로젝트는 `uv` 패키지 매니저를 사용하여 의존성을 관리합니다.

### 1. 요구 사항 (Prerequisites)
- **Python 3.11+**
- **uv** (최신 Python 패키지 매니저)
- **AWS Credentials**: 로컬 환경에 AWS 자격 증명 설정 (`~/.aws/credentials`).
    *   `anthropic.claude-3-haiku-20240307-v1:0` 모델 접근 권한 필요.

### 2. 설치 및 실행
터미널에서 다음 명령어를 순서대로 실행하세요.

```bash
# 1. 의존성 설치 및 가상환경 생성
uv sync

# 2. Playwright 브라우저 설치 (최초 1회)
uv run playwright install chromium

# 3. 서버 실행
uv run run.py
```

서버가 실행되면 `http://127.0.0.1:8000` 에서 API가 대기합니다.

---

## 📡 API 사용법 (Usage)

### 상품 정보 상세 조회

**POST** `/api/v1/product/info`

**Request Example:**
```json
{
  "urls": [
    "https://www.amazon.com/dp/B00FLYWNYQ",
    "https://www.amazon.com/dp/B00GJ82VK4",
    "https://www.amazon.com/-/ko/dp/B00FLYWNYQ"
  ]
}
```

**Response Example (축약됨):**
```json
[
  {
    "title": "인스턴트팟 듀오 7-in-1 멀티쿠커",
    "price": "KRW 117,952",
    "features": [
      "압력솥, 슬로쿠커 등 7가지 기능을 하나로 담았습니다.",
      "버튼 하나로 완성되는 13가지 요리 프로그램 제공"
    ],
    "full_description": "인스턴트팟 듀오는 빠르고 편리한 조리를 돕는 스마트 멀티쿠커입니다...",
    
    "images": [
      "https://m.media-amazon.com/images/I/41OFXY6pMRL.jpg",
      "https://m.media-amazon.com/images/I/51uTO5fYDzL.jpg"
    ],
    "brand_story_images": [
      "https://m.media-amazon.com/images/I/71Vzpy79kIL.jpg"
    ],
    "manufacturer_images": [
      "https://m.media-amazon.com/images/S/aplus-media-library-service-media/6bed2cc4.jpg"
    ],
    
    "usage": {
      "prompt_tokens": 4200,
      "completion_tokens": 2500,
      "total_tokens": 6700
    }
  },
  {
    "title": "두 번째 상품 제목...",
    "price": "$25.99",
    ...
  }
]
```

---

## 🧠 아키텍처 (Architecture)

1.  **Fetch (Playwright)**: 브라우저를 띄워 동적 페이지를 렌더링하고 HTML을 확보합니다.
2.  **Parse (BeautifulSoup + Regex)**:
    *   HTML 파싱 및 스크립트(`hiRes` JSON) 분석.
    *   CSS 선택자(`id`, `class`)를 기반으로 이미지 영역(갤러리/브랜드/제조사)을 분리 추출.
    *   Regex로 이미지 URL을 고화질(High-Res)로 변환하고 중복 제거.
3.  **Extract & Rewrite (Bedrock Claude)**:
    *   정제된 텍스트와 이미지 목록을 LLM에 전달.
    *   데이터 구조화 및 "자연스러운 한국어"로 텍스트 리라이팅 수행.

## 🛠️ 기술 스택 (Tech Stack)
*   **Language**: Python 3.11+
*   **Web Framework**: FastAPI
*   **Orchestration**: LangGraph
*   **Browser Automation**: Playwright (Async)
*   **LLM**: AWS Bedrock (Claude 3 Haiku)
*   **Parsing**: BeautifulSoup4, Regex
*   **Package Manager**: uv
