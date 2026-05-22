#!/usr/bin/env python3
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os, glob

# ---- フォント ----
FONT_DIR = "/usr/share/fonts/truetype/noto"
font_paths = glob.glob(f"{FONT_DIR}/NotoSansCJK*.ttc") + \
             glob.glob("/usr/share/fonts/**/*CJK*.ttf", recursive=True) + \
             glob.glob("/usr/share/fonts/**/*Gothic*.ttf", recursive=True)

USE_CJK = False
if font_paths:
    try:
        pdfmetrics.registerFont(TTFont("NotoSans", font_paths[0]))
        BASE_FONT = "NotoSans"
        USE_CJK = True
    except Exception:
        BASE_FONT = "Helvetica"
else:
    BASE_FONT = "Helvetica"

W, H = A4
MARGIN = 18 * mm

# ---- スタイル ----
BRAND   = colors.HexColor("#1a1a2e")
ACCENT  = colors.HexColor("#4f8ef7")
ACCENT2 = colors.HexColor("#22c55e")
BG_LIGHT= colors.HexColor("#f0f4ff")
BG_DARK = colors.HexColor("#e8f5e9")
GRAY    = colors.HexColor("#64748b")
WHITE   = colors.white

def style(name, **kw):
    s = ParagraphStyle(name, fontName=BASE_FONT, **kw)
    return s

H1  = style("H1",  fontSize=22, textColor=WHITE,  spaceAfter=4,  leading=28, alignment=TA_CENTER)
H2  = style("H2",  fontSize=14, textColor=ACCENT,  spaceAfter=4,  leading=20, spaceBefore=10)
H3  = style("H3",  fontSize=11, textColor=BRAND,   spaceAfter=2,  leading=16, spaceBefore=6)
BODY= style("BODY",fontSize=9,  textColor=colors.HexColor("#1e293b"), spaceAfter=3, leading=14)
MONO= style("MONO",fontSize=8,  textColor=colors.HexColor("#334155"), spaceAfter=2, leading=12,
            backColor=colors.HexColor("#f8fafc"))
SMALL=style("SMALL",fontSize=7.5,textColor=GRAY, leading=12)
META= style("META", fontSize=8,  textColor=GRAY,  alignment=TA_CENTER, leading=12)

def p(text, st=BODY):
    return Paragraph(text, st)

def bullet(items, st=BODY):
    return [Paragraph(f"&#x25cf;&nbsp;&nbsp;{i}", st) for i in items]

def code_block(lines):
    rows = [[Paragraph(ln, MONO)] for ln in lines]
    t = Table(rows, colWidths=[W - 2*MARGIN])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ("BOX",        (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ("LEFTPADDING", (0,0),(-1,-1), 8),
        ("RIGHTPADDING",(0,0),(-1,-1), 8),
        ("TOPPADDING",  (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1),4),
    ]))
    return t

def section_header(title, color=ACCENT):
    tbl = Table([[Paragraph(title, H2)]], colWidths=[W - 2*MARGIN])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,-1), BG_LIGHT),
        ("LEFTPADDING",(0,0),(-1,-1), 10),
        ("TOPPADDING", (0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LINEBELOW", (0,0),(-1,-1), 2, ACCENT),
    ]))
    return tbl

def kv_table(rows, col1=60*mm, col2=None):
    if col2 is None:
        col2 = W - 2*MARGIN - col1
    data = [[Paragraph(f"<b>{k}</b>", BODY), Paragraph(v, BODY)] for k,v in rows]
    t = Table(data, colWidths=[col1, col2])
    t.setStyle(TableStyle([
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[colors.white, BG_LIGHT]),
        ("GRID",(0,0),(-1,-1),0.3,colors.HexColor("#e2e8f0")),
        ("LEFTPADDING",(0,0),(-1,-1),8),
        ("RIGHTPADDING",(0,0),(-1,-1),8),
        ("TOPPADDING",(0,0),(-1,-1),4),
        ("BOTTOMPADDING",(0,0),(-1,-1),4),
    ]))
    return t

