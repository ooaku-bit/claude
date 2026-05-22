#!/usr/bin/env python3
"""Claude Code 環境構成レポート PDF 生成スクリプト"""
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

# ── フォント ──────────────────────────────────────────────────────────
pdfmetrics.registerFont(TTFont("JP", "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"))
F = "JP"

W, H = A4
ML = MR = 16 * mm
MT = MB = 14 * mm
CW = W - ML - MR

# ── カラーパレット ────────────────────────────────────────────────────
NAVY   = colors.HexColor("#0f2350")
BLUE   = colors.HexColor("#1d4ed8")
LBLUE  = colors.HexColor("#eff6ff")
DBLUE  = colors.HexColor("#bfdbfe")
TEAL   = colors.HexColor("#0d9488")
LTEAL  = colors.HexColor("#f0fdfa")
GREEN  = colors.HexColor("#15803d")
LGREEN = colors.HexColor("#f0fdf4")
AMBER  = colors.HexColor("#b45309")
LAMBER = colors.HexColor("#fffbeb")
RED    = colors.HexColor("#b91c1c")
LRED   = colors.HexColor("#fef2f2")
GRAY   = colors.HexColor("#475569")
LGRAY  = colors.HexColor("#f8fafc")
MGRAY  = colors.HexColor("#e2e8f0")
BLACK  = colors.HexColor("#0f172a")
WHITE  = colors.white

# ── スタイル ──────────────────────────────────────────────────────────
def st(name, size, color=BLACK, align=TA_LEFT, sa=3, leading=None, bold=False):
    return ParagraphStyle(name, fontName=F, fontSize=size, textColor=color,
                          alignment=align, spaceAfter=sa,
                          leading=leading or round(size * 1.65))

sCover   = st("cv",   22, WHITE,  TA_CENTER, sa=6, leading=30)
sCoverS  = st("cvs",  12, colors.HexColor("#93c5fd"), TA_CENTER, sa=4)
sMeta    = st("meta",  8, colors.HexColor("#94a3b8"), TA_CENTER, sa=2)
sChap    = st("chap", 14, WHITE,  TA_LEFT,   sa=0, leading=20)
sH3      = st("h3",   10, NAVY,   TA_LEFT,   sa=2, leading=16)
sBody    = st("body",  9, BLACK,  TA_LEFT,   sa=2, leading=15)
sCode    = st("code",  8, colors.HexColor("#1e3a5f"), TA_LEFT, sa=1, leading=13)
sSmall   = st("sm",    7, GRAY,   TA_LEFT,   sa=1, leading=12)
sFoot    = st("ft",    7, GRAY,   TA_CENTER, sa=0, leading=11)
sBadge   = st("bdg",   8, WHITE,  TA_CENTER, sa=0, leading=13)
sBadgeD  = st("bdgd",  8, BLACK,  TA_CENTER, sa=0, leading=13)
sLabel   = st("lbl",   8, GRAY,   TA_RIGHT,  sa=0, leading=13)
sNum     = st("num",  28, BLUE,   TA_CENTER, sa=0, leading=34)

def p(text, style=sBody): return Paragraph(text, style)

# ── 章ヘッダー ────────────────────────────────────────────────────────
def chapter(num, title, color=NAVY):
    inner = Table(
        [[p(f"<b>{num}</b>", st("cn", 13, WHITE, TA_CENTER, sa=0, leading=18)),
          p(f"<b>{title}</b>", sChap)]],
        colWidths=[12*mm, CW - 12*mm]
    )
    inner.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (0,-1), BLUE),
        ("BACKGROUND",    (1,0), (1,-1), color),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (0,-1),  4),
        ("LEFTPADDING",   (1,0), (1,-1), 12),
    ]))
    return inner

# ── サブヘッダー ──────────────────────────────────────────────────────
def subhead(title, bg=LBLUE, line=BLUE):
    t = Table([[p(f"<b>{title}</b>", sH3)]], colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), bg),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LINEBELOW",     (0,0), (-1,-1), 1.5, line),
    ]))
    return t

