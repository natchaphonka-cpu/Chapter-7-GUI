import gradio as gr

# ============================================================
# LUCIDE SVG ICONS (inline, stroke only)
# ============================================================

def icon(name, size=18, stroke="#3a7a3a", cls=""):
    """Return inline Lucide SVG for common icons."""
    paths = {
        # check-circle
        "check-circle": '<polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
        # x-circle
        "x-circle": '<circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>',
        # check
        "check": '<polyline points="20 6 9 17 4 12"/>',
        # x
        "x": '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>',
        # clock
        "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
        # clipboard-check
        "clipboard-check": '<rect x="9" y="2" width="6" height="4" rx="1"/><path d="M8 4H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-2"/><path d="m9 14 2 2 4-4"/>',
        # award
        "award": '<circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/>',
        # user
        "user": '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
        # graduation-cap
        "graduation-cap": '<path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
        # bar-chart
        "bar-chart": '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>',
        # circle
        "circle": '<circle cx="12" cy="12" r="10"/>',
        # sparkles
        "sparkles": '<path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3z"/>',
        # refresh-cw
        "refresh-cw": '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
        # play-circle
        "play-circle": '<circle cx="12" cy="12" r="10"/><polygon points="10 8 16 12 10 16 10 8"/>',
    }
    inner = paths.get(name, '<circle cx="12" cy="12" r="10"/>')
    cls_attr = f' class="{cls}"' if cls else ""
    return (
        f'<svg{cls_attr} xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{stroke}" '
        f'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
        f'{inner}</svg>'
    )


# ============================================================
# LOGIC
# ============================================================

def process_evaluation(name, score, hours, year, mode, confirmed, topics):
    name   = name.strip() if name else "ไม่ระบุชื่อ"
    score  = score  if score  is not None else 0
    hours  = hours  if hours  is not None else 0
    topics = topics or []

    score_pass      = score >= 60
    hours_pass      = hours >= 6
    attendance_pass = confirmed
    passed          = score_pass and hours_pass and attendance_pass

    topic_chips = "".join(
        f'<span class="chip">{t}</span>' for t in topics
    ) if topics else '<span class="no-data">ยังไม่ได้เลือก</span>'

    ring_color = "#3a7a3a" if score_pass else "#c04040"
    deg = round(score * 3.6)

    def req_row(ok, label, detail):
        cls    = "req-ok"  if ok else "req-fail"
        ic     = icon("check", 14, "#ffffff") if ok else icon("x", 14, "#ffffff")
        return f"""<div class="req-row {cls}">
            <div class="req-icon">{ic}</div>
            <div class="req-body">
                <div class="req-label">{label}</div>
                <div class="req-detail">{detail}</div>
            </div>
        </div>"""

    reqs = (
        req_row(score_pass,      "คะแนนทดสอบ",         f"{score}/100 &nbsp;·&nbsp; เกณฑ์ ≥ 60") +
        req_row(hours_pass,      "ชั่วโมงการอบรม",      f"{hours} ชั่วโมง &nbsp;·&nbsp; เกณฑ์ ≥ 6") +
        req_row(attendance_pass, "การเข้าร่วมกิจกรรม",  "ยืนยันแล้ว" if attendance_pass else "ยังไม่ได้ยืนยัน")
    )

    ok_icon   = icon("check", 26, "#ffffff")
    fail_icon = icon("x",     26, "#ffffff")
    banner = f"""<div class="banner {'b-ok' if passed else 'b-fail'}">
        <div class="b-icon">{ ok_icon if passed else fail_icon }</div>
        <div>
            <div class="b-title">{'ผ่านการอบรม' if passed else 'ไม่ผ่านการอบรม'}</div>
            <div class="b-sub">{'ผ่านเกณฑ์ครบทุกข้อ — Congratulations!' if passed else 'กรุณาตรวจสอบเกณฑ์ที่ยังไม่ผ่าน'}</div>
        </div>
    </div>"""

    clock_ic = icon("clock", 20, "#3a7a3a")
    clip_ic  = icon("clipboard-check", 20, "#3a7a3a")

    return f"""<div class="out">

        <div class="ocard profile-card">
            <div class="av">{icon("user", 26, "#3a7a3a")}</div>
            <div class="pi">
                <div class="pname">{name}</div>
                <div class="pmeta">{year} &nbsp;·&nbsp; {mode}</div>
            </div>
            <div class="chips">{topic_chips}</div>
        </div>

        <div class="grid2">

            <div class="ocard score-card">
                <div class="ring" style="background:conic-gradient({ring_color} {deg}deg,#e8e8e8 {deg}deg);">
                    <div class="ring-in">
                        <div class="snum">{score}</div>
                        <div class="sden">/100</div>
                    </div>
                </div>
                <div class="sinfo">
                    <div class="eyebrow">คะแนนทดสอบ</div>
                    <div class="slabel">{'ผ่านเกณฑ์' if score_pass else 'ไม่ผ่านเกณฑ์'}</div>
                    <div class="snote">เกณฑ์ขั้นต่ำ 60 คะแนน</div>
                </div>
            </div>

            <div class="scol">
                <div class="ocard scard">
                    <div class="sicon">{clock_ic}</div>
                    <div>
                        <div class="eyebrow">ชั่วโมงอบรม</div>
                        <div class="sval">{hours}<span>hrs</span></div>
                        <div class="snote2">เกณฑ์ ≥ 6 ชั่วโมง</div>
                    </div>
                </div>
                <div class="ocard scard">
                    <div class="sicon">{clip_ic}</div>
                    <div>
                        <div class="eyebrow">การเข้าร่วม</div>
                        <div class="sval">{'ครบ' if confirmed else 'ไม่ครบ'}</div>
                        <div class="snote2">{'ยืนยันแล้ว' if confirmed else 'ยังไม่ยืนยัน'}</div>
                    </div>
                </div>
            </div>

        </div>

        <div class="ocard">
            <div class="req-heading">
                {icon("bar-chart", 16, "#3a7a3a")}
                <span>เกณฑ์การประเมิน</span>
            </div>
            <div class="rlist">{reqs}</div>
        </div>

        {banner}
    </div>"""


