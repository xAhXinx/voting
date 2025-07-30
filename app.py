import streamlit as st
import matplotlib
from matplotlib import pyplot as plt
import pandas as pd
import os
import matplotlib.font_manager as fm
import gspread
from google.oauth2.service_account import Credentials
my_font = fm.FontProperties(fname="NotoSansSC-Regular.ttf")

VOTES_FILE_PATH = "votes.csv"

# 初始化文件
if not os.path.exists(VOTES_FILE_PATH):
    with open(VOTES_FILE_PATH, "w") as f:
        f.write("user_id,choice_team,choice_speaker\n")

# 读取CSV为DataFrame
def load_votes_df():
    return pd.read_csv(VOTES_FILE_PATH)

# 读取CSV为DataFrame
def load_users():
    # Define correct scope for Sheets and Drive access
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # Load service account with scope
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )

    # Authorize gspread client
    client = gspread.authorize(creds)

    # Load sheet
    spreadsheet = client.open("voting")
    sheet = spreadsheet.worksheet("Form Responses 1")
    data = sheet.get_all_records()

    # Extract emails
    users = [row['Email Address'] for row in data]
    return users

# 更新或插入投票
def submit_vote(user_id, choice_team, choice_speaker):
    votes_df = load_votes_df()

    if user_id in votes_df['user_id'].values:
        votes_df.loc[votes_df['user_id'] == user_id, 'choice_team'] = choice_team
        votes_df.loc[votes_df['user_id'] == user_id, 'choice_speaker'] = choice_speaker
    else:
        new_row = pd.DataFrame([{'user_id': user_id, 'choice_team': choice_team, 'choice_speaker': choice_speaker}])
        votes_df = pd.concat([votes_df, new_row], ignore_index=True)
    votes_df.to_csv(VOTES_FILE_PATH, index=False)

# 显示统计图
votes_df = load_votes_df()
st.title("🗳️ 当前投票结果")
if votes_df.empty:
    st.info("暂无投票")
else:
    # 统计投票并按固定顺序
    vote_counts = votes_df['choice_team'].value_counts()
    vote_counts = vote_counts.reindex(['正方', '反方'], fill_value=0)

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

    # 统计最佳辩手票数（按票数降序排列）
    speaker_counts = votes_df['choice_speaker'].value_counts()
    speaker_counts = speaker_counts.sort_values(ascending=True)

    # 横向柱状图颜色（按降序后重新分配颜色）
    speaker_order = speaker_counts.index.tolist()
    bar_colors = ['White' if '正方' in name else 'Red' for name in speaker_order]

    fig2, ax2 = plt.subplots(facecolor='#f3f5f9')
    fig2.patch.set_facecolor('#f3f5f9')
    ax2.set_facecolor('#f3f5f9')

    bars = ax2.barh(speaker_counts.index, speaker_counts.values, color=bar_colors, edgecolor='black', linewidth=2)
    ax2.set_title("最佳辩手投票分布", fontproperties=my_font)
    ax2.set_yticklabels(speaker_counts.index, rotation=0, fontproperties=my_font)
    ax2.set_xlabel("")  # 不显示数轴标签
    ax2.xaxis.set_ticks([])  # 不显示数轴刻度

    for bar in bars:
        width = bar.get_width()
        ax2.annotate(f'{int(width)}',
                     xy=(width, bar.get_y() + bar.get_height() / 2),
                     xytext=(3, 0),
                     textcoords="offset points",
                     va='center', ha='left',
                     fontproperties=my_font)

    st.pyplot(fig2)

# 自动刷新按钮（可选）
st.button("🔄 手动刷新图表", use_container_width=True)

st.markdown("<hr style='border: 2px solid black;'>", unsafe_allow_html=True)

# 前端页面
st.subheader("📊 实时可改票投票系统")

user_id = st.text_input("请输入你的电子邮箱：", max_chars=99)
choice_team = st.radio("你选择支持哪一方？", ["正方", "反方"], horizontal=True)
choice_speaker = st.radio("你选择支持哪位辩手为最佳辩手？", ["正方一辩", "正方二辩", "正方三辩", "正方四辩", "反方一辩", "反方二辩", "反方三辩", "反方四辩"], horizontal=False)

if st.button("提交/修改投票", use_container_width=True):
    if user_id.strip() == "":
        st.warning("请输入一个有效的电子邮箱")
    else:
        votes_df = load_votes_df()
        
        if user_id in votes_df['user_id'].values:
            submit_vote(user_id, choice_team, choice_speaker)
            st.success("✅ 投票成功，你可以随时更改")
        else:
            users = load_users()
            if user_id in users:
                submit_vote(user_id, choice_team, choice_speaker)
                st.success("✅ 投票成功，你可以随时更改")
            else:
                st.warning("请先到 https://forms.gle/eZh1wPnjPnmDbLvS9 提交Google Form进行注册")