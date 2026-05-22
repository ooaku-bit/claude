#!/usr/bin/env python3
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ---- フォント登録 ----
FONT_PATH = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"
pdfmetrics.registerFont(TTFont("IPAGothic", FONT_PATH))
F = "IPAGothic"

W, H = A4
MARGIN = 18 * mm
CW = W - 2 * MARGIN  # コンテンツ幅

# ---- カラー ----
C_NAVY   = colors.HexColor("#1a2744")
C_BLUE   = colors.HexColor("#2563eb")
C_LBLUE  = colors.HexColor("#dbeafe")
C_GREEN  = colors.HexColor("#16a34a")
C_LGREEN = colors.HexColor("#dcfce7")
C_RED    = colors.HexColor("#dc2626")
C_LRED   = colors.HexColor("#fee2e2")
C_GRAY   = colors.HexColor("#64748b")
C_LGRAY  = colors.HexColor("#f1f5f9")
C_WHITE  = colors.white
C_BLACK  = colors.HexColor("#0f172a")
C_LINE   = colors.HexColor("#cbd5e1")

def S(name, size, color=C_BLACK, align=TA_LEFT, bold=False, space_after=4, leading=None):
    return ParagraphStyle(
        name, fontName=F, fontSize=size,
        textColor=color, alignment=align,
        spaceAfter=space_after,
        leading=leading or size * 1.6,
    )

sTitle  = S("title",  20, C_WHITE,  TA_CENTER, leading=28)
sSub    = S("sub",    11, colors.HexColor("#93c5fd"), TA_CENTER)
sMeta   = S("meta",    8, colors.HexColor("#94a3b8"), TA_CENTER)
sH2     = S("h2",     13, C_BLUE,   leading=20, space_after=2)
sH3     = S("h3",     10, C_NAVY,   leading=16, space_after=2)
sBody   = S("body",    9, C_BLACK,  leading=15, space_after=2)
sCode   = S("code",    8, colors.HexColor("#1e3a5f"), leading=13, space_after=1)
sSmall  = S("small",   7, C_GRAY,   leading=12, space_after=1)
sFooter = S("footer",  7, C_GRAY,   TA_CENTER,  leading=11)

def p(text, style=sBody):
    return Paragraph(text, style)

# ヘッダーブロック（セクション見出し）
def sec(title):
    t = Table([[p(title, sH2)]], colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,-1), C_LBLUE),
        ("LEFTPADDING",(0,0),(-1,-1), 10),
        ("TOPPADDING", (0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LINEBELOW",  (0,0),(-1,-1), 2, C_BLUE),
    ]))
    return t

# キー・バリュー表
def kv(rows, c1=55*mm):
    c2 = CW - c1
    data = [[p(f"<b>{k}</b>"), p(v)] for k, v in rows]
    t = Table(data, colWidths=[c1, c2])
    t.setStyle(TableStyle([
        ("ROWBACKGROUNDS",(0,0),(-1,-1), [C_WHITE, C_LGRAY]),
        ("GRID",         (0,0),(-1,-1), 0.3, C_LINE),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("RIGHTPADDING", (0,0),(-1,-1), 8),
        ("TOPPADDING",   (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
    ]))
    return t

# コードブロック風テーブル
def codeblock(lines):
    data = [[p(ln, sCode)] for ln in lines]
    t = Table(data, colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), colors.HexColor("#f8fafc")),
        ("BOX",          (0,0),(-1,-1), 0.5, C_LINE),
        ("LEFTPADDING",  (0,0),(-1,-1), 10),
        ("RIGHTPADDING", (0,0),(-1,-1), 10),
        ("TOPPADDING",   (0,0),(-1,-1), 3),
        ("BOTTOMPADDING",(0,0),(-1,-1), 3),
    ]))
    return t

# バッジ行
def badges(items, bg=C_BLUE, fg=C_WHITE):
    bs = S("bdg", 8, fg, TA_CENTER)
    cells = [[p(f"<b>{i}</b>", bs) for i in items]]
    n = len(items)
    t = Table(cells, colWidths=[CW/n]*n)
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), bg),
        ("TOPPADDING",   (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING",  (0,0),(-1,-1), 4),
        ("RIGHTPADDING", (0,0),(-1,-1), 4),
        ("INNERGRID",    (0,0),(-1,-1), 0.5, colors.HexColor("#ffffff55")),
    ]))
    return t

# ====================================================================
story = []

