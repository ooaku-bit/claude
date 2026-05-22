#!/usr/bin/env python3
"""Claude Code 環境構成レポート — 完全版 v3"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether, Image
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, String, Circle, Line
from reportlab.graphics import renderPDF

# ── フォント ─────────────────────────────────────────────────────────
pdfmetrics.registerFont(TTFont("JP",  "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"))
F = "JP"

W, H = A4
ML = MR = 14 * mm
MT = 12 * mm
MB = 16 * mm
CW = W - ML - MR

# ── カラーパレット ────────────────────────────────────────────────────
NAVY    = colors.HexColor("#0a1628")
DBLUE   = colors.HexColor("#1e3a8a")
BLUE    = colors.HexColor("#2563eb")
MBLUE   = colors.HexColor("#3b82f6")
LBLUE   = colors.HexColor("#eff6ff")
XBLUE   = colors.HexColor("#dbeafe")
TEAL    = colors.HexColor("#0d9488")
LTEAL   = colors.HexColor("#ccfbf1")
GREEN   = colors.HexColor("#15803d")
LGREEN  = colors.HexColor("#dcfce7")
PURPLE  = colors.HexColor("#7c3aed")
LPURP   = colors.HexColor("#f5f3ff")
DPURP   = colors.HexColor("#ede9fe")
AMBER   = colors.HexColor("#d97706")
LAMBER  = colors.HexColor("#fef3c7")
RED     = colors.HexColor("#dc2626")
LRED    = colors.HexColor("#fee2e2")
CORAL   = colors.HexColor("#e11d48")
LCORAL  = colors.HexColor("#fff1f2")
GRAY    = colors.HexColor("#6b7280")
LGRAY   = colors.HexColor("#f9fafb")
MGRAY   = colors.HexColor("#e5e7eb")
DGRAY   = colors.HexColor("#9ca3af")
BLACK   = colors.HexColor("#111827")
WHITE   = colors.white
GOLD    = colors.HexColor("#f59e0b")

# ── スタイル ──────────────────────────────────────────────────────────
def S(name, sz, color=BLACK, align=TA_LEFT, sa=2, ld=None):
    return ParagraphStyle(name, fontName=F, fontSize=sz, textColor=color,
                          alignment=align, spaceAfter=sa, leading=ld or round(sz*1.65))

sH1    = S("h1", 24, WHITE,  TA_CENTER, sa=4, ld=30)
sH1s   = S("h1s",13, colors.HexColor("#93c5fd"), TA_CENTER, sa=3)
sMeta  = S("mt", 8,  colors.HexColor("#94a3b8"), TA_CENTER, sa=2)
sChNum = S("cn", 14, WHITE,  TA_CENTER, sa=0, ld=18)
sChTit = S("ct", 13, WHITE,  TA_LEFT,   sa=0, ld=18)
sH3    = S("h3", 10, NAVY,   TA_LEFT,   sa=2, ld=16)
sH3w   = S("h3w",10, WHITE,  TA_LEFT,   sa=0, ld=16)
sBody  = S("bd",  9, BLACK,  TA_LEFT,   sa=2, ld=15)
sBodyW = S("bdw", 9, WHITE,  TA_LEFT,   sa=1, ld=15)
sCode  = S("cd",  8, colors.HexColor("#1e3a5f"), sa=1, ld=13)
sSm    = S("sm",  7, GRAY,   sa=1, ld=12)
sSmW   = S("smw", 7, colors.HexColor("#c7d2fe"), TA_LEFT, sa=0, ld=12)
sFt    = S("ft",  7, DGRAY,  TA_CENTER, sa=0, ld=11)
sTH    = S("th",  9, WHITE,  sa=0, ld=14)
sBdg   = S("bg",  8, WHITE,  TA_CENTER, sa=0, ld=13)
sTag   = S("tg",  7, WHITE,  TA_CENTER, sa=0, ld=11)
sToc   = S("tc",  9, BLACK,  sa=0, ld=15)
sTocN  = S("tn",  9, BLUE,   TA_CENTER, sa=0, ld=15)

def p(t, s=sBody): return Paragraph(t, s)
def SP(n=6):       return Spacer(1, n)
def HR(c=MGRAY, t=0.4): return HRFlowable(width="100%", thickness=t, color=c)

# ── 章ヘッダー ────────────────────────────────────────────────────────
def chap(num, title, sub="", color=DBLUE):
    rows = [[
        p(str(num), sChNum),
        [p(f"<b>{title}</b>", sChTit)] + ([p(sub, sSmW)] if sub else [])
    ]]
    t = Table(rows, colWidths=[12*mm, CW-12*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(0,-1), MBLUE),
        ("BACKGROUND",    (1,0),(1,-1), color),
        ("VALIGN",        (0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",    (0,0),(-1,-1), 9),
        ("BOTTOMPADDING", (0,0),(-1,-1), 9),
        ("LEFTPADDING",   (0,0),(0,-1),  3),
        ("LEFTPADDING",   (1,0),(1,-1), 12),
        ("RIGHTPADDING",  (0,0),(-1,-1), 8),
    ]))
    return t

# ── セクションバー ────────────────────────────────────────────────────
def secbar(title, bg=XBLUE, bar=BLUE, tc=NAVY):
    t = Table([[p(f"<b>{title}</b>", S("sb",10,tc,sa=0,ld=16))]], colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), bg),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("LINEBELOW",     (0,0),(-1,-1), 2, bar),
    ]))
    return t

# ── KVテーブル ────────────────────────────────────────────────────────
def kv(rows, c1=46*mm, s1=WHITE, s2=LGRAY):
    c2 = CW - c1
    data = [[p(f"<b>{k}</b>"), p(v)] for k,v in rows]
    t = Table(data, colWidths=[c1, c2])
    t.setStyle(TableStyle([
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[s1,s2]),
        ("GRID",         (0,0),(-1,-1), 0.3, MGRAY),
        ("LEFTPADDING",  (0,0),(-1,-1), 9),
        ("RIGHTPADDING", (0,0),(-1,-1), 9),
        ("TOPPADDING",   (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("VALIGN",       (0,0),(-1,-1),"TOP"),
    ]))
    return t

# ── データテーブル ────────────────────────────────────────────────────
def dtbl(headers, rows, widths, hbg=NAVY):
    hrow = [p(f"<b>{h}</b>", sTH) for h in headers]
    drows = [[p(c, sBody) for c in r] for r in rows]
    t = Table([hrow]+drows, colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  hbg),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE,LGRAY]),
        ("GRID",         (0,0),(-1,-1), 0.3, MGRAY),
        ("TOPPADDING",   (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("RIGHTPADDING", (0,0),(-1,-1), 8),
        ("VALIGN",       (0,0),(-1,-1),"TOP"),
    ]))
    return t

# ── コードブロック ────────────────────────────────────────────────────
def codeblk(lines):
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

# ── バッジ ────────────────────────────────────────────────────────────
def badges(items, bg=BLUE, fg=WHITE):
    s = S("bg2", 8, fg, TA_CENTER, sa=0, ld=13)
    cells = [p(item, s) for item in items]
    t = Table([cells], colWidths=[CW/len(items)]*len(items))
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), bg),
        ("TOPPADDING",   (0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("INNERGRID",    (0,0),(-1,-1), 0.5, colors.HexColor("#ffffff30")),
    ]))
    return t

# ── 部署カード（横並び） ──────────────────────────────────────────────
def dept_cards(depts):
    """depts: [(icon_char, name, en_name, role, color, lcolor), ...]"""
    n = len(depts)
    w = CW / n
    cells = []
    for icon, name, en, role, c, lc in depts:
        sn = S(f"dn{name}", 9, c, TA_CENTER, sa=1, ld=14)
        se = S(f"de{name}", 7, GRAY, TA_CENTER, sa=1, ld=11)
        sr = S(f"dr{name}", 8, BLACK, TA_LEFT, sa=0, ld=13)
        inner = Table([
            [p(icon, S(f"ic{name}", 20, c, TA_CENTER, sa=2, ld=26))],
            [p(f"<b>{name}</b>", sn)],
            [p(en, se)],
            [HR(c, 1)],
            [p(role, sr)],
        ], colWidths=[w - 6*mm])
        inner.setStyle(TableStyle([
            ("BACKGROUND",   (0,0),(-1,-1), lc),
            ("BOX",          (0,0),(-1,-1), 1, c),
            ("TOPPADDING",   (0,0),(-1,-1), 6),
            ("BOTTOMPADDING",(0,0),(-1,-1), 6),
            ("LEFTPADDING",  (0,0),(-1,-1), 5),
            ("RIGHTPADDING", (0,0),(-1,-1), 5),
            ("ALIGN",        (0,0),(-1,2),  "CENTER"),
        ]))
        cells.append(inner)
    t = Table([cells], colWidths=[w]*n)
    t.setStyle(TableStyle([
        ("VALIGN",       (0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",  (0,0),(-1,-1), 2),
        ("RIGHTPADDING", (0,0),(-1,-1), 2),
        ("TOPPADDING",   (0,0),(-1,-1), 0),
        ("BOTTOMPADDING",(0,0),(-1,-1), 0),
    ]))
    return t

# ── スキルカード（2列） ───────────────────────────────────────────────
def skill_cards(skills):
    """skills: [(name, desc, tools, color), ...]"""
    rows = []
    for i in range(0, len(skills), 2):
        pair = skills[i:i+2]
        cells = []
        for name, desc, tools, c in pair:
            lc = colors.HexColor(c + "15") if len(c)==7 else LGRAY
            sn2 = S(f"sk{name}", 9, colors.HexColor(c), TA_LEFT, sa=1, ld=14)
            inner = Table([
                [p(f"<b>{name}</b>", sn2)],
                [p(desc, sSm)],
                [p(f"Tools: {tools}", S(f"st{name}",7,GRAY,sa=0,ld=11))],
            ], colWidths=[(CW-6*mm)/2])
            inner.setStyle(TableStyle([
                ("BACKGROUND",   (0,0),(-1,-1), LGRAY),
                ("LINEBELOW",    (0,0),(0,0), 2, colors.HexColor(c)),
                ("TOPPADDING",   (0,0),(-1,-1), 7),
                ("BOTTOMPADDING",(0,0),(-1,-1), 7),
                ("LEFTPADDING",  (0,0),(-1,-1), 9),
                ("RIGHTPADDING", (0,0),(-1,-1), 9),
            ]))
            cells.append(inner)
        if len(cells) == 1:
            cells.append(p(""))
        rows.append(cells)
    t = Table(rows, colWidths=[(CW-4*mm)/2]*2)
    t.setStyle(TableStyle([
        ("VALIGN",       (0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",  (0,0),(-1,-1), 0),
        ("RIGHTPADDING", (0,0),(-1,-1), 4),
        ("TOPPADDING",   (0,0),(-1,-1), 0),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
    ]))
    return t

# ── コマンドカード（2列） ─────────────────────────────────────────────
def cmd_cards(cmds):
    """cmds: [(cmd, desc, color), ...]"""
    rows = []
    for i in range(0, len(cmds), 2):
        pair = cmds[i:i+2]
        cells = []
        for cmd, desc, c in pair:
            sc = S(f"cc{cmd}", 10, colors.HexColor(c), TA_LEFT, sa=1, ld=15)
            inner = Table([
                [p(f"<b>{cmd}</b>", sc)],
                [p(desc, sSm)],
            ], colWidths=[(CW-6*mm)/2])
            inner.setStyle(TableStyle([
                ("BACKGROUND",   (0,0),(-1,-1), LGRAY),
                ("BOX",          (0,0),(-1,-1), 0.5, MGRAY),
                ("LINEBELOW",    (0,0),(0,0), 2, colors.HexColor(c)),
                ("TOPPADDING",   (0,0),(-1,-1), 7),
                ("BOTTOMPADDING",(0,0),(-1,-1), 7),
                ("LEFTPADDING",  (0,0),(-1,-1), 9),
                ("RIGHTPADDING", (0,0),(-1,-1), 9),
            ]))
            cells.append(inner)
        if len(cells) == 1:
            cells.append(p(""))
        rows.append(cells)
    t = Table(rows, colWidths=[(CW-4*mm)/2]*2)
    t.setStyle(TableStyle([
        ("VALIGN",       (0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",  (0,0),(-1,-1), 0),
        ("RIGHTPADDING", (0,0),(-1,-1), 4),
        ("TOPPADDING",   (0,0),(-1,-1), 0),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
    ]))
    return t

# ── 許可/拒否バー ─────────────────────────────────────────────────────
def allow_deny_bar(allows, denies):
    a_cells = [p(f"✓ {a}", S(f"al{i}",8,GREEN,TA_LEFT,sa=0,ld=13)) for i,a in enumerate(allows)]
    d_cells = [p(f"✗ {d}", S(f"dn{i}",8,RED,TA_LEFT,sa=0,ld=13)) for i,d in enumerate(denies)]
    rows = []
    max_n = max(len(a_cells), len(d_cells))
    for i in range(max_n):
        r = [a_cells[i] if i < len(a_cells) else p(""),
             d_cells[i] if i < len(d_cells) else p("")]
        rows.append(r)
    t = Table(rows, colWidths=[CW/2]*2)
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(0,-1), LGREEN),
        ("BACKGROUND",   (1,0),(1,-1), LRED),
        ("GRID",         (0,0),(-1,-1), 0.3, MGRAY),
        ("TOPPADDING",   (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING",  (0,0),(-1,-1), 10),
        ("RIGHTPADDING", (0,0),(-1,-1), 10),
    ]))
    return t

# ════════════════════════════════════════════════════════════════════
# ページ番号
# ════════════════════════════════════════════════════════════════════
class Doc(SimpleDocTemplate):
    def afterPage(self):
        c = self.canv
        c.saveState()
        c.setFont(F, 7)
        c.setFillColor(DGRAY)
        pg = c.getPageNumber()
        # 下線
        c.setStrokeColor(MGRAY)
        c.setLineWidth(0.3)
        c.line(ML, 11*mm, W-MR, 11*mm)
        c.drawString(ML, 8*mm, "Claude Code  Workspace  Environment Report")
        c.drawRightString(W-MR, 8*mm, f"{pg}")
        c.restoreState()

# ════════════════════════════════════════════════════════════════════
story = []

# ══════════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════════
# 上部カラーブロック
cover_top = Table([[
    p("Claude Code", sH1),
    SP(2),
    p("Workspace  Environment Report", sH1s),
    SP(2),
    p("ワークスペース環境構成レポート", S("cjs",11,colors.HexColor("#bfdbfe"),TA_CENTER,sa=4)),
]], colWidths=[CW])
cover_top.setStyle(TableStyle([
    ("BACKGROUND",   (0,0),(-1,-1), NAVY),
    ("TOPPADDING",   (0,0),(-1,-1), 30),
    ("BOTTOMPADDING",(0,0),(-1,-1), 20),
    ("LEFTPADDING",  (0,0),(-1,-1), 20),
    ("RIGHTPADDING", (0,0),(-1,-1), 20),
]))
story.append(cover_top)

# メタ情報ブロック
meta_rows = [
    ["リポジトリ", "ooaku-bit / claude"],
    ["実行環境",   "Claude Code on the Web  |  Linux / ephemeral container"],
    ["使用モデル", "claude-sonnet-4-6"],
    ["作業ブランチ","claude / quirky-newton-vlU0Z"],
    ["作成日",     "2026 年 5 月 22 日"],
]
meta_data = [[p(f"<b>{k}</b>", S("mk",8,DGRAY,sa=0,ld=13)),
              p(v, S("mv",8,BLACK,sa=0,ld=13))] for k,v in meta_rows]
meta_tbl = Table(meta_data, colWidths=[36*mm, CW-36*mm])
meta_tbl.setStyle(TableStyle([
    ("ROWBACKGROUNDS",(0,0),(-1,-1),[WHITE,LGRAY]),
    ("GRID",         (0,0),(-1,-1), 0.3, MGRAY),
    ("TOPPADDING",   (0,0),(-1,-1), 5),
    ("BOTTOMPADDING",(0,0),(-1,-1), 5),
    ("LEFTPADDING",  (0,0),(-1,-1), 10),
    ("RIGHTPADDING", (0,0),(-1,-1), 10),
]))
story.append(meta_tbl)
story.append(SP(10))

# サマリーカウンター
counts = [
    ("5", "Agents\nエージェント"),
    ("7", "Skills\nスキル"),
    ("6", "Commands\nコマンド"),
    ("2", "Scripts\nスクリプト"),
    ("1", "Hook\nフック"),
]
cs = S("cnum",22,BLUE,TA_CENTER,sa=1,ld=28)
cl = S("clbl",7,GRAY,TA_CENTER,sa=0,ld=11)
count_cells = []
for num, lbl in counts:
    inner = Table([
        [p(num, cs)],
        [p(lbl, cl)],
    ], colWidths=[CW/len(counts) - 4*mm])
    inner.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), LBLUE),
        ("BOX",          (0,0),(-1,-1), 0.5, XBLUE),
        ("TOPPADDING",   (0,0),(-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ("ALIGN",        (0,0),(-1,-1),"CENTER"),
    ]))
    count_cells.append(inner)
count_tbl = Table([count_cells], colWidths=[CW/len(counts)]*len(counts))
count_tbl.setStyle(TableStyle([
    ("VALIGN",       (0,0),(-1,-1),"TOP"),
    ("LEFTPADDING",  (0,0),(-1,-1), 2),
    ("RIGHTPADDING", (0,0),(-1,-1), 2),
]))
story.append(count_tbl)
story.append(SP(14))

# 目次
story.append(secbar("目次  /  Table of Contents", bg=NAVY, bar=MBLUE, tc=WHITE))
story.append(SP(4))
toc_items = [
    ("1", "プロジェクト概要",     "リポジトリ情報・実行環境"),
    ("2", "ディレクトリ構成",     "全ファイル・フォルダのマップ"),
    ("3", "設定ファイル",         "settings.json（権限・フック）"),
    ("4", "部署構成（エージェント）","経営者サポート5部署 + システムエージェント"),
    ("5", "スキル構成",           "プロジェクト7スキル + システムスキル"),
    ("6", "コマンド一覧",         "6つのスラッシュコマンド詳細"),
    ("7", "スクリプト",           "Windows 自動同期スクリプト"),
    ("8", "ワークフロールール",    "CLAUDE.md に定義された開発原則"),
    ("9", "Git 情報",             "ブランチ・コミット履歴"),
]
toc_rows = [[p(n, sTocN), p(f"<b>{t}</b>", sToc), p(d, sSm)]
            for n,t,d in toc_items]
toc_tbl = Table(toc_rows, colWidths=[10*mm, 62*mm, CW-72*mm])
toc_tbl.setStyle(TableStyle([
    ("ROWBACKGROUNDS",(0,0),(-1,-1),[WHITE,LGRAY]),
    ("GRID",         (0,0),(-1,-1), 0.3, MGRAY),
    ("TOPPADDING",   (0,0),(-1,-1), 5),
    ("BOTTOMPADDING",(0,0),(-1,-1), 5),
    ("LEFTPADDING",  (0,0),(-1,-1), 8),
    ("VALIGN",       (0,0),(-1,-1),"MIDDLE"),
]))
story += [toc_tbl, PageBreak()]

# ══════════════════════════════════════════════════
# 1. プロジェクト概要
# ══════════════════════════════════════════════════
story += [chap("1","プロジェクト概要","Project Overview"), SP(8)]
story.append(kv([
    ("リポジトリ",    "ooaku-bit / claude"),
    ("目的",         "Claude Code の自動化・運用ワークスペース。\n経営者サポート機能（エージェント・スキル・コマンド）を一元管理する。"),
    ("実行環境",     "Claude Code on the Web — Linux / ephemeral container（クラウド）"),
    ("使用モデル",   "claude-sonnet-4-6"),
    ("ブランチ",     "claude / quirky-newton-vlU0Z（開発）/ master（本番）"),
    ("リモート",     "GitHub（ローカルプロキシ 127.0.0.1:32817 経由）"),
    ("自動保護",     "Stop フック：セッション終了時に自動 git push で変更を保護"),
], c1=38*mm))
story.append(SP(14))

# ══════════════════════════════════════════════════
# 2. ディレクトリ構成
# ══════════════════════════════════════════════════
story += [chap("2","ディレクトリ構成","Directory Structure"), SP(8)]
story.append(codeblk([
    "/home/user/claude/",
    "├── CLAUDE.md                          ← プロジェクトルール・部署構成マスター",
    "├── README.md                          ← リポジトリ概要",
    "├── .gitignore",
    "├── claude_code_environment_report.pdf ← 本レポート",
    "├── generate_report.py                 ← PDF 生成スクリプト（Python）",
    "├── scripts/",
    "│   ├── auto-sync.ps1                  ← Windows 自動同期（15 分ごと git pull）",
    "│   └── setup-task-scheduler.ps1       ← Windows タスクスケジューラ登録",
    "└── .claude/",
    "    ├── settings.json                  ← 権限・フック設定",
    "    ├── agents/                        ← エージェント定義（5 部署）",
    "    │   ├── executive-secretary.md     ← 秘書室",
    "    │   ├── strategy-analyst.md        ← 経営企画室",
    "    │   ├── risk-advisor.md            ← リスク管理室",
    "    │   ├── pr-director.md             ← 広報室",
    "    │   └── security-reviewer.md       ← セキュリティ審査室",
    "    ├── commands/                      ← スラッシュコマンド定義（6 種）",
    "    │   ├── brief.md  minutes.md  report.md",
    "    │   ├── research.md  press.md  deploy.md",
    "    ├── skills/                        ← スキル定義（7 種）",
    "    │   ├── report-writing/   meeting-prep/   market-research/",
    "    │   ├── risk-assessment/  press-release/",
    "    │   ├── code-review/      testing/",
    "    └── hooks/                         ← フックスクリプト（gitignore 除外）",
    "        └── auto-push.sh              ← Stop フック本体",
]))
story.append(SP(8))
story.append(dtbl(
    ["種別", "件数", "主なファイル"],
    [
        ["Markdown (.md)","12","CLAUDE.md / agents ×5 / commands ×6 / SKILL.md ×7"],
        ["JSON (.json)",   "1", "settings.json"],
        ["PowerShell (.ps1)","2","auto-sync.ps1 / setup-task-scheduler.ps1"],
        ["Python (.py)",   "1", "generate_report.py"],
        ["Shell (.sh)",    "1", "auto-push.sh（gitignore 除外）"],
    ],
    [30*mm,14*mm,CW-44*mm]
))
story.append(SP(14))

# ══════════════════════════════════════════════════
# 3. 設定ファイル
# ══════════════════════════════════════════════════
story += [chap("3","設定ファイル","settings.json  /  .gitignore"), SP(8)]

# 許可/拒否を2列で見せる
story.append(secbar("権限ルール  ( permissions )", bg=LBLUE, bar=BLUE))
story.append(SP(5))
hdr_row = [
    p("<b>✓ 許可（allow）</b>", S("ah",9,GREEN,sa=0,ld=14)),
    p("<b>✗ 拒否（deny）</b>",  S("dh",9,RED,  sa=0,ld=14))
]
allow_items = ["Read:*（全ファイル読み取り）","Bash:git:*（git コマンド）",
               "Write:*（全ファイル書き込み）","Edit:*（全ファイル編集）"]
deny_items  = ["Read:.env*（環境変数ファイル禁止）",
               "Bash:sudo:*（管理者権限禁止）",
               "Bash:rm -rf /（ルート削除禁止）"]
a_rows = [p(f"  {a}", S(f"ai{i}",8,GREEN,sa=0,ld=13)) for i,a in enumerate(allow_items)]
d_rows = [p(f"  {d}", S(f"di{i}",8,RED,  sa=0,ld=13)) for i,d in enumerate(deny_items)]
max_r = max(len(a_rows), len(d_rows))
perm_data = [hdr_row]
for i in range(max_r):
    perm_data.append([
        a_rows[i] if i < len(a_rows) else p(""),
        d_rows[i] if i < len(d_rows) else p(""),
    ])
perm_tbl = Table(perm_data, colWidths=[CW/2]*2)
perm_tbl.setStyle(TableStyle([
    ("BACKGROUND",   (0,0),(0,0),  LGREEN),
    ("BACKGROUND",   (1,0),(1,0),  LRED),
    ("BACKGROUND",   (0,1),(0,-1), colors.HexColor("#f0fdf4")),
    ("BACKGROUND",   (1,1),(1,-1), colors.HexColor("#fff5f5")),
    ("GRID",         (0,0),(-1,-1), 0.3, MGRAY),
    ("TOPPADDING",   (0,0),(-1,-1), 5),
    ("BOTTOMPADDING",(0,0),(-1,-1), 5),
    ("LEFTPADDING",  (0,0),(-1,-1), 10),
    ("RIGHTPADDING", (0,0),(-1,-1), 10),
]))
story.append(perm_tbl)
story.append(SP(10))

story.append(secbar("フック設定  ( hooks.Stop )", bg=LAMBER, bar=AMBER))
story.append(SP(5))
story.append(kv([
    ("トリガー",     "Stop — Claude セッション停止のたびに実行"),
    ("実行コマンド", "bash /home/user/claude/.claude/hooks/auto-push.sh"),
    ("タイムアウト", "30 秒"),
    ("目的",        "クラウド環境はセッション終了でデータが失われるため、\n終了ごとに自動 git push して変更を GitHub に保護する"),
], c1=38*mm, s1=LAMBER, s2=WHITE))
story.append(SP(10))

story.append(secbar(".gitignore 除外設定", bg=LGRAY, bar=GRAY))
story.append(SP(5))
story.append(codeblk([
    ".claude/settings.local.json   ← ローカル専用設定（個人差異を除外）",
    ".claude/hooks/                 ← フックスクリプト（環境依存パスを除外）",
]))
story.append(SP(14))

# ══════════════════════════════════════════════════
# 4. 部署構成
# ══════════════════════════════════════════════════
story += [chap("4","部署構成（エージェント）","Agent / Department Structure", color=TEAL), SP(8)]

story.append(secbar("4-1.  経営者サポート部署  ―  プロジェクト定義エージェント（5 部署）",
                    bg=LTEAL, bar=TEAL))
story.append(SP(8))

# 部署カード
depts = [
    ("S", "秘書室",   "Executive\nSecretary",
     "文書起草・要約\n議事録・スケジュール",
     "#0d9488", "#f0fdfa"),
    ("企", "経営企画室","Strategy\nAnalyst",
     "SWOT分析・競合調査\n戦略立案・KPI設計",
     "#2563eb", "#eff6ff"),
    ("R", "リスク管理室","Risk\nAdvisor",
     "リスク洗い出し\n契約確認・コンプライアンス",
     "#dc2626", "#fef2f2"),
    ("PR","広報室",   "PR\nDirector",
     "プレスリリース\nスピーチ・SNS・危機対応",
     "#7c3aed", "#f5f3ff"),
    ("Sec","セキュリティ\n審査室","Security\nReviewer",
     "OWASP準拠\nコード脆弱性診断",
     "#d97706", "#fef3c7"),
]
story.append(dept_cards(depts))
story.append(SP(10))

# 各部署の詳細
story.append(secbar("各部署の詳細業務", bg=XBLUE, bar=BLUE))
story.append(SP(5))
dept_detail = [
    ["秘書室\n(executive-secretary)",
     "・文書起草（メール・挨拶文・依頼状）\n・長文を3点以内に要約\n・議事録作成（決定/宿題/次回）\n・スケジュール優先順位整理",
     "BLUF原則（結論先出し）・最速アウトプット"],
    ["経営企画室\n(strategy-analyst)",
     "・SWOT / 3C / PEST 分析\n・競合他社の比較表作成\n・戦略オプション提示（推奨案1つ）\n・KPI設計",
     "MECE思考・「So What?」を常に意識"],
    ["リスク管理室\n(risk-advisor)",
     "・法務・財務・評判・事業リスク洗い出し\n・発生確率×影響度のマトリクス評価\n・契約書の重要条項（解約・免責）要約\n・対策立案（回避/軽減/移転/受容）",
     "最悪シナリオ想定・専門家相談を明示"],
    ["広報室\n(pr-director)",
     "・プレスリリース作成（5W1H必須）\n・経営者スピーチ原稿\n・全社メール・SNS投稿（LinkedIn/X）\n・危機対応文（謝罪・再発防止）",
     "炎上リスクチェック・ブランド保護"],
    ["セキュリティ審査室\n(security-reviewer)",
     "・Injection（SQLi/XSS）検査\n・認証・機密データ露出の確認\n・アクセス制御・設定ミスの検出\n・CRITICAL/HIGH/MEDIUM/LOWで報告",
     "OWASP Top 10 準拠"],
]
story.append(dtbl(
    ["部署名（エージェント）","主な業務","行動原則"],
    dept_detail,
    [44*mm, 76*mm, CW-120*mm]
))
story.append(SP(10))

story.append(secbar("4-2.  システムエージェント（Claude Code 組み込み・7 種）",
                    bg=DPURP, bar=PURPLE))
story.append(SP(5))
story.append(dtbl(
    ["エージェント名","役割・説明","主なツール"],
    [
        ["claude（汎用）",      "どれにも当てはまらないタスクを処理するデフォルト", "全ツール"],
        ["claude-code-guide",  "Claude Code CLI / API / SDK の Q&A 専門",          "Bash/Read/WebFetch"],
        ["Explore（探索）",     "コードベースの高速検索・ファイル探索・参照調査",    "Read/Bash（検索系）"],
        ["general-purpose",    "複雑な調査・マルチステップタスクの汎用処理",         "全ツール"],
        ["Plan（設計）",        "実装計画・アーキテクチャ設計・トレードオフ分析",    "Read/Bash（参照系）"],
        ["security-reviewer",  "セキュリティレビュー専門（本プロジェクト定義）",    "全ツール"],
        ["statusline-setup",   "ステータスライン表示の設定構成",                    "Read/Edit"],
    ],
    [38*mm, 72*mm, CW-110*mm]
))
story.append(SP(14))

# ══════════════════════════════════════════════════
# 5. スキル構成
# ══════════════════════════════════════════════════
story += [chap("5","スキル構成","Skills", color=GREEN), SP(8)]

story.append(secbar("5-1.  プロジェクト定義スキル（7 種）", bg=LGREEN, bar=GREEN))
story.append(SP(6))

proj_skills = [
    ("report-writing",  "経営レポート・月次報告書を\nエグゼクティブサマリー付きで作成",
     "Read / Write / Edit", "#15803d"),
    ("meeting-prep",    "会議アジェンダ・事前ブリーフィング・\n議事録・フォローアップリスト作成",
     "Read / Write / Edit", "#0d9488"),
    ("market-research", "市場規模・競合比較・トレンド調査を\nレポートにまとめる",
     "Read / WebSearch / WebFetch / Write", "#2563eb"),
    ("risk-assessment", "発生確率×影響度のリスクマトリクス評価と\n対策立案",
     "Read / Write / Edit", "#dc2626"),
    ("press-release",   "プレスリリース・スピーチ・SNS・\n危機対応文の広報文書作成",
     "Read / Write / Edit", "#7c3aed"),
    ("code-review",     "差分を分析しバグ・セキュリティ・\n品質の問題を[HIGH/MED/LOW]で指摘",
     "Read / Bash / Edit", "#d97706"),
    ("testing",         "describe+it+AAAパターンで\nテスト作成・実行",
     "Read / Bash / Edit / Write", "#0891b2"),
]
story.append(skill_cards(proj_skills))
story.append(SP(10))

story.append(secbar("5-2.  システムスキル（Claude Code 組み込み・14 種）",
                    bg=DPURP, bar=PURPLE))
story.append(SP(5))
story.append(dtbl(
    ["スキル名","説明","カテゴリ"],
    [
        ["session-start-hook",       "スタートアップフック設定",         "設定管理"],
        ["code-review",              "差分レビュー・PRインラインコメント","開発支援"],
        ["testing",                  "テスト作成・実行（AAA パターン）",  "開発支援"],
        ["deploy",                   "デプロイ前チェックリスト実行",      "リリース"],
        ["update-config",            "settings.json 自動更新",           "設定管理"],
        ["keybindings-help",         "キーバインドカスタマイズ",          "設定管理"],
        ["verify",                   "変更の実動作検証",                  "開発支援"],
        ["fewer-permission-prompts", "allowlist 自動追加で承認削減",      "設定管理"],
        ["loop",                     "コマンドを定期間隔で繰り返し実行",  "運用"],
        ["claude-api",               "Anthropic SDK 開発・最適化",        "開発支援"],
        ["run",                      "アプリ起動・動作確認",              "開発支援"],
        ["init",                     "CLAUDE.md 自動生成・初期化",        "初期化"],
        ["review",                   "PR レビュー",                       "レビュー"],
        ["security-review",          "ブランチのセキュリティレビュー",    "セキュリティ"],
    ],
    [50*mm, 76*mm, CW-126*mm]
))
story.append(SP(14))

# ══════════════════════════════════════════════════
# 6. コマンド
# ══════════════════════════════════════════════════
story += [chap("6","コマンド一覧","Slash Commands"), SP(8)]

cmds = [
    ("/brief",   "今日の最重要アクション Top3 を\n1枚のブリーフィングシートにまとめる", "#0d9488"),
    ("/minutes", "会議メモを貼り付けるだけで\n決定事項・宿題・次回予定の議事録を即生成", "#2563eb"),
    ("/report",  "月次・週次・案件レポートを\nエグゼクティブサマリー付きで自動作成",   "#7c3aed"),
    ("/research","テーマを指定して市場・競合・\nトレンド調査レポートを作成",           "#dc2626"),
    ("/press",   "プレスリリース・スピーチ・\nSNS・危機対応文を種別指定で作成",       "#d97706"),
    ("/deploy",  "テスト→Lint→機密スキャン→\nタグ付け→プッシュの7ステップ実行",     "#15803d"),
]
story.append(cmd_cards(cmds))
story.append(SP(8))

story.append(secbar("コマンド詳細", bg=XBLUE, bar=BLUE))
story.append(SP(5))
story.append(dtbl(
    ["コマンド","使い方例","出力"],
    [
        ["/brief",   "/brief 今日の重点: 新規提案先へのアプローチ",
         "ブリーフィングシート（今日の Top3 / 予定 / 持ち越し）"],
        ["/minutes", "/minutes [会議テキストを貼り付け]",
         "議事録ファイル（決定 / 宿題テーブル / 次回予定）"],
        ["/report",  "/report 月次 [データを貼り付け]",
         "経営レポート（サマリー / 実績 / 課題 / アクション）"],
        ["/research","/research 国内 SaaS 市場の競合比較",
         "市場調査レポート（市場概況 / 競合比較表 / インサイト）"],
        ["/press",   "/press release [内容を入力]",
         "プレスリリース草稿（5W1H / 会社概要 / 連絡先）"],
        ["/deploy",  "/deploy",
         "7 ステップのデプロイチェックリスト実行ログ"],
    ],
    [22*mm, 68*mm, CW-90*mm]
))
story.append(SP(14))

# ══════════════════════════════════════════════════
# 7. スクリプト
# ══════════════════════════════════════════════════
story += [chap("7","スクリプト","scripts/  Windows Automation", color=AMBER), SP(8)]

story.append(secbar("auto-sync.ps1  ―  Windows 自動同期スクリプト", bg=LAMBER, bar=AMBER))
story.append(SP(5))
story.append(kv([
    ("目的",      "Windows PC 上の C:\\Claude を GitHub master と自動同期する"),
    ("動作",      "git fetch → ローカル/リモートのハッシュ比較 → 差分あれば git pull"),
    ("ログ",      "scripts/sync.log にタイムスタンプ付きで全操作を記録"),
    ("対象",      "master ブランチ（固定）"),
], c1=32*mm, s1=LAMBER, s2=WHITE))
story.append(SP(10))

story.append(secbar("setup-task-scheduler.ps1  ―  タスクスケジューラ登録", bg=LAMBER, bar=AMBER))
story.append(SP(5))
story.append(kv([
    ("目的",      "auto-sync.ps1 を Windows タスクスケジューラに登録し 15 分ごとに自動実行"),
    ("実行権限",  "管理者権限（Run as Administrator）が必要"),
    ("タスク名",  "ClaudeAutoSync"),
    ("実行間隔",  "15 分ごと（$interval 変数で変更可能）"),
    ("実行条件",  "ネットワーク接続時のみ / 遅延スタート時も実行（-StartWhenAvailable）"),
    ("タイムアウト","最大 2 分（-ExecutionTimeLimit）"),
], c1=38*mm, s1=LAMBER, s2=WHITE))
story.append(SP(14))

# ══════════════════════════════════════════════════
# 8. ワークフロールール
# ══════════════════════════════════════════════════
story += [chap("8","ワークフロールール","CLAUDE.md  Workflow Rules"), SP(8)]

story.append(secbar("開発ワークフロー  6 原則", bg=XBLUE, bar=BLUE))
story.append(SP(5))
story.append(dtbl(
    ["#","原則","内容"],
    [
        ["1","Plan Mode を使う",
         "調査フェーズと実装フェーズを分離する。いきなりコードを書かない。"],
        ["2","小さく実装・すぐ検証",
         "小さく作る → 動作確認 → 改善 のサイクルを繰り返す。"],
        ["3","Todo リストで管理",
         "優先順位と進捗を常に可視化する。"],
        ["4","Commit は頻繁に",
         "1 タスク完了ごとにすぐコミット。複数タスクをまとめない。"],
        ["5","ブランチ戦略",
         "main（本番）/ feature/*（機能）/ spike/*（実験）を使い分ける。"],
        ["6","/compact を定期的に",
         "コンテキスト圧縮で作業余白を確保。実行前に重要情報を CLAUDE.md へ退避。"],
    ],
    [8*mm, 44*mm, CW-52*mm]
))
story.append(SP(10))

story.append(secbar("セキュリティポリシー", bg=LRED, bar=RED))
story.append(SP(5))
story.append(kv([
    (".env・認証情報", "絶対にコミットしない。.gitignore と deny ルールで二重防止。"),
    ("外部副作用",     "DB 操作・外部 API 呼び出しはユーザー確認後に実行する。"),
    ("sudo",          "settings.json の deny ルールで強制禁止。"),
    ("自動保護",       "Stop フック（auto-push.sh）がセッション終了時に自動 push。"),
], c1=38*mm, s1=LRED, s2=WHITE))
story.append(SP(14))

# ══════════════════════════════════════════════════
# 9. Git 情報
# ══════════════════════════════════════════════════
story += [chap("9","Git 情報","Branches  /  Commits"), SP(8)]

story.append(secbar("ブランチ構成", bg=XBLUE, bar=BLUE))
story.append(SP(5))
story.append(dtbl(
    ["ブランチ名","種別","説明"],
    [
        ["master",                     "本番ブランチ", "安定した動作確認済みコード"],
        ["claude/quirky-newton-vlU0Z", "開発ブランチ（現在）", "経営者サポート機能を開発中"],
    ],
    [56*mm, 28*mm, CW-84*mm]
))
story.append(SP(10))

story.append(secbar("コミット履歴（全 11 件）", bg=XBLUE, bar=BLUE))
story.append(SP(5))
story.append(dtbl(
    ["ハッシュ","ブランチ","コミットメッセージ"],
    [
        ["32dd7ca","claude/quirky-...","Add executive support department structure: agents, skills, commands"],
        ["559241d","claude/quirky-...","Add complete environment report with agent/skill architecture"],
        ["bab9c4c","claude/quirky-...","Rebuild full Japanese environment report PDF with detailed sections"],
        ["9b918db","claude/quirky-...","Update report PDF with Japanese font (IPAGothic) for proper rendering"],
        ["a3e2c86","claude/quirky-...","Add Claude Code environment report PDF and generation script"],
        ["69ae13f","claude/quirky-...","Fix PowerShell encoding: replace Japanese with English"],
        ["b4fe020","claude/quirky-...","Fix emoji encoding error in setup-task-scheduler.ps1"],
        ["69ca2bd","claude/quirky-...","Add Task Scheduler setup script for auto-sync"],
        ["71cfe7b","master",          "Add auto-sync: Stop hook + Windows PowerShell sync script"],
        ["e3cf942","master",          "Track .claude/ config files for GitHub-local sync"],
        ["1323d56","master",          "Add CLAUDE.md with workspace rules and workflow guidelines"],
    ],
    [22*mm, 28*mm, CW-50*mm]
))
story.append(SP(14))

# ── フッター ──────────────────────────────────────────────────────────
story.append(HR(MGRAY, 0.5))
story.append(SP(4))
story.append(p("本レポートは Claude Code により自動生成されました  |  2026-05-22  |  ooaku-bit / claude", sFt))

# ── ビルド ────────────────────────────────────────────────────────────
OUT = "/home/user/claude/claude_code_environment_report.pdf"
doc = Doc(
    OUT, pagesize=A4,
    leftMargin=ML, rightMargin=MR,
    topMargin=MT, bottomMargin=MB+2*mm,
    title="Claude Code 環境構成レポート",
    author="Claude Code",
    subject="ooaku-bit/claude — Executive Support Workspace",
)
doc.build(story)
print(f"PDF 生成完了: {OUT}")