# ── KV テーブル ───────────────────────────────────────────────────────
def kv(rows, c1=50*mm, stripe1=WHITE, stripe2=LGRAY):
    c2 = CW - c1
    data = [[p(f"<b>{k}</b>", sBody), p(v, sBody)] for k, v in rows]
    t = Table(data, colWidths=[c1, c2])
    t.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [stripe1, stripe2]),
        ("GRID",           (0,0), (-1,-1), 0.3, MGRAY),
        ("LEFTPADDING",    (0,0), (-1,-1), 9),
        ("RIGHTPADDING",   (0,0), (-1,-1), 9),
        ("TOPPADDING",     (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",  (0,0), (-1,-1), 5),
        ("VALIGN",         (0,0), (-1,-1), "TOP"),
    ]))
    return t

# ── コードブロック ────────────────────────────────────────────────────
def codeblock(lines, bg=colors.HexColor("#f1f5f9")):
    data = [[p(ln, sCode)] for ln in lines]
    t = Table(data, colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), bg),
        ("BOX",           (0,0), (-1,-1), 0.5, MGRAY),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("RIGHTPADDING",  (0,0), (-1,-1), 12),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    return t

# ── バッジ列 ─────────────────────────────────────────────────────────
def badges(items, bg=BLUE, fg=WHITE, dark_text=False):
    s = sBadgeD if dark_text else sBadge
    cells = [p(item, s) for item in items]
    n = len(items)
    t = Table([cells], colWidths=[CW / n] * n)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), bg),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("INNERGRID",     (0,0), (-1,-1), 0.5, colors.HexColor("#ffffff40")),
        ("BOX",           (0,0), (-1,-1), 0, WHITE),
    ]))
    return t

# ── データテーブル（ヘッダー付き）────────────────────────────────────
def datatable(headers, rows, widths):
    hrow = [p(f"<b>{h}</b>", st("th", 9, WHITE, TA_LEFT, sa=0)) for h in headers]
    drows = []
    for i, row in enumerate(rows):
        bg = LGRAY if i % 2 else WHITE
        drows.append([p(cell, sBody) for cell in row])
    t = Table([hrow] + drows, colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  NAVY),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, LGRAY]),
        ("GRID",          (0,0), (-1,-1), 0.3, MGRAY),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]))
    return t

def SP(n=6): return Spacer(1, n)
def HR(): return HRFlowable(width="100%", thickness=0.5, color=MGRAY)

# ====================================================================
# ページ番号フッター
# ====================================================================
class NumberedDoc(SimpleDocTemplate):
    def handle_pageEnd(self):
        super().handle_pageEnd()

    def afterPage(self):
        canvas = self.canv
        canvas.saveState()
        canvas.setFont(F, 7)
        canvas.setFillColor(GRAY)
        pg = canvas.getPageNumber()
        canvas.drawCentredString(W / 2, 9 * mm,
            f"Claude Code 環境構成レポート  |  2026-05-22  |  ooaku-bit/claude  |  {pg} ページ")
        canvas.restoreState()

# ====================================================================
story = []

# ══════════════════════════════════════════════════════════════════════
# カバーページ
# ══════════════════════════════════════════════════════════════════════
cover = Table([[
    p("Claude Code", sCover),
    SP(4),
    p("ワークスペース 環境構成レポート", sCoverS),
    SP(6),
    p("Claude Code Workspace Environment Report", st("cve", 9, colors.HexColor("#60a5fa"), TA_CENTER, sa=2)),
    SP(10),
    HR(),
    SP(8),
    p("リポジトリ :  ooaku-bit / claude", st("ci", 9, colors.HexColor("#cbd5e1"), TA_CENTER, sa=3)),
    p("作業ブランチ :  claude/quirky-newton-vlU0Z", st("ci2", 9, colors.HexColor("#cbd5e1"), TA_CENTER, sa=3)),
    p("作成日 :  2026年5月22日", st("ci3", 9, colors.HexColor("#cbd5e1"), TA_CENTER, sa=3)),
]], colWidths=[CW])
cover.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), NAVY),
    ("TOPPADDING",    (0,0), (-1,-1), 36),
    ("BOTTOMPADDING", (0,0), (-1,-1), 36),
    ("LEFTPADDING",   (0,0), (-1,-1), 24),
    ("RIGHTPADDING",  (0,0), (-1,-1), 24),
]))
story += [cover, SP(12)]