# ========== カバー ==========
cover = Table(
    [[p("Claude Code ワークスペース", sTitle),
      Spacer(1,6),
      p("環境構成レポート", sSub),
      Spacer(1,4),
      p("2026年5月22日  |  リポジトリ: ooaku-bit/claude", sMeta)]],
    colWidths=[CW]
)
cover.setStyle(TableStyle([
    ("BACKGROUND",   (0,0),(-1,-1), C_NAVY),
    ("TOPPADDING",   (0,0),(-1,-1), 28),
    ("BOTTOMPADDING",(0,0),(-1,-1), 28),
    ("LEFTPADDING",  (0,0),(-1,-1), 20),
    ("RIGHTPADDING", (0,0),(-1,-1), 20),
]))
story += [cover, Spacer(1,14)]

# ========== 1. プロジェクト概要 ==========
story += [sec("1. プロジェクト概要"), Spacer(1,6)]
story.append(kv([
    ("リポジトリ",     "ooaku-bit/claude"),
    ("目的",          "Claude Code の自動化・運用ワークスペース"),
    ("作業ブランチ",   "claude/quirky-newton-vlU0Z"),
    ("ベースブランチ", "master"),
    ("リモート",       "GitHub（ローカルプロキシ経由）"),
    ("レポート作成日", "2026年5月22日"),
]))
story.append(Spacer(1,12))

# ========== 2. ディレクトリ構成 ==========
story += [sec("2. ディレクトリ構成"), Spacer(1,6)]
story.append(codeblock([
    "/home/user/claude/                        ← ワークスペースルート",
    "├── CLAUDE.md                             ← プロジェクトルール・ガイドライン",
    "├── README.md                             ← リポジトリ概要",
    "├── .gitignore                            ← Git 除外設定",
    "├── claude_code_environment_report.pdf    ← 本レポート（PDF）",
    "├── generate_report.py                    ← PDF 生成スクリプト",
    "├── scripts/",
    "│   ├── auto-sync.ps1                     ← Windows 自動同期スクリプト",
    "│   └── setup-task-scheduler.ps1          ← タスクスケジューラ設定",
    "└── .claude/                              ← Claude Code 設定ディレクトリ",
    "    ├── settings.json                     ← 権限・フック設定",
    "    ├── agents/",
    "    │   └── security-reviewer.md          ← セキュリティレビュー専用エージェント",
    "    ├── commands/",
    "    │   └── deploy.md                     ← /deploy カスタムコマンド",
    "    └── skills/",
    "        ├── code-review/SKILL.md           ← コードレビュースキル",
    "        └── testing/SKILL.md              ← テストスキル",
]))
story.append(Spacer(1,12))

# ========== 3. settings.json ==========
story += [sec("3. 権限・フック設定（.claude/settings.json）"), Spacer(1,8)]

story.append(p("<b>許可ルール（permissions.allow）</b>", sH3))
story.append(Spacer(1,3))
story.append(badges(["Read:*（全ファイル読み取り可）", "Bash:git:*（git コマンド可）",
                     "Write:*（全ファイル書き込み可）", "Edit:*（全ファイル編集可）"],
                    bg=C_GREEN))
story.append(Spacer(1,8))

story.append(p("<b>拒否ルール（permissions.deny）</b>", sH3))
story.append(Spacer(1,3))
story.append(badges(["Read:.env*（.env 読み取り禁止）",
                     "Bash:sudo:*（sudo 禁止）",
                     "Bash:rm -rf /（ルート削除禁止）"],
                    bg=C_RED))
story.append(Spacer(1,8))

story.append(p("<b>フック設定（hooks）</b>", sH3))
story.append(Spacer(1,3))
story.append(kv([
    ("トリガー",       "Stop（Claude セッション停止時）"),
    ("実行コマンド",   "bash ~/.claude/hooks/auto-push.sh"),
    ("タイムアウト",   "30 秒"),
    ("動作",          "セッション終了のたびに自動で git push を実行する"),
], c1=40*mm))
story.append(Spacer(1,12))

# ========== 4. エージェント ==========
story += [sec("4. エージェント定義（.claude/agents/）"), Spacer(1,6)]

hdr = [p("<b>ファイル名</b>"), p("<b>エージェント名</b>"), p("<b>説明</b>")]
row = [p("security-reviewer.md", sCode),
       p("security-reviewer"),
       p("OWASP Top 10 を基準にセキュリティ脆弱性を検出する専門エージェント")]
