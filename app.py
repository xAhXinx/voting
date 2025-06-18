import streamlit as st
import pandas as pd
import os

VOTES_FILE_PATH = "votes.csv"
USERS_FILE_PATH = "users.csv"

# 初始化文件
if not os.path.exists(VOTES_FILE_PATH):
    with open(VOTES_FILE_PATH, "w") as f:
        f.write("user_id,choice\n")

# 初始化文件
if not os.path.exists(USERS_FILE_PATH):
    with open(USERS_FILE_PATH, "w") as f:
        f.write("user_id\n")

# 读取CSV为DataFrame
def load_votes():
    return pd.read_csv(VOTES_FILE_PATH)

# 读取CSV为DataFrame
def load_users():
    return pd.read_csv(USERS_FILE_PATH)

# 更新或插入投票
def submit_vote(user_id, choice):
    votes_df = load_votes()

    if user_id in votes_df['user_id'].values:
        votes_df.loc[votes_df['user_id'] == user_id, 'choice'] = choice
    else:
        new_row = pd.DataFrame([{'user_id': user_id, 'choice': choice}])
        df = pd.concat([df, new_row], ignore_index=True)
    votes_df.to_csv(VOTES_FILE_PATH, index=False)
        

# 前端页面
st.title("📊 实时可改票投票系统")

user_id = st.text_input("请输入你的电话号码", max_chars=30)
choice = st.radio("你选择支持哪一项？", ["正", "反"])

if st.button("提交/修改投票"):
    if user_id.strip() == "":
        st.warning("请输入一个有效的电话号码")
    else:
        users_df = load_users()
        if user_id in users_df['user_id'].values:
            submit_vote(user_id.strip(), choice)
            st.success("✅ 投票成功，你可以随时更改")
        else:
            st.warning("请先提交Google Form")

# 显示统计图
votes_df = load_votes()
st.subheader("🗳️ 当前投票结果")
if votes_df.empty:
    st.info("暂无投票")
else:
    vote_counts = votes_df['choice'].value_counts()
    st.bar_chart(vote_counts)

# 自动刷新按钮（可选）
st.button("🔄 手动刷新图表")