# 目次的サマリー
toc_data = [
    ["1", "プロジェクト概要",         "リポジトリの目的・基本情報"],
    ["2", "ディレクトリ構成",         "全ファイル・フォルダの配置"],
    ["3", "設定ファイル（settings.json）", "権限ルール・フック設定"],
    ["4", "エージェント定義",         "security-reviewer エージェント"],
    ["5", "カスタムコマンド",         "/deploy コマンドの手順"],
    ["6", "スキル定義",               "code-review / testing スキル"],
    ["7", "スクリプト",               "Windows 自動同期スクリプト"],
    ["8", "ワークフロールール",        "CLAUDE.md に定義された開発ルール"],
    ["9", "Git 情報",                 "ブランチ・コミット履歴"],
]
toc_rows = [[p(n, st("tcn",9,BLUE,TA_CENTER,sa=0)), p(f"<b>{t}</b>"), p(d, sSmall)]
            for n,t,d in toc_data]
toc = Table(toc_rows, colWidths=[10*mm, 60*mm, CW-70*mm])
toc.setStyle(TableStyle([
    ("ROWBACKGROUNDS", (0,0),(-1,-1), [WHITE, LGRAY]),
    ("GRID",           (0,0),(-1,-1), 0.3, MGRAY),
    ("TOPPADDING",     (0,0),(-1,-1), 5),
    ("BOTTOMPADDING",  (0,0),(-1,-1), 5),
    ("LEFTPADDING",    (0,0),(-1,-1), 8),
    ("VALIGN",         (0,0),(-1,-1), "MIDDLE"),
]))
story += [p("<b>目次</b>", sH3), SP(4), toc, PageBreak()]

# ══════════════════════════════════════════════════════════════════════
# 1. プロジェクト概要
# ══════════════════════════════════════════════════════════════════════
story += [chapter("1", "プロジェクト概要"), SP(8)]
story.append(kv([
    ("リポジトリ名",    "ooaku-bit/claude"),
    ("目的・用途",      "Claude Code の自動化・運用ワークスペース。\n設定・スキル・エージェント・スクリプトを一元管理する。"),
    ("現在のブランチ",  "claude/quirky-newton-vlU0Z（開発用）"),
    ("ベースブランチ",  "master"),
    ("リモート URL",    "GitHub（ローカルプロキシ 127.0.0.1:32817 経由）"),
    ("リポジトリ種別",  "Git リポジトリ（クラウド実行環境にクローン済み）"),
    ("作成日",         "2026年5月22日"),
], c1=42*mm))
story.append(SP(14))

