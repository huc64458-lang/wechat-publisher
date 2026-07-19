# WeChat Publisher

公众号 AI 写作工作流插件 — 写作 · 配图 · 封面 · 检测 · 发布一条龙

## 安装

```bash
git clone https://github.com/ziyecodex/wechat-publisher
cd wechat-publisher
python scripts/install.py
```

安装脚本会引导你完成所有配置。

## 前置依赖

- Python 3.8+
- Node.js 18+（用于 md2wechat）
- md2wechat: `npm install -g md2wechat`
- 一个微信公众号（获取 AppID / AppSecret）
- 生图 API Key

## 使用

### 一键发布

```bash
python scripts/main.py publish --type tutorial --topic "ComfyUI第3天" --level beginner
```

自动完成：写作 → 配图 → 封面 → AI 检测 → 推送到公众号草稿箱

### 分步执行

```bash
# 只写文章
python scripts/main.py write --type tutorial --topic "我的主题" --output article.md

# 只配图
python scripts/main.py illustrate --input article.md --count 4

# 只生成封面
python scripts/main.py cover --title "文章标题" --subtitle "副标题" --theme tutorial

# 只推草稿箱
python scripts/main.py push --input article.md --title "文章标题" --cover cover.png
```

## 文章类型

| 类型 | 说明 | 适用 |
|------|------|------|
| tutorial | 深度教程 | ComfyUI、CLI 工具、编程框架 |
| daily | AI 日报 | 每日资讯简报 |
| review | 工具测评 | 横向对比、体验报告 |

## 项目结构

```
wechat-publisher/
├── .codex-plugin/plugin.json    # 插件元数据
├── scripts/
│   ├── main.py                  # CLI 主入口
│   ├── install.py               # 安装脚本
│   ├── writers/                 # 写作模板
│   │   ├── tutorial.py
│   │   ├── daily.py
│   │   └── review.py
│   └── illustrators/            # 配图模块
├── skills/wechat-publisher/
│   └── SKILL.md                 # AI 技能定义
├── articles/                    # 文章输出
├── images/                      # 图片输出
│   └── covers/                  # 封面输出
└── .env                         # 配置（不提交）
```

## 配置

创建 `.env` 文件：

```
WECHAT_APP_ID=你的AppID
WECHAT_APP_SECRET=你的AppSecret
IMAGE_API_KEY=你的生图APIKey
```

## License

MIT
