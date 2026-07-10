import streamlit as st
import random

# 1. 網頁頁面基本設定
st.set_page_config(page_title="AI 知識對答小考箱", page_icon="🎒", layout="centered")

# --- 【核心開發者：賴以航 原生穩定版區塊】 ---
with st.container(border=True):
    st.subheader("👨‍💻 核心開發者：賴以航 (Yi-Hang Lai)")
    st.caption("🤖 雲端全端自動化專案 | 核心技術：Streamlit 狀態機控制 & 動態計分系統")

st.title("🎒 AI 歷史/科學知識對答小考箱")
st.write("歡迎來到智慧挑戰賽！請選擇考科，系統將為您準備 3 題隨機大考驗，完成後會自動評分並給出專業解析喔！")
st.write("---")

# 2. 內建核心題庫（歷史與科學領域）
DB_QUIZ = {
    "歷史領域 📜": [
        {
            "question": "請問歷史上著名的「三國時代」，魏、蜀、吳三國中，最後是由誰篡魏並統一全國建立晉朝？",
            "options": ["曹操", "劉備", "司馬炎", "孫權"],
            "answer": "司馬炎",
            "hint": "他是司馬懿的孫子，逼迫魏元帝曹奐禪讓，改國號為晉。"
        },
        {
            "question": "西元 1912 年，亞洲第一個民主共和國「中華民國」正式成立，請問首任臨時大總統是誰？",
            "options": ["袁世凱", "孫中山", "蔣中正", "黎元洪"],
            "answer": "孫中山",
            "hint": "他被尊稱為國父，領導了多次革命運動。"
        },
        {
            "question": "歐洲中世紀爆發了俗稱「黑死病」的恐怖大瘟疫，奪走數千萬條人命，請問這是一種什麼疾病？",
            "options": ["天花", "鼠疫", "霍亂", "流感"],
            "answer": "鼠疫",
            "hint": "這種疾病主要透過跳蚤叮咬囓齒動物（如老鼠）再傳染給人類。"
        }
    ],
    "科學領域 🧪": [
        {
            "question": "在元素週期表中，原子序為 1、全宇宙含量最多、最輕的化學元素是什麼？",
            "options": ["氦 (He)", "氧 (O)", "氫 (H)", "碳 (C)"],
            "answer": "氫 (H)",
            "hint": "太陽內部最主要的核融合燃料就是這個元素。"
        },
        {
            "question": "當光線從空氣進入水中時，傳播方向會發生偏折，這種物理現象稱稱為什麽？",
            "options": ["反射", "折射", "繞射", "漫反射"],
            "answer": "折射",
            "hint": "這是因為光在不同介質中的「傳播速度不同」所導致的現象。"
        },
        {
            "question": "人體內最大的解毒器官，同時也是唯一具有強大自我再生能力的內臟器官是哪一個？",
            "options": ["胃", "心臟", "腎臟", "肝臟"],
            "answer": "肝臟",
            "hint": "保持規律作息與充足睡眠，就是保護它的最佳方式。"
        }
    ]
}

# 3. 使用 Session State 初始化狀態機，避免刷新時資料遺失
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
    start_btn = st.button("🚀 開始測驗！", use_container_width=True)
    
    if start_btn:
        st.session_state.quiz_started = True
        st.session_state.current_questions = DB_QUIZ[category]
        st.session_state.user_answers = {}
        st.session_state.submitted = False
        st.rerun()

# 5. 測驗進行中介面
else:
    st.info("📝 請認真作答以下題目，完成後點擊最下方的「提交答案」按鈕。")
    
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
                st.write(f"🟢 **您的答案**：`{u_ans}` (正確！+33.3分)")
                score += 1
            else:
                st.write(f"🔴 **您的答案**：`{u_ans}` (錯誤❌)")
                st.write(f"💡 **正確答案**：`{q['answer']}`")
                
            st.info(f"🔍 **知識小解析**：{q['hint']}")
            st.write("---")
            
        final_score = round((score / total) * 100)
        
        st.markdown(f"## 🏆 最終得分：`{final_score} / 100` 分")
        if final_score == 100:
            st.balloons() # 滿分噴氣球特效！
            st.success("🤖 報告 **賴以航** 總工程師！玩家獲得滿分天梯成就！👑")
        elif final_score >= 60:
            st.warning("👌 表現不錯喔！已經及格了，再接再厲就能挑戰滿分！")
        else:
            st.error("😢 哎呀，差一點點就及格了！別氣餒，看過解析後再挑戰一次吧！")
            
        retry_btn = st.button("🔄 重新選擇考科挑戰", use_container_width=True)
        if retry_btn:
            st.session_state.quiz_started = False
            st.session_state.submitted = False
            st.rerun()

st.write("\n---")
st.caption("⚡ Powered by Streamlit & Python Chat Bot")
st.caption("© 2026 賴以航 (Yi-Hang Lai). All rights reserved. 專案產權所有，翻印必究。")
