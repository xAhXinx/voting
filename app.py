import streamlit as st
import matplotlib
from matplotlib import pyplot as plt
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
        votes_df = pd.concat([votes_df, new_row], ignore_index=True)
    votes_df.to_csv(VOTES_FILE_PATH, index=False)

# 插入用户
def add_user(user_id):
    users_df = load_users()
    if user_id not in users_df['user_id'].values:
        new_row = pd.DataFrame([{'user_id': user_id}])
        users_df = pd.concat([users_df, new_row], ignore_index=True)
        users_df.to_csv(USERS_FILE_PATH, index=False)
        
# 前端页面
st.title("📊 实时可改票投票系统")

user_id = st.text_input("请输入你的电子邮箱", max_chars=30)
choice = st.radio("你选择支持哪一项？", ["正", "反"])

if st.button("提交/修改投票"):
    if user_id.strip() == "":
        st.warning("请输入一个有效的电子邮箱")
    else:
        users_df = load_users()
        if user_id in users_df['user_id'].values:
            submit_vote(user_id, choice)
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
    fig, ax = plt.subplots()
    ax.pie(vote_counts, labels=vote_counts.index, autopct='%1.1f%%', startangle=90, textprops={'fontname': 'DejaVu Sans'})
    ax.axis('equal')
    st.pyplot(fig)

# 自动刷新按钮（可选）
st.button("🔄 手动刷新图表")

st.subheader("👤 新用户注册")
admin_password = st.text_input("请输入管理员密码", type="password", key="admin_pwd")
ADMIN_PASSWORD = "password@abc123"  # 请替换为你的管理员密码

if admin_password == ADMIN_PASSWORD:
    new_user_id = st.text_input("请输入新用户电子邮箱进行注册", key="register")
    if st.button("注册新用户"):
        if new_user_id.strip() == "":
            st.warning("请输入一个有效的电子邮箱进行注册")
        else:
            users_df = load_users()
            if new_user_id in users_df['user_id'].values:
                st.info("该用户已注册")
            else:
                add_user(new_user_id)
                st.success("注册成功！请返回上方进行投票")
else:
    st.info("请输入管理员密码以注册新用户")