# ══════════════════════════════════════════════════════════════════════
# 2. ディレクトリ構成
# ══════════════════════════════════════════════════════════════════════
story += [chapter("2", "ディレクトリ構成"), SP(8)]
story.append(p("<b>ファイルツリー</b>（.git ディレクトリを除く全ファイル）", sH3))
story.append(SP(4))
story.append(codeblock([
    "/home/user/claude/",
    "├── CLAUDE.md                             ← プロジェクトルール・ガイドライン（最重要）",
    "├── README.md                             ← リポジトリ概要（1行）",
    "├── .gitignore                            ← Git 除外設定",
    "├── claude_code_environment_report.pdf    ← 本レポート PDF",
    "├── generate_report.py                    ← PDF 生成スクリプト（Python）",
    "├── scripts/",
    "│   ├── auto-sync.ps1                     ← Windows 自動同期 PowerShell スクリプト",
    "│   └── setup-task-scheduler.ps1          ← Windows タスクスケジューラ登録スクリプト",
    "└── .claude/                              ← Claude Code 設定ディレクトリ",
    "    ├── settings.json                     ← 権限・フック設定（gitignore 対象外・追跡済み）",
    "    ├── agents/",
    "    │   └── security-reviewer.md          ← セキュリティレビュー専用エージェント定義",
    "    ├── commands/",
    "    │   └── deploy.md                     ← /deploy スラッシュコマンド定義",
    "    ├── skills/",
    "    │   ├── code-review/SKILL.md           ← コードレビュースキル定義",
    "    │   └── testing/SKILL.md              ← テストスキル定義",
    "    └── hooks/                            ← フックスクリプト置き場（.gitignore 除外）",
    "        └── auto-push.sh                  ← Stop フックで自動実行される git push スクリプト",
]))
story.append(SP(8))

story.append(p("<b>ファイル種別サマリー</b>", sH3))
story.append(SP(4))
file_summary = [
    ["Markdown（.md）", "5 ファイル", "CLAUDE.md / README.md / agents / commands / skills"],
    ["JSON（.json）",   "1 ファイル", ".claude/settings.json（権限・フック設定）"],
    ["PowerShell（.ps1）","2 ファイル","auto-sync.ps1 / setup-task-scheduler.ps1"],
    ["Python（.py）",   "1 ファイル", "generate_report.py（PDF 生成）"],
    ["PDF（.pdf）",     "1 ファイル", "claude_code_environment_report.pdf"],
]
story.append(datatable(
    ["ファイル種別", "件数", "内容"],
    file_summary,
    [38*mm, 20*mm, CW-58*mm]
))
story.append(SP(14))

# ══════════════════════════════════════════════════════════════════════
# 3. settings.json
# ══════════════════════════════════════════════════════════════════════
story += [chapter("3", "設定ファイル（.claude/settings.json）"), SP(8)]

story.append(subhead("3-1. 許可ルール（permissions.allow）", bg=LGREEN, line=GREEN))
story.append(SP(5))
story.append(badges(
    ["Read:*", "Bash:git:*", "Write:*", "Edit:*"],
    bg=GREEN
))
story.append(SP(4))
story.append(kv([
    ("Read:*",      "ワークスペース内の全ファイルの読み取りを許可"),
    ("Bash:git:*",  "git コマンドのみ Bash 実行を許可（他のコマンドは個別許可が必要）"),
    ("Write:*",     "全ファイルへの書き込みを許可"),
    ("Edit:*",      "全ファイルの編集（差分更新）を許可"),
], c1=38*mm, stripe1=LGREEN, stripe2=WHITE))
story.append(SP(10))

story.append(subhead("3-2. 拒否ルール（permissions.deny）", bg=LRED, line=RED))
story.append(SP(5))
story.append(badges(
    ["Read:.env*（.env 読み取り禁止）", "Bash:sudo:*（sudo 禁止）", "Bash:rm -rf /（ルート削除禁止）"],
    bg=RED
))
story.append(SP(4))
story.append(kv([
    ("Read:.env*",      "環境変数ファイル（.env / .env.local など）の読み取りを強制禁止"),
    ("Bash:sudo:*",     "管理者権限コマンドの実行を全面禁止"),
    ("Bash:rm -rf /",   "ルートディレクトリ以下の再帰削除コマンドを禁止（誤操作防止）"),
], c1=38*mm, stripe1=LRED, stripe2=WHITE))
story.append(SP(10))

story.append(subhead("3-3. フック設定（hooks）", bg=LAMBER, line=AMBER))
story.append(SP(5))
story.append(kv([
    ("トリガータイミング", "Stop — Claude セッションが停止するたびに実行"),
    ("フックタイプ",       "command（シェルコマンドを直接実行）"),
    ("実行コマンド",       "bash /home/user/claude/.claude/hooks/auto-push.sh"),
    ("タイムアウト",       "30 秒（超過した場合は強制終了）"),
    ("目的・効果",         "作業内容をセッション終了ごとに自動でリモートへ push し、\nクラウド環境のデータ消失を防ぐ"),
], c1=42*mm, stripe1=LAMBER, stripe2=WHITE))
story.append(SP(14))