at = Table([hdr, row], colWidths=[50*mm, 42*mm, CW-92*mm])
at.setStyle(TableStyle([
    ("BACKGROUND",   (0,0),(-1,0), C_NAVY),
    ("TEXTCOLOR",    (0,0),(-1,0), C_WHITE),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[C_WHITE, C_LGRAY]),
    ("GRID",         (0,0),(-1,-1), 0.3, C_LINE),
    ("TOPPADDING",   (0,0),(-1,-1), 5),
    ("BOTTOMPADDING",(0,0),(-1,-1), 5),
    ("LEFTPADDING",  (0,0),(-1,-1), 8),
]))
story.append(at)
story.append(Spacer(1,8))

story.append(p("<b>検査項目（OWASP Top 10 準拠）</b>", sH3))
story.append(Spacer(1,3))
story.append(kv([
    ("1. Injection",          "SQL インジェクション・コマンドインジェクション・XSS"),
    ("2. 認証・セッション管理", "ハードコードされた認証情報・弱いトークン"),
    ("3. 機密データ露出",      ".env ファイル・API キー・パスワードの平文保存"),
    ("4. アクセス制御",        "権限チェック漏れ・水平権限昇格"),
    ("5. セキュリティ設定ミス", "デフォルト設定のまま・不要な機能の有効化"),
], c1=52*mm))
story.append(Spacer(1,12))

# ========== 5. カスタムコマンド ==========
story += [sec("5. カスタムコマンド（.claude/commands/）"), Spacer(1,6)]
story.append(p("<b>/deploy コマンド</b>　―　デプロイ前チェックリストを実行して安全にデプロイする", sH3))
story.append(Spacer(1,4))

steps = [
    ("ステップ 1", "テスト実行",     "全テストがパスすることを確認（npm test など）"),
    ("ステップ 2", "Lint チェック",  "コード品質チェック（npm run lint など）"),
    ("ステップ 3", "機密情報確認",   "SECRET / API_KEY などがコミットに含まれていないか検査"),
    ("ステップ 4", "ブランチ確認",   "main または release/* ブランチであることを確認"),
    ("ステップ 5", "差分最終確認",   "git diff main で変更内容を最終チェック"),
    ("ステップ 6", "タグ付け",       "バージョンタグを付与（git tag -a vYYYYMMDD）"),
    ("ステップ 7", "プッシュ",       "リモートにプッシュ（git push -u origin HEAD --tags）"),
]
sh = [p("<b>No.</b>"), p("<b>手順</b>"), p("<b>内容</b>")]
srows = [[p(s), p(f"<b>{n}</b>"), p(d)] for s,n,d in steps]
st_tbl = Table([sh]+srows, colWidths=[22*mm, 35*mm, CW-57*mm])
st_tbl.setStyle(TableStyle([
    ("BACKGROUND",   (0,0),(-1,0), C_NAVY),
    ("TEXTCOLOR",    (0,0),(-1,0), C_WHITE),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[C_WHITE, C_LGRAY]),
    ("GRID",         (0,0),(-1,-1), 0.3, C_LINE),
    ("TOPPADDING",   (0,0),(-1,-1), 4),
    ("BOTTOMPADDING",(0,0),(-1,-1), 4),
    ("LEFTPADDING",  (0,0),(-1,-1), 8),
]))
story.append(st_tbl)
story.append(Spacer(1,12))

# ========== 6. スキル ==========
story += [sec("6. スキル定義（.claude/skills/）"), Spacer(1,8)]

# code-review
story.append(p("<b>6-1.  code-review スキル</b>", sH3))
story.append(Spacer(1,3))
story.append(kv([
    ("説明",      "変更差分を分析し、バグ・セキュリティ・品質の問題を指摘する"),
    ("使用ツール", "Read・Bash・Edit"),
    ("出力形式",  "[HIGH] / [MEDIUM] / [LOW] の重大度ラベルで問題点と修正提案を提示"),
], c1=38*mm))
story.append(Spacer(1,4))
story.append(kv([
    ("正確性",   "バグ・ロジックエラー・エッジケースの検出"),
    ("セキュリティ","インジェクション・認証不備・機密情報露出の確認"),
    ("品質",     "命名・重複コード・不要な複雑性の指摘"),
    ("テスト",   "カバレッジ不足・エッジケース漏れの確認"),
], c1=38*mm))
story.append(Spacer(1,10))

