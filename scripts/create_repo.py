import requests, os, sys, json

# Try to create repo via GitHub API
token = os.environ.get("GH_TOKEN", "")
headers = {"Accept": "application/vnd.github.v3+json"}

if token:
    headers["Authorization"] = f"token {token}"
else:
    # Try browser-stored credentials
    print("No GH_TOKEN found, trying unauthenticated...")

data = {
    "name": "wechat-publisher",
    "description": "公众号AI写作工作流插件 — 写作·配图·封面·检测·发布一条龙",
    "private": False,
    "auto_init": False
}

r = requests.post("https://api.github.com/user/repos", json=data, headers=headers, timeout=10)
print(f"Status: {r.status_code}")
if r.status_code == 201:
    print(f"✅ 仓库已创建: {r.json()['html_url']}")
    print(f"   SSH: {r.json()['ssh_url']}")
    with open("_tmp_gh_url.txt", "w") as f:
        f.write(r.json()["ssh_url"])
elif r.status_code == 401:
    print("❌ 需要 GitHub Token")
    print("   1. 去 https://github.com/settings/tokens 生成 token")
    print("   2. 运行: $env:GH_TOKEN='你的token'")
    print("   3. 重新运行本脚本")
else:
    print(f"❌ {r.text[:300]}")
