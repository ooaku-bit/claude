#!/usr/bin/env python3
"""
sync-claude-settings.py
公式ソースから Claude Code の最新設定情報を取得し docs/ に反映する。

取得元:
  - npm registry         : バージョン情報
  - GitHub raw           : README / CHANGELOG
  - code.claude.com/docs : 設定・フック・概要

Usage: python3 sync-claude-settings.py [--force]
"""

import json
import re
import sys
from datetime import datetime, timedelta
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
CACHE_FILE = REPO_ROOT / ".claude" / ".sync-timestamp"
SETTINGS_FILE = REPO_ROOT / ".claude" / "settings.json"
OUTPUT_FILE = DOCS_DIR / "claude-code-latest.md"

SYNC_INTERVAL_HOURS = 24

SOURCES = {
    "npm":       "https://registry.npmjs.org/@anthropic-ai/claude-code/latest",
    "readme":    "https://raw.githubusercontent.com/anthropics/claude-code/main/README.md",
    "changelog": "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md",
    "llms_txt":  "https://code.claude.com/docs/llms.txt",
    "settings":  "https://code.claude.com/docs/en/settings",
    "hooks":     "https://code.claude.com/docs/en/hooks",
    "overview":  "https://code.claude.com/docs/en/overview",
}

MODEL_RE = re.compile(r'claude-(?:opus|sonnet|haiku)-[\w\.\-]+')
HOOK_RE = re.compile(
    r'\b(PreToolUse|PostToolUse|Stop|StopFailure|SessionStart|SessionEnd|'
    r'Notification|SubagentStop|UserPromptSubmit|UserPromptExpansion|'
    r'PermissionRequest|PermissionDenied|PostToolUseFailure|Setup)\b'
)
SETTINGS_KEY_RE = re.compile(
    r'`?(permissions|hooks|model|apiKeyHelper|env|cleanupPeriodDays|'
    r'autoUpdaterStatus|allowedTools|disabledTools|includeCoAuthoredBy|'
    r'preferredNotifChannel|parallelTasksCount|spinnerTipsEnabled|'
    r'theme|verbose|forceLoginOrgUUID|forceLoginMethod)`?'
)


# ── HTTP ──────────────────────────────────────────────────────────────────────

def fetch(url, timeout=30):
    req = Request(url, headers={
        "User-Agent": "curl/8.5.0",
        "Accept": "text/html,application/json,text/plain,*/*",
    })
    try:
        with urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace")
    except URLError as e:
        print(f"  [warn] {url}: {e}", file=sys.stderr)
        return None


# ── HTML → text ───────────────────────────────────────────────────────────────

class TextExtractor(HTMLParser):
    """code.claude.com の mdx-content ブロックだけを抽出する。"""
    SKIP = {"script", "style", "nav", "footer", "head", "svg", "button"}
    CONTENT_CLASS = "mdx-content"

    def __init__(self, target_class=None):
        super().__init__()
        self._skip_depth = 0
        self._in_target = target_class is None  # None なら全体
        self._target_class = target_class
        self._target_depth = 0
        self._depth = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        self._depth += 1
        attr_dict = dict(attrs)
        cls = attr_dict.get("class", "")
        if self._target_class and self._target_class in cls:
            self._in_target = True
            self._target_depth = self._depth
        if tag in self.SKIP:
            self._skip_depth += 1

    def handle_endtag(self, tag):
        if self._target_class and self._in_target and self._depth == self._target_depth:
            self._in_target = False
        self._depth -= 1
        if tag in self.SKIP:
            self._skip_depth = max(0, self._skip_depth - 1)
        if tag in ("p", "h1", "h2", "h3", "h4", "li", "tr", "br", "td", "th"):
            self.parts.append("\n")

    def handle_data(self, data):
        if self._in_target and self._skip_depth == 0 and data.strip():
            self.parts.append(data.strip())

    def get_text(self):
        return " ".join(self.parts)


def html_to_text(html, target_class="mdx-content"):
    p = TextExtractor(target_class=target_class)
    p.feed(html)
    text = p.get_text()
    # ターゲット抽出で短すぎる場合は全体抽出にフォールバック
    if len(text) < 200:
        p2 = TextExtractor(target_class=None)
        p2.feed(html)
        return p2.get_text()
    return text


# ── 個別取得 ──────────────────────────────────────────────────────────────────

def fetch_npm():
    raw = fetch(SOURCES["npm"])
    if not raw:
        return {}
    try:
        d = json.loads(raw)
        return {
            "version": d.get("version", ""),
            "description": d.get("description", ""),
        }
    except Exception:
        return {}


def fetch_changelog(lines=120):
    raw = fetch(SOURCES["changelog"])
    if not raw:
        return ""
    # 最新 4 リリース分だけ返す
    result, count = [], 0
    for line in raw.splitlines():
        if line.startswith("## "):
            count += 1
            if count > 4:
                break
        result.append(line)
    return "\n".join(result)


def fetch_readme():
    raw = fetch(SOURCES["readme"])
    return raw or ""


def fetch_doc(key):
    raw = fetch(SOURCES[key])
    if not raw:
        return ""
    return html_to_text(raw)


# ── 情報抽出 ──────────────────────────────────────────────────────────────────

def find_models(*texts):
    found = set()
    for t in texts:
        found.update(MODEL_RE.findall(t))
    return sorted(found)


def find_hooks(*texts):
    found = set()
    for t in texts:
        found.update(HOOK_RE.findall(t))
    return sorted(found)


def find_settings_keys(*texts):
    found = set()
    for t in texts:
        found.update(SETTINGS_KEY_RE.findall(t))
    return sorted(found)


