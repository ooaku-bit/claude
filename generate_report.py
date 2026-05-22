#!/usr/bin/env python3
"""Claude Code 環境構成レポート — 完全版"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ─── フォント ────────────────────────────────────────────────────────
pdfmetrics.registerFont(TTFont("JP", "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"))
F = "JP"

W, H = A4
ML = MR = 15 * mm
MT = 14 * mm
MB = 18 * mm
CW = W - ML - MR

# ─── カラー ──────────────────────────────────────────────────────────
NAVY   = colors.HexColor("#0d1b3e")
BLUE   = colors.HexColor("#1e40af")
MBLUE  = colors.HexColor("#3b82f6")
LBLUE  = colors.HexColor("#eff6ff")
DBLUE  = colors.HexColor("#dbeafe")
TEAL   = colors.HexColor("#0f766e")
LTEAL  = colors.HexColor("#f0fdfa")
GREEN  = colors.HexColor("#166534")
LGREEN = colors.HexColor("#f0fdf4")
DGREEN = colors.HexColor("#bbf7d0")
PURPLE = colors.HexColor("#6b21a8")
LPURP  = colors.HexColor("#faf5ff")
DPURP  = colors.HexColor("#e9d5ff")
AMBER  = colors.HexColor("#92400e")
LAMBER = colors.HexColor("#fffbeb")
DAMBER = colors.HexColor("#fde68a")
RED    = colors.HexColor("#991b1b")
LRED   = colors.HexColor("#fef2f2")
GRAY   = colors.HexColor("#4b5563")
LGRAY  = colors.HexColor("#f9fafb")
MGRAY  = colors.HexColor("#e5e7eb")
DGRAY  = colors.HexColor("#9ca3af")
BLACK  = colors.HexColor("#111827")
WHITE  = colors.white

# ─── スタイルファクトリ ──────────────────────────────────────────────
def S(name, sz, color=BLACK, align=TA_LEFT, sa=3, ld=None):
    return ParagraphStyle(name, fontName=F, fontSize=sz, textColor=color,
                          alignment=align, spaceAfter=sa,
                          leading=ld or round(sz * 1.65))

sCV   = S("cv",  22, WHITE,  TA_CENTER, sa=5, ld=28)
sCVs  = S("cvs", 11, colors.HexColor("#93c5fd"), TA_CENTER, sa=3)
sCVm  = S("cvm",  8, colors.HexColor("#94a3b8"), TA_CENTER, sa=2)
sH2   = S("h2",  13, WHITE,  TA_LEFT,   sa=0, ld=19)
sH3   = S("h3",  10, NAVY,   TA_LEFT,   sa=2, ld=16)
sBody = S("bd",   9, BLACK,  TA_LEFT,   sa=2, ld=15)
sCode = S("cd",   8, colors.HexColor("#1e3a5f"), sa=1, ld=13)
sSm   = S("sm",   7, GRAY,   sa=1, ld=12)
sFt   = S("ft",   7, DGRAY,  TA_CENTER, sa=0, ld=11)
sTH   = S("th",   9, WHITE,  sa=0, ld=14)
sTD   = S("td",   9, BLACK,  sa=0, ld=14)
sBdg  = S("bg",   8, WHITE,  TA_CENTER, sa=0, ld=13)

def p(t, s=sBody): return Paragraph(t, s)
def SP(n=6):       return Spacer(1, n)
def HR(c=MGRAY):   return HRFlowable(width="100%", thickness=0.4, color=c)

# ─── 章ヘッダー ──────────────────────────────────────────────────────
def chap(num, title, accent=BLUE):
    row = [[
        p(str(num), S("cn", 14, WHITE, TA_CENTER, sa=0, ld=18)),
        p(f"<b>{title}</b>", sH2)
    ]]
    t = Table(row, colWidths=[11*mm, CW - 11*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(0,-1), MBLUE),
        ("BACKGROUND",    (1,0),(1,-1), accent),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0),(-1,-1), 8),
        ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ("LEFTPADDING",   (0,0),(0,-1),  3),
        ("LEFTPADDING",   (1,0),(1,-1), 12),
        ("RIGHTPADDING",  (0,0),(-1,-1),  8),
    ]))
    return t

# ─── サブヘッダー ────────────────────────────────────────────────────
def sub(title, bg=LBLUE, bar=BLUE):
    t = Table([[p(f"<b>{title}</b>", sH3)]], colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), bg),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("LINEBELOW",     (0,0),(-1,-1), 2, bar),
    ]))
    return t

# ─── KVテーブル ──────────────────────────────────────────────────────
def kv(rows, c1=48*mm, s1=WHITE, s2=LGRAY, key_color=BLACK):
    c2 = CW - c1
    ks = S("kk", 9, key_color, sa=0, ld=15)
    data = [[p(f"<b>{k}</b>", ks), p(v, sBody)] for k, v in rows]
    t = Table(data, colWidths=[c1, c2])
    t.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0,0),(-1,-1), [s1, s2]),
        ("GRID",           (0,0),(-1,-1), 0.3, MGRAY),
        ("LEFTPADDING",    (0,0),(-1,-1), 9),
        ("RIGHTPADDING",   (0,0),(-1,-1), 9),
        ("TOPPADDING",     (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",  (0,0),(-1,-1), 5),
        ("VALIGN",         (0,0),(-1,-1), "TOP"),
    ]))
    return t

# ─── データテーブル ──────────────────────────────────────────────────
def tbl(headers, rows, widths):
    hrow = [p(f"<b>{h}</b>", sTH) for h in headers]
    drows = [[p(c, sTD) for c in r] for r in rows]
    t = Table([hrow] + drows, colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  NAVY),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, LGRAY]),
        ("GRID",          (0,0),(-1,-1), 0.3, MGRAY),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("RIGHTPADDING",  (0,0),(-1,-1), 8),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ]))
    return t

# ─── コードブロック ──────────────────────────────────────────────────
def code(lines):
    data = [[p(ln, sCode)] for ln in lines]
    t = Table(data, colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), colors.HexColor("#f1f5f9")),
        ("BOX",          (0,0),(-1,-1), 0.5, MGRAY),
        ("LEFTPADDING",  (0,0),(-1,-1), 12),
        ("RIGHTPADDING", (0,0),(-1,-1), 12),
        ("TOPPADDING",   (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
    ]))
    return t

# ─── バッジ ──────────────────────────────────────────────────────────
def badge(items, bg=BLUE, fg=WHITE):
    s = S("bg2", 8, fg, TA_CENTER, sa=0, ld=13)
    cells = [p(item, s) for item in items]
    t = Table([cells], colWidths=[CW / len(items)] * len(items))
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), bg),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("INNERGRID",     (0,0),(-1,-1), 0.5, colors.HexColor("#ffffff30")),
    ]))
    return t

# ─── カードグリッド（2列） ────────────────────────────────────────────
def cards2(items):
    """items: [(title, body_lines), ...]  2列グリッド"""
    rows = []
    for i in range(0, len(items), 2):
        pair = items[i:i+2]
        cells = []
        for title, lines in pair:
            inner = [p(f"<b>{title}</b>", sH3)] + [p(f"  {ln}", sSm) for ln in lines]
            cell_tbl = Table([[inner]], colWidths=[(CW - 4*mm) / 2])
            cell_tbl.setStyle(TableStyle([
                ("BACKGROUND",    (0,0),(-1,-1), LGRAY),
                ("BOX",           (0,0),(-1,-1), 0.5, MGRAY),
                ("TOPPADDING",    (0,0),(-1,-1), 7),
                ("BOTTOMPADDING", (0,0),(-1,-1), 7),
                ("LEFTPADDING",   (0,0),(-1,-1), 8),
                ("RIGHTPADDING",  (0,0),(-1,-1), 8),
            ]))
            cells.append(cell_tbl)
        if len(cells) == 1:
            cells.append(p(""))
        rows.append(cells)
    t = Table(rows, colWidths=[(CW - 4*mm)/2, (CW - 4*mm)/2], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("VALIGN",       (0,0),(-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0),(-1,-1), 0),
        ("RIGHTPADDING", (0,0),(-1,-1), 4),
        ("TOPPADDING",   (0,0),(-1,-1), 0),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
    ]))
    return t

# ════════════════════════════════════════════════════════════════════
# ページ番号付きドキュメント
# ════════════════════════════════════════════════════════════════════
class Doc(SimpleDocTemplate):
    def afterPage(self):
        c = self.canv
        c.saveState()
        c.setFont(F, 7)
        c.setFillColor(DGRAY)
        pg = c.getPageNumber()
        c.drawCentredString(W/2, 9*mm,
            f"Claude Code 環境構成レポート  |  2026-05-22  |  ooaku-bit/claude  |  {pg}")
        c.restoreState()

# ════════════════════════════════════════════════════════════════════
story = []

# ══════════════════════════════════════════════════
# ▌ カバーページ
# ══════════════════════════════════════════════════
cover = Table([[
    p("Claude Code", sCV),
    SP(3),
    p("ワークスペース 環境構成レポート", sCVs),
    SP(4),
    p("Environment Configuration Report", S("ce", 9, colors.HexColor("#60a5fa"), TA_CENTER, sa=2)),
    SP(14),
    HR(colors.HexColor("#334155")),
    SP(12),
    p("リポジトリ :  ooaku-bit / claude", S("ci", 9, colors.HexColor("#cbd5e1"), TA_CENTER, sa=4)),
    p("作業ブランチ :  claude / quirky-newton-vlU0Z", S("ci2", 9, colors.HexColor("#cbd5e1"), TA_CENTER, sa=4)),
    p("作成日 :  2026 年 5 月 22 日", S("ci3", 9, colors.HexColor("#cbd5e1"), TA_CENTER, sa=4)),
    SP(12),
    HR(colors.HexColor("#334155")),
    SP(10),
    p("Claude Code on the Web  |  クラウド実行環境（Linux / ephemeral container）",
      S("ci4", 8, colors.HexColor("#64748b"), TA_CENTER, sa=2)),
]], colWidths=[CW])
cover.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,-1), NAVY),
    ("TOPPADDING",    (0,0),(-1,-1), 32),
    ("BOTTOMPADDING", (0,0),(-1,-1), 32),
    ("LEFTPADDING",   (0,0),(-1,-1), 24),
    ("RIGHTPADDING",  (0,0),(-1,-1), 24),
]))
story += [cover, SP(14)]

# 目次
toc_items = [
    ("1", "プロジェクト概要",           "リポジトリ情報・実行環境"),
    ("2", "ディレクトリ構成",           "全ファイル・フォルダのマップ"),
    ("3", "設定ファイル",               "settings.json（権限・フック）"),
    ("4", "エージェント構成",           "プロジェクト定義 + システムエージェント"),
    ("5", "カスタムコマンド",           "/deploy スラッシュコマンド"),
    ("6", "スキル構成",                 "プロジェクト定義 + システムスキル一覧"),
    ("7", "スクリプト",                 "Windows 自動同期スクリプト群"),
    ("8", "ワークフロールール",          "CLAUDE.md に定義された開発原則"),
    ("9", "Git 情報",                   "ブランチ・コミット履歴・除外設定"),
]
toc_rows = [
    [p(n, S("tn", 9, MBLUE, TA_CENTER, sa=0)),
     p(f"<b>{t}</b>", sBody),
     p(d, sSm)]
    for n, t, d in toc_items
]
toc_tbl = Table(toc_rows, colWidths=[10*mm, 60*mm, CW - 70*mm])
toc_tbl.setStyle(TableStyle([
    ("ROWBACKGROUNDS", (0,0),(-1,-1), [WHITE, LGRAY]),
    ("GRID",           (0,0),(-1,-1), 0.3, MGRAY),
    ("TOPPADDING",     (0,0),(-1,-1), 5),
    ("BOTTOMPADDING",  (0,0),(-1,-1), 5),
    ("LEFTPADDING",    (0,0),(-1,-1), 8),
    ("VALIGN",         (0,0),(-1,-1), "MIDDLE"),
]))
story += [p("<b>目次</b>", sH3), SP(4), toc_tbl, PageBreak()]

# ══════════════════════════════════════════════════
# ▌ 1. プロジェクト概要
# ══════════════════════════════════════════════════
story += [chap("1", "プロジェクト概要"), SP(8)]
story.append(kv([
    ("リポジトリ名",    "ooaku-bit / claude"),
    ("目的",           "Claude Code の自動化・運用ワークスペース。\n設定・スキル・エージェント・スクリプトを一元管理する。"),
    ("現在のブランチ", "claude / quirky-newton-vlU0Z（開発ブランチ）"),
    ("ベースブランチ", "master"),
    ("実行環境",       "Claude Code on the Web — Linux / ephemeral container（クラウド）"),
    ("リモート",       "GitHub（ローカルプロキシ 127.0.0.1:32817 経由）"),
    ("モデル",         "claude-sonnet-4-6"),
    ("作成日",        "2026 年 5 月 22 日"),
], c1=42*mm))
story.append(SP(14))

# ══════════════════════════════════════════════════
# ▌ 2. ディレクトリ構成
# ══════════════════════════════════════════════════
story += [chap("2", "ディレクトリ構成"), SP(8)]
story.append(code([
    "/home/user/claude/",
    "│",
    "├── CLAUDE.md                          ← プロジェクトルール・ガイドライン（最重要設定ファイル）",
    "├── README.md                          ← リポジトリ概要（1行）",
    "├── .gitignore                         ← Git 除外設定",
    "├── claude_code_environment_report.pdf ← 本レポート PDF",
    "├── generate_report.py                 ← PDF 生成スクリプト（Python / reportlab）",
    "│",
    "├── scripts/                           ← Windows 向け自動化スクリプト",
    "│   ├── auto-sync.ps1                  ← 15 分ごとに GitHub から git pull する同期スクリプト",
    "│   └── setup-task-scheduler.ps1       ← Windows タスクスケジューラへの自動登録スクリプト",
    "│",
    "└── .claude/                           ← Claude Code 設定ディレクトリ（全体追跡済み）",
    "    ├── settings.json                  ← 権限ルール・フック設定",
    "    │",
    "    ├── agents/                        ← カスタムエージェント定義",
    "    │   └── security-reviewer.md       ← OWASP準拠セキュリティレビューエージェント",
    "    │",
    "    ├── commands/                      ← スラッシュコマンド定義",
    "    │   └── deploy.md                  ← /deploy コマンド（7ステップデプロイチェックリスト）",
    "    │",
    "    ├── skills/                        ← プロジェクトスキル定義",
    "    │   ├── code-review/SKILL.md       ← コードレビュースキル",
    "    │   └── testing/SKILL.md           ← テスト作成・実行スキル",
    "    │",
    "    └── hooks/                         ← フックスクリプト（.gitignore 除外）",
    "        └── auto-push.sh              ← Stop フック：セッション終了時に自動 git push",
]))
story.append(SP(8))

story.append(sub("ファイル種別サマリー", bg=DBLUE, bar=BLUE))
story.append(SP(5))
story.append(tbl(
    ["ファイル種別", "件数", "ファイル名"],
    [
        ["Markdown (.md)", "5",  "CLAUDE.md / README.md / security-reviewer.md / deploy.md / SKILL.md ×2"],
        ["JSON (.json)",   "1",  ".claude/settings.json"],
        ["PowerShell (.ps1)", "2", "auto-sync.ps1 / setup-task-scheduler.ps1"],
        ["Python (.py)",   "1",  "generate_report.py"],
        ["PDF (.pdf)",     "1",  "claude_code_environment_report.pdf"],
        ["Shell (.sh)",    "1",  ".claude/hooks/auto-push.sh（gitignore 除外）"],
    ],
    [30*mm, 14*mm, CW - 44*mm]
))
story.append(SP(14))

# ══════════════════════════════════════════════════
# ▌ 3. 設定ファイル（settings.json）
# ══════════════════════════════════════════════════
story += [chap("3", "設定ファイル（.claude/settings.json）"), SP(8)]

story.append(sub("許可ルール  permissions.allow", bg=LGREEN, bar=GREEN))
story.append(SP(5))
story.append(badge(["Read:*", "Bash:git:*", "Write:*", "Edit:*"], bg=GREEN))
story.append(SP(5))
story.append(kv([
    ("Read:*",      "ワークスペース内の全ファイルの読み取りを許可"),
    ("Bash:git:*",  "git コマンドのみ Bash 実行を許可（他のコマンドは都度承認が必要）"),
    ("Write:*",     "全ファイルへの新規書き込みを許可"),
    ("Edit:*",      "全ファイルの差分編集を許可"),
], c1=36*mm, s1=LGREEN, s2=WHITE))
story.append(SP(10))

story.append(sub("拒否ルール  permissions.deny", bg=LRED, bar=RED))
story.append(SP(5))
story.append(badge(["Read:.env*", "Bash:sudo:*", "Bash:rm -rf /"], bg=RED))
story.append(SP(5))
story.append(kv([
    ("Read:.env*",    "環境変数ファイル（.env .env.local など）の読み取りを強制禁止"),
    ("Bash:sudo:*",   "管理者権限コマンドの実行を全面禁止"),
    ("Bash:rm -rf /", "ルートディレクトリの再帰削除コマンドを禁止（誤操作防止）"),
], c1=36*mm, s1=LRED, s2=WHITE))
story.append(SP(10))

story.append(sub("フック設定  hooks.Stop", bg=LAMBER, bar=AMBER))
story.append(SP(5))
story.append(kv([
    ("トリガー",     "Stop — Claude セッションが停止するたびに自動実行"),
    ("タイプ",       "command（シェルコマンドを直接実行）"),
    ("実行コマンド", "bash /home/user/claude/.claude/hooks/auto-push.sh"),
    ("タイムアウト", "30 秒（超過した場合は強制終了）"),
    ("目的",        "クラウド環境（ephemeral）はセッション終了でデータが消えるため、\n作業内容をリモートへ自動 push して保護する"),
], c1=40*mm, s1=LAMBER, s2=WHITE))
story.append(SP(14))

# ══════════════════════════════════════════════════
# ▌ 4. エージェント構成
# ══════════════════════════════════════════════════
story += [chap("4", "エージェント構成", accent=TEAL), SP(8)]

story.append(sub("4-1.  プロジェクト定義エージェント（.claude/agents/）", bg=LTEAL, bar=TEAL))
story.append(SP(5))
story.append(tbl(
    ["エージェント名", "定義ファイル", "説明"],
    [["security-reviewer",
      "agents/security-reviewer.md",
      "OWASP Top 10 を基準にコード変更のセキュリティ脆弱性を検出・報告する専門エージェント"]],
    [38*mm, 52*mm, CW - 90*mm]
))
story.append(SP(6))
story.append(kv([
    ("検査1: Injection",          "SQLi / コマンドインジェクション / XSS"),
    ("検査2: 認証・セッション管理", "ハードコード認証情報・弱いトークン・セッション固定"),
    ("検査3: 機密データ露出",      ".env / API キー / パスワード平文保存の検出"),
    ("検査4: アクセス制御",        "権限チェック漏れ・水平権限昇格・直接オブジェクト参照"),
    ("検査5: セキュリティ設定ミス", "デフォルト設定のまま運用・不要機能の有効化"),
    ("出力形式",                  "CRITICAL / HIGH / MEDIUM / LOW の重大度別で問題と修正提案を提示"),
], c1=50*mm))
story.append(SP(10))

story.append(sub("4-2.  システムエージェント（Claude Code 組み込み）", bg=DPURP, bar=PURPLE))
story.append(SP(5))
story.append(tbl(
    ["エージェント名", "用途・説明", "主なツール"],
    [
        ["claude\n（汎用）",
         "どのエージェントにも当てはまらないタスクを処理するデフォルトエージェント",
         "全ツール"],
        ["claude-code-guide",
         "Claude Code CLI の機能・API・SDK に関する質問に回答する専門エージェント",
         "Bash / Read / WebFetch / WebSearch"],
        ["Explore",
         "コードベースの高速検索エージェント。ファイル探索・シンボル検索・参照調査に特化",
         "Read / Bash（検索系）"],
        ["general-purpose",
         "複雑な調査・マルチステップタスクに対応する汎用エージェント",
         "全ツール"],
        ["Plan\n（設計）",
         "実装計画を設計するアーキテクト役エージェント。手順書・トレードオフ分析を出力",
         "Read / Bash（参照系）"],
        ["security-reviewer",
         "セキュリティレビュー専門エージェント（本プロジェクト定義）",
         "全ツール"],
        ["statusline-setup",
         "Claude Code のステータスライン表示設定を構成するエージェント",
         "Read / Edit"],
    ],
    [30*mm, 72*mm, CW - 102*mm]
))
story.append(SP(14))

# ══════════════════════════════════════════════════
# ▌ 5. カスタムコマンド
# ══════════════════════════════════════════════════
story += [chap("5", "カスタムコマンド（.claude/commands/）"), SP(8)]
story.append(kv([
    ("定義ファイル", ".claude/commands/deploy.md"),
    ("コマンド名",  "/deploy"),
    ("目的",       "デプロイ前のチェックリストを順番に実行し、安全にリモートへリリースする"),
], c1=36*mm))
story.append(SP(8))

story.append(sub("/deploy コマンド — 実行ステップ", bg=DBLUE, bar=BLUE))
story.append(SP(5))
story.append(tbl(
    ["No.", "ステップ名", "内容", "コマンド例"],
    [
        ["1", "テスト実行",     "全テストがパスすることを確認",
         "npm test"],
        ["2", "Lint チェック",  "コード品質と構文エラーをチェック",
         "npm run lint"],
        ["3", "機密情報スキャン","SECRET / API_KEY がコミットに含まれていないか検査",
         "git diff --name-only | xargs grep -l 'SECRET'"],
        ["4", "ブランチ確認",   "main または release/* ブランチ上であることを確認",
         "git branch --show-current"],
        ["5", "差分最終確認",   "git diff main で変更内容を人の目で最終チェック",
         "git diff main"],
        ["6", "タグ付け",       "日付ベースのバージョンタグを付与",
         "git tag -a vYYYYMMDD -m 'Release'"],
        ["7", "プッシュ",       "タグごとリモートへプッシュして完了",
         "git push -u origin HEAD --tags"],
    ],
    [9*mm, 28*mm, 50*mm, CW - 87*mm]
))
story.append(SP(14))

# ══════════════════════════════════════════════════
# ▌ 6. スキル構成
# ══════════════════════════════════════════════════
story += [chap("6", "スキル構成", accent=GREEN), SP(8)]

story.append(sub("6-1.  プロジェクト定義スキル（.claude/skills/）", bg=LGREEN, bar=GREEN))
story.append(SP(6))

# code-review
story.append(p("<b>code-review スキル</b>", sH3))
story.append(SP(3))
story.append(kv([
    ("定義ファイル",  ".claude/skills/code-review/SKILL.md"),
    ("説明",         "変更差分を分析し、バグ・セキュリティ・品質の問題を指摘するコードレビュースキル"),
    ("使用ツール",   "Read・Bash・Edit"),
    ("出力形式",     "[HIGH] / [MEDIUM] / [LOW] の重大度ラベルで問題箇所と修正提案を提示"),
], c1=38*mm))
story.append(SP(4))
story.append(tbl(
    ["観点", "チェック内容"],
    [
        ["正確性",       "バグ・ロジックエラー・エッジケースの見落とし"],
        ["セキュリティ", "インジェクション・認証不備・機密情報の誤コミット"],
        ["品質",        "命名・重複コード・不要な複雑性・可読性"],
        ["テスト",      "カバレッジ不足・エッジケース漏れ"],
    ],
    [28*mm, CW - 28*mm]
))
story.append(SP(10))

# testing
story.append(p("<b>testing スキル</b>", sH3))
story.append(SP(3))
story.append(kv([
    ("定義ファイル",  ".claude/skills/testing/SKILL.md"),
    ("説明",         "テストコードを作成・実行するスキル。describe + it + AAA パターンを採用"),
    ("使用ツール",   "Read・Bash・Edit・Write"),
    ("テスト構造",   "describe（テスト群）→ it（個別ケース）→ Arrange / Act / Assert の3段階"),
    ("カバー範囲",   "正常系（Happy Path）・異常系（Error Path）・境界値（Edge Cases）"),
], c1=38*mm))
story.append(SP(4))
story.append(code([
    "def test_機能名_条件_期待結果():",
    "    # Arrange（準備）",
    "    input_value = create_test_fixture()",
    "    mock_svc    = MockService(return_value=expected)",
    "    # Act（実行）",
    "    result = target_function(input_value, service=mock_svc)",
    "    # Assert（検証）",
    "    assert result == expected_value",
    "    assert mock_svc.was_called_once()",
]))
story.append(SP(10))

story.append(sub("6-2.  システムスキル（Claude Code 組み込み）", bg=DPURP, bar=PURPLE))
story.append(SP(6))
story.append(tbl(
    ["スキル名", "説明", "主なトリガー"],
    [
        ["session-start-hook",
         "Claude Code on the Web のスタートアップフックを設定する",
         "リポジトリのセットアップ時"],
        ["code-review",
         "変更差分を分析しバグ・セキュリティ・品質の問題を指摘。PRへのインラインコメントも可能",
         "「レビューして」「/code-review」"],
        ["testing",
         "describe + it + AAA パターンでテストを作成・実行する",
         "「テストして」「/testing」"],
        ["deploy",
         "デプロイ前チェックリストを実行して安全にリリースする",
         "「デプロイして」「/deploy」"],
        ["update-config",
         "settings.json を更新して自動化ビヘイビアやフック・権限を設定する",
         "「設定して」「from now on...」"],
        ["keybindings-help",
         "keybindings.json のカスタマイズ・ショートカットキーの変更を支援する",
         "「キーバインド変更」"],
        ["verify",
         "コード変更が実際に動作するかアプリを起動して動作確認する",
         "「動作確認して」「/verify」"],
        ["fewer-permission-prompts",
         "よく使うツール呼び出しを解析してallowlistを自動追加しプロンプト削減",
         "「/fewer-permission-prompts」"],
        ["loop",
         "スキルやプロンプトを定期間隔で繰り返し実行する（例: 5分ごとに /foo）",
         "「/loop 5m /foo」"],
        ["claude-api",
         "Claude API / Anthropic SDK のビルド・デバッグ・最適化（プロンプトキャッシュ含む）",
         "anthropic ライブラリのインポート検出時"],
        ["run",
         "プロジェクトのアプリを起動して変更が実際に動作するか確認する",
         "「起動して」「/run」"],
        ["init",
         "CLAUDE.md を新規作成してコードベースのドキュメントを初期化する",
         "「/init」"],
        ["review",
         "プルリクエストをレビューする",
         "「PRレビューして」「/review」"],
        ["security-review",
         "現在のブランチの変更に対してセキュリティレビューを実行する",
         "「/security-review」"],
    ],
    [34*mm, 72*mm, CW - 106*mm]
))
story.append(SP(14))

# ══════════════════════════════════════════════════
# ▌ 7. スクリプト
# ══════════════════════════════════════════════════
story += [chap("7", "スクリプト（scripts/）", accent=AMBER), SP(8)]

story.append(sub("7-1.  auto-sync.ps1 — Windows 自動同期スクリプト", bg=LAMBER, bar=AMBER))
story.append(SP(5))
story.append(kv([
    ("ファイルパス",  "scripts/auto-sync.ps1"),
    ("目的",         "Windows PC 上の C:\\Claude を GitHub の master ブランチと自動同期する"),
    ("動作フロー",   "git fetch → ローカルと origin/master を比較 → 差分があれば git pull を実行"),
    ("ログ出力",     "scripts/sync.log にタイムスタンプ付きで全操作を記録"),
    ("対象ブランチ", "master（固定）"),
], c1=40*mm))
story.append(SP(10))

story.append(sub("7-2.  setup-task-scheduler.ps1 — タスクスケジューラ登録スクリプト", bg=LAMBER, bar=AMBER))
story.append(SP(5))
story.append(kv([
    ("ファイルパス",  "scripts/setup-task-scheduler.ps1"),
    ("目的",         "auto-sync.ps1 を Windows タスクスケジューラに登録し 15 分ごとに自動実行する"),
    ("実行権限",     "管理者権限（Run as Administrator）が必要"),
    ("タスク名",     "ClaudeAutoSync"),
    ("実行間隔",     "15 分ごと（$interval 変数で変更可能）"),
    ("実行条件",     "ネットワーク接続時のみ / 遅延スタート時も実行"),
    ("タイムアウト", "最大 2 分（-ExecutionTimeLimit）"),
], c1=40*mm))
story.append(SP(14))

# ══════════════════════════════════════════════════
# ▌ 8. ワークフロールール（CLAUDE.md）
# ══════════════════════════════════════════════════
story += [chap("8", "ワークフロールール（CLAUDE.md）"), SP(8)]

story.append(sub("8-1.  開発ワークフロー 6 原則", bg=DBLUE, bar=BLUE))
story.append(SP(5))
story.append(tbl(
    ["原則", "ルール", "目的・補足"],
    [
        ["1", "Plan Mode を使う",
         "調査フェーズと実装フェーズを明確に分離する。いきなりコードを書かない。"],
        ["2", "小さく実装・すぐ検証",
         "小さく作る → 動作確認 → 改善のサイクルを繰り返す。一度に大きく変えない。"],
        ["3", "Todo リストで進捗管理",
         "優先順位と進捗を常に可視化する。作業前にタスクを列挙し完了から消していく。"],
        ["4", "Commit は頻繁に",
         "1 タスク完了ごとにすぐコミットする。複数タスクをまとめてコミットしない。"],
        ["5", "ブランチ戦略",
         "main（本番）/ feature/*（機能）/ spike/*（実験）を目的に応じて使い分ける。"],
        ["6", "/compact を定期的に",
         "コンテキストが圧迫されたら /compact で圧縮する。\n※ 実行前に重要情報を CLAUDE.md へ退避すること（取消不可）。"],
    ],
    [9*mm, 38*mm, CW - 47*mm]
))
story.append(SP(10))

story.append(sub("8-2.  コンテキスト管理", bg=DBLUE, bar=BLUE))
story.append(SP(5))
story.append(kv([
    ("CLAUDE.md を活用",    "重要情報・ルール・約束事はすべて CLAUDE.md に記録する"),
    ("ローカルコンテキスト", "サブフォルダには .claude/ や CLAUDE.md を追加してスコープを分ける"),
    ("ファイルサイズ制限",  "各ファイルは 200 行未満に保つ（可読性・管理コスト低減）"),
    ("/compact の注意",     "実行すると取消不可。重要情報を先に CLAUDE.md へ退避してから実行する"),
], c1=44*mm))
story.append(SP(10))

story.append(sub("8-3.  セキュリティポリシー", bg=LRED, bar=RED))
story.append(SP(5))
story.append(kv([
    (".env・認証情報",  "絶対にコミットしない。.gitignore と deny ルールで二重防止。"),
    ("外部副作用",      "DB 操作・外部 API 呼び出しは必ずユーザー確認を取ってから実行する。"),
    ("sudo コマンド",   "settings.json の deny ルールで強制禁止。"),
], c1=40*mm, s1=LRED, s2=WHITE))
story.append(SP(14))

# ══════════════════════════════════════════════════
# ▌ 9. Git 情報
# ══════════════════════════════════════════════════
story += [chap("9", "Git 情報"), SP(8)]

story.append(sub("9-1.  ブランチ構成", bg=DBLUE, bar=BLUE))
story.append(SP(5))
story.append(tbl(
    ["ブランチ名", "種別", "説明"],
    [
        ["master",
         "本番ブランチ",
         "安定した動作確認済みのコードを格納する。直接コミットは原則禁止。"],
        ["claude/quirky-newton-vlU0Z",
         "開発ブランチ（現在）",
         "現在の作業ブランチ。完了後 master へマージする。"],
    ],
    [54*mm, 28*mm, CW - 82*mm]
))
story.append(SP(10))

story.append(sub("9-2.  コミット履歴（全 10 件）", bg=DBLUE, bar=BLUE))
story.append(SP(5))
story.append(tbl(
    ["ハッシュ", "ブランチ", "コミットメッセージ"],
    [
        ["bab9c4c", "claude/quirky-...", "Rebuild full Japanese environment report PDF with detailed sections"],
        ["9b918db", "claude/quirky-...", "Update report PDF with Japanese font (IPAGothic) for proper rendering"],
        ["a3e2c86", "claude/quirky-...", "Add Claude Code environment report PDF and generation script"],
        ["69ae13f", "claude/quirky-...", "Fix PowerShell encoding: replace Japanese with English"],
        ["b4fe020", "claude/quirky-...", "Fix emoji encoding error in setup-task-scheduler.ps1"],
        ["69ca2bd", "claude/quirky-...", "Add Task Scheduler setup script for auto-sync"],
        ["71cfe7b", "master",           "Add auto-sync: Stop hook + Windows PowerShell sync script"],
        ["e3cf942", "master",           "Track .claude/ config files for GitHub-local sync"],
        ["1323d56", "master",           "Add CLAUDE.md with workspace rules and workflow guidelines"],
        ["8559dad", "master",           "Initial commit"],
    ],
    [22*mm, 30*mm, CW - 52*mm]
))
story.append(SP(10))

story.append(sub("9-3.  .gitignore 設定", bg=LGRAY, bar=GRAY))
story.append(SP(5))
story.append(code([
    ".claude/settings.local.json   ← ローカル専用設定（個人の環境差異を含むため除外）",
    ".claude/hooks/                 ← フックスクリプト（環境依存パスを含むため除外）",
]))
story.append(SP(14))

# ─── フッター ────────────────────────────────────────────────────────
story.append(HR())
story.append(SP(4))
story.append(p("本レポートは Claude Code により自動生成されました  |  2026-05-22  |  ooaku-bit/claude", sFt))

# ════════════════════════════════════════════════════════════════════
OUT = "/home/user/claude/claude_code_environment_report.pdf"
doc = Doc(
    OUT, pagesize=A4,
    leftMargin=ML, rightMargin=MR,
    topMargin=MT, bottomMargin=MB,
    title="Claude Code 環境構成レポート",
    author="Claude Code",
    subject="ooaku-bit/claude ワークスペース環境構成",
)
doc.build(story)
print(f"PDF 生成完了: {OUT}")
