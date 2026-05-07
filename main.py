import 
name = st.text_input("이름이 뭐야?")
choice = st.selectbox("오늘 기분은?", ["좋음", "보통", "피곤"])
score = st.slider("나의 에너지 점수", 0, 100)