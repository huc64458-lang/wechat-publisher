"""
日报模板 — AI 资讯简报，3-5 条要闻

Generate via: from writers import daily; daily.generate(topic, level)
"""

def generate(topic, level="beginner"):
    return f"""## 🤖 AI信号实验室日报 | 7月19日

**今日速览：** [一句话概括今天最重要的信号]

---

**1. [新闻标题]**
[2-3 句话：发生了什么 + 为什么重要]

**2. [新闻标题]**
[2-3 句话：发生了什么 + 为什么重要]

**3. [新闻标题]**
[2-3 句话：发生了什么 + 为什么重要]

---

📮 每天追踪前沿信号，动手试新东西。明天见。
"""