def extract_section(text, heading, max_chars=1200):
    """code.claude.com テキストから見出し以降のセクションを抽出。"""
    heading_lower = heading.lower()
    idx = text.lower().find(heading_lower)
    if idx == -1:
        return ""
    chunk = text[idx: idx + max_chars]
    # 次のセクション見出し風のテキストで切る
    for sep in ["\n \n", "  \n"]:
        p = chunk.find(sep, len(heading) + 10)
        if p != -1:
            chunk = chunk[:p]
    return chunk.strip()


# ── タイムスタンプ管理 ────────────────────────────────────────────────────────

def should_sync(force):
    if force:
        return True
    if not CACHE_FILE.exists():
        return True
    try:
        last = datetime.fromisoformat(CACHE_FILE.read_text().strip())
        return datetime.now() - last > timedelta(hours=SYNC_INTERVAL_HOURS)
    except Exception:
        return True


# ── レポート生成 ──────────────────────────────────────────────────────────────

def load_current_settings():
    try:
        return json.loads(SETTINGS_FILE.read_text())
    except Exception:
        return {}


def build_report(npm, changelog, models, hooks, settings_keys,
                 settings_doc, hooks_doc, llms_txt, current_settings):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    v = npm.get("version", "(不明)")

    lines = [
        "# Claude Code 最新設定リファレンス",
        f"_自動同期: {ts}_  |  _CLI バージョン: v{v}_",
        "",
        "---",
        "",
    ]

    # モデル ID
    lines += ["## 最新モデル ID", ""]
    if models:
        lines += [f"- `{m}`" for m in models]
    else:
        lines += [
            "- `claude-opus-4-7`           — Opus 4.7 (最高性能)",
            "- `claude-sonnet-4-6`          — Sonnet 4.6 (バランス)",
            "- `claude-haiku-4-5-20251001`  — Haiku 4.5 (高速)",
            "",
            "> _抽出失敗時のフォールバック (システムプロンプト参照値)_",
        ]
    lines.append("")

    # フックイベント
    lines += ["## フックイベント", ""]
    if hooks:
        lines += [f"- `{h}`" for h in hooks]
    else:
        lines += [f"- `{h}`" for h in
                  ["PreToolUse", "PostToolUse", "Stop", "SessionStart",
                   "Notification", "SubagentStop"]]
    lines.append("")

    # settings.json キー
    lines += ["## settings.json キー", ""]
    if settings_keys:
        lines += [f"- `{k}`" for k in settings_keys]
    lines.append("")

    # 公式ドキュメント抜粋 (settings)
    if settings_doc:
        excerpt = settings_doc[:2500].strip()
        lines += [
            "## 公式ドキュメント抜粋: Settings",
            "",
            "```",
            excerpt,
            "```",
            "",
        ]

    # 公式ドキュメント抜粋 (hooks)
    if hooks_doc:
        excerpt = hooks_doc[:2500].strip()
        lines += [
            "## 公式ドキュメント抜粋: Hooks",
            "",
            "```",
            excerpt,
            "```",
            "",
        ]

    # llms.txt (ドキュメントインデックス)
    if llms_txt:
        lines += [
            "## 公式ドキュメントページ一覧 (llms.txt より抜粋)",
            "",
            "```",
            llms_txt[:2000].strip(),
            "```",
            "",
        ]

    # CHANGELOG
    if changelog:
        lines += [
            "## CHANGELOG (最新 4 リリース)",
            "",
            changelog,
            "",
        ]

    # 現在の settings.json
    lines += [
        "## 現在の .claude/settings.json",
        "",
        "```json",
        json.dumps(current_settings, ensure_ascii=False, indent=2),
        "```",
        "",
        "## 取得元",
    ]
    lines += [f"- {url}" for url in SOURCES.values()]
    lines.append("")

    return "\n".join(lines)


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    force = "--force" in sys.argv

    if not should_sync(force):
        print("Sync skipped: 最終同期から24時間未満。--force で強制実行。")
        return 0

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Claude Code 設定を同期中...")

    DOCS_DIR.mkdir(exist_ok=True)

    print("  npm バージョン取得...")
    npm = fetch_npm()
    print(f"  → v{npm.get('version', '不明')}")

    print("  CHANGELOG 取得...")
    changelog = fetch_changelog()

    print("  README 取得...")
    readme = fetch_readme()

    print("  ドキュメントインデックス (llms.txt) 取得...")
    llms_txt = fetch(SOURCES["llms_txt"]) or ""
    if llms_txt:
        print(f"  → {len(llms_txt.splitlines())} 行")

    print("  Settings ドキュメント取得...")
    settings_doc = fetch_doc("settings")

    print("  Hooks ドキュメント取得...")
    hooks_doc = fetch_doc("hooks")

    all_texts = [changelog, readme, settings_doc, hooks_doc, llms_txt]
    models = find_models(*all_texts)
    hooks = find_hooks(*all_texts)
    settings_keys = find_settings_keys(*all_texts)

    print(f"  モデル: {models}")
    print(f"  フック: {hooks}")
    print(f"  設定キー: {settings_keys}")

    current_settings = load_current_settings()
    report = build_report(
        npm, changelog, models, hooks, settings_keys,
        settings_doc, hooks_doc, llms_txt, current_settings,
    )

    OUTPUT_FILE.write_text(report, encoding="utf-8")
    print(f"  出力: {OUTPUT_FILE.relative_to(REPO_ROOT)}")

    CACHE_FILE.write_text(datetime.now().isoformat(), encoding="utf-8")
    print("同期完了。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
