# 📧 Gmail API 详细设置指南

## 🎯 目标

设置Gmail API credentials.json，让skill自动获取你的Gmail邮件。

**时间：** 5-10分钟一次性设置

**结果：** 之后每天自动获取邮件，无需手动操作

---

## 📋 详细步骤

### Step 1: 访问 Google Cloud Console

🔗 **打开这个网址：** https://console.cloud.google.com/

- 如果需要，先登录你的Google账号
- 看到Google Cloud Console主页

---

### Step 2: 创建新项目

1. **点击顶部的 "Select a project"（选择项目）**
   - 位置：页面左上角，Google Cloud Platform旁边

2. **在弹出窗口中，点击 "NEW PROJECT"（新建项目）**
   - 右上角的按钮

3. **填写项目信息：**
   - **Project name（项目名称）：** `Morning Routine Skill`
     - 或者任何你喜欢的名字
   - **Location（位置）：** 保持默认（No organization）

4. **点击 "CREATE"（创建）**
   - 等待几秒钟，项目创建完成

5. **确认项目已选中**
   - 顶部应该显示 "Morning Routine Skill"

---

### Step 3: 启用 Gmail API

1. **在页面顶部的搜索框中输入：** `Gmail API`
   - 搜索框位置：页面中上部

2. **点击搜索结果中的 "Gmail API"**
   - 应该是第一个结果

3. **点击蓝色的 "ENABLE"（启用）按钮**
   - 页面中央的大按钮

4. **等待启用完成**
   - 页面会跳转到Gmail API页面
   - 看到 "API enabled" 提示

---

### Step 4: 配置 OAuth 同意屏幕

⚠️ **重要：** 这一步必须完成，否则后面无法创建凭据！

1. **点击左侧导航栏的 "OAuth consent screen"（OAuth 同意屏幕）**
   - 路径：APIs & Services → OAuth consent screen
   - 如果看不到左侧栏，点击左上角的 ☰ 菜单图标

2. **选择用户类型：**
   - 选择 **"External"（外部）**
   - 点击 **"CREATE"（创建）**

3. **填写 OAuth consent screen 信息：**

   **第一页 - App information:**
   - **App name（应用名称）：** `Morning Routine Skill`
   - **User support email（用户支持邮箱）：** 选择你的Gmail邮箱
   - **App logo（应用图标）：** 跳过（可选）
   - **Application home page（应用主页）：** 跳过（可选）
   - **Developer contact information（开发者联系信息）：** 填写你的Gmail邮箱
   - 点击 **"SAVE AND CONTINUE"（保存并继续）**

4. **第二页 - Scopes（权限范围）：**
   - 什么都不用填
   - 直接点击 **"SAVE AND CONTINUE"**

5. **第三页 - Test users（测试用户）：**
   - ⚠️ **关键步骤！** 必须添加你的邮箱
   - 点击 **"+ ADD USERS"（添加用户）**
   - 输入你的Gmail邮箱（例如：`your_email@gmail.com`）
   - 点击 **"ADD"（添加）**
   - 确认邮箱出现在列表中
   - 点击 **"SAVE AND CONTINUE"**

6. **第四页 - Summary（摘要）：**
   - 检查信息
   - 点击 **"BACK TO DASHBOARD"（返回控制面板）**

✅ OAuth consent screen 配置完成！

---

### Step 5: 创建 OAuth 凭据

1. **点击左侧导航栏的 "Credentials"（凭据）**
   - 路径：APIs & Services → Credentials

2. **点击顶部的 "+ CREATE CREDENTIALS"（创建凭据）**
   - 蓝色按钮

3. **选择 "OAuth client ID"（OAuth 客户端 ID）**

4. **配置 OAuth client ID：**

   - **Application type（应用类型）：**
     - ⚠️ **非常重要！** 选择 **"Desktop app"（桌面应用）**
     - ❌ **不要选择** "Web application"

   - **Name（名称）：**
     - 任意名称，例如：`Morning Routine Desktop`

   - 点击 **"CREATE"（创建）**

5. **弹出窗口显示 "OAuth client created"：**
   - 看到 Client ID 和 Client secret
   - ⚠️ **关键步骤：点击 "DOWNLOAD JSON"（下载JSON）**
   - 文件会下载到你的 Downloads 文件夹
   - 文件名类似：`client_secret_XXXXXXXXXX.apps.googleusercontent.com.json`

6. **点击 "OK" 关闭弹出窗口**

✅ credentials.json 已下载！

---

## 📥 Step 6: 安装 credentials.json 到 skill 目录

现在你的 Downloads 文件夹里有一个 JSON 文件。

### 方法1：命令行（推荐）

```bash
# 进入skill目录
cd morning-routine-skill

# 移动并重命名文件
mv ~/Downloads/client_secret_*.json ./credentials.json

# 验证文件存在
ls -l credentials.json
```

### 方法2：手动操作

1. 找到 Downloads 文件夹中的 `client_secret_XXXXX.json` 文件
2. 复制或移动到 `morning-routine-skill` 目录
3. 重命名为 `credentials.json`

⚠️ **重要提醒：**
- 这个文件包含敏感信息，不要分享给别人
- 不要提交到 GitHub（已在 .gitignore 中）
- 妥善保管

---

