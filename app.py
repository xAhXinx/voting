import streamlit as st
import matplotlib
from matplotlib import pyplot as plt
import pandas as pd
import os
import matplotlib.font_manager as fm
import gspread
from oauth2client.service_account import ServiceAccountCredentials
my_font = fm.FontProperties(fname="NotoSansTC-VariableFont_wght.ttf")

VOTES_FILE_PATH = "votes.csv"

# 初始化文件
if not os.path.exists(VOTES_FILE_PATH):
    with open(VOTES_FILE_PATH, "w") as f:
        f.write("user_id,choice\n")

# 读取CSV为DataFrame
def load_votes_df():
    return pd.read_csv(VOTES_FILE_PATH)

# 读取CSV为DataFrame
def load_users():
    # Define scope
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Authenticate
    creds = ServiceAccountCredentials.from_json_keyfile_name("voting-464016-35d60f0bca00.json", scope)
    client = gspread.authorize(creds)

    spreadsheet = client.open("voting")
    sheet = spreadsheet.worksheet("Form Responses 1")
    data = sheet.get_all_records()

    # Extract only the email addresses
    users = [row['Email Address'] for row in data]
    return users

# 更新或插入投票
def submit_vote(user_id, choice):
    votes_df = load_votes_df()

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

# 显示统计图
votes_df = load_votes_df()
st.title("🗳️ 当前投票结果")
if votes_df.empty:
    st.info("暂无投票")
else:
    # 统计投票并按固定顺序
    vote_counts = votes_df['choice'].value_counts()
    vote_counts = vote_counts.reindex(['正', '反'], fill_value=0)

    # 设置颜色
    colors = ['white', 'red']  # 正为白，反为红

    # 创建白色背景图
    fig, ax = plt.subplots(facecolor='#f3f5f9')
    fig.patch.set_facecolor('#f3f5f9')
    ax.set_facecolor('#f3f5f9')

    # 绘制带黑边的饼图
    wedges, texts, autotexts = ax.pie(
        vote_counts,
        labels=vote_counts.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        wedgeprops={'edgecolor': 'black', 'linewidth': 2},  # 黑色边框
        textprops={'color': 'black'}
    )

    # 手动设置标签字体
    for text in texts + autotexts:
        text.set_fontproperties(my_font)

    ax.axis('equal')

    # 显示图
    st.pyplot(fig)

# 自动刷新按钮（可选）
st.button("🔄 手动刷新图表", use_container_width=True)

st.markdown("<hr style='border: 2px solid black;'>", unsafe_allow_html=True)

# 前端页面
st.subheader("📊 实时可改票投票系统")

user_id = st.text_input("请输入你的电子邮箱：", max_chars=99)
choice = st.radio("你选择支持哪一方？", ["正", "反"], horizontal=True)

if st.button("提交/修改投票", use_container_width=True):
    if user_id.strip() == "":
        st.warning("请输入一个有效的电子邮箱")
    else:
        votes_df = load_votes_df()
        
        if user_id in votes_df['user_id'].values:
            submit_vote(user_id, choice)
            st.success("✅ 投票成功，你可以随时更改")
        else:
            users = load_users()
            if user_id in users:
                submit_vote(user_id, choice)
                st.success("✅ 投票成功，你可以随时更改")
            else:
                st.warning("请先到（https://forms.gle/eZh1wPnjPnmDbLvS9）提交Google Form进行注册")