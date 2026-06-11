import streamlit as st
import json
from datetime import datetime
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="오늘의 운동 기록",
    page_icon="🏃",
    layout="centered"
)

# CSS 스타일링
st.markdown("""
    <style>
        .title-main {
            text-align: center;
            color: #1f77b4;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            color: #666666;
            font-size: 14px;
            margin-bottom: 30px;
        }
        .result-box {
            background-color: #f0f5ff;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #1f77b4;
            margin-top: 20px;
        }
        .message-positive {
            color: #2ecc71;
            font-weight: bold;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

# 제목 섹션
st.markdown('<h1 class="title-main">🏃 오늘의 운동 기록</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">매일 운동을 쉽게 기록하고 확인해보세요</p>', unsafe_allow_html=True)

# 데이터 저장 경로
data_dir = Path("exercise_data")
data_dir.mkdir(exist_ok=True)
today_file = data_dir / f"{datetime.now().strftime('%Y-%m-%d')}.json"

# 세션 상태 초기화
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# 존재하는 데이터 로드
def load_today_data():
    if today_file.exists():
        with open(today_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

# 데이터 저장
def save_exercise_data(data):
    with open(today_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 칼로리 계산 함수
def calculate_calories(exercise_type, duration, intensity):
    """운동 종류, 시간, 강도에 따른 예상 칼로리 계산"""
    base_calories = {
        "걷기": 4,      # 분당 칼로리
        "달리기": 10,
        "사이클": 8,
        "수영": 11,
        "스트레칭": 3
    }
    
    base = base_calories.get(exercise_type, 5)
    # 강도에 따른 배수 (약함: 0.8, 보통: 1.0, 강함: 1.3)
    intensity_multiplier = {"약함": 0.8, "보통": 1.0, "강함": 1.3}.get(intensity, 1.0)
    
    return int(duration * base * intensity_multiplier)

# 입력 섹션
st.markdown("### 📝 운동 정보 입력")

with st.form("exercise_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        exercise_name = st.text_input("운동 종류", placeholder="예: 걷기, 달리기, 사이클")
    
    with col2:
        exercise_duration = st.number_input("운동 시간 (분)", min_value=0, max_value=480, value=30, step=5)
    
    col3, col4 = st.columns(2)
    
    with col3:
        steps = st.number_input("걸음 수", min_value=0, max_value=100000, value=0, step=100)
    
    with col4:
        distance = st.number_input("거리 (km)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    
    intensity = st.radio("운동 강도", ["약함", "보통", "강함"], horizontal=True)
    
    exercise_type = st.selectbox(
        "운동 유형",
        ["걷기", "달리기", "사이클", "수영", "스트레칭"]
    )
    
    col_button1, col_button2, col_button3 = st.columns(3)
    
    with col_button1:
        submit_button = st.form_submit_button("💾 기록 저장", use_container_width=True)
    
    with col_button2:
        reset_button = st.form_submit_button("🔄 초기화", use_container_width=True)
    
    with col_button3:
        view_result_button = st.form_submit_button("📊 결과 보기", use_container_width=True)

# 폼 제출 처리
if submit_button and (exercise_name or exercise_duration > 0):
    calories = calculate_calories(exercise_type, exercise_duration, intensity)
    
    exercise_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "exercise_name": exercise_name,
        "duration": exercise_duration,
        "steps": steps,
        "distance": distance,
        "intensity": intensity,
        "exercise_type": exercise_type,
        "calories": calories
    }
    
    save_exercise_data(exercise_data)
    st.session_state.form_submitted = True
    st.success("✅ 운동 기록이 저장되었습니다!")

if reset_button:
    if today_file.exists():
        today_file.unlink()
    st.session_state.form_submitted = False
    st.info("🔄 오늘의 기록이 초기화되었습니다.")

# 결과 섹션
if view_result_button or st.session_state.form_submitted:
    today_data = load_today_data()
    
    if today_data:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown("## 📊 오늘의 운동 요약")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("운동 종류", today_data.get("exercise_type", "N/A"))
        
        with col2:
            st.metric("운동 시간", f"{today_data.get('duration', 0)}분")
        
        with col3:
            st.metric("예상 칼로리", f"{today_data.get('calories', 0)}kcal")
        
        with col4:
            st.metric("걸음 수", f"{today_data.get('steps', 0):,}")
        
        if today_data.get('distance', 0) > 0:
            st.metric("거리", f"{today_data.get('distance', 0):.1f}km")
        
        st.markdown("---")
        
        # 동기 부여 메시지
        calories = today_data.get('calories', 0)
        duration = today_data.get('duration', 0)
        
        messages = []
        if duration >= 60:
            messages.append("🌟 오늘 1시간 이상 운동했어요! 정말 멋져요!")
        elif duration >= 30:
            messages.append("👍 30분 운동 완료! 꾸준히 가고 있어요!")
        else:
            messages.append("💪 오늘도 운동했어요! 멋진 첫 발입니다!")
        
        if calories >= 500:
            messages.append("🔥 500kcal 이상 소모했어요! 우와!")
        
        for msg in messages:
            st.markdown(f'<p class="message-positive">{msg}</p>', unsafe_allow_html=True)
        
        st.markdown(f"✨ **내일도 함께해요! 당신은 할 수 있어요!** ✨")
        
        st.markdown("---")
        st.markdown(f"**기록 시간**: {today_data.get('timestamp', 'N/A')}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("📌 오늘의 운동 기록이 없습니다. 위의 입력창에서 운동을 기록해주세요!")