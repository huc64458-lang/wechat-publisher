#!/usr/bin/env python3
"""
WeChat Publisher 安装脚本
自动检测依赖、配置公众号信息、设置 API Key
"""
import os, subprocess, sys, json
from pathlib import Path

ROOT = Path(__file__).parent
ENV_PATH = ROOT / ".env"


def check_python():
    print(f"[1/5] Python: {sys.version.split()[0]} ✅")


def check_node():
    try:
        r = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=5)
        print(f"[2/5] Node.js: {r.stdout.strip()} ✅")
        return True
    except:
        print("[2/5] Node.js: ❌ 未安装")
        print("      请从 https://nodejs.org 下载安装")
        return False


def check_md2wechat():
    try:
        r = subprocess.run(["md2wechat", "--version"], capture_output=True, text=True, timeout=5)
        print(f"[3/5] md2wechat: ✅")
        return True
    except:
        print("[3/5] md2wechat: ❌ 未安装")
        print("      运行: npm install -g md2wechat")
        return False


def configure_wechat():
    if ENV_PATH.exists():
        env = ENV_PATH.read_text()
        if "WECHAT_APP_ID" in env and "WECHAT_APP_SECRET" in env:
            print(f"[4/5] 公众号配置: ✅ (已存在)")
            return

    print("[4/5] 公众号配置:")
    app_id = input("  请输入 AppID (回车跳过): ").strip()
    if not app_id:
        print("      跳过，可之后在 .env 中配置")
        return
    app_secret = input("  请输入 AppSecret: ").strip()
    if not app_secret:
        print("      跳过")
        return

    with open(ENV_PATH, "w") as f:
        f.write(f"WECHAT_APP_ID={app_id}\n")
        f.write(f"WECHAT_APP_SECRET={app_secret}\n")
    print("      ✅ 已保存")


def configure_api_key():
    if not ENV_PATH.exists():
        ENV_PATH.write_text("")
    env = ENV_PATH.read_text()
    if "IMAGE_API_KEY" in env:
        print(f"[5/5] 生图 API Key: ✅ (已配置)")
        return

    key = input("[5/5] 请输入生图 API Key (回车跳过): ").strip()
    if not key:
        print("      跳过，可之后用 python main.py set-key 配置")
        return

    with open(ENV_PATH, "a") as f:
        f.write(f"IMAGE_API_KEY={key}\n")
    print("      ✅ 已保存")


def create_dirs():
    for d in ["articles", "images", "images/covers"]:
        (ROOT / d).mkdir(exist_ok=True)


def main():
    print("=" * 50)
    print("  WeChat Publisher 安装")
    print("=" * 50)
    print()

    create_dirs()
    check_python()
    has_node = check_node()
    if has_node:
        check_md2wechat()
    configure_wechat()
    configure_api_key()

    print()
    print("=" * 50)
    print("  安装完成！")
    print("=" * 50)
    print()
    print("  快速开始:")
    print("    python main.py publish --type tutorial --topic '你的第一篇'")
    print()
    print("  分步使用:")
    print("    python main.py write --type tutorial --topic 'xxx'")
    print("    python main.py cover --title 'xxx' --subtitle 'xxx'")
    print("    python main.py push --input article.md --title 'xxx' --cover cover.png")
    print()


if __name__ == "__main__":
    main()
