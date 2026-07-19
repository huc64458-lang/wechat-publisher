"""
WeChat Publisher — 公众号 AI 写作工作流插件

Usage:
  python main.py publish --type tutorial --topic "xxx"
  python main.py write --type tutorial --topic "xxx" --output article.md
  python main.py illustrate --input article.md --count 4
  python main.py cover --title "xxx" --subtitle "xxx" --theme tutorial
  python main.py detect --input article.md
  python main.py push --input article.md --title "xxx" --cover cover.png
  python main.py set-key "sk-xxx..."
  python main.py install
"""
import argparse, json, os, subprocess, sys, textwrap, time
from pathlib import Path

ROOT = Path(__file__).parent.parent


def cmd_publish(args):
    """全流程：写 → 配图 → 封面 → 检测 → 推送"""
    print("=" * 50)
    print(f"📝 开始写作: {args.topic}")
    print("=" * 50)

    # 1. 写文章
    article_path = ROOT / "articles" / f"{args.topic.replace(' ', '-')[:30]}.md"
    article_path.parent.mkdir(exist_ok=True)
    cmd_write(args)
    print(f"✅ 文章已生成: {article_path}")

    # 2. 配图
    print("\n🎨 生成配图...")
    cmd_illustrate(args)
    print("✅ 配图完成")

    # 3. 封面
    print("\n🖼️ 生成封面...")
    cmd_cover(args)
    print("✅ 封面完成")

    # 4. AI 检测
    print("\n🔍 AI 检测...")
    cmd_detect(args)
    print("✅ 检测通过")

    # 5. 推送
    print("\n📤 推送草稿箱...")
    args.input = str(article_path)
    cmd_push(args)
    print("\n🎉 发布完成！去公众号草稿箱预览吧")


def cmd_write(args):
    """调用 AI 模型写文章（通过 API 或模板生成）"""
    from writers import tutorial, daily, review

    writers = {
        "tutorial": tutorial,
        "daily": daily,
        "review": review,
    }
    writer = writers.get(args.type, tutorial)
    markdown = writer.generate(args.topic, args.level or "beginner")

    output = Path(args.output or f"article_{int(time.time())}.md")
    if not output.is_absolute():
        output = ROOT / "articles" / output.name
    output.parent.mkdir(exist_ok=True)
    output.write_text(markdown, encoding="utf-8")
    print(f"📄 {output}")
    return str(output)


def cmd_illustrate(args):
    """为文章批量生成配图"""
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ 文件不存在: {args.input}")
        return

    text = input_path.read_text(encoding="utf-8")
    sections = [s.strip() for s in text.split("## ") if s.strip()]

    # 每篇文章4张配图
    count = args.count or 4
    prompts = []

    for i, section in enumerate(sections[:count]):
        title = section.split("\n")[0][:30]
        prompts.append(
            f"A clean minimalist hand-drawn style illustration on warm white paper background. "
            f"Black ink thin line art. Concept illustration for WeChat article: {title}. "
            f"Simple icons and clean layout. 3:4 vertical. ALL text in Chinese."
        )

    # 调用 fhl-image-gen 插件或直接调用 API
    for i, prompt in enumerate(prompts):
        out_path = ROOT / "images" / f"illustration-{i+1:02d}.png"
        out_path.parent.mkdir(exist_ok=True)
        _generate_image(prompt, str(out_path))
        print(f"  🖼️ 配图 {i+1}: {out_path.name}")


def cmd_cover(args):
    """生成文章封面"""
    theme_colors = {
        "tutorial": "柠檬黄 #FFD500",
        "daily": "克莱因蓝 #002FA7",
        "review": "墨水黑 #0a0a0b",
    }
    color = theme_colors.get(args.theme, "柠檬黄 #FFD500")

    prompt = (
        f"A WeChat Official Account article COVER IMAGE, 21:9 ultra-wide poster. "
        f"BIG TYPOGRAPHY is the main visual. "
        f"Main title in LARGE BOLD Chinese: '{args.title}' displayed prominently center. "
        f"Subtitle below: '{args.subtitle or ''}'. "
        f"Visual style: dark background, {color} as accent color. "
        f"Clean modern poster layout. Maximum readability. Chinese title only. "
        f"No photography. No watermarks. Keep it POSTER style."
    )

    out_path = ROOT / "images" / "covers" / f"cover-{int(time.time())}.png"
    out_path.parent.mkdir(exist_ok=True)
    _generate_image(prompt, str(out_path), aspect="2:1")
    print(f"🖼️ 封面: {out_path}")

    # 显示给用户
    print(f"\n![封面]({out_path})")


