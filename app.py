import streamlit as st
import random
import json
import os

# 1. 網頁頁面基本設定
st.set_page_config(page_title="AI 知識對答小考箱 Pro+", page_icon="🎒", layout="centered")

# --- 【核心開發者：賴以航 原生穩定版區塊】 ---
with st.container(border=True):
    st.subheader("👨‍💻 核心開發者：賴以航 (Yi-Hang Lai)")
    st.caption("🤖 雲端全端自動化專案 v3.0 | 核心技術：JSON 外掛大題庫 & 動態抽取演算法")

st.title("🎒 AI 知識對答小考箱 Pro+ 100題超級版")
st.write("本系統已對接外部 JSON 題庫軍火庫，支援無限題目擴充，每次開考隨機抽選！")
st.write("---")

# 2. 自動讀取外部 JSON 題庫
@st.cache_data # 讓網頁記住題庫，讀取速度快 10 倍
def load_quiz_database():
    filename = "questions.json"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # 防錯機制：如果檔案不存在，提供基礎緊急題目
        return {"錯誤": [{"question": "找不到 questions.json 檔案！", "options": ["A", "B"], "answer": "A", "hint": "請檢查 GitHub"}]}

DB_QUIZ = load_quiz_database()

# 3. 使用 Session State 初始化狀態機
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "current_questions" not in st.session_state:
    st.session_state.current_questions = []
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# 4. 主介面：選擇考科
if not st.session_state.quiz_started:
    category = st.selectbox("🎯 請選擇您想挑戰的知識領域：", list(DB_QUIZ.keys()))
    
    # 動態顯示該科目目前總共有幾題
    total_q_in_db = len(DB_QUIZ[category])
    st.write(f"📊 目前該題庫實時連線題目總數： **{total_q_in_db}** 題")
    
    start_btn = st.button("🚀 開始隨機抽取 3 題挑戰！", use_container_width=True)
    
    if start_btn:
        st.session_state.quiz_started = True
        all_questions = DB_QUIZ[category]
        
        # 智慧防錯：如果題庫小於 3 題就全抽，大於 3 題就隨機抽 3 題
        sample_size = min(len(all_questions), 3)
        st.session_state.current_questions = random.sample(all_questions, sample_size)
        
        st.session_state.user_answers = {}
        st.session_state.submitted = False
        st.rerun()

# 5. 測驗進行中介面
else:
    st.info("📝 題目已從大題庫中隨機生成！完成後點擊最下方的「提交答案」按鈕。")
    
    for idx, q in enumerate(st.session_state.current_questions):
        st.markdown(f"### **Q{idx+1}. {q['question']}**")
        
        box_key = f"q_{idx}"
        user_choice = st.radio(
            "請選擇答案：", 
            q["options"], 
            key=box_key, 
            disabled=st.session_state.submitted
        )
        st.session_state.user_answers[idx] = user_choice
        st.write("") 
    
    st.write("---")
    
    if not st.session_state.submitted:
        submit_btn = st.button("🔔 檢查答案並計算分數", use_container_width=True)
        if submit_btn:
            st.session_state.submitted = True
            st.rerun()
            
    # 6. 顯示結果與解析
    else:
        st.success("🎉 測驗完成！正在為您核對標準答案：")
        
        score = 0
        total = len(st.session_state.current_questions)
        
        for idx, q in enumerate(st.session_state.current_questions):
            u_ans = st.session_state.user_answers.get(idx)
            st.markdown(f"#### **題目 {idx+1} 解析：**")
            st.write(f"❓ **問題**：{q['question']}")
            
            if u_ans == q["answer"]:
                st.write(f"🟢 **您的答案**：`{u_ans}` (正確！)")
                score += 1
            else:
                st.write(f"🔴 **您的答案**：`{u_ans}` (錯誤❌)")
                st.write(f"💡 **正確答案**：`{q['answer']}`")
                
            st.info(f"🔍 **知識小解析**：{q['hint']}")
            st.write("---")
            
        final_score = round((score / total) * 100)
        
        st.markdown(f"## 🏆 最終得分：`{final_score} / 100` 分")
        if final_score == 100:
            st.balloons() 
            st.success("🤖 報告 **賴以航** 總工程師！玩家獲得大題庫盲刷滿分成就！👑")
        elif final_score >= 60:
            st.warning("👌 表現不錯喔！已經及格了，再接再厲就能挑戰滿分！")
        else:
            st.error("😢 哎呀，差一點點就及格了！別氣餒，看過解析後再挑戰一次吧！")
            
        retry_btn = st.button("🔄 重新選擇考科（重新洗牌抽題）", use_container_width=True)
        if retry_btn:
            st.session_state.quiz_started = False
            st.session_state.submitted = False
            st.rerun()

st.write("\n---")
st.caption("⚡ Powered by Streamlit & Python Chat Bot")
st.caption("© 2026 賴以航 (Yi-Hang Lai). All rights reserved. 專案產權所有，翻印必究。")