# testing
story.append(p("<b>6-2.  testing スキル</b>", sH3))
story.append(Spacer(1,3))
story.append(kv([
    ("説明",      "テストを作成・実行する。describe + it + AAA パターンを使用"),
    ("使用ツール", "Read・Bash・Edit・Write"),
    ("テストパターン","Arrange（準備）→ Act（実行）→ Assert（検証）の3ステップ"),
    ("カバー範囲", "正常系・異常系・境界値のすべてを網羅"),
], c1=38*mm))
story.append(Spacer(1,4))
story.append(codeblock([
    "def test_機能名_条件_期待結果():",
    "    # Arrange（データ準備）",
    "    input_value = ...",
    "    # Act（処理実行）",
    "    result = 対象関数(input_value)",
    "    # Assert（結果検証）",
    "    assert result == expected_value",
]))
story.append(Spacer(1,12))

# ========== 7. ワークフロールール ==========
story += [sec("7. ワークフロールール（CLAUDE.md）"), Spacer(1,6)]
story.append(kv([
    ("Plan Mode を使う",       "調査フェーズと実装フェーズを明確に分離する"),
    ("小さく実装・すぐ検証",   "小さく作る → 動作確認 → 改善 のサイクルを繰り返す"),
    ("Todo リストで管理",      "優先順位と進捗を常に可視化する"),
    ("Commit 頻繁に",          "1 タスク完了ごとにすぐコミットする"),
    ("ブランチ戦略",           "main / feature/* / spike/* を目的に応じて使い分ける"),
    ("/compact を定期的に",    "コンテキストウィンドウを圧縮して作業余白を確保する"),
], c1=52*mm))
story.append(Spacer(1,12))

# ========== 8. セキュリティポリシー ==========
story += [sec("8. セキュリティポリシー"), Spacer(1,6)]
story.append(kv([
    (".env・認証情報",   "絶対にコミットしない（.gitignore + deny ルールで二重防止）"),
    ("外部副作用",       "DB 操作・API 呼び出しは必ずユーザー確認を取ってから実行する"),
    ("sudo コマンド",    "settings.json の deny ルールにより強制的に禁止"),
    ("Stop フック",      "セッション終了時に auto-push.sh が自動実行され変更を保護する"),
], c1=40*mm))
story.append(Spacer(1,12))

# ========== 9. Git コミット履歴 ==========
story += [sec("9. Git コミット履歴（直近 8 件）"), Spacer(1,6)]
commits = [
    ("a3e2c86", "claude/quirky-newton-vlU0Z", "環境構成レポート PDF と生成スクリプトを追加"),
    ("69ae13f", "claude/quirky-newton-vlU0Z", "PowerShell エンコーディング修正：日本語→英語"),
    ("b4fe020", "claude/quirky-newton-vlU0Z", "setup-task-scheduler.ps1 の絵文字エンコード修正"),
    ("69ca2bd", "claude/quirky-newton-vlU0Z", "自動同期用タスクスケジューラスクリプトを追加"),
    ("71cfe7b", "master",                     "自動同期：Stop フック + Windows PowerShell スクリプト追加"),
    ("e3cf942", "master",                     ".claude/ 設定ファイルを GitHub 同期対象に追加"),
    ("1323d56", "master",                     "ワークフロールール記載の CLAUDE.md を追加"),
    ("8559dad", "master",                     "Initial commit"),
]
ch = [p("<b>ハッシュ</b>"), p("<b>ブランチ</b>"), p("<b>コミットメッセージ</b>")]
crows = [[p(h, sCode), p(b, sSmall), p(m)] for h,b,m in commits]
ct = Table([ch]+crows, colWidths=[22*mm, 55*mm, CW-77*mm])
ct.setStyle(TableStyle([
    ("BACKGROUND",   (0,0),(-1,0), C_NAVY),
    ("TEXTCOLOR",    (0,0),(-1,0), C_WHITE),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[C_WHITE, C_LGRAY]),
    ("GRID",         (0,0),(-1,-1), 0.3, C_LINE),
    ("TOPPADDING",   (0,0),(-1,-1), 4),
    ("BOTTOMPADDING",(0,0),(-1,-1), 4),
    ("LEFTPADDING",  (0,0),(-1,-1), 8),
]))
story.append(ct)
story.append(Spacer(1,14))

# ========== フッター ==========
story.append(HRFlowable(width="100%", thickness=1, color=C_LINE))
story.append(Spacer(1,4))
story.append(p("Generated by Claude Code  |  2026-05-22  |  ooaku-bit/claude", sFooter))

# ====================================================================
OUT = "/home/user/claude/claude_code_environment_report.pdf"
doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=MARGIN, bottomMargin=MARGIN,
    title="Claude Code 環境構成レポート",
    author="Claude Code",
)
doc.build(story)
print(f"PDF 生成完了: {OUT}")
