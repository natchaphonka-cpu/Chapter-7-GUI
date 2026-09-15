import gradio as gr

# ──────────────────────────────────────────────────────────────
# ICONS  (Lucide SVG inline)
# ──────────────────────────────────────────────────────────────
def ic(name, size=18, color="#3a7a3a"):
    P = {
        "check":    '<polyline points="20 6 9 17 4 12"/>',
        "x":        '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>',
        "clock":    '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
        "clip":     '<rect x="9" y="2" width="6" height="4" rx="1"/><path d="M8 4H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-2"/><path d="m9 14 2 2 4-4"/>',
        "user":     '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
        "grad":     '<path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
        "bar":      '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>',
        "star":     '<path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3z"/>',
    }
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
            f'viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
            f'{P.get(name,"")}</svg>')


# ──────────────────────────────────────────────────────────────
# LOGIC
# ──────────────────────────────────────────────────────────────
def evaluate(name, score, hours, year, mode, confirmed, topics):
    name   = (name or "").strip() or "ไม่ระบุชื่อ"
    score  = max(0, min(100, int(score  or 0)))
    hours  = max(0,          int(hours  or 0))
    topics = topics or []

    sp = score >= 60
    hp = hours >= 6
    ap = bool(confirmed)
    ok = sp and hp and ap

    chips = "".join(f'<span class="chip">{t}</span>' for t in topics) or '<span class="muted">ยังไม่ได้เลือก</span>'
    deg   = round(score * 3.6)
    rc    = "#3a7a3a" if sp else "#c03030"

    def row(passed, label, detail):
        bg  = "#f0f7f0" if passed else "#fdf2f1"
        ic_ = ic("check", 14, "#fff") if passed else ic("x", 14, "#fff")
        bc  = "#3a7a3a"               if passed else "#c03030"
        return f'''<div style="display:flex;align-items:center;gap:12px;padding:12px 16px;border-radius:12px;background:{bg};margin-bottom:8px;">
          <div style="width:28px;height:28px;border-radius:50%;background:{bc};display:flex;align-items:center;justify-content:center;flex-shrink:0;">{ic_}</div>
          <div><div style="font-size:13px;font-weight:700;color:#111;">{label}</div>
          <div style="font-size:11px;color:#666;margin-top:2px;">{detail}</div></div>
        </div>'''

    reqs = (row(sp, "คะแนนทดสอบ",        f"{score}/100 · คะแนน 60 คะแนนขึ้นไป") +
            row(hp, "ชั่วโมงการอบรม",     f"{hours} ชั่วโมง · เข้าร่วมอบรม 6 ชั่วโมงขึ้นไป") +
            row(ap, "การเข้าร่วมกิจกรรม", "ยืนยันแล้ว" if ap else "ยังไม่ได้ยืนยัน"))

    b_bg  = "#ecf6ec" if ok else "#fdf2f1"
    b_bdr = "#aed4ae" if ok else "#e8bab6"
    b_ic  = ic("check", 26, "#fff") if ok else ic("x", 26, "#fff")
    b_bc  = "#3a7a3a" if ok else "#c03030"
    b_title = "ผ่านการอบรม" if ok else "ไม่ผ่านการอบรม"
    b_sub   = "ผ่านเกณฑ์ครบทุกข้อ — Congratulations!" if ok else "กรุณาตรวจสอบเกณฑ์ที่ยังไม่ผ่าน"
    b_tc    = "#1a4e1a" if ok else "#7a1e1e"

    return f'''<div style="display:flex;flex-direction:column;gap:14px;font-family:Inter,Segoe UI,Noto Sans Thai,sans-serif;">

      <!-- profile -->
      <div class="ocard" style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;">
        <div style="width:52px;height:52px;border-radius:14px;background:#e4f0e4;display:flex;align-items:center;justify-content:center;flex-shrink:0;">{ic("user",26)}</div>
        <div style="flex:1;min-width:0;">
          <div style="font-size:17px;font-weight:800;color:#111;">{name}</div>
          <div style="font-size:12px;color:#666;margin-top:3px;">{year} · {mode}</div>
        </div>
        <div style="display:flex;flex-wrap:wrap;gap:6px;">{chips}</div>
      </div>

      <!-- score + stats -->
      <div class="grid2">

        <div class="ocard" style="display:flex;align-items:center;gap:20px;">
          <div style="width:110px;height:110px;border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center;
               background:conic-gradient({rc} {deg}deg,#ebebeb {deg}deg);">
            <div style="width:84px;height:84px;border-radius:50%;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;">
              <div style="font-size:28px;font-weight:900;color:#111;line-height:1;">{score}</div>
              <div style="font-size:11px;color:#aaa;margin-top:2px;">/100</div>
            </div>
          </div>
          <div>
            <div style="font-size:10px;font-weight:800;color:#999;letter-spacing:.9px;text-transform:uppercase;">คะแนนทดสอบ</div>
            <div style="font-size:16px;font-weight:800;color:#111;margin-top:5px;">{"ผ่านเกณฑ์" if sp else "ไม่ผ่านเกณฑ์"}</div>
            <div style="font-size:11px;color:#777;margin-top:2px;">เกณฑ์ขั้นต่ำ 60 คะแนน</div>
          </div>
        </div>

        <div style="display:flex;flex-direction:column;gap:14px;">

          <div class="ocard" style="display:flex;align-items:center;gap:13px;">
            <div style="width:40px;height:40px;border-radius:11px;background:#e4f0e4;display:flex;align-items:center;justify-content:center;flex-shrink:0;">{ic("clock",20)}</div>
            <div>
              <div style="font-size:10px;font-weight:800;color:#999;letter-spacing:.9px;text-transform:uppercase;">ชั่วโมงอบรม</div>
              <div style="font-size:20px;font-weight:900;color:#111;margin-top:2px;">{hours}<span style="font-size:11px;color:#aaa;font-weight:500;margin-left:3px;">hrs</span></div>
              <div style="font-size:10px;color:#888;margin-top:1px;">เกณฑ์ขั้นต่ำ 6 ชั่วโมง</div>
            </div>
          </div>

          <div class="ocard" style="display:flex;align-items:center;gap:13px;">
            <div style="width:40px;height:40px;border-radius:11px;background:#e4f0e4;display:flex;align-items:center;justify-content:center;flex-shrink:0;">{ic("clip",20)}</div>
            <div>
              <div style="font-size:10px;font-weight:800;color:#999;letter-spacing:.9px;text-transform:uppercase;">การเข้าร่วม</div>
              <div style="font-size:20px;font-weight:900;color:#111;margin-top:2px;">{"ครบ" if ap else "ไม่ครบ"}</div>
              <div style="font-size:10px;color:#888;margin-top:1px;">{"ยืนยันแล้ว" if ap else "ยังไม่ยืนยัน"}</div>
            </div>
          </div>

        </div>
      </div>

      <!-- requirements -->
      <div class="ocard">
        <div style="display:flex;align-items:center;gap:7px;font-size:13px;font-weight:800;color:#111;margin-bottom:14px;">
          {ic("bar",15)} <span>เกณฑ์การประเมิน</span>
        </div>
        {reqs}
      </div>

      <!-- banner -->
      <div style="display:flex;align-items:center;gap:16px;padding:18px 22px;border-radius:18px;background:{b_bg};border:1.5px solid {b_bdr};">
        <div style="width:50px;height:50px;border-radius:14px;background:{b_bc};display:flex;align-items:center;justify-content:center;flex-shrink:0;">{b_ic}</div>
        <div>
          <div style="font-size:18px;font-weight:900;color:{b_tc};">{b_title}</div>
          <div style="font-size:12px;color:#666;margin-top:3px;">{b_sub}</div>
        </div>
      </div>

    </div>'''