# ══════════════════════════════════════════════════════════════════════
# 4. エージェント定義
# ══════════════════════════════════════════════════════════════════════
story += [chapter("4", "エージェント定義（.claude/agents/）"), SP(8)]
story.append(kv([
    ("ファイル",   ".claude/agents/security-reviewer.md"),
    ("エージェント名", "security-reviewer"),
    ("説明",       "OWASP Top 10 を基準に、コード変更のセキュリティ脆弱性を検出・報告する専門エージェント"),
    ("起動方法",   "/review コマンドや手動指定で呼び出す"),
], c1=42*mm))
story.append(SP(8))

story.append(subhead("検査項目（OWASP Top 10 準拠）", bg=LBLUE, line=BLUE))
story.append(SP(5))
owasp_rows = [
    ["1", "Injection",              "SQL インジェクション / コマンドインジェクション / XSS"],
    ["2", "認証・セッション管理",    "ハードコードされた認証情報 / 弱いトークン / セッション固定"],
    ["3", "機密データ露出",          ".env ファイル / API キー / パスワードの平文保存"],
    ["4", "アクセス制御",            "権限チェック漏れ / 水平権限昇格 / 直接オブジェクト参照"],
    ["5", "セキュリティ設定ミス",    "デフォルト設定のまま運用 / 不要な機能の有効化"],
]
story.append(datatable(
    ["No.", "カテゴリ", "検査内容"],
    owasp_rows,
    [10*mm, 48*mm, CW-58*mm]
))
story.append(SP(8))

story.append(subhead("出力フォーマット", bg=LTEAL, line=TEAL))
story.append(SP(4))
story.append(codeblock([
    "## セキュリティレビュー結果",
    "",
    "### CRITICAL: （重大な脆弱性 — 即時対応必須）",
    "### HIGH:     （高リスク — 早急な対応が必要）",
    "### MEDIUM:   （中リスク — 計画的に対応）",
    "### LOW:      （低リスク — 余裕があるときに対応）",
]))
story.append(SP(14))

# ══════════════════════════════════════════════════════════════════════
# 5. カスタムコマンド
# ══════════════════════════════════════════════════════════════════════
story += [chapter("5", "カスタムコマンド（.claude/commands/）"), SP(8)]
story.append(kv([
    ("ファイル",     ".claude/commands/deploy.md"),
    ("コマンド名",   "/deploy"),
    ("目的",        "デプロイ前のチェックリストを順番に実行し、安全にリモートへリリースする"),
], c1=38*mm))
story.append(SP(8))

story.append(subhead("/deploy コマンド — 実行ステップ詳細", bg=LBLUE, line=BLUE))
story.append(SP(5))
deploy_rows = [
    ["1", "テスト実行",     "npm test などで全テストがパスすることを確認",
     "npm test"],
    ["2", "Lint チェック",  "コード品質と構文エラーをチェック",
     "npm run lint"],
    ["3", "機密情報スキャン","SECRET / PASSWORD / API_KEY が含まれていないか検査",
     "git diff --name-only | xargs grep -l 'SECRET|API_KEY'"],
    ["4", "ブランチ確認",   "main または release/* ブランチ上にいることを確認",
     "git branch --show-current"],
    ["5", "差分最終確認",   "git diff main で変更内容を人の目で最終チェック",
     "git diff main"],
    ["6", "タグ付け",       "日付ベースのバージョンタグを付与",
     "git tag -a vYYYYMMDD -m 'Release'"],
    ["7", "プッシュ",       "タグごとリモートへプッシュして完了",
     "git push -u origin HEAD --tags"],
]
deploy_tbl_rows = [
    [p(s, sSmall), p(f"<b>{n}</b>"), p(d, sBody), p(cmd, sCode)]
    for s, n, d, cmd in deploy_rows
]
deploy_hdr = [p(f"<b>{h}</b>", st("dh",9,WHITE,sa=0)) for h in ["No.", "手順", "内容", "コマンド例"]]
dt = Table([deploy_hdr] + deploy_tbl_rows, colWidths=[9*mm, 28*mm, 48*mm, CW-85*mm])
dt.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0),  NAVY),
    ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, LGRAY]),
    ("GRID",          (0,0), (-1,-1), 0.3, MGRAY),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING",   (0,0), (-1,-1), 7),
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
]))
story.append(dt)
story.append(SP(14))