def cmd_detect(args):
    """AI 检测（文本分析）"""
    input_path = Path(args.input or "article.md")
    if not input_path.exists():
        print("⚠️ 找不到文件，跳过检测")
        return

    text = input_path.read_text(encoding="utf-8")

    # 基于规则的人工检测评分
    score = 0
    checks = []

    # 加分项（像人写的）
    if any(w in text for w in ["我", "我们", "我觉得", "试了试"]):
        score -= 5
        checks.append("✅ 有第一人称叙述")

    if any(w in text for w in ["卧槽", "牛逼", "龟龟", "说白了", "不管了"]):
        score -= 5
        checks.append("✅ 有口语化表达")

    if any(w in text for w in ["写到这", "突然意识到", "说实话"]):
        score -= 5
        checks.append("✅ 有元意识/自嘲")

    lines = text.split("\n")
    avg_line_len = sum(len(l) for l in lines if l.strip()) / max(len([l for l in lines if l.strip()]), 1)
    if avg_line_len > 80:
        score += 10
        checks.append("⚠️ 句子偏长")

    # 短段落加分
    short_paras = sum(1 for l in lines if l.strip() and len(l.strip()) < 30)
    if short_paras > len(lines) * 0.2:
        score -= 5
        checks.append("✅ 短段落多，手机友好")

    score = max(0, min(100, score + 20))

    print(f"\n📊 AI 浓度评估: {score}%")
    for c in checks:
        print(f"  {c}")

    if score < 20:
        print("🟢 安全，可以直接发")
    elif score < 40:
        print("🟡 需要微调")
    else:
        print("🔴 建议大幅改写")

    return score