def reset():
    return ("", 75, 10, "ปี 3", "Online", True, ["Python","Chatbot"],
            f'''<div style="padding:68px 20px;text-align:center;background:#fff;border:1.5px dashed #ddd;border-radius:18px;font-family:Inter,sans-serif;">
              <div style="display:flex;justify-content:center;margin-bottom:12px;">{ic("star",30,"#ccc")}</div>
              <div style="font-size:16px;font-weight:800;color:#111;">พร้อมประเมินผล</div>
              <div style="font-size:12px;color:#999;margin-top:6px;">กรอกข้อมูลแล้วกด <b>ประเมินผล</b></div>
            </div>''')


# ──────────────────────────────────────────────────────────────
# CSS  — ควบคุมทุกอย่างเอง ไม่พึ่ง theme
# ──────────────────────────────────────────────────────────────
CSS = """
/* 0. reset */
*, *::before, *::after { box-sizing: border-box; margin: 0; }

:root {
    --green:  #3a7a3a;
    --green2: #2e6a2e;
    --gl:     #e4f0e4;
    --red:    #c03030;
    --border: #e2e2e2;
    --bg:     #f0f2f0;
    --card:   #ffffff;
    --text:   #111111;
    --muted:  #666666;
    --radius: 18px;
}

html, body {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: "Inter","Segoe UI","Noto Sans Thai",sans-serif !important;
    color-scheme: light !important;
}

/* container */
.gradio-container {
    max-width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    background: var(--bg) !important;
    min-height: 100vh !important;
}

/* ล้าง Gradio internals */
.gradio-container > *,
.main,.wrap,.gap,.form,.block,.panel,.contain,
[data-testid="block"] {
    background: transparent !important;
    box-shadow: none !important;
    border: none !important;
}

/* ─── header ─────────────────────────── */
.hdr {
    display: flex; align-items: center; gap: 14px;
    max-width: 1100px; margin: 0 auto;
    padding: 36px 28px 0;
}
.hdr-logo {
    width: 48px; height: 48px; border-radius: 14px;
    background: var(--green); color: #fff;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    box-shadow: 0 4px 14px rgba(58,122,58,.28);
}
.hdr-title { font-size: 20px; font-weight: 800; color: var(--text); }
.hdr-sub   { font-size: 12px; color: var(--muted); margin-top: 2px; }
.hdiv {
    height: 1px; background: #e0e0e0;
    max-width: 1100px; margin: 22px auto 28px;
}

/* ─── content wrapper ────────────────── */
.content {
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 28px 60px;
}

/* ─── section label ──────────────────── */
.slbl { display: flex; align-items: center; gap: 10px; margin-bottom: 16px; }
.snum {
    width: 28px; height: 28px; border-radius: 8px;
    background: var(--gl); color: var(--green);
    font-size: 11px; font-weight: 800;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.stitle { font-size: 15px; font-weight: 800; color: var(--text); }
.ssub   { font-size: 11px; color: #888; margin-top: 1px; }

/* ─── input grid ─────────────────────── */
.input-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    align-items: stretch;
}

/* ─── input card ─────────────────────── */
.icard {
    background: var(--card) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 20px !important;
    padding: 26px !important;
    box-shadow: 0 2px 16px rgba(0,0,0,.06) !important;
}

/* ─── ลบ gap ระหว่าง flabel กับ dropdown ── */
.icard .block {
    margin-top: 0 !important;
    padding-top: 0 !important;
}
.icard .prose, .icard .prose p {
    margin: 0 !important; padding: 0 !important;
}

/* ─── field label ────────────────────── */
.flabel {
    font-size: 13px;
    font-weight: 700;
    color: var(--text);
    display: block;
    margin-bottom: 6px;
}

/* ─── Gradio label override ──────────── */
label span,
label > span,
.block > label > span,
fieldset > span {
    font-size: 13px !important;
    font-weight: 700 !important;
    color: var(--text) !important;
    opacity: 1 !important;
    background: transparent !important;
}

/* ─── inputs ─────────────────────────── */
input:not([type=checkbox]):not([type=radio]),
textarea, select {
    background: #fafafa !important;
    border: 1.5px solid #ddd !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    min-height: 44px !important;
    padding: 0 14px !important;
    width: 100% !important;
    transition: border-color .18s, box-shadow .18s !important;
}
input:not([type=checkbox]):not([type=radio]):focus,
textarea:focus {
    border-color: var(--green) !important;
    box-shadow: 0 0 0 3px rgba(58,122,58,.12) !important;
    background: #fff !important;
    outline: none !important;
}
::placeholder { color: #bbb !important; }

/* ─── checkbox / radio ───────────────── */
input[type=checkbox], input[type=radio] {
    accent-color: var(--green) !important;
    width: 16px !important; height: 16px !important;
}

/* radio/checkbox labels */
[data-testid="radio"] label,
[data-testid="checkbox-group"] label {
    background: #fafafa !important;
    border: 1.5px solid #e0e0e0 !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: all .15s !important;
}
[data-testid="radio"] label:hover,
[data-testid="checkbox-group"] label:hover {
    background: #edf5ed !important;
    border-color: var(--green) !important;
}

/* selected */
[data-testid="radio"] label:has(input:checked),
[data-testid="checkbox-group"] label:has(input:checked) {
    background: var(--gl) !important;
    border-color: var(--green) !important;
    color: #1a4e1a !important;
}

/* dropdown popup */
ul[role=listbox], [role=listbox] {
    background: #fff !important;
    border: 1.5px solid #e0e0e0 !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 24px rgba(0,0,0,.10) !important;
}
[role=option] {
    background: #fff !important;
    color: var(--text) !important;
    font-size: 14px !important;
}
[role=option]:hover, [role=option][aria-selected=true] {
    background: #edf5ed !important;
    color: #1a4e1a !important;
}

/* ─── button row ─────────────────────── */
.btn-row {
    display: flex !important;
    gap: 14px !important;
    margin: 22px 0 30px !important;
}
.btn-row > * { flex: 1 1 0 !important; min-width: 0 !important; }

.btn-eval button {
    width: 100% !important; min-height: 52px !important;
    border-radius: 14px !important;
    background: var(--green) !important;
    color: #fff !important;
    font-size: 15px !important; font-weight: 700 !important;
    border: none !important;
    box-shadow: 0 4px 16px rgba(58,122,58,.26) !important;
    transition: transform .18s, box-shadow .18s !important;
    cursor: pointer !important;
}
.btn-eval button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(58,122,58,.36) !important;
}
.btn-clear button {
    width: 100% !important; min-height: 52px !important;
    border-radius: 14px !important;
    background: #fff !important;
    border: 1.5px solid #d0d0d0 !important;
    color: #333 !important;
    font-size: 15px !important; font-weight: 600 !important;
    cursor: pointer !important;
    transition: background .18s, border-color .18s !important;
}
.btn-clear button:hover {
    background: #f5f5f5 !important;
    border-color: #aaa !important;
}

/* ─── output ocard + grid ────────────── */
.ocard {
    background: var(--card);
    border: 1.5px solid #e8e8e8;
    border-radius: var(--radius);
    padding: 22px 24px;
    box-shadow: 0 2px 12px rgba(0,0,0,.05);
}
.grid2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
}
.chip {
    padding: 5px 12px; border-radius: 100px;
    background: var(--gl); color: #1a4e1a;
    font-size: 11px; font-weight: 700;
}
.muted { font-size: 12px; color: #bbb; }

/* ─── footer ─────────────────────────── */
.footer {
    text-align: center;
    font-size: 11px; color: #bbb;
    padding: 0 0 32px;
    max-width: 1100px; margin: 0 auto;
}

/* ─── responsive ─────────────────────── */
@media (max-width: 820px) {
    .input-grid { grid-template-columns: 1fr; }
    .grid2 { grid-template-columns: 1fr; }
}
@media (max-width: 560px) {
    .hdr   { padding: 20px 16px 0; }
    .hdiv  { margin: 16px 16px 22px; }
    .content { padding: 0 16px 48px; }
    .icard { padding: 18px !important; }
    .btn-row {
        flex-direction: column !important;
        gap: 10px !important;
    }
    .btn-row > * {
        flex: unset !important;
        width: 100% !important;
    }
    .btn-eval button,
    .btn-clear button {
        min-height: 50px !important;
        font-size: 15px !important;
        width: 100% !important;
    }
    .hdr-title { font-size: 17px; }
    .hdr-logo  { width: 42px; height: 42px; }
}
"""