# ══════════════════════════════════════════════════════════════════════
# 6. スキル定義
# ══════════════════════════════════════════════════════════════════════
story += [chapter("6", "スキル定義（.claude/skills/）"), SP(8)]

# ── 6-1. code-review ──────────────────────────────────────────────
story.append(subhead("6-1.  code-review スキル", bg=LBLUE, line=BLUE))
story.append(SP(5))
story.append(kv([
    ("ファイル",     ".claude/skills/code-review/SKILL.md"),
    ("説明",        "変更差分を分析し、バグ・セキュリティ・品質の問題を指摘するコードレビュースキル"),
    ("使用ツール",   "Read（ファイル参照）・Bash（git diff 実行）・Edit（修正提案の適用）"),
    ("起動方法",     "ユーザーが「レビューして」などと指示したとき自動適用"),
    ("出力形式",     "[HIGH] / [MEDIUM] / [LOW] のラベル付きで問題箇所と修正提案を提示"),
], c1=38*mm))
story.append(SP(5))

story.append(p("<b>レビュー観点</b>", sH3))
story.append(SP(3))
cr_rows = [
    ["正確性",       "バグ・ロジックエラー・エッジケースの見落とし・型の不一致"],
    ["セキュリティ", "インジェクション攻撃・認証不備・機密情報の誤コミット"],
    ["品質",        "変数/関数の命名・重複コード・不要な複雑性・可読性"],
    ["テスト",      "テストカバレッジの不足・エッジケース漏れ・モックの妥当性"],
]
story.append(datatable(["観点", "チェック内容"], cr_rows, [28*mm, CW-28*mm]))
story.append(SP(10))

# ── 6-2. testing ──────────────────────────────────────────────────
story.append(subhead("6-2.  testing スキル", bg=LGREEN, line=GREEN))
story.append(SP(5))
story.append(kv([
    ("ファイル",     ".claude/skills/testing/SKILL.md"),
    ("説明",        "テストコードを作成・実行するスキル。describe + it + AAA パターンを採用"),
    ("使用ツール",   "Read・Bash・Edit・Write（テストファイルの新規作成も行う）"),
    ("テスト構造",   "describe（テスト群）→ it（個別ケース）→ Arrange / Act / Assert の3段階"),
    ("カバー範囲",   "正常系（Happy Path）・異常系（Error Path）・境界値（Edge Cases）"),
], c1=38*mm))
story.append(SP(5))

story.append(p("<b>テストテンプレート（Python）</b>", sH3))
story.append(SP(3))
story.append(codeblock([
    "def test_機能名_条件_期待結果():",
    "    # Arrange（テストデータ・モックの準備）",
    "    input_value = create_test_fixture()",
    "    mock_service = MockService(return_value=expected)",
    "",
    "    # Act（テスト対象の処理を実行）",
    "    result = target_function(input_value, service=mock_service)",
    "",
    "    # Assert（結果を検証）",
    "    assert result == expected_value",
    "    assert mock_service.was_called_once()",
]))
story.append(SP(14))

# ══════════════════════════════════════════════════════════════════════
# 7. スクリプト
# ══════════════════════════════════════════════════════════════════════
story += [chapter("7", "スクリプト（scripts/）"), SP(8)]