def clear_all():
    empty = f"""<div class="empty">
        <div class="eico">{icon("sparkles", 32, "#cccccc")}</div>
        <div class="etitle">พร้อมประเมินผล</div>
        <div class="esub">กรอกข้อมูลแล้วกด <b>ประเมินผล</b></div>
    </div>"""
    return "", 75, 10, "ปี 3", "Online", True, ["Python", "Chatbot"], empty


# ============================================================
# THEME
# ============================================================

theme = gr.themes.Base(
    primary_hue=gr.themes.colors.green,
    secondary_hue=gr.themes.colors.gray,
    neutral_hue=gr.themes.colors.gray,
    font=gr.themes.GoogleFont("Inter"),
).set(
    body_background_fill="#ffffff",
    body_background_fill_dark="#ffffff",
    body_text_color="#111111",
    body_text_color_dark="#111111",
    body_text_color_subdued="#555555",
    body_text_color_subdued_dark="#555555",
    background_fill_primary="#ffffff",
    background_fill_primary_dark="#ffffff",
    background_fill_secondary="#f5f5f5",
    background_fill_secondary_dark="#f5f5f5",
    border_color_primary="#e0e0e0",
    border_color_primary_dark="#e0e0e0",

    input_background_fill="#fafafa",
    input_background_fill_dark="#fafafa",
    input_background_fill_focus="#ffffff",
    input_background_fill_focus_dark="#ffffff",
    input_border_color="#dddddd",
    input_border_color_dark="#dddddd",
    input_border_color_focus="#3a7a3a",
    input_border_color_focus_dark="#3a7a3a",
    input_border_color_hover="#bbbbbb",
    input_border_color_hover_dark="#bbbbbb",
    input_placeholder_color="#bbbbbb",
    input_placeholder_color_dark="#bbbbbb",
    input_shadow="none",
    input_shadow_dark="none",
    input_shadow_focus="0 0 0 3px rgba(58,122,58,0.13)",
    input_shadow_focus_dark="0 0 0 3px rgba(58,122,58,0.13)",

    block_label_text_color="#444444",
    block_label_text_color_dark="#444444",
    block_label_background_fill="transparent",
    block_label_background_fill_dark="transparent",
    block_background_fill="#ffffff",
    block_background_fill_dark="#ffffff",
    block_border_color="#e0e0e0",
    block_border_color_dark="#e0e0e0",
    block_shadow="none",
    block_shadow_dark="none",
    panel_background_fill="#ffffff",
    panel_background_fill_dark="#ffffff",
    panel_border_color="#e0e0e0",
    panel_border_color_dark="#e0e0e0",

    checkbox_label_background_fill="#fafafa",
    checkbox_label_background_fill_dark="#fafafa",
    checkbox_label_background_fill_hover="#f0f7f0",
    checkbox_label_background_fill_hover_dark="#f0f7f0",
    checkbox_label_background_fill_selected="#e8f3e8",
    checkbox_label_background_fill_selected_dark="#e8f3e8",
    checkbox_label_border_color="#e0e0e0",
    checkbox_label_border_color_dark="#e0e0e0",
    checkbox_label_border_color_hover="#3a7a3a",
    checkbox_label_border_color_hover_dark="#3a7a3a",
    checkbox_label_border_color_selected="#3a7a3a",
    checkbox_label_border_color_selected_dark="#3a7a3a",
    checkbox_label_text_color="#111111",
    checkbox_label_text_color_dark="#111111",
    checkbox_label_text_color_selected="#1a4e1a",
    checkbox_label_text_color_selected_dark="#1a4e1a",
    checkbox_background_color="#ffffff",
    checkbox_background_color_dark="#ffffff",
    checkbox_background_color_selected="#3a7a3a",
    checkbox_background_color_selected_dark="#3a7a3a",
    checkbox_border_color="#cccccc",
    checkbox_border_color_dark="#cccccc",
    checkbox_border_color_selected="#3a7a3a",
    checkbox_border_color_selected_dark="#3a7a3a",
    checkbox_border_color_focus="#3a7a3a",
    checkbox_border_color_focus_dark="#3a7a3a",

    button_primary_background_fill="#3a7a3a",
    button_primary_background_fill_dark="#3a7a3a",
    button_primary_background_fill_hover="#2e6a2e",
    button_primary_background_fill_hover_dark="#2e6a2e",
    button_primary_text_color="#ffffff",
    button_primary_text_color_dark="#ffffff",
    button_primary_border_color="#3a7a3a",
    button_primary_border_color_dark="#3a7a3a",
    button_primary_shadow="0 4px 18px rgba(58,122,58,0.28)",
    button_primary_shadow_dark="0 4px 18px rgba(58,122,58,0.28)",
    button_primary_shadow_hover="0 8px 26px rgba(58,122,58,0.38)",
    button_primary_shadow_hover_dark="0 8px 26px rgba(58,122,58,0.38)",

    button_secondary_background_fill="#ffffff",
    button_secondary_background_fill_dark="#ffffff",
    button_secondary_background_fill_hover="#f5f5f5",
    button_secondary_background_fill_hover_dark="#f5f5f5",
    button_secondary_text_color="#333333",
    button_secondary_text_color_dark="#333333",
    button_secondary_border_color="#d0d0d0",
    button_secondary_border_color_dark="#d0d0d0",
    button_secondary_border_color_hover="#aaaaaa",
    button_secondary_border_color_hover_dark="#aaaaaa",
    button_secondary_shadow="none",
    button_secondary_shadow_dark="none",
)


