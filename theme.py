"""Neon-green dark theme and custom CSS for the CodeScribe Gradio app."""

import gradio as gr

# Palette
NEON = "#39ff14"
BG = "#07090c"
PANEL = "#0d1117"
PANEL_RAISED = "#111820"
BORDER = "#1f2a30"
TEXT = "#e6edf3"
MUTED = "#8b949e"

# A custom neon-green colour scale, so Gradio's accents (tab underline,
# focus rings, highlights) all use the same green.
neon = gr.themes.Color(
    c50="#eaffe5", c100="#c9ffbd", c200="#a3ff8f", c300="#7dff5f",
    c400="#5aff38", c500="#39ff14", c600="#2fd611", c700="#25a80d",
    c800="#1b7a0a", c900="#114d06", c950="#0a2e04",
    name="neon",
)


BASE = gr.themes.Base(
    primary_hue=neon,
    neutral_hue=gr.themes.colors.gray,
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "sans-serif"],
    font_mono=[gr.themes.GoogleFont("JetBrains Mono"), "ui-monospace", "monospace"],
    radius_size=gr.themes.sizes.radius_md,
)


def both_modes(theme, **colours):
    """Set each theme colour for light and dark mode, so the app is always dark.

    Only settings the theme actually has are included, because some settings
    have no separate dark-mode version and Gradio rejects unknown names.
    """
    result = {}
    for name, value in colours.items():
        if hasattr(theme, name):
            result[name] = value
        if hasattr(theme, name + "_dark"):
            result[name + "_dark"] = value
    return result


THEME = BASE.set(
    **both_modes(
        BASE,
        body_background_fill=BG,
        body_text_color=TEXT,
        body_text_color_subdued=MUTED,
        background_fill_primary=PANEL,
        background_fill_secondary=PANEL_RAISED,
        block_background_fill=PANEL,
        block_border_color=BORDER,
        block_label_background_fill=PANEL_RAISED,
        block_label_text_color=MUTED,
        block_title_text_color=TEXT,
        panel_background_fill=PANEL,
        border_color_primary=BORDER,
        border_color_accent=NEON,
        color_accent=NEON,
        color_accent_soft="rgba(57, 255, 20, 0.15)",
        input_background_fill=PANEL_RAISED,
        input_border_color=BORDER,
        input_border_color_focus=NEON,
        code_background_fill=PANEL,
        link_text_color=NEON,
        button_primary_background_fill=NEON,
        button_primary_background_fill_hover="#5aff38",
        button_primary_text_color="#031000",
        button_primary_border_color=NEON,
        button_secondary_background_fill="transparent",
        button_secondary_background_fill_hover="rgba(57, 255, 20, 0.08)",
        button_secondary_text_color=TEXT,
        button_secondary_border_color=BORDER,
    )
)


CSS = """
.header-row {
    align-items: flex-end !important;
}
/* ---------- Page background ---------- */
.gradio-container {
    background: #07090c !important;
}

/* ---------- Header ---------- */
.app-header h1 {
    font-family: 'JetBrains Mono', monospace;
    color: #39ff14;
    letter-spacing: 0.04em;
    text-shadow: 0 0 8px rgba(57, 255, 20, 0.6), 0 0 24px rgba(57, 255, 20, 0.3);
    margin-bottom: 0;
}
.app-header p {
    color: #8b949e;
    margin-top: 4px;
}

/* ---------- Buttons with hover glow ---------- */
button {
    transition: box-shadow 0.2s ease, transform 0.2s ease,
                border-color 0.2s ease, color 0.2s ease !important;
}
button.primary {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
button.primary:hover {
    box-shadow: 0 0 10px #39ff14, 0 0 28px rgba(57, 255, 20, 0.45);
    transform: translateY(-1px);
}
button.secondary {
    font-family: 'JetBrains Mono', monospace;
    border-width: 1px !important;
}
button.secondary:hover {
    border-color: #39ff14 !important;
    color: #39ff14 !important;
    box-shadow: 0 0 10px rgba(57, 255, 20, 0.6), 0 0 22px rgba(57, 255, 20, 0.25);
    transform: translateY(-1px);
}

/* ---------- Tabs ---------- */
button[role="tab"] {
    font-family: 'JetBrains Mono', monospace;
    color: #8b949e !important;
}
button[role="tab"][aria-selected="true"] {
    color: #39ff14 !important;
    text-shadow: 0 0 8px rgba(57, 255, 20, 0.5);
}

/* ---------- Code boxes: size ---------- */
.code-box { min-height: 470px; }
.code-box .cm-editor { height: 460px; }
.code-box .cm-scroller { overflow: auto; }

/* ---------- Code boxes: look ---------- */
.code-box, .diff-box {
    border: 1px solid #1f2a30 !important;
    border-radius: 10px !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.code-box:focus-within {
    border-color: #39ff14 !important;
    box-shadow: 0 0 0 1px #39ff14, 0 0 18px rgba(57, 255, 20, 0.25);
}
.code-box .cm-editor,
.code-box .cm-gutters {
    background: #0d1117 !important;
}
.code-box .cm-gutters {
    border-right: 1px solid #1f2a30 !important;
    color: #3d4a52 !important;
}
.code-box .cm-activeLine,
.code-box .cm-activeLineGutter {
    background: rgba(57, 255, 20, 0.05) !important;
}
.code-box .cm-cursor {
    border-left-color: #39ff14 !important;
}

/* ---------- Diff view ---------- */
.diff-box { height: 470px; overflow-y: auto; }
.diff-box * { font-family: 'JetBrains Mono', monospace; line-height: 1.4; }

/* ---------- Status line ---------- */
.status-line {
    font-family: 'JetBrains Mono', monospace;
    color: #8b949e;
}

/* ---------- Scrollbars ---------- */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #1f2a30; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #39ff14; }
"""