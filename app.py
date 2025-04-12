import streamlit as st
from supabase_client import add_user, add_goal, get_user_id_by_name, get_goals_by_user, delete_goal
from logic import estimate_lifespan, calculate_remaining_life
from openai_api import get_goal_plan
import datetime
import re

st.set_page_config(page_title="mirailog", layout="centered")
st.title("🪣 mirailog - バスケットリスト")

# セッションステート初期化
if "plan" not in st.session_state:
    st.session_state.plan = ""

tab1, tab2, tab3 = st.tabs(["👤 ユーザー登録", "🎯 やりたいこと登録", "📋 やりたいこと一覧"])

with tab1:
    st.header("👤 ユーザー登録")
    name = st.text_input("名前")
    birthdate = st.date_input(
    "生年月日",
    value=datetime.date(1990, 1, 1),
    min_value=datetime.date(1900, 1, 1),
    max_value=datetime.date.today()
    )  
    gender = st.selectbox("性別", ["男性", "女性"])

    if st.button("登録して寿命を計算"):
        lifespan = estimate_lifespan(gender)
        remaining_days = calculate_remaining_life(str(birthdate), lifespan)
        add_user(name, str(birthdate), gender, lifespan)
        st.success(f"{name} さんの残り寿命は {remaining_days:,} 日です。")

with tab2:
    st.header("🎯 やりたいこと登録")
    user_name = st.text_input("登録済みユーザー名", key="user_input")
    goal = st.text_input("やりたいこと")
    deadline = st.date_input("いつまでに？")
    tag = st.text_input("タグ（例：旅行・学び・趣味 など）")

    if st.button("AIで提案をもらう"):
        if goal:
            plan = get_goal_plan(goal)
            st.session_state.plan = plan
            st.text_area("AIからの提案", plan, height=200)
        else:
            st.warning("やりたいことを入力してください。")

    if st.button("提案を登録"):
        if not st.session_state.plan:
            st.warning("まず『AIで提案をもらう』を押してください。")
        else:
            user_id = get_user_id_by_name(user_name)
            if user_id:
                plan_text = st.session_state.plan
                time = ""
                cost = ""
                action = ""

                # 正規表現で抽出
                match_time = re.search(r"時間[:：]\s*(.*)", plan_text)
                if match_time:
                    time = match_time.group(1).strip()

                match_cost = re.search(r"費用[:：]\s*(.*)", plan_text)
                if match_cost:
                    cost = match_cost.group(1).strip()

                match_action = re.search(r"(次にやること|Next)[:：]\s*(.*)", plan_text)
                if match_action:
                    action = match_action.group(2).strip()
                add_goal(user_id, goal, str(deadline), tag, time, cost, action)
                st.success("やりたいことを登録しました。")
                st.session_state.plan = ""  # 登録後にクリア
            else:
                st.warning("ユーザーが見つかりません。")

with tab3:
    st.header("📋 やりたいこと一覧")
    search_user = st.text_input("ユーザー名を指定")

    # セッションでゴールを保持
    if "search_triggered" not in st.session_state:
        st.session_state.search_triggered = False
    if "goals_cache" not in st.session_state:
        st.session_state.goals_cache = []

    if st.button("表示"):
        user_id = get_user_id_by_name(search_user)
        if user_id:
            st.session_state.goals_cache = get_goals_by_user(user_id)
            st.session_state.search_triggered = True
        else:
            st.warning("ユーザーが見つかりません。")
            st.session_state.search_triggered = False

    if st.session_state.search_triggered:
        for g in st.session_state.goals_cache:
            with st.container():
                st.markdown(f"""
                ### 🎯 {g['goal']}
                - ⏳ 期限: {g['deadline']}
                - 🏷️ タグ: {g['tag']}
                - 🕐 時間: {g['estimated_time']}
                - 💰 費用: {g['estimated_cost']}
                - ✅ Next: {g['next_action']}
                """)

                if st.button("🗑 削除", key=f"delete_{g['id']}"):
                    delete_goal(g['id'])
                    st.success("削除しました！")
                    st.session_state.goals_cache = [goal for goal in st.session_state.goals_cache if goal['id'] != g['id']]
                    st.rerun()

    if "user_not_found" in st.session_state and st.session_state.user_not_found:
        st.warning("ユーザーが見つかりません。")
