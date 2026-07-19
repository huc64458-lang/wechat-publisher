"""
教程模板 — 深度教程，适合 ComfyUI / CLI 工具 / 编程框架类内容

Generate via: from writers import tutorial; tutorial.generate(topic, level)
"""

def generate(topic, level="beginner"):
    """返回教程文章的 Markdown 字符串"""
    title = topic if topic else "教程标题"
    return f"""## {title}

[1-2 句引语：这篇文章解决什么问题]

---

## 准备什么

[前置条件，不超过 3 条]

## 第一步：操作

[具体步骤 + 为什么这么做]

## 第二步：操作

[具体步骤 + 为什么这么做]

## 效果展示

[配图占位]

---

📮 关注「AI信号实验室」，追踪前沿信号，动手实验每一个新能力。
"""
