# 实时可改票投票系统

本项目是一个基于 Streamlit 的实时投票系统，支持用户通过邮箱注册和投票，并可随时修改自己的投票。投票数据本地存储于 CSV 文件，用户注册信息通过 Google 表单同步。

## 功能简介

- 用户通过 Google 表单注册邮箱
- 通过邮箱登录后可投票（正/反），并可随时修改
- 投票结果以饼图实时展示
- 支持手动刷新投票结果

## 文件结构

- `app.py`：主应用代码
- `votes.csv`：本地投票数据
- `requirements.txt`：依赖包列表
- `NotoSansTC-VariableFont_wght.ttf`：用于中文显示的字体
- `.streamlit/secrets.toml`：Google Service Account 配置（需自行配置）
- `.devcontainer/`：开发容器配置

## 快速开始

1. **安装依赖**

   ```sh
   pip install -r requirements.txt
   pip install streamlit matplotlib gspread google-auth
   ```

2. **配置 Google Service Account**

   - 将 Google Service Account 信息填写到 `.streamlit/secrets.toml`
   - 确保 Google Sheet 名称为 `voting`，表单页为 `Form Responses 1`

3. **运行应用**

   ```sh
   streamlit run app.py
   ```

4. **访问应用**

   打开浏览器访问 [https://debate-voting.streamlit.app/]

## 注意事项

- 仅注册邮箱可参与投票，未注册邮箱会提示先填写 Google Form
- 投票数据保存在 `votes.csv`
- 请勿将敏感密钥文件提交到公共仓库

## 依赖

- streamlit
- matplotlib
- gspread
- google-auth
- pandas