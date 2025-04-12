from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ユーザー追加
def add_user(name, birthdate, gender, lifespan):
    data = {
        "name": name,
        "birthdate": birthdate,
        "gender": gender,
        "estimated_lifespan": lifespan
    }
    return supabase.table("users").insert(data).execute()

# やりたいこと追加
def add_goal(user_id, goal, deadline, tag, time, cost, action):
    data = {
        "user_id": user_id,
        "goal": goal,
        "deadline": deadline,
        "tag": tag,
        "estimated_time": time,
        "estimated_cost": cost,
        "next_action": action
    }
    return supabase.table("goals").insert(data).execute()

# ユーザーID取得
def get_user_id_by_name(name):
    response = supabase.table("users").select("id").eq("name", name).execute()
    return response.data[0]["id"] if response.data else None

# やりたいこと一覧取得
def get_goals_by_user(user_id):
    response = supabase.table("goals").select("*").eq("user_id", user_id).execute()
    return response.data

# やりたいことを削除する機能
def delete_goal(goal_id):
    return supabase.table("goals").delete().eq("id", goal_id).execute()