def badge_table(items, bg=ACCENT, fg=WHITE):
    """横並びバッジ"""
    cells = [Paragraph(f"<b>{i}</b>", style("badge", fontSize=8, textColor=fg)) for i in items]
    t = Table([cells], colWidths=[(W-2*MARGIN)/len(items)]*len(items))
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), bg),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("TOPPADDING",(0,0),(-1,-1),5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("ROUNDEDCORNERS",(0,0),(-1,-1),4),
    ]))
    return t

# ====================================================================
story = []

# ---- カバー ----
cover_bg = Table(
    [[Paragraph("Claude Code Workspace", H1),
      Spacer(1, 6),
      Paragraph("Environment Configuration Report", style("sub", fontSize=13, textColor=colors.HexColor("#93c5fd"), alignment=TA_CENTER)),
      Spacer(1, 4),
      Paragraph("2026-05-22  |  ooaku-bit/claude", META)]],
    colWidths=[W - 2*MARGIN]
)
cover_bg.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1), BRAND),
    ("TOPPADDING",(0,0),(-1,-1),28),
    ("BOTTOMPADDING",(0,0),(-1,-1),28),
    ("LEFTPADDING",(0,0),(-1,-1),20),
    ("RIGHTPADDING",(0,0),(-1,-1),20),
    ("ROUNDEDCORNERS",(0,0),(-1,-1),8),
]))
story.append(cover_bg)
story.append(Spacer(1, 12))

# ---- 1. プロジェクト概要 ----
story.append(section_header("1. プロジェクト概要"))
story.append(Spacer(1,4))
story.append(kv_table([
    ("リポジトリ",   "ooaku-bit/claude"),
    ("目的",        "Claude Code の自動化・運用ワークスペース"),
    ("作業ブランチ", "claude/quirky-newton-vlU0Z"),
    ("ベースブランチ","master"),
    ("リモート",    "GitHub (local proxy 経由)"),
    ("レポート日",   "2026-05-22"),
]))
story.append(Spacer(1,8))

# ---- 2. ディレクトリ構成 ----
story.append(section_header("2. ディレクトリ構成"))
story.append(Spacer(1,4))
story.append(code_block([
    "/home/user/claude/              # ワークスペースルート",
    "├── CLAUDE.md                   # プロジェクトルール・ガイドライン",
    "├── README.md                   # リポジトリ概要",
    "├── .gitignore                  # Git除外設定",
    "├── scripts/",
    "│   ├── auto-sync.ps1           # Windows 自動同期スクリプト",
    "│   └── setup-task-scheduler.ps1# タスクスケジューラ設定",
    "└── .claude/                    # Claude Code 設定ディレクトリ (gitignored一部)",
    "    ├── settings.json           # 権限・フック設定",
    "    ├── agents/",
    "    │   └── security-reviewer.md# セキュリティレビュー専門エージェント",
    "    ├── commands/",
    "    │   └── deploy.md           # /deploy カスタムコマンド",
    "    └── skills/",
    "        ├── code-review/SKILL.md # コードレビュースキル",
    "        └── testing/SKILL.md    # テストスキル",
]))
story.append(Spacer(1,8))

# ---- 3. settings.json ----
story.append(section_header("3. 権限・フック設定 (.claude/settings.json)"))
story.append(Spacer(1,6))

story.append(p("<b>3-1. 許可ルール (permissions.allow)</b>", H3))
story.append(badge_table(["Read:*", "Bash:git:*", "Write:*", "Edit:*"], bg=ACCENT2))
story.append(Spacer(1,4))

story.append(p("<b>3-2. 拒否ルール (permissions.deny)</b>", H3))
story.append(badge_table(["Read:.env*", "Bash:sudo:*", "Bash:rm -rf /:*"], bg=colors.HexColor("#ef4444")))
story.append(Spacer(1,6))