HEAD = """
<meta name="color-scheme" content="light">
<style>
:root, html, body { color-scheme: light !important; }
html, body { background: #f0f2f0 !important; }

/* บังคับสีทุก label ของ Gradio ผ่าน CSS variable */
:root {
    --block-label-text-color: #111111 !important;
    --block-label-text-size: 13px !important;
    --body-text-color: #111111 !important;
    --body-text-color-subdued: #111111 !important;
    --background-fill-primary: #ffffff !important;
    --background-fill-secondary: #f5f5f5 !important;
    --color-accent: #3a7a3a !important;
}

/* fallback selector ครอบทุกรูปแบบที่ Gradio ใช้ */
label, label span, label > span,
.block > label > span,
[data-testid] > label > span,
[data-testid] > div > label > span,
.svelte-1gfkn6j, span.svelte-1gfkn6j,
.wrap > span, .container > span,
fieldset > span {
    color: #111111 !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    opacity: 1 !important;
    background: transparent !important;
}
</style>
"""

# ──────────────────────────────────────────────────────────────
# APP
# ──────────────────────────────────────────────────────────────
with gr.Blocks(
    title="Training Evaluation",
    css=CSS, head=HEAD,
    theme=gr.themes.Base(
        font=gr.themes.GoogleFont("Inter"),
    ).set(
        body_background_fill="#ffffff",
        body_background_fill_dark="#ffffff",
        body_text_color="#111111",
        body_text_color_dark="#111111",
        body_text_color_subdued="#111111",
        body_text_color_subdued_dark="#111111",
        background_fill_primary="#ffffff",        background_fill_primary_dark="#ffffff",
        background_fill_secondary="#f5f5f5",
        background_fill_secondary_dark="#f5f5f5",
        block_background_fill="#ffffff",
        block_background_fill_dark="#ffffff",
        block_label_background_fill="transparent",
        block_label_background_fill_dark="transparent",
        block_label_text_color="#111111",
        block_label_text_color_dark="#111111",
        block_border_color="#e0e0e0",
        block_border_color_dark="#e0e0e0",
        block_shadow="none",
        block_shadow_dark="none",
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
        input_placeholder_color="#bbbbbb",
        input_placeholder_color_dark="#bbbbbb",
        input_shadow="none",
        input_shadow_dark="none",
        input_shadow_focus="0 0 0 3px rgba(58,122,58,0.12)",
        input_shadow_focus_dark="0 0 0 3px rgba(58,122,58,0.12)",
        checkbox_label_background_fill="#fafafa",
        checkbox_label_background_fill_dark="#fafafa",
        checkbox_label_background_fill_selected="#e4f0e4",
        checkbox_label_background_fill_selected_dark="#e4f0e4",
        checkbox_label_border_color="#e0e0e0",
        checkbox_label_border_color_dark="#e0e0e0",
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
        button_primary_background_fill="#3a7a3a",
        button_primary_background_fill_dark="#3a7a3a",
        button_primary_background_fill_hover="#2e6a2e",
        button_primary_background_fill_hover_dark="#2e6a2e",
        button_primary_text_color="#ffffff",
        button_primary_text_color_dark="#ffffff",
        button_primary_border_color="#3a7a3a",
        button_primary_border_color_dark="#3a7a3a",
        button_secondary_background_fill="#ffffff",
        button_secondary_background_fill_dark="#ffffff",
        button_secondary_background_fill_hover="#f5f5f5",
        button_secondary_background_fill_hover_dark="#f5f5f5",
        button_secondary_text_color="#333333",
        button_secondary_text_color_dark="#333333",
        button_secondary_border_color="#d0d0d0",
        button_secondary_border_color_dark="#d0d0d0",
    )
) as demo:

    # ── Header
    gr.HTML(f"""
    <div class="hdr">
      <div class="hdr-logo">{ic("grad",22,"#fff")}</div>
      <div>
        <div class="hdr-title">Training Evaluation</div>
        <div class="hdr-sub">ระบบประเมินผลการเข้าร่วมอบรม · Student Management System</div>
      </div>
    </div>
    <div class="hdiv"></div>
    <div class="content">
    """)

    # ── Input grid (HTML wrapper)
    gr.HTML('<div class="input-grid">')

    with gr.Column(elem_classes="icard"):
        gr.HTML("""<div class="slbl">
          <div class="snum">01</div>
          <div><div class="stitle">ข้อมูลนักศึกษา</div>
          <div class="ssub">Student information</div></div>
        </div>""")
        name_input = gr.Textbox(label="ชื่อ-นามสกุล", placeholder="กรอกชื่อ-นามสกุล")
        year_input = gr.Dropdown(
            choices=["ปี 1","ปี 2","ปี 3","ปี 4"],
            value="ปี 3", label="ชั้นปี"
        )
        mode_input = gr.Radio(
            choices=["Onsite","Online"], value="Online", label="รูปแบบการอบรม"
        )

    with gr.Column(elem_classes="icard"):
        gr.HTML("""<div class="slbl">
          <div class="snum">02</div>
          <div><div class="stitle">รายละเอียดการอบรม</div>
          <div class="ssub">Training details</div></div>
        </div>""")
        score_input     = gr.Number(label="คะแนนทดสอบ (0–100)", value=75, minimum=0, maximum=100, precision=0)
        hours_input     = gr.Number(label="จำนวนชั่วโมงที่อบรม", value=10, minimum=0, precision=0)
        confirmed_input = gr.Checkbox(label="ยืนยันการเข้าร่วมกิจกรรมครบถ้วน", value=True)
        topics_input    = gr.CheckboxGroup(
            choices=["Python","AI","Chatbot","Web Application"],
            value=["Python","Chatbot"], label="หัวข้อที่สนใจ"
        )

    gr.HTML('</div>')   # /input-grid

    # ── Buttons
    with gr.Row(elem_classes="btn-row"):
        clear_btn  = gr.Button("↺  ล้างข้อมูล", variant="secondary", elem_classes="btn-clear")
        submit_btn = gr.Button("✓  ประเมินผล",  variant="primary",   elem_classes="btn-eval")

    # ── Output
    gr.HTML("""<div class="slbl" style="margin-top:4px;">
      <div class="snum">03</div>
      <div><div class="stitle">ผลการประเมิน</div>
      <div class="ssub">Evaluation result</div></div>
    </div>""")

    result = gr.HTML(value=f"""
    <div style="padding:68px 20px;text-align:center;background:#fff;border:1.5px dashed #ddd;border-radius:18px;font-family:Inter,sans-serif;">
      <div style="display:flex;justify-content:center;margin-bottom:12px;">{ic("star",30,"#ccc")}</div>
      <div style="font-size:16px;font-weight:800;color:#111;">พร้อมประเมินผล</div>
      <div style="font-size:12px;color:#999;margin-top:6px;">กรอกข้อมูลแล้วกด <b>ประเมินผล</b></div>
    </div>""")

    gr.HTML('</div>')   # /content

    gr.HTML('<div class="footer">Training Evaluation System · Chapter 7</div>')

    # ── Events
    submit_btn.click(
        fn=evaluate,
        inputs=[name_input, score_input, hours_input,
                year_input, mode_input, confirmed_input, topics_input],
        outputs=[result]
    )
    clear_btn.click(
        fn=reset,
        inputs=None,
        outputs=[name_input, score_input, hours_input,
                 year_input, mode_input, confirmed_input,
                 topics_input, result]
    )

if __name__ == "__main__":
    demo.launch()
