"""
测评模板 — 工具横向对比 / 体验报告

Generate via: from writers import review; review.generate(topic, level)
"""

def generate(topic, level="beginner"):
    return f"""## {topic}

[1-2 句引语：我为什么要测这个东西]

---

## 快速结论

[适合谁 / 不适合谁]

## 功能对比

| 维度 | 工具A | 工具B |
|------|-------|-------|
| 功能1 | ✅ | ❌ |
| 功能2 | ✅ | ✅ |

## 实际体验

[具体场景 + 截图]

## 优缺点

**优点：**
• [优点1]
• [优点2]

**缺点：**
• [缺点1]

## 适合谁

[明确建议]

---

📮 关注「AI信号实验室」，追踪前沿信号，动手实验每一个新能力。
"""