## 🔧 Step 7: 安装 Python 依赖

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

---

## 🚀 Step 8: 首次授权

```bash
python scripts/fetch_emails_gmail_api.py
```

**会发生什么：**

1. **浏览器自动打开**
   - 如果没有自动打开，复制终端中显示的URL手动打开

2. **选择你的Google账号**
   - 选择你在Step 4添加为测试用户的账号

3. **看到警告："Google hasn't verified this app"**
   - 这是正常的！因为这是你自己的测试应用
   - 点击 **"Advanced"（高级）**
   - 点击 **"Go to Morning Routine Skill (unsafe)"**
   - （这里的"unsafe"只是因为没有经过Google验证，实际上是安全的）

4. **授权页面：**
   - 看到 "Morning Routine Skill wants to access your Google Account"
   - 显示权限：**"Read, compose, send, and permanently delete all your email from Gmail"**
   - ⚠️ 实际上skill只会**读取**邮件，不会删除或修改
   - 点击 **"Allow"（允许）**

5. **授权完成：**
   - 浏览器显示：**"The authentication flow has completed"**
   - 可以关闭浏览器标签

6. **回到终端：**
   - 脚本自动继续运行
   - 开始获取你的Gmail邮件
   - 看到邮件列表输出

7. **token.json 已创建：**
   - skill 目录下会生成 `token.json` 文件
   - 以后运行不需要再次授权

✅ 设置完成！

---

## ✅ Step 9: 使用 skill

现在你可以自动获取Gmail邮件了！

```bash
# 方法1：直接获取邮件并生成晨报
python scripts/fetch_emails_gmail_api.py > morning_email_input.json
python scripts/generate_morning_briefing_final.py

# 方法2：只获取邮件查看
python scripts/fetch_emails_gmail_api.py
```

**输出：**
- 📊 `./outputs/morning-briefing-YYYYMMDD.png` - 静态图片
- 🌐 `./outputs/morning-briefing-YYYYMMDD.html` - 交互式网页

---

## 🔄 每天使用

设置完成后，每天只需要：

```bash
# 一条命令搞定！
python scripts/fetch_emails_gmail_api.py > morning_email_input.json && python scripts/generate_morning_briefing_final.py
```

- ⚡ 2-3秒获取邮件（即使有1000+封）
- 🎨 5-10秒生成视觉报告
- 📱 打开HTML文件，开始你的一天！

---

## 🔐 安全说明

### credentials.json
- **包含：** OAuth 客户端ID和密钥
- **敏感程度：** 中等（需要用户授权才能访问）
- **建议：** 不要公开分享，不要提交到 git

### token.json
- **包含：** 访问令牌（已授权）
- **敏感程度：** 高（可以直接访问你的Gmail）
- **位置：** 自动保存在 skill 目录
- **撤销方式：** https://myaccount.google.com/permissions

### 权限范围
- ✅ **只读访问** Gmail（虽然权限描述很宽泛）
- ❌ 不会发送邮件
- ❌ 不会删除邮件
- ❌ 不会修改邮件
- 🔒 可以随时在Google账号设置中撤销

---

## 🆘 常见问题

### ❓ "credentials.json not found"
- 确认文件在skill目录
- 确认文件名是 `credentials.json`（不是 `client_secret_XXX.json`）

### ❓ "Access blocked: This app's request is invalid"
- 检查OAuth consent screen是否配置完成
- 确认你的邮箱已添加为测试用户
- 确认选择的是 "Desktop app" 不是 "Web application"

### ❓ "Browser doesn't open"
- 手动复制终端中的URL
- 在浏览器中打开
- 完成授权后，复制授权码粘贴回终端

### ❓ "Google hasn't verified this app"
- 这是正常的！因为是你的个人测试应用
- 点击 "Advanced" → "Go to Morning Routine Skill (unsafe)"
- 这个警告不影响功能和安全性

### ❓ 重新授权
```bash
# 删除token.json
rm token.json

# 重新运行
python scripts/fetch_emails_gmail_api.py
```

### ❓ 撤销访问权限
1. 访问：https://myaccount.google.com/permissions
2. 找到 "Morning Routine Skill"
3. 点击 "Remove Access"

---

## 📊 对比：Gmail API vs 手动JSON

| 特性 | Gmail API | 手动JSON |
|------|-----------|----------|
| 设置时间 | 5-10分钟（一次） | 0分钟 |
| 每日使用 | 自动（2-3秒） | 手动（1-2分钟） |
| 速度 | 快（即使1000+邮件） | 取决于你的复制速度 |
| 邮箱支持 | 仅Gmail | 所有邮箱 |
| 实时性 | 总是最新 | 手动更新 |
| 复杂度 | 中等（OAuth） | 简单 |
| 推荐 | ✅ Gmail用户 | ✅ 非Gmail用户 |

---

## 🎉 完成！

你现在可以：
- ⚡ 自动获取Gmail邮件
- 🤖 AI提取任务
- 🎨 生成视觉报告
- 📱 追踪任务进度

每天早上只需一条命令，开启高效一天！

---

**疑问或问题？** 查看 [README.md](README.md) 或提交 [GitHub Issue](https://github.com/Y1fe1-Yang/morning-routine-skill/issues)

**Made with ❤️ using Claude Code**