story.append(p("<b>3-3. フック (hooks)</b>", H3))
story.append(kv_table([
    ("トリガー",  "Stop（Claude が停止したとき）"),
    ("タイプ",    "command"),
    ("コマンド",  "bash /home/user/claude/.claude/hooks/auto-push.sh"),
    ("タイムアウト","30 秒"),
    ("説明",      "Claude セッション終了時に自動で git push を実行"),
], col1=40*mm))
story.append(Spacer(1,8))

# ---- 4. Agents ----
story.append(section_header("4. エージェント定義 (.claude/agents/)"))
story.append(Spacer(1,4))

agent_data = [
    [Paragraph("<b>ファイル</b>", BODY),
     Paragraph("<b>名前</b>", BODY),
     Paragraph("<b>説明</b>", BODY)],
    [Paragraph("security-reviewer.md", MONO),
     Paragraph("security-reviewer", BODY),
     Paragraph("OWASP Top 10 を基準にセキュリティ脆弱性を検出する専門エージェント", BODY)],
]
at = Table(agent_data, colWidths=[55*mm, 40*mm, W-2*MARGIN-95*mm])
at.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0), BRAND),
    ("TEXTCOLOR",(0,0),(-1,0), WHITE),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, BG_LIGHT]),
    ("GRID",(0,0),(-1,-1),0.3,colors.HexColor("#e2e8f0")),
    ("TOPPADDING",(0,0),(-1,-1),5),
    ("BOTTOMPADDING",(0,0),(-1,-1),5),
    ("LEFTPADDING",(0,0),(-1,-1),8),
]))
story.append(at)
story.append(Spacer(1,4))

story.append(p("<b>検査項目（OWASP Top 10 準拠）</b>", H3))
story.append(kv_table([
    ("1. Injection",       "SQLi / Command injection / XSS"),
    ("2. 認証・セッション",  "ハードコード認証情報・弱いトークン"),
    ("3. 機密データ露出",   ".env / API keys / パスワード平文保存"),
    ("4. アクセス制御",     "権限チェック漏れ・水平権限昇格"),
    ("5. セキュリティ設定", "デフォルト設定・不要な機能の有効化"),
], col1=50*mm))
story.append(Spacer(1,8))

# ---- 5. Commands ----
story.append(section_header("5. カスタムコマンド (.claude/commands/)"))
story.append(Spacer(1,4))

story.append(p("<b>/deploy コマンド</b>", H3))
deploy_steps = [
    "テスト実行 — 全テストがパスすることを確認",
    "Lint — コード品質チェック",
    "セキュリティ — 機密情報がコミットされていないか確認",
    "ブランチ確認 — main / release/* ブランチであることを確認",
    "変更差分確認 — git diff main で最終確認",
    "タグ付け — バージョンタグを付与",
    "プッシュ — リモートにプッシュ",
]
for i, s in enumerate(deploy_steps, 1):
    story.append(p(f"&nbsp;&nbsp;<b>{i}.</b>&nbsp;{s}"))
story.append(Spacer(1,8))

# ---- 6. Skills ----
story.append(section_header("6. スキル定義 (.claude/skills/)"))
story.append(Spacer(1,6))

# code-review
story.append(p("<b>6-1. code-review</b>", H3))
story.append(kv_table([
    ("説明", "変更差分を分析し、バグ・セキュリティ・品質の問題を指摘する"),
    ("使用ツール", "Read, Bash, Edit"),
], col1=35*mm))
story.append(Spacer(1,3))
review_points = [
    "正確性: バグ・ロジックエラー・エッジケース",
    "セキュリティ: インジェクション・認証・機密情報露出",
    "品質: 命名・重複・不要な複雑性",
    "テスト: カバレッジ・エッジケース",
]
for rp in review_points:
    story.append(p(f"&nbsp;&nbsp;&#x25cf;&nbsp;{rp}"))
story.append(Spacer(1,6))