story.append(subhead("7-1.  auto-sync.ps1 — Windows 自動同期スクリプト", bg=LAMBER, line=AMBER))
story.append(SP(5))
story.append(kv([
    ("ファイル",     "scripts/auto-sync.ps1"),
    ("目的",        "Windows PC 上の C:\\Claude フォルダを GitHub から自動的に最新状態に保つ"),
    ("動作",        "ローカルとリモートのコミットハッシュを比較し、差分があれば git pull を実行"),
    ("ログ出力",    "scripts/sync.log にタイムスタンプ付きでログを記録"),
    ("対象ブランチ", "master（固定）"),
], c1=42*mm))
story.append(SP(5))
story.append(codeblock([
    "# 動作フロー",
    "1. Set-Location C:\\Claude                    # リポジトリへ移動",
    "2. git fetch origin master                   # リモートの最新情報を取得",
    "3. ローカルHEAD と origin/master を比較",
    "4. 同じ場合 → 「Already up to date.」をログに記録して終了",
    "5. 異なる場合 → git pull origin master を実行してログに記録",
]))
story.append(SP(10))

story.append(subhead("7-2.  setup-task-scheduler.ps1 — タスクスケジューラ登録スクリプト", bg=LAMBER, line=AMBER))
story.append(SP(5))
story.append(kv([
    ("ファイル",     "scripts/setup-task-scheduler.ps1"),
    ("目的",        "auto-sync.ps1 を Windows タスクスケジューラに登録し、15分ごとに自動実行する"),
    ("実行権限",    "管理者権限（Run as Administrator）が必要"),
    ("タスク名",    "ClaudeAutoSync"),
    ("実行間隔",    "15 分ごと（$interval 変数で変更可能）"),
    ("実行条件",    "ネットワーク接続時のみ実行 / スタート遅延があっても実行"),
    ("タイムアウト", "最大 2 分（-ExecutionTimeLimit）"),
], c1=42*mm))
story.append(SP(14))

# ══════════════════════════════════════════════════════════════════════
# 8. ワークフロールール
# ══════════════════════════════════════════════════════════════════════
story += [chapter("8", "ワークフロールール（CLAUDE.md）"), SP(8)]

story.append(subhead("8-1.  開発ワークフロー 6原則", bg=LBLUE, line=BLUE))
story.append(SP(5))
workflow_rows = [
    ["Plan Mode を使う",
     "調査フェーズと実装フェーズを明確に分離する。\nいきなりコードを書かず、まず構造を把握してから実装に入る。"],
    ["小さく実装・すぐ検証",
     "小さく作る → 動作確認 → 改善 のサイクルを繰り返す。\n一度に大きく変えず、確認できる単位で進める。"],
    ["Todo リストで進捗管理",
     "優先順位と進捗を常に可視化する。\n作業前にタスクを列挙し、完了したものから消していく。"],
    ["Commit は頻繁に",
     "1 タスク完了ごとにすぐコミットする。\n複数タスクをまとめてコミットしない。"],
    ["ブランチ戦略",
     "main（本番）/ feature/*（機能開発）/ spike/*（実験）を目的に応じて使い分ける。"],
    ["/compact を定期的に",
     "コンテキストウィンドウが圧迫されたら /compact で圧縮して作業余白を確保する。\n※ 実行前に重要情報を CLAUDE.md へ退避すること。"],
]
story.append(datatable(
    ["ルール", "内容と目的"],
    workflow_rows,
    [44*mm, CW-44*mm]
))
story.append(SP(10))

story.append(subhead("8-2.  コンテキスト管理ルール", bg=LTEAL, line=TEAL))
story.append(SP(5))
story.append(kv([
    ("CLAUDE.md を活用",  "重要な情報・ルール・約束事はすべて CLAUDE.md に記録する"),
    ("ローカルコンテキスト", "サブフォルダには .claude/ や CLAUDE.md を追加してスコープを分ける"),
    ("ファイルサイズ制限",  "各ファイルは 200 行未満に保つ（可読性と管理のため）"),
    ("/compact の注意",    "実行すると戻せないため、重要情報を先に CLAUDE.md へ退避してから実行"),
], c1=46*mm))
story.append(SP(10))

