import openai
import os
from dotenv import load_dotenv
load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_goal_plan(goal):
    prompt = f"""
    あなたは人生設計をサポートするアシスタントです。

    ユーザーが「やりたいこと」を1つ入力します。  
    それに対して、以下の3つの項目を日本語で出力してください。

    1. 時間：そのやりたいことにかかるおおよその時間（例：3日間、週末2回、半年 など）
    2. 費用：かかる費用の目安（例：5万円、10ドル、ほぼ無料 など）
    3. 次にやること：その目標に向けて最初に着手すべき具体的な行動（例：航空券を予約する、友人に相談する など）

    出力形式は以下に厳密に従ってください：

    時間：〇〇  
    費用：〇〇  
    次にやること：〇〇

    ※ 文章や前置きはいらないので、上記の3行だけを返してください。

    やりたいこと：{goal}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # または gpt-3.5-turbo など
        messages=[
            {"role": "system", "content": "あなたは夢の実現を支援する専門家です。"},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content
    return content