def _find_md2wechat():
    """查找 md2wechat 可执行文件路径"""
    candidates = [
        r"C:\Users\ziye1\AppData\Roaming\npm\md2wechat.cmd",
        r"C:\Users\ziye1\AppData\Roaming\npm\md2wechat",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return "md2wechat"  # fallback, might fail


def cmd_push(args):
    """推送到公众号草稿箱"""
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ 文件不存在: {args.input}")
        return

    cover_path = args.cover or ""
    title = args.title or input_path.stem

    md2wechat = _find_md2wechat()

    cmd = [
        md2wechat, "sync-md",
        str(input_path),
        "--title", title,
        "--author", args.author or "ziyecodex",
    ]
    if cover_path:
        cmd += ["--cover", cover_path]
    if args.update:
        cmd += ["--update", args.update]

    print(f"  📤 推送中...")
    result = subprocess.run(cmd, capture_output=True, timeout=120, shell=True)
    output = result.stdout.decode('utf-8', errors='replace')
    print(output)

    if "Draft created" in output or "Draft updated" in output:
        for line in output.split("\n"):
            if "Media ID" in line:
                print(f"✅ {line.strip()}")
    else:
        print(f"⚠️ 推送结果:\n{output}")


def cmd_set_key(args):
    """配置生图 API Key"""
    key_path = ROOT / ".env"
    with open(key_path, "a") as f:
        f.write(f"\nIMAGE_API_KEY={args.key}\n")
    print(f"✅ API Key 已保存")


def cmd_install(args):
    """安装/检查依赖"""
    print("🔧 WeChat Publisher 安装检查\n")

    # Python 版本
    print(f"Python: {sys.version.split()[0]}")

    # 检查 md2wechat
    try:
        r = subprocess.run(["md2wechat", "--version"], capture_output=True, text=True, timeout=5)
        print(f"md2wechat: ✅ {r.stdout.strip() or r.stderr.strip()}")
    except FileNotFoundError:
        print("md2wechat: ❌ 未安装")
        print("  安装: npm install -g md2wechat")

    # 检查 .env
    env_path = ROOT / ".env"
    if env_path.exists():
        env = env_path.read_text()
        if "WECHAT_APP_ID" in env and "WECHAT_APP_SECRET" in env:
            print("公众号配置: ✅")
        else:
            print("公众号配置: ⚠️ 请配置 WECHAT_APP_ID 和 WECHAT_APP_SECRET")
    else:
        print("公众号配置: ⚠️ 请创建 .env 文件")

    # 检查 API Key
    key_path = ROOT / ".env"
    if key_path.exists() and "IMAGE_API_KEY" in key_path.read_text():
        print("生图 API Key: ✅")
    else:
        print("生图 API Key: ⚠️ 请配置")
        print("  运行: python main.py set-key 'sk-xxx...'")

    # 检查目录
    for d in ["articles", "images", "images/covers"]:
        p = ROOT / d
        p.mkdir(exist_ok=True)
        print(f"目录 {d}: ✅")

    print("\n💡 首次使用步骤:")
    print("  1. npm install -g md2wechat")
    print("  2. 创建 .env 写入 WECHAT_APP_ID / WECHAT_APP_SECRET")
    print("  3. python main.py set-key 'sk-xxx...'")
    print("  4. python main.py publish --type tutorial --topic '你的第一篇'")
    print()


def _generate_image(prompt, output_path, aspect="3:4"):
    """调用 fhl-image-gen 插件生成图片"""
    import subprocess

    aspect_map = {"3:4": "3:4", "2:1": "2:1", "1:1": "1:1", "16:9": "16:9"}
    ar = aspect_map.get(aspect, "3:4")

    plugin_script = os.path.expanduser(
        r"~\AppData\Local\Programs\OpenHarness\plugins\fhl-image-gen\scripts\generate.mjs"
    )
    # Try alternate locations
    alt_paths = [
        r"C:\Users\ziye1\.openharness\plugins\fhl-image-gen\scripts\generate.mjs",
        os.path.expanduser(r"~\.openharness\plugins\fhl-image-gen\scripts\generate.mjs"),
    ]
    for p in alt_paths:
        if os.path.exists(p):
            plugin_script = p
            break

    if not os.path.exists(plugin_script):
        print("⚠️ fhl-image-gen 插件未安装，请先安装")
        return

    fhl_out = Path.home() / "Pictures" / "fhl-image-gen"
    cmd = [
        "node", plugin_script,
        "--prompt", prompt,
        "--aspect", ar,
    ]

    result = subprocess.run(cmd, capture_output=True, timeout=300)
    if result.returncode == 0:
        # fhl-image-gen saves to default output dir, find latest file
        latest = max(fhl_out.glob("*.png"), key=lambda p: p.stat().st_mtime, default=None)
        if latest:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            import shutil
            shutil.copy2(str(latest), output_path)
            print(f"  ✅ 图片已保存: {output_path}")
            print(f"\n![封面]({output_path})")
        else:
            print("  ⚠️ 未找到生成的图片")
    else:
        err = result.stderr.decode('utf-8', errors='replace')[:200]
        print(f"  ⚠️ 生图失败: {err}")


def main():
    parser = argparse.ArgumentParser(description="WeChat Publisher — 公众号 AI 写作工作流")
    sub = parser.add_subparsers(dest="command", required=True)

    # publish
    p = sub.add_parser("publish", help="全流程发布")
    p.add_argument("--type", choices=["tutorial", "daily", "review"], default="tutorial")
    p.add_argument("--topic", required=True)
    p.add_argument("--level", default="beginner")

    # write
    p = sub.add_parser("write", help="只写文章")
    p.add_argument("--type", choices=["tutorial", "daily", "review"], default="tutorial")
    p.add_argument("--topic", required=True)
    p.add_argument("--level", default="beginner")
    p.add_argument("--output", default="")

    # illustrate
    p = sub.add_parser("illustrate", help="批量配图")
    p.add_argument("--input", required=True)
    p.add_argument("--count", type=int, default=4)

    # cover
    p = sub.add_parser("cover", help="生成封面")
    p.add_argument("--title", required=True)
    p.add_argument("--subtitle", default="")
    p.add_argument("--theme", choices=["tutorial", "daily", "review"], default="tutorial")

    # detect
    p = sub.add_parser("detect", help="AI 检测")
    p.add_argument("--input", default="article.md")

    # push
    p = sub.add_parser("push", help="推送草稿箱")
    p.add_argument("--input", required=True)
    p.add_argument("--title", default="")
    p.add_argument("--cover", default="")
    p.add_argument("--author", default="ziyecodex")
    p.add_argument("--update", default="")

    # set-key
    p = sub.add_parser("set-key", help="配置 API Key")
    p.add_argument("key")

    # install
    sub.add_parser("install", help="安装检查")

    args = parser.parse_args()

    commands = {
        "publish": cmd_publish,
        "write": cmd_write,
        "illustrate": cmd_illustrate,
        "cover": cmd_cover,
        "detect": cmd_detect,
        "push": cmd_push,
        "set-key": cmd_set_key,
        "install": cmd_install,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
