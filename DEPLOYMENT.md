# 部署到 Streamlit Cloud 指南

## 🚀 快速部署步骤

### 1. 创建 GitHub 仓库

1. 访问 [GitHub](https://github.com) 并登录您的账户
2. 点击右上角的 "+" 按钮，选择 "New repository"
3. 仓库名称建议：`ai-investment-assistant`
4. 设置为 Public（公开仓库）
5. 不要初始化 README（我们已经有了）
6. 点击 "Create repository"

### 2. 上传代码到 GitHub

在您的项目目录中运行以下命令：

```bash
# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交代码
git commit -m "Initial commit: AI Investment Assistant"

# 添加远程仓库（替换为您的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/ai-investment-assistant.git

# 推送代码
git push -u origin main
```

### 3. 部署到 Streamlit Cloud

1. 访问 [Streamlit Cloud](https://share.streamlit.io/)
2. 使用您的 GitHub 账户登录
3. 点击 "New app"
4. 选择您刚创建的仓库：`YOUR_USERNAME/ai-investment-assistant`
5. 主文件路径：`app.py`
6. 点击 "Deploy!"

### 4. 等待部署完成

- 部署通常需要 2-5 分钟
- 您会看到构建日志
- 部署成功后，您会获得一个公开的 URL

## 📝 重要说明

- **API 密钥安全**：当前代码中 API 密钥是硬编码的，这仅适用于演示
- **生产环境**：建议使用 Streamlit Cloud 的 Secrets 管理功能
- **访问地址**：部署成功后，任何人都可以通过分配的 URL 访问您的应用

## 🔧 故障排除

如果部署失败，请检查：
1. requirements.txt 文件格式是否正确
2. 所有 Python 文件是否有语法错误
3. 依赖包版本是否兼容

## 🌐 部署成功后

您的应用将获得类似这样的 URL：
`https://your-app-name-random-string.streamlit.app/`

这个 URL 可以分享给任何人，他们都可以直接访问您的 AI 投资分析助手！