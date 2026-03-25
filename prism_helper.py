import sys
import requests
import os
import subprocess
import re

API_KEY = "sk-3ddb9ed1ec454c56b93f4f55f02b7331"
REPO_PATH = r"C:\Users\lgdln\Documents\GitHub\prism-interconnect"

def call_deepseek(prompt):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }
    resp = requests.post(url, json=payload, headers=headers)
    if resp.status_code != 200:
        raise Exception(f"API 调用失败: {resp.text}")
    return resp.json()["choices"][0]["message"]["content"]

def git_pull():
    try:
        subprocess.run(["git", "pull"], cwd=REPO_PATH, check=True, capture_output=True, text=True)
        return True, "git pull 成功"
    except subprocess.CalledProcessError as e:
        return False, f"git pull 失败: {e.stderr}"

def git_push(filename, instruction):
    try:
        subprocess.run(["git", "add", filename], cwd=REPO_PATH, check=True, capture_output=True, text=True)
        subprocess.run(["git", "commit", "-m", f"AI: {instruction}"], cwd=REPO_PATH, check=True, capture_output=True, text=True)
        subprocess.run(["git", "push"], cwd=REPO_PATH, check=True, capture_output=True, text=True)
        return True, "推送成功"
    except subprocess.CalledProcessError as e:
        return False, f"Git 操作失败: {e.stderr}"

def main():
    if len(sys.argv) < 2:
        print("❌ 缺少 instruction 参数")
        return

    instruction = sys.argv[1].strip()
    target_file = sys.argv[2] if len(sys.argv) > 2 else ""

    # 如果指令是“拉取”相关，只做 pull
    pull_keywords = ["pull", "拉取", "更新", "同步", "fetch"]
    if any(kw in instruction.lower() for kw in pull_keywords):
        success, msg = git_pull()
        print(f"✅ {msg}" if success else f"❌ {msg}")
        return

    # 否则先 pull 确保本地最新
    pull_ok, pull_msg = git_pull()
    if not pull_ok:
        print(f"⚠️ {pull_msg}，继续尝试生成文档...")

    # 生成内容
    prompt = f"""你是棱镜协议项目的代码助手。用户指令：{instruction}
请生成相应的 Markdown 或代码内容。
如果是指令生成文档，请保持“入棱镜须知”和“留白”风格。
只输出文件内容，不要额外解释。"""
    content = call_deepseek(prompt)

    # 确定文件名
    if not target_file:
        match = re.search(r"(?:生成|创建|写)(?:一个)?\s*([^，,。\s]+)\s*(?:的)?(?:文档|代码)", instruction)
        if match:
            keyword = match.group(1).strip()
            filename = f"docs/spectrum-{keyword}.md"
        else:
            filename = "docs/auto-generated.md"
    else:
        filename = target_file

    full_path = os.path.join(REPO_PATH, filename)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Git 提交
    push_ok, push_msg = git_push(filename, instruction)
    print(f"✅ 文件已生成并推送：{filename}" if push_ok else f"❌ {push_msg}")

if __name__ == "__main__":
    main()