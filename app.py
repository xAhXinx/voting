import streamlit as st
import pandas as pd
import os

FILE_PATH = "votes.csv"

# 初始化文件
if not os.path.exists(FILE_PATH):
    with open(FILE_PATH, "w") as f:
        f.write("user_id,choice\n")

# 读取CSV为DataFrame
def load_votes():
    return pd.read_csv(FILE_PATH)

# 更新或插入投票
def submit_vote(user_id, choice):
    df = load_votes()
    if user_id in df['user_id'].values:
        df.loc[df['user_id'] == user_id, 'choice'] = choice
    else:
        df = df.append({'user_id': user_id, 'choice': choice}, ignore_index=True)
    df.to_csv(FILE_PATH, index=False)

# 前端页面
st.title("📊 实时可改票投票系统")

user_id = st.text_input("请输入你的昵称或ID（唯一）", max_chars=30)
choice = st.radio("你选择支持哪一项？", ["A", "B", "C"])

if st.button("提交/修改投票"):
    if user_id.strip() == "":
        st.warning("请输入一个有效的ID")
    else:
        submit_vote(user_id.strip(), choice)
        st.success("✅ 投票成功，你可以随时更改")

# 显示统计图
df = load_votes()
st.subheader("🗳️ 当前投票结果")
if df.empty:
    st.info("暂无投票")
else:
    vote_counts = df['choice'].value_counts()
    st.bar_chart(vote_counts)

# 自动刷新按钮（可选）
st.button("🔄 手动刷新图表")