# ============================================================
# CSS
# ============================================================

CSS = """
*, *::before, *::after { box-sizing: border-box; }

.gradio-container {
    max-width: 100% !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    background: #f0f2f0 !important;
    min-height: 100vh !important;
}

/* ── header ──────────────────────────────────────────── */
.hdr {
    display: flex; align-items: center; gap: 14px;
    max-width: 1080px; margin: 0 auto;
    padding: 36px 28px 0;
}
.hdr-logo {
    width: 48px; height: 48px; border-radius: 14px;
    background: #3a7a3a; color: #fff;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    box-shadow: 0 4px 16px rgba(58,122,58,.30);
}
.hdr-title { font-size: 20px; font-weight: 800; color: #111; letter-spacing: -.3px; }
.hdr-sub   { font-size: 12px; color: #666; margin-top: 3px; font-weight: 500; }
.hdiv {
    height: 1px; background: #e0e0e0;
    max-width: 1080px; margin: 22px auto 30px;
}

/* ── section label ───────────────────────────────────── */
.slbl { display: flex; align-items: center; gap: 10px; margin-bottom: 18px; }
.snum {
    width: 28px; height: 28px; border-radius: 8px;
    background: #e8f3e8; color: #3a7a3a;
    font-size: 11px; font-weight: 800;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.stitle { font-size: 15px; font-weight: 800; color: #111; letter-spacing: -.2px; }
.ssub   { font-size: 11px; color: #777; margin-top: 2px; font-weight: 500; }

/* ── input card ──────────────────────────────────────── */
.icard {
    background: #fff !important;
    border: 1.5px solid #e4e4e4 !important;
    border-radius: 20px !important;
    padding: 26px !important;
    box-shadow: 0 2px 18px rgba(0,0,0,.06) !important;
}
.icard:hover {
    box-shadow: 0 6px 28px rgba(0,0,0,.10) !important;
}

/* ── Gradio labels — เข้มขึ้น ─────────────────────────── */
label span,
.block label span,
fieldset > span,
.label-wrap span {
    font-size: 13px !important;
    font-weight: 700 !important;
    color: #333 !important;
    letter-spacing: .1px !important;
    background: transparent !important;
}

/* ── inputs — text เข้มขึ้น ──────────────────────────── */
input:not([type=range]):not([type=checkbox]):not([type=radio]),
textarea, select {
    background: #fafafa !important;
    border: 1.5px solid #ddd !important;
    border-radius: 10px !important;
    color: #111 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    min-height: 44px !important;
    padding: 0 14px !important;
    transition: border-color .18s, box-shadow .18s !important;
}
input:not([type=range]):not([type=checkbox]):not([type=radio]):focus,
textarea:focus {
    border-color: #3a7a3a !important;
    box-shadow: 0 0 0 3px rgba(58,122,58,.13) !important;
    background: #fff !important;
    outline: none !important;
}
::placeholder { color: #bbb !important; font-weight: 400 !important; }
input[type=range] {
    accent-color: #3a7a3a !important;
    background: transparent !important;
    border: none !important; box-shadow: none !important;
    min-height: unset !important;
}
.gr-slider input[type=number],
[data-testid="slider"] input[type=number] {
    background: #fff !important; color: #111 !important;
    border: 1.5px solid #ddd !important; border-radius: 8px !important;
    font-weight: 700 !important; min-height: 36px !important;
}
input[type=checkbox], input[type=radio] {
    accent-color: #3a7a3a !important;
    width: 16px !important; height: 16px !important;
    min-height: unset !important;
}
.gr-radio label, .gr-checkboxgroup label,
[data-testid="radio"] label,
[data-testid="checkbox-group"] label {
    color: #111 !important; font-weight: 600 !important;
    font-size: 13px !important;
}

/* ── button row ──────────────────────────────────────── */
.btn-row {
    display: flex !important; flex-direction: row !important;
    gap: 14px !important; margin: 24px 0 32px !important;
}
.btn-row > * { flex: 1 1 0 !important; min-width: 0 !important; }
.btn-eval button, .btn-clear button {
    min-height: 52px !important; width: 100% !important;
    border-radius: 14px !important;
    font-size: 15px !important; font-weight: 700 !important;
    cursor: pointer !important; letter-spacing: -.1px !important;
}

/* ── output ──────────────────────────────────────────── */
.out { display: flex; flex-direction: column; gap: 14px; }

.ocard {
    background: #fff;
    border: 1.5px solid #e8e8e8;
    border-radius: 18px;
    padding: 22px 24px;
    box-shadow: 0 2px 14px rgba(0,0,0,.05);
}

/* profile */
.profile-card { display: flex; align-items: center; gap: 16px; flex-wrap: wrap; }
.av {
    width: 54px; height: 54px; border-radius: 16px;
    background: #e8f3e8;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.pi    { flex: 1; min-width: 0; }
.pname { font-size: 18px; font-weight: 800; color: #111; letter-spacing: -.3px; }
.pmeta { font-size: 13px; color: #555; margin-top: 3px; font-weight: 500; }
.chips { display: flex; flex-wrap: wrap; gap: 6px; margin-left: auto; }
.chip  {
    padding: 5px 12px; border-radius: 100px;
    background: #e8f3e8; color: #1a4e1a;
    font-size: 12px; font-weight: 700;
}
.no-data { font-size: 12px; color: #bbb; font-weight: 500; }

/* score + stats */
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }

.score-card {
    display: flex; align-items: center; gap: 20px;
    background: #fff; border: 1.5px solid #e8e8e8;
    border-radius: 18px; padding: 22px 24px;
    box-shadow: 0 2px 14px rgba(0,0,0,.05);
}
.ring {
    width: 112px; height: 112px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.ring-in {
    width: 86px; height: 86px; border-radius: 50%;
    background: #fff;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
}
.snum   { font-size: 30px; font-weight: 900; color: #111; line-height: 1; letter-spacing: -1px; }
.sden   { font-size: 11px; color: #aaa; margin-top: 2px; font-weight: 600; }
.sinfo  { flex: 1; }
.slabel { font-size: 16px; font-weight: 800; color: #111; margin-top: 6px; letter-spacing: -.2px; }
.snote  { font-size: 12px; color: #777; margin-top: 3px; font-weight: 500; }
.eyebrow {
    font-size: 10px; font-weight: 800;
    color: #888; letter-spacing: 1px; text-transform: uppercase;
}

.scol  { display: flex; flex-direction: column; gap: 14px; }
.scard {
    display: flex; align-items: center; gap: 14px;
    background: #fff; border: 1.5px solid #e8e8e8;
    border-radius: 18px; padding: 16px 20px;
    box-shadow: 0 2px 14px rgba(0,0,0,.05); flex: 1;
}
.sicon {
    width: 42px; height: 42px; border-radius: 12px;
    background: #e8f3e8;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.sval      { font-size: 22px; font-weight: 900; color: #111; margin-top: 3px; letter-spacing: -.5px; }
.sval span { font-size: 12px; color: #aaa; font-weight: 600; margin-left: 3px; }
.snote2    { font-size: 11px; color: #777; margin-top: 2px; font-weight: 500; }

/* requirements */
.req-heading {
    display: flex; align-items: center; gap: 7px;
    margin-bottom: 14px;
    font-size: 13px; font-weight: 800; color: #333;
    letter-spacing: -.1px;
}
.rlist { display: flex; flex-direction: column; gap: 9px; }
.req-row {
    display: flex; align-items: center; gap: 12px;
    padding: 12px 16px; border-radius: 12px;
}
.req-ok   { background: #f0f7f0; }
.req-fail { background: #fdf2f1; }
.req-icon {
    width: 30px; height: 30px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.req-ok   .req-icon { background: #3a7a3a; }
.req-fail .req-icon { background: #c04040; }
.req-label  { font-size: 13px; font-weight: 700; color: #111; }
.req-detail { font-size: 12px; color: #666; margin-top: 2px; font-weight: 500; }

/* banner */
.banner {
    display: flex; align-items: center; gap: 18px;
    padding: 20px 24px; border-radius: 18px;
}
.b-ok   { background: #edf6ed; border: 1.5px solid #b0d8b0; }
.b-fail { background: #fdf2f1; border: 1.5px solid #eabdb8; }
.b-icon {
    width: 52px; height: 52px; border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.b-ok   .b-icon { background: #3a7a3a; }
.b-fail .b-icon { background: #c04040; }
.b-title { font-size: 19px; font-weight: 900; letter-spacing: -.3px; }
.b-ok   .b-title { color: #1a4e1a; }
.b-fail .b-title { color: #7a2020; }
.b-sub  { font-size: 12px; color: #666; margin-top: 3px; font-weight: 500; }

/* empty */
.empty {
    padding: 72px 20px; text-align: center;
    background: #fff; border: 1.5px dashed #ddd; border-radius: 18px;
}
.eico   { margin-bottom: 12px; display:flex; justify-content:center; }
.etitle { font-size: 16px; font-weight: 800; color: #111; }
.esub   { font-size: 13px; color: #888; margin-top: 6px; font-weight: 500; }

.footer { text-align: center; font-size: 11px; color: #bbb; padding-top: 28px; font-weight: 500; }

/* ── responsive ──────────────────────────────────────── */
@media (max-width: 800px) {
    .grid2 { grid-template-columns: 1fr; }
    .scol  { flex-direction: row; }
}
@media (max-width: 560px) {
    .hdr { padding: 20px 16px 0; }
    .hdiv { margin: 18px 16px 24px; }
    .icard { padding: 18px !important; }
    .profile-card { flex-direction: column; align-items: flex-start; }
    .chips { margin-left: 0; }
    .scol  { flex-direction: column; }
    .score-card { flex-direction: column; align-items: center; text-align: center; }
    .btn-row { flex-direction: column !important; }
}
"""