story.append(subhead("8-3.  セキュリティポリシー", bg=LRED, line=RED))
story.append(SP(5))
story.append(kv([
    (".env ファイル・認証情報", "絶対にコミットしない。.gitignore と deny ルールで二重に防止。"),
    ("外部副作用",              "DB 操作・外部 API 呼び出しは必ずユーザーの確認を取ってから実行する。"),
    ("sudo コマンド",           "settings.json の deny ルールで強制禁止。原則として使用不可。"),
], c1=46*mm, stripe1=LRED, stripe2=WHITE))
story.append(SP(14))

# ══════════════════════════════════════════════════════════════════════
# 9. Git 情報
# ══════════════════════════════════════════════════════════════════════
story += [chapter("9", "Git 情報"), SP(8)]

story.append(subhead("9-1.  ブランチ構成", bg=LBLUE, line=BLUE))
story.append(SP(5))
branch_rows = [
    ["master",                    "本番ブランチ", "安定した動作確認済みコードを格納"],
    ["claude/quirky-newton-vlU0Z", "開発ブランチ（現在）", "現在の作業ブランチ。完了後 master へマージ"],
]
story.append(datatable(
    ["ブランチ名", "種別", "説明"],
    branch_rows,
    [58*mm, 30*mm, CW-88*mm]
))
story.append(SP(10))

story.append(subhead("9-2.  コミット履歴（全 9 件）", bg=LBLUE, line=BLUE))
story.append(SP(5))
commit_rows = [
    ["9b918db", "claude/quirky-...", "Update report PDF with Japanese font (IPAGothic) for proper rendering"],
    ["a3e2c86", "claude/quirky-...", "Add Claude Code environment report PDF and generation script"],
    ["69ae13f", "claude/quirky-...", "Fix PowerShell encoding: replace Japanese with English"],
    ["b4fe020", "claude/quirky-...", "Fix emoji encoding error in setup-task-scheduler.ps1"],
    ["69ca2bd", "claude/quirky-...", "Add Task Scheduler setup script for auto-sync"],
    ["71cfe7b", "master",           "Add auto-sync: Stop hook + Windows PowerShell sync script"],
    ["e3cf942", "master",           "Track .claude/ config files for GitHub-local sync"],
    ["1323d56", "master",           "Add CLAUDE.md with workspace rules and workflow guidelines"],
    ["8559dad", "master",           "Initial commit"],
]
story.append(datatable(
    ["ハッシュ", "ブランチ", "コミットメッセージ"],
    commit_rows,
    [22*mm, 28*mm, CW-50*mm]
))
story.append(SP(10))

story.append(subhead("9-3.  .gitignore 設定", bg=LGRAY, line=GRAY))
story.append(SP(5))
story.append(codeblock([
    ".claude/settings.local.json    ← ローカル専用設定（個人の環境差異を除外）",
    ".claude/hooks/                  ← フックスクリプト（環境依存のため除外）",
]))
story.append(SP(14))

# ══════════════════════════════════════════════════════════════════════
# フッター
# ══════════════════════════════════════════════════════════════════════
story.append(HR())
story.append(SP(4))
story.append(p("本レポートは Claude Code により自動生成されました  |  2026-05-22  |  ooaku-bit/claude", sFoot))

# ====================================================================
OUT = "/home/user/claude/claude_code_environment_report.pdf"
doc = NumberedDoc(
    OUT, pagesize=A4,
    leftMargin=ML, rightMargin=MR,
    topMargin=MT, bottomMargin=MB + 8*mm,
    title="Claude Code 環境構成レポート",
    author="Claude Code",
    subject="ooaku-bit/claude ワークスペース環境構成",
)
doc.build(story)
print(f"PDF 生成完了: {OUT}")
