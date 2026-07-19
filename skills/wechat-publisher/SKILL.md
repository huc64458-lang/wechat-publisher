---
name: "wechat-publisher"
description: "Write WeChat Official Account articles with full pipeline: writing, illustration, cover, AI detection, and draft push. One command from idea to draft."
---

# WeChat Publisher

公众号 AI 写作插件。支持以下文章类型：

- **tutorial** — 深度教程，含代码块和操作步骤
- **daily** — AI 日报，3-5 条要闻简报
- **review** — 工具测评，含对比表格

## 先决条件

第一次使用前，运行安装检查：

```bash
python scripts/install.py
```

安装脚本会自动检测依赖并引导配置。

## 用法

### 一键发布全流程

```bash
python scripts/main.py publish \
  --type tutorial \
  --topic "ComfyUI 第3天：搭建第一个自动化流程" \
  --level beginner
```

插件会自动完成：

```
写作 → 配图(4张) → 封面(21:9) → AI检测 → 推草稿箱
```

### 分步执行

只写作，不配图不发布：

```bash
python scripts/main.py write --type tutorial --topic "xxx" --output article.md
```

只配图（文章已写好）：

```bash
python scripts/main.py illustrate --input article.md --count 4
```

只生成封面：

```bash
python scripts/main.py cover --title "文章标题" --subtitle "副标题" --theme tutorial
```

只 AI 检测：

```bash
python scripts/main.py detect --input article.md
```

只推送到公众号草稿箱：

```bash
python scripts/main.py push --input article.md --title "xxx" --cover cover.png
```

### 配置

首次运行 `install.py` 后，在项目根目录创建 `.env` 文件：

```
WECHAT_APP_ID=你的AppID
WECHAT_APP_SECRET=你的AppSecret
```

生图 API Key 通过插件 worker 系统配置：

```bash
python scripts/main.py set-key "sk-xxx..."
```

## 排版规范

### 标题
- 15-25 字，含数字更好
- 避免标题党，但要有钩子

### 正文
- 短段落，每段不超过 4 行
- 用小标题 `##` 分隔
- **正文内禁止使用 `#` H1 标题**
- 不要用 `###` H3（渲染会变橙方块+编号）
- 不要用 markdown 列表语法 `-` 或 `1.`（用 `•` 替代）
- 代码块标注语言类型
- 关键数据加粗

### 配图
- 风格：简约手绘风（黑线白底）
- 比例：3:4 竖版，手机友好
- 每篇至少 4 张概念图

### 封面
- 21:9 超宽海报，大字标题占 50%+
- 教程用柠檬黄 #FFD500
- 日报用克莱因蓝 #002FA7
- 观点用墨水黑 #0a0a0b

### 文末
```
📮 关注「AI信号实验室」，追踪前沿信号，动手实验每一个新能力。
```

## 发布前检查清单

- [ ] 配图已生成且插入正文
- [ ] 封面已通过 `--cover` 传入
- [ ] AI 浓度 < 20%
- [ ] `--title` 已传入
- [ ] 文末关注引导已添加
- [ ] 全文无 `###` H3
- [ ] 全文无 `- ` 或 `1. ` 列表语法

## Codex Display Rule

每次成功生成封面或配图后，立即在对话中展示：

```
![描述](绝对路径.png)
```

推送成功后，显示草稿的 Media ID。