HEAD = """
<meta name="color-scheme" content="light">
<style>
  :root, html, body { color-scheme: light !important; }
  html, body { background: #f0f2f0 !important; color: #111 !important; }
</style>
"""

# ============================================================
# APP
# ============================================================

CHECK_ICON = icon("check", 22, "#ffffff")
REFRESH_ICON = icon("refresh-cw", 18, "#444444")
GRAD_ICON = icon("graduation-cap", 22, "#ffffff")

with gr.Blocks(
    title="Training Evaluation",
    css=CSS,
    head=HEAD,
    theme=theme,
) as demo:

    gr.HTML(f"""
    <div class="hdr">
        <div class="hdr-logo">{GRAD_ICON}</div>
        <div>
            <div class="hdr-title">Training Evaluation</div>
            <div class="hdr-sub">ระบบประเมินผลการเข้าร่วมอบรม &nbsp;·&nbsp; Student Management System</div>
        </div>
    </div>
    <div class="hdiv"></div>
    """)

    with gr.Row(equal_height=False):

        with gr.Column(elem_classes="icard"):
            gr.HTML(f"""<div class="slbl">
                <div class="snum">01</div>
                <div>
                    <div class="stitle">ข้อมูลนักศึกษา</div>
                    <div class="ssub">Student information</div>
                </div>
            </div>""")
            name_input = gr.Textbox(label="ชื่อ-นามสกุล", placeholder="กรอกชื่อ-นามสกุล")
            year_input = gr.Dropdown(
                choices=["ปี 1","ปี 2","ปี 3","ปี 4"], value="ปี 3", label="ชั้นปี"
            )
            mode_input = gr.Radio(
                choices=["Onsite","Online"], value="Online", label="รูปแบบการอบรม"
            )

        with gr.Column(elem_classes="icard"):
            gr.HTML(f"""<div class="slbl">
                <div class="snum">02</div>
                <div>
                    <div class="stitle">รายละเอียดการอบรม</div>
                    <div class="ssub">Training details</div>
                </div>
            </div>""")
            score_input = gr.Slider(
                minimum=0, maximum=100, value=75, step=1, label="คะแนนทดสอบ"
            )
            hours_input     = gr.Number(label="จำนวนชั่วโมงที่อบรม", value=10, minimum=0)
            confirmed_input = gr.Checkbox(label="ยืนยันการเข้าร่วมกิจกรรมครบถ้วน", value=True)
            topics_input    = gr.CheckboxGroup(
                choices=["Python","AI","Chatbot","Web Application"],
                value=["Python","Chatbot"], label="หัวข้อที่สนใจ"
            )

    with gr.Row(elem_classes="btn-row"):
        clear_btn  = gr.Button(
            "↺  ล้างข้อมูล", variant="secondary", elem_classes="btn-clear"
        )
        submit_btn = gr.Button(
            "✓  ประเมินผล",  variant="primary",   elem_classes="btn-eval"
        )

    gr.HTML(f"""<div class="slbl" style="margin-top:8px;">
        <div class="snum">03</div>
        <div>
            <div class="stitle">ผลการประเมิน</div>
            <div class="ssub">Evaluation result</div>
        </div>
    </div>""")

    empty_html = f"""<div class="empty">
        <div class="eico">{icon("sparkles", 32, "#cccccc")}</div>
        <div class="etitle">พร้อมประเมินผล</div>
        <div class="esub">กรอกข้อมูลแล้วกด <b>ประเมินผล</b></div>
    </div>"""

    result_output = gr.HTML(value=empty_html)

    gr.HTML('<div class="footer">Training Evaluation System &nbsp;·&nbsp; Chapter 7</div>')

    submit_btn.click(
        fn=process_evaluation,
        inputs=[name_input, score_input, hours_input,
                year_input, mode_input, confirmed_input, topics_input],
        outputs=[result_output]
    )
    clear_btn.click(
        fn=clear_all,
        inputs=None,
        outputs=[name_input, score_input, hours_input,
                 year_input, mode_input, confirmed_input,
                 topics_input, result_output]
    )

if __name__ == "__main__":
    demo.launch()