# testing
story.append(p("<b>6-2. testing</b>", H3))
story.append(kv_table([
    ("説明", "テストを作成・実行する。describe + it + AAAパターンを使用"),
    ("使用ツール", "Read, Bash, Edit, Write"),
], col1=35*mm))
story.append(Spacer(1,3))
test_items = [
    "describe + it + AAA (Arrange / Act / Assert) パターン",
    "ファクトリーモックを使用",
    "エッジケースを必ずカバー（正常系・異常系・境界値）",
]
for ti in test_items:
    story.append(p(f"&nbsp;&nbsp;&#x25cf;&nbsp;{ti}"))
story.append(Spacer(1,8))

# ---- 7. ワークフロールール ----
story.append(section_header("7. ワークフロールール (CLAUDE.md)"))
story.append(Spacer(1,4))
rules = [
    ("Plan Mode を使う",    "調査と実装を明確に分離する"),
    ("小さく実装してすぐ検証", "小さく → 検証 → 改善を繰り返す"),
    ("Todoリストで管理",     "優先順位と進捗を常に明確に"),
    ("Commit 頻繁に",       "1タスクに集中し完了したらすぐコミット"),
    ("ブランチ戦略",         "main / feature/* / spike/* を使い分ける"),
    ("/compact を定期的に",  "コンテキストを圧縮して余白を確保"),
]
story.append(kv_table(rules, col1=55*mm))
story.append(Spacer(1,8))

# ---- 8. セキュリティポリシー ----
story.append(section_header("8. セキュリティポリシー"))
story.append(Spacer(1,4))
sec = [
    ".env / 認証情報は絶対にコミットしない",
    "外部副作用（DB操作・API呼び出し）は必ず確認してから実行",
    "sudo コマンドは原則禁止（settings.json の deny ルールで強制）",
    "Stop フック: セッション終了時に自動 push（auto-push.sh）",
]
for s in sec:
    story.append(p(f"&#x25cf;&nbsp;&nbsp;{s}"))
story.append(Spacer(1,8))

# ---- 9. Git 履歴サマリー ----
story.append(section_header("9. Git コミット履歴"))
story.append(Spacer(1,4))
commits = [
    ("69ae13f", "Fix PowerShell encoding: replace Japanese with English"),
    ("b4fe020", "Fix emoji encoding error in setup-task-scheduler.ps1"),
    ("69ca2bd", "Add Task Scheduler setup script for auto-sync"),
    ("71cfe7b", "Add auto-sync: Stop hook + Windows PowerShell sync script"),
    ("e3cf942", "Track .claude/ config files for GitHub-local sync"),
    ("1323d56", "Add CLAUDE.md with workspace rules and workflow guidelines"),
    ("8559dad", "Initial commit"),
]
commit_data = [[Paragraph("<b>Hash</b>",BODY), Paragraph("<b>Message</b>",BODY)]] + \
              [[Paragraph(h, MONO), Paragraph(m, BODY)] for h,m in commits]
ct = Table(commit_data, colWidths=[25*mm, W-2*MARGIN-25*mm])
ct.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0), BRAND),
    ("TEXTCOLOR",(0,0),(-1,0), WHITE),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, BG_LIGHT]),
    ("GRID",(0,0),(-1,-1),0.3,colors.HexColor("#e2e8f0")),
    ("TOPPADDING",(0,0),(-1,-1),4),
    ("BOTTOMPADDING",(0,0),(-1,-1),4),
    ("LEFTPADDING",(0,0),(-1,-1),8),
]))
story.append(ct)
story.append(Spacer(1,12))

# ---- フッター代わりのまとめ ----
story.append(HRFlowable(width="100%", thickness=1, color=ACCENT))
story.append(Spacer(1,4))
story.append(p("Generated by Claude Code  |  2026-05-22  |  ooaku-bit/claude", META))

# ---- PDF 生成 ----
OUT = "/home/user/claude/claude_code_environment_report.pdf"
doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=MARGIN, bottomMargin=MARGIN,
    title="Claude Code Environment Report",
    author="Claude Code",
)
doc.build(story)
print(f"PDF generated: {OUT}")
