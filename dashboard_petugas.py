import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime, date
from zoneinfo import ZoneInfo
from io import BytesIO

from config_se2026 import LATEST_FILE

# ─────────────────────────────────────────────────────────────────────────────
# Konfigurasi Halaman
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Monitoring SE2026",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS (Tema Modern Orange #ECB65F - Mode Terang) ────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap');

/* ── Reset Global ── */
html, body, [class*="css"], [data-testid="stAppViewContainer"], [data-testid="stMain"], .main {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: #FAF8F5 !important;
    color: #2D3748 !important;
}

/* Sembunyikan Sidebar Total */
[data-testid="collapsedControl"], section[data-testid="stSidebar"] {
    display: none !important;
}

.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2.5rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
    max-width: 100%;
}

/* ── Header Banner ── */
.header-container {
    background: linear-gradient(135deg, #ECB65F 0%, #D8983B 100%);
    padding: 1.5rem 2rem;
    border-radius: 16px;
    color: #FFFFFF;
    box-shadow: 0 10px 25px -5px rgba(236, 182, 95, 0.3);
    margin-bottom: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
}

.header-title {
    font-size: 1.75rem;
    font-weight: 700;
    margin: 0;
    letter-spacing: -0.02em;
    color: #FFFFFF !important;
}

.header-subtitle {
    margin: 0.25rem 0 0 0;
    font-size: 0.875rem;
    opacity: 0.92;
    color: #FFF8EE !important;
}

.header-badge {
    background: rgba(255, 255, 255, 0.25);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.4);
    padding: 0.4rem 1rem;
    border-radius: 30px;
    font-size: 0.8rem;
    font-weight: 600;
    color: #FFFFFF;
}

/* ── Container Filter ── */
.filter-card {
    background: #FFFFFF;
    border: 1px solid #F0E6D8;
    border-radius: 14px;
    padding: 1rem 1.25rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}

/* ── KPI Cards ── */
div[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #F2E3CE !important;
    border-radius: 14px !important;
    padding: 1rem 1.25rem !important;
    box-shadow: 0 4px 12px rgba(236, 182, 95, 0.08) !important;
    border-top: 4px solid #ECB65F !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(236, 182, 95, 0.15) !important;
}

div[data-testid="stMetric"] label {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    color: #8C7355 !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    color: #2D3748 !important;
}

/* ── Styling Tab Modern ── */
div[data-baseweb="tab-list"] {
    gap: 8px;
    background-color: #EFE9E0;
    padding: 6px;
    border-radius: 12px;
    margin-bottom: 1.5rem;
}

button[data-baseweb="tab"] {
    border: none !important;
    background-color: transparent !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.25rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    color: #64748B !important;
    transition: all 0.2s ease !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background-color: #ECB65F !important;
    color: #FFFFFF !important;
    box-shadow: 0 2px 6px rgba(236, 182, 95, 0.3) !important;
}

/* ── Custom Button & Controls ── */
.stButton > button, div[data-testid="stDownloadButton"] > button {
    background-color: #ECB65F !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.25rem !important;
    transition: background-color 0.2s ease !important;
}

.stButton > button:hover, div[data-testid="stDownloadButton"] > button:hover {
    background-color: #D8983B !important;
    border: none !important;
    color: #FFFFFF !important;
}

/* ── Dataframe ── */
div[data-testid="stDataFrame"] {
    border: 1px solid #EFE9E0 !important;
    border-radius: 12px !important;
    background: #FFFFFF !important;
}

/* ── Chart Container ── */
.stPlotlyChart {
    background: #FFFFFF !important;
    border: 1px solid #F0E6D8 !important;
    border-radius: 14px !important;
    padding: 0.5rem !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
}

/* ── Expander & Alert ── */
details {
    border: 1px solid #F0E6D8 !important;
    border-radius: 10px !important;
    background: #FFFFFF !important;
}

div[data-testid="stAlert"] {
    border-radius: 10px !important;
    background-color: #FFF8EE !important;
    color: #8C5E14 !important;
    border: 1px solid #F2E3CE !important;
}

hr {
    border-color: #EFE9E0 !important;
    margin: 1.5rem 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Auto-refresh
# ─────────────────────────────────────────────────────────────────────────────
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=60 * 1000, key="auto_refresh_dashboard")
except ImportError:
    pass

# ─────────────────────────────────────────────────────────────────────────────
# Konstanta & Layout Chart
# ─────────────────────────────────────────────────────────────────────────────
IDENTITY_COLS = [
    "userId", "username", "email", "role", "regionCode",
    "total_data", "scraped_at",
    "nmkab", "nmkec", "nmdesa", "nmsls", "nmsubsls",
    "pengawas", "pencacah",
    "nama_pcl", "nama_pml",
    "jumlah_prelist_awal",
]

COL_LABELS = {
    "nama_pcl":  "Nama Pencacah",
    "nama_pml":  "Nama Pengawas",
    "nmkec":     "Kecamatan",
    "nmdesa":    "Desa",
    "nmkab":     "Kabupaten",
    "nmsls":     "SLS",
    "nmsubsls":  "Sub-SLS",
    "total_data":"Total Muatan",
    "regionCode":"Kode Wilayah",
    "Progress (%)": "Progress (%)",
    "Jumlah PCL": "Jumlah Pencacah",
    "Selisih":   "Selisih",
    "jumlah_prelist_awal": "Jumlah Prelist Awal",
}

def nice_col(c: str) -> str:
    return COL_LABELS.get(c, c)

DONE_KEYWORDS     = ["APPROVED", "SUBMITTED"]
NOT_DONE_KEYWORDS = ["OPEN", "DRAFT"]

# Tema Grafik Tetap Menggunakan Variasi Warna Visual yang Jelas (Mode Terang)
PLOT_TEMPLATE = "plotly_white"
PLOT_BG       = "rgba(0,0,0,0)"
PAPER_BG      = "rgba(0,0,0,0)"
CHART_PALETTE = [
    "#ECB65F", "#2A9D8F", "#E76F51", "#E9C46A",
    "#457B9D", "#6A4C93", "#F4A261", "#264653"
]

def styled_chart_layout(**kwargs):
    return dict(
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(color="#4A5568", family="Plus Jakarta Sans, sans-serif", size=11),
        margin=dict(l=15, r=15, t=35, b=15),
        **kwargs,
    )

# ─────────────────────────────────────────────────────────────────────────────
# Helper functions
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data(path_or_file, cache_key=None) -> pd.DataFrame:
    name = getattr(path_or_file, "name", str(path_or_file))
    if str(name).lower().endswith(".csv"):
        df = pd.read_csv(path_or_file)
    else:
        df = pd.read_excel(path_or_file)
    df.columns = [str(c).strip() for c in df.columns]
    return df

def detect_status_cols(df: pd.DataFrame) -> list:
    return [c for c in df.columns if c not in IDENTITY_COLS]

def to_numeric_safe(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    df = df.copy()
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
    return df

def rename_display(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns=nice_col)

def to_excel(df, sheet_name="Rekap"):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    return output.getvalue()

# ─────────────────────────────────────────────────────────────────────────────
# Load data otomatis
# ─────────────────────────────────────────────────────────────────────────────
if not os.path.exists(LATEST_FILE):
    st.error(
        f"Belum ada hasil scraping di `{LATEST_FILE}`. "
        "Jalankan `scrapping_sls.py` terlebih dahulu."
    )
    st.stop()

file_mtime   = os.path.getmtime(LATEST_FILE)
df_raw       = load_data(LATEST_FILE, cache_key=file_mtime)
last_updated = datetime.fromtimestamp(
    file_mtime, tz=ZoneInfo("Asia/Makassar")
).strftime("%d %b %Y · %H:%M WITA")

# ─────────────────────────────────────────────────────────────────────────────
# Header (Gaya Modern Orange Accent)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="header-container">
    <div>
        <h1 class="header-title">Monitoring SE2026 Kabupaten Ende</h1>
        <p class="header-subtitle">Progress Pencacahan & Pengawasan · Data Otomatis FASIH</p>
    </div>
    <div class="header-badge">Diperbarui: {last_updated}</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Deteksi kolom status
# ─────────────────────────────────────────────────────────────────────────────
status_cols  = detect_status_cols(df_raw)
numeric_cols = status_cols + (["total_data"] if "total_data" in df_raw.columns else [])
df_raw       = to_numeric_safe(df_raw, numeric_cols)

if not status_cols:
    st.error("Tidak ada kolom status terdeteksi dalam file data.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# Filter Bar (Tanpa Sidebar)
# ─────────────────────────────────────────────────────────────────────────────
f1, f2 = st.columns([1, 1])

with f1:
    if "nmkec" in df_raw.columns:
        all_kec = sorted(df_raw["nmkec"].dropna().unique().tolist())
        sel_kec = st.multiselect(
            "Filter Kecamatan", all_kec,
            default=[], placeholder="Pilih kecamatan...",
        )
    else:
        sel_kec = []

with f2:
    if "nama_pcl" in df_raw.columns:
        all_pcl = sorted(df_raw["nama_pcl"].dropna().unique().tolist())
        sel_pcl = st.multiselect(
            "Filter Pencacah", all_pcl,
            default=[], placeholder="Cari nama pencacah...",
        )
    else:
        sel_pcl = []

df = df_raw.copy()
if sel_kec and "nmkec" in df.columns:
    df = df[df["nmkec"].isin(sel_kec)]
if sel_pcl and "nama_pcl" in df.columns:
    df = df[df["nama_pcl"].isin(sel_pcl)]

if len(df) < len(df_raw):
    st.caption(f"Filter Aktif: Menampilkan {len(df):,} dari {len(df_raw):,} baris data.")

# ─────────────────────────────────────────────────────────────────────────────
# KPI Cards
# ─────────────────────────────────────────────────────────────────────────────
n_pcl      = df["nama_pcl"].nunique() if "nama_pcl" in df.columns else 0
n_pml      = df["nama_pml"].nunique() if "nama_pml" in df.columns else 0
n_desa     = df["nmdesa"].nunique()   if "nmdesa"   in df.columns else 0
total_data = int(df["total_data"].sum()) if "total_data" in df.columns else int(df[status_cols].sum().sum())

done_cols     = [c for c in status_cols if any(k in c.upper() for k in DONE_KEYWORDS)]
draft_cols    = [c for c in status_cols if "DRAFT" in c.upper()]
rejected_cols = [c for c in status_cols if any(k in c.upper() for k in ["REJECT", "DITOLAK"])]

total_draft    = int(df[draft_cols].sum().sum())    if draft_cols    else 0
total_done     = int(df[done_cols].sum().sum())     if done_cols     else 0
total_rejected = int(df[rejected_cols].sum().sum()) if rejected_cols else 0

progress_without_draft_cols = [
    c for c in status_cols
    if not any(k in c.upper() for k in ["DRAFT", "OPEN"])
]
progress_with_draft_cols = [
    c for c in status_cols
    if not any(k in c.upper() for k in ["OPEN"])
]

total_progress_without_draft = int(df[progress_without_draft_cols].sum().sum()) if progress_without_draft_cols else 0
total_progress_with_draft    = int(df[progress_with_draft_cols].sum().sum())    if progress_with_draft_cols else 0

pct_progress_without_draft = (total_progress_without_draft / total_data * 100) if total_data else 0
pct_progress_with_draft    = (total_progress_with_draft / total_data * 100)    if total_data else 0

k1, k2, k3, k4, k5, k6, k7 = st.columns(7)
k1.metric("Pencacah", f"{n_pcl:,}")
k2.metric("Pengawas", f"{n_pml:,}")
k3.metric("Desa", f"{n_desa:,}")
k4.metric("Total Muatan", f"{total_data:,}")
k5.metric("Draft", f"{total_draft:,}")
k6.metric("Selesai", f"{total_done:,}")
k7.metric("Ditolak", f"{total_rejected:,}")

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# TABS (Menggunakan Tampilan Tab Bertema Tanpa Ikon)
# ─────────────────────────────────────────────────────────────────────────────
tab_overview, tab_pcl, tab_pml, tab_target, tab_desa, tab_raw = st.tabs([
    "Distribusi Status",
    "Kinerja Pencacah",
    "Kinerja Pengawas",
    "Target & Proyeksi",
    "Rekap Wilayah",
    "Data Mentah",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Distribusi Status
# ══════════════════════════════════════════════════════════════════════════════
with tab_overview:
    st.subheader("Distribusi Status Keseluruhan")

    status_totals_all = df[status_cols].sum().sort_values(ascending=False)
    status_totals_all = status_totals_all[status_totals_all > 0]

    status_cols_without_draft = [c for c in status_cols if c not in draft_cols]
    status_totals_without_draft = df[status_cols_without_draft].sum().sort_values(ascending=False) if status_cols_without_draft else pd.Series(dtype=float)
    status_totals_without_draft = status_totals_without_draft[status_totals_without_draft > 0]

    def render_status_distribution(status_totals_view, pct_value, title_gauge, total_progress_value, key_prefix="default"):
        if status_totals_view.empty:
            st.info("Belum ada data status bernilai lebih dari 0.")
            return

        c_bar, c_pie, c_gauge = st.columns([3, 2, 2])

        with c_bar:
            fig_bar = px.bar(
                x=status_totals_view.values,
                y=status_totals_view.index,
                orientation="h",
                labels={"x": "Jumlah Usaha", "y": ""},
                text=[f"{int(v):,}" for v in status_totals_view.values],
                color=status_totals_view.index,
                color_discrete_sequence=CHART_PALETTE,
                template=PLOT_TEMPLATE,
            )
            fig_bar.update_traces(textposition="outside", textfont_size=11)
            fig_bar.update_layout(
                **styled_chart_layout(showlegend=False, height=360),
                xaxis=dict(showgrid=True, gridcolor="#EFE9E0"),
                yaxis=dict(showgrid=False),
            )
            st.plotly_chart(fig_bar, use_container_width=True, key=f"bar_{key_prefix}")

        with c_pie:
            fig_pie = px.pie(
                values=status_totals_view.values,
                names=status_totals_view.index,
                hole=0.5,
                color_discrete_sequence=CHART_PALETTE,
                template=PLOT_TEMPLATE,
            )
            fig_pie.update_traces(
                textinfo="percent",
                textfont_size=11,
                hovertemplate="<b>%{label}</b><br>%{value:,} usaha<br>%{percent}<extra></extra>",
            )
            fig_pie.update_layout(**styled_chart_layout(
                height=360, showlegend=True,
                legend=dict(orientation="v", x=1.0),
            ))
            st.plotly_chart(fig_pie, use_container_width=True, key=f"pie_{key_prefix}")

        with c_gauge:
            st.metric("Jumlah Progress Ditangani", f"{total_progress_value:,}")

            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=pct_value,
                number={"suffix": "%", "valueformat": ".2f", "font": {"size": 34, "color": "#2D3748", "family": "JetBrains Mono"}},
                title={"text": title_gauge, "font": {"color": "#8C7355", "size": 13, "family": "Plus Jakarta Sans"}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#CBD5E1", "tickfont": {"color": "#64748B", "size": 10}},
                    "bar": {"color": "#ECB65F", "thickness": 0.28},
                    "bgcolor": "rgba(0,0,0,0)",
                    "bordercolor": "#EFE9E0",
                    "steps": [
                        {"range": [0, 50], "color": "#FFF8EE"},
                        {"range": [50, 80], "color": "#FDF0D5"},
                        {"range": [80, 100], "color": "#FCE3B4"},
                    ],
                    "threshold": {"line": {"color": "#D8983B", "width": 3}, "thickness": 0.8, "value": pct_value},
                },
            ))
            fig_gauge.update_layout(**styled_chart_layout(height=300))
            st.plotly_chart(fig_gauge, use_container_width=True, key=f"gauge_{key_prefix}")

    sub_tab1, sub_tab2 = st.tabs(["Tanpa Draft", "Termasuk Draft"])

    with sub_tab1:
        render_status_distribution(
            status_totals_without_draft,
            pct_progress_without_draft,
            "Progress Tanpa Draft",
            total_progress_without_draft,
            key_prefix="no_draft",
        )

    with sub_tab2:
        render_status_distribution(
            status_totals_all,
            pct_progress_with_draft,
            "Progress Termasuk Draft",
            total_progress_with_draft,
            key_prefix="with_draft",
        )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Per Pencacah (PCL)
# ══════════════════════════════════════════════════════════════════════════════
with tab_pcl:
    st.subheader("Monitoring Per Pencacah (PCL)")

    if "nama_pcl" not in df.columns:
        st.warning("Kolom nama_pcl tidak ditemukan dalam dataset.")
    else:
        agg_cols = status_cols + (["total_data"] if "total_data" in df.columns else [])
        agg_pcl  = df.groupby("nama_pcl")[agg_cols].sum().reset_index()

        if "total_data" in agg_pcl.columns and done_cols:
            agg_pcl["Progress (%)"] = (
                agg_pcl[done_cols].sum(axis=1)
                / agg_pcl["total_data"].replace(0, pd.NA) * 100
            ).round(1).fillna(0)
        if "total_data" in agg_pcl.columns:
            agg_pcl = agg_pcl.sort_values("total_data", ascending=False)

        max_show  = 30
        chart_pcl = agg_pcl.head(max_show)
        if len(agg_pcl) > max_show:
            st.caption(f"Menampilkan {max_show} pencacah terbesar dari total {len(agg_pcl)} pencacah.")

        fig_pcl = go.Figure()
        for i, c in enumerate(status_cols):
            if c in chart_pcl.columns:
                fig_pcl.add_trace(go.Bar(
                    name=c,
                    x=chart_pcl["nama_pcl"],
                    y=chart_pcl[c],
                    marker_color=CHART_PALETTE[i % len(CHART_PALETTE)],
                    hovertemplate="<b>%{x}</b><br>" + c + ": %{y:,}<extra></extra>",
                ))
        fig_pcl.update_layout(
            barmode="stack",
            **styled_chart_layout(height=420),
            xaxis=dict(tickangle=-40, showgrid=False, tickfont_size=10, title="Nama Pencacah"),
            yaxis=dict(showgrid=True, gridcolor="#EFE9E0", title="Jumlah Usaha"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font_size=11),
        )
        st.plotly_chart(fig_pcl, use_container_width=True)

        st.markdown("#### Detail Tabel Pencacah")

        if "total_data" in agg_pcl.columns:
            agg_pcl["_sum"]    = agg_pcl[status_cols].sum(axis=1)
            agg_pcl["Selisih"] = agg_pcl["total_data"] - agg_pcl["_sum"]
            agg_pcl = agg_pcl.drop(columns=["_sum"])

        if "nama_pml" in df.columns:
            pml_map = df.groupby("nama_pcl")["nama_pml"].first().reset_index()
            agg_pcl = agg_pcl.merge(pml_map, on="nama_pcl", how="left")
            col_order = ["nama_pcl", "nama_pml"] + [
                c for c in agg_pcl.columns if c not in ["nama_pcl", "nama_pml"]
            ]
            agg_pcl = agg_pcl[col_order]

        disp_pcl = rename_display(agg_pcl)
        col_cfg_pcl = {}

        if "Progress (%)" in disp_pcl.columns:
            col_cfg_pcl["Progress (%)"] = st.column_config.ProgressColumn(
                "Progress (%)",
                min_value=0,
                max_value=100,
                format="%.1f%%"
            )

        st.dataframe(
            disp_pcl,
            use_container_width=True,
            column_config=col_cfg_pcl,
            hide_index=True
        )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.download_button(
            label="Download Rekap Pencacah (XLSX)",
            data=to_excel(disp_pcl, sheet_name="Rekap Pencacah"),
            file_name=f"rekap_pencacah_{timestamp}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_pcl"
        )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Per Pengawas (PML)
# ══════════════════════════════════════════════════════════════════════════════
with tab_pml:
    st.subheader("Monitoring Per Pengawas (PML)")
    st.caption("Aktivitas penanganan pengawas dihitung dari total status Approve, Reject, dan Edited.")

    if "nama_pml" not in df.columns:
        st.warning("Kolom nama_pml tidak ditemukan dalam dataset.")
    else:
        approve_cols_pml = [c for c in status_cols if "APPROV" in c.upper()]
        reject_cols_pml  = [c for c in status_cols if any(k in c.upper() for k in ["REJECT", "DITOLAK"])]
        edited_cols_pml  = [c for c in status_cols if any(k in c.upper() for k in ["EDIT", "EDITED", "DIEDIT"])]

        agg_cols_pml = (
            status_cols
            + (["total_data"] if "total_data" in df.columns else [])
            + (["jumlah_prelist_awal"] if "jumlah_prelist_awal" in df.columns else [])
        )
        agg_pml = df.groupby("nama_pml")[agg_cols_pml].sum().reset_index()

        if "nama_pcl" in df.columns:
            pcl_count = df.groupby("nama_pml")["nama_pcl"].nunique().reset_index(name="Jumlah Pencacah")
            agg_pml = agg_pml.merge(pcl_count, on="nama_pml", how="left")

        agg_pml["Approve"] = agg_pml[approve_cols_pml].sum(axis=1) if approve_cols_pml else 0
        agg_pml["Reject"]  = agg_pml[reject_cols_pml].sum(axis=1)  if reject_cols_pml  else 0
        agg_pml["Edited"]  = agg_pml[edited_cols_pml].sum(axis=1)  if edited_cols_pml  else 0

        if "total_data" in agg_pml.columns:
            agg_pml["Progress Pengawas (Total Muatan) (%)"] = (
                (agg_pml["Approve"] + agg_pml["Reject"] + agg_pml["Edited"])
                / agg_pml["total_data"].replace(0, pd.NA) * 100
            ).round(1).fillna(0)

        if "jumlah_prelist_awal" in agg_pml.columns:
            agg_pml["Progress Pengawas (Jumlah Prelist Awal) (%)"] = (
                (agg_pml["Approve"] + agg_pml["Reject"] + agg_pml["Edited"])
                / agg_pml["jumlah_prelist_awal"].replace(0, pd.NA) * 100
            ).round(1).fillna(0)

        if "Progress Pengawas (Total Muatan) (%)" in agg_pml.columns:
            agg_pml = agg_pml.sort_values("Progress Pengawas (Total Muatan) (%)", ascending=False)
        else:
            agg_pml = agg_pml.sort_values("Approve", ascending=False)

        total_approve_pml = int(agg_pml["Approve"].sum()) if "Approve" in agg_pml.columns else 0
        total_reject_pml  = int(agg_pml["Reject"].sum())  if "Reject"  in agg_pml.columns else 0
        total_edited_pml  = int(agg_pml["Edited"].sum())  if "Edited"  in agg_pml.columns else 0

        p1, p2, p3, p4 = st.columns(4)
        p1.metric("Total Pengawas", f"{agg_pml['nama_pml'].nunique():,}")
        p2.metric("Approve", f"{total_approve_pml:,}")
        p3.metric("Reject", f"{total_reject_pml:,}")
        p4.metric("Edited", f"{total_edited_pml:,}")

        st.divider()

        chart_cols_pml = [c for c in ["Approve", "Reject", "Edited"] if c in agg_pml.columns]
        if chart_cols_pml:
            chart_pml = agg_pml.copy()
            chart_pml["Total Ditangani"] = chart_pml[chart_cols_pml].sum(axis=1)
            chart_pml = chart_pml.sort_values("Total Ditangani", ascending=False)

            top_n_pml = 30
            chart_pml_top = chart_pml.head(top_n_pml)

            melt_pml = chart_pml_top.melt(
                id_vars="nama_pml",
                value_vars=chart_cols_pml,
                var_name="Status",
                value_name="Jumlah"
            )

            fig_pml = px.bar(
                melt_pml,
                x="Jumlah",
                y="nama_pml",
                color="Status",
                orientation="h",
                barmode="stack",
                text="Jumlah",
                color_discrete_map={
                    "Approve": "#2A9D8F",
                    "Reject": "#E76F51",
                    "Edited": "#ECB65F",
                },
                template=PLOT_TEMPLATE,
                labels={"nama_pml": "", "Jumlah": "Jumlah Muatan"},
            )
            fig_pml.update_traces(textposition="inside", textfont_size=10)
            fig_pml.update_layout(
                **styled_chart_layout(height=max(380, len(chart_pml_top) * 28)),
                xaxis=dict(showgrid=True, gridcolor="#EFE9E0"),
                yaxis=dict(showgrid=False, categoryorder="total ascending"),
                legend=dict(orientation="h", y=1.08),
            )
            st.plotly_chart(fig_pml, use_container_width=True)

        st.markdown("#### Detail Tabel Pengawas")

        show_cols_pml = ["nama_pml"]
        if "Jumlah Pencacah" in agg_pml.columns:
            show_cols_pml.append("Jumlah Pencacah")
        if "total_data" in agg_pml.columns:
            show_cols_pml.append("total_data")
        if "jumlah_prelist_awal" in agg_pml.columns:
            show_cols_pml.append("jumlah_prelist_awal")
        show_cols_pml += ["Approve", "Reject", "Edited"]
        if "Progress Pengawas (Total Muatan) (%)" in agg_pml.columns:
            show_cols_pml.append("Progress Pengawas (Total Muatan) (%)")

        disp_pml = agg_pml[show_cols_pml].rename(columns={
            "nama_pml": "Nama Pengawas",
            "total_data": "Total Muatan",
            "jumlah_prelist_awal": "Jumlah Prelist Awal",
        })

        col_cfg_pml = {}
        if "Progress Pengawas (Total Muatan) (%)" in disp_pml.columns:
            col_cfg_pml["Progress Pengawas (Total Muatan) (%)"] = st.column_config.ProgressColumn(
                "Progress Pengawas (%)",
                min_value=0,
                max_value=100,
                format="%.1f%%"
            )

        st.dataframe(
            disp_pml,
            use_container_width=True,
            column_config=col_cfg_pml,
            hide_index=True
        )

        st.download_button(
            label="Download Rekap Pengawas (XLSX)",
            data=to_excel(disp_pml, sheet_name="Rekap Pengawas"),
            file_name=f"rekap_pengawas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_pml"
        )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — Target Harian & Proyeksi
# ══════════════════════════════════════════════════════════════════════════════
with tab_target:
    st.subheader("Jadwal & Target Proyeksi Penyelesaian")

    if "nama_pcl" not in df.columns or "total_data" not in df.columns:
        st.warning("Kolom nama_pcl atau total_data tidak ditemukan.")
    else:
        today_wit = datetime.now(ZoneInfo("Asia/Jayapura")).date()

        if "milestone_editor_data" not in st.session_state:
            st.session_state["milestone_editor_data"] = pd.DataFrame([
                {"Tanggal": date(2026, 6, 30), "Target (%)": 25},
                {"Tanggal": date(2026, 7, 14), "Target (%)": 40},
                {"Tanggal": date(2026, 7, 31), "Target (%)": 75},
                {"Tanggal": date(2026, 8, 31), "Target (%)": 100},
            ])

        milestone_df = st.data_editor(
            st.session_state["milestone_editor_data"],
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            key="milestone_editor",
            column_config={
                "Tanggal": st.column_config.DateColumn("Tanggal Target", format="DD MMM YYYY"),
                "Target (%)": st.column_config.NumberColumn("Target (%)", min_value=0, max_value=100, step=1),
            },
        )
        milestone_df = milestone_df.dropna().copy()
        milestone_df["Tanggal"] = pd.to_datetime(milestone_df["Tanggal"]).dt.date
        milestone_df = milestone_df.sort_values("Tanggal").reset_index(drop=True)

        if not milestone_df.empty:
            total_data_all = float(df["total_data"].sum())
            total_progress_nodraft = float(df[progress_without_draft_cols].sum().sum()) if progress_without_draft_cols else 0.0
            pct_now = (total_progress_nodraft / total_data_all * 100) if total_data_all else 0.0

            status_rows = []
            next_milestone = None
            for _, m in milestone_df.iterrows():
                m_date, m_pct = m["Tanggal"], m["Target (%)"]
                if m_date < today_wit:
                    status = "Tercapai" if pct_now >= m_pct else "Belum Tercapai (Lewat)"
                elif m_date == today_wit:
                    status = "Tercapai" if pct_now >= m_pct else "Target Hari Ini"
                else:
                    status = "Akan Datang"
                    if next_milestone is None and pct_now < m_pct:
                        next_milestone = (m_date, m_pct)
                status_rows.append({
                    "Tanggal": m_date,
                    "Target (%)": m_pct,
                    "Target Muatan": int(total_data_all * m_pct / 100),
                    "Status": status,
                })
            milestone_status_df = pd.DataFrame(status_rows)

            st.dataframe(milestone_status_df, use_container_width=True, hide_index=True)

            fig_curve = go.Figure()
            fig_curve.add_trace(go.Scatter(
                x=pd.to_datetime(milestone_status_df["Tanggal"]),
                y=milestone_status_df["Target (%)"],
                mode="lines+markers+text",
                name="Rencana",
                text=[f"{p}%" for p in milestone_status_df["Target (%)"]],
                textposition="top center",
                line=dict(color="#D8983B", width=3, dash="dot"),
                marker=dict(size=8, color="#D8983B"),
            ))
            fig_curve.add_trace(go.Scatter(
                x=[pd.to_datetime(today_wit)],
                y=[pct_now],
                mode="markers+text",
                name="Realisasi Saat Ini",
                text=[f"{pct_now:.1f}%"],
                textposition="bottom center",
                marker=dict(size=14, color="#2A9D8F", symbol="circle"),
            ))
            fig_curve.update_layout(
                **styled_chart_layout(height=340),
                xaxis=dict(title="Tanggal", showgrid=False),
                yaxis=dict(title="Progress (%)", range=[0, 108], showgrid=True, gridcolor="#EFE9E0"),
                legend=dict(orientation="h", y=1.12),
            )
            st.plotly_chart(fig_curve, use_container_width=True)

            st.divider()

            if next_milestone is not None:
                target_date, target_pct = next_milestone
                days_left = max((target_date - today_wit).days, 1)

                target_value_team = total_data_all * target_pct / 100
                sisa_team = max(target_value_team - total_progress_nodraft, 0)
                target_harian_team = int(np.ceil(sisa_team / days_left))

                tk1, tk2, tk3, tk4 = st.columns(4)
                tk1.metric("Progress Realisasi", f"{pct_now:.1f}%")
                tk2.metric("Milestone Target", f"{target_pct:.0f}%")
                tk3.metric("Sisa Waktu", f"{days_left} hari")
                tk4.metric("Target Harian Tim", f"{target_harian_team:,}/hari")

                st.divider()

                agg_t = df.groupby("nama_pcl")[status_cols + ["total_data"]].sum().reset_index()
                agg_t["Progres"] = agg_t[progress_without_draft_cols].sum(axis=1) if progress_without_draft_cols else 0
                agg_t["Progress (%)"] = (
                    agg_t["Progres"] / agg_t["total_data"].replace(0, pd.NA) * 100
                ).round(1).fillna(0)
                agg_t["Target Muatan"] = (
                    agg_t["total_data"] * target_pct / 100
                ).round().astype(int)
                agg_t["Sisa Target"] = (
                    agg_t["Target Muatan"] - agg_t["Progres"]
                ).clip(lower=0)
                agg_t["Target Harian"] = np.ceil(agg_t["Sisa Target"] / days_left).astype(int)
                agg_t = agg_t.sort_values("Target Harian", ascending=False)

                st.markdown("#### Detail Target Harian per Pencacah")

                cols_show = ["nama_pcl", "total_data", "Progres", "Progress (%)",
                             "Target Muatan", "Sisa Target", "Target Harian"]
                if "nama_pml" in df.columns:
                    pml_map = df.groupby("nama_pcl")["nama_pml"].first().reset_index()
                    agg_t = agg_t.merge(pml_map, on="nama_pcl", how="left")
                    cols_show.insert(1, "nama_pml")

                disp_t = rename_display(agg_t[cols_show])

                st.dataframe(
                    disp_t,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Progress (%)": st.column_config.ProgressColumn(
                            "Progress (%)", min_value=0, max_value=100, format="%.1f%%"
                        )
                    },
                )

                st.download_button(
                    "Download Target Harian (XLSX)",
                    data=to_excel(disp_t, sheet_name="Target Harian"),
                    file_name=f"target_harian_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_target",
                )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — Per Desa
# ══════════════════════════════════════════════════════════════════════════════
with tab_desa:
    st.subheader("Rekapitualisasi Per Desa / Kelurahan")

    if "nmdesa" not in df.columns:
        st.warning("Kolom nmdesa tidak ditemukan.")
    else:
        grp_keys   = [c for c in ["nmkec", "nmdesa"] if c in df.columns]
        agg_cols_d = status_cols + (["total_data"] if "total_data" in df.columns else [])
        agg_desa   = df.groupby(grp_keys)[agg_cols_d].sum().reset_index()

        if "total_data" in agg_desa.columns and done_cols:
            agg_desa["Progress (%)"] = (
                agg_desa[done_cols].sum(axis=1)
                / agg_desa["total_data"].replace(0, pd.NA) * 100
            ).round(1).fillna(0)
            agg_desa = agg_desa.sort_values("Progress (%)", ascending=False)

        if "nama_pcl" in df.columns:
            pcl_per_desa = df.groupby(grp_keys)["nama_pcl"].nunique().reset_index(
                name="Jumlah PCL")
            agg_desa = agg_desa.merge(pcl_per_desa, on=grp_keys, how="left")

        if "Progress (%)" in agg_desa.columns:
            top_desa = 30
            hm_df    = agg_desa.head(top_desa).copy()

            label_col = "nmdesa"
            if "nmkec" in hm_df.columns:
                hm_df["_label"] = hm_df["nmkec"] + " - " + hm_df["nmdesa"]
                label_col = "_label"

            fig_desa_bar = px.bar(
                hm_df.sort_values("Progress (%)"),
                x="Progress (%)", y=label_col,
                orientation="h",
                text="Progress (%)",
                color="Progress (%)",
                color_continuous_scale=["#E76F51", "#ECB65F", "#2A9D8F"],
                range_color=[0, 100],
                template=PLOT_TEMPLATE,
                labels={label_col: ""},
            )
            fig_desa_bar.update_traces(
                texttemplate="%{text:.1f}%",
                textposition="outside",
                textfont_size=10,
            )
            fig_desa_bar.update_layout(
                **styled_chart_layout(
                    height=max(400, len(hm_df) * 22),
                    coloraxis_showscale=False,
                ),
                xaxis=dict(range=[0, 115], showgrid=False),
                yaxis=dict(showgrid=False),
            )
            st.plotly_chart(fig_desa_bar, use_container_width=True)

        st.markdown("#### Detail Tabel Desa")

        disp_desa = agg_desa.drop(columns=["_label"], errors="ignore")
        disp_desa = rename_display(disp_desa)

        col_cfg_desa = {}
        if "Progress (%)" in disp_desa.columns:
            col_cfg_desa["Progress (%)"] = st.column_config.ProgressColumn(
                "Progress (%)", min_value=0, max_value=100, format="%.1f%%"
            )

        st.dataframe(disp_desa, use_container_width=True,
                     column_config=col_cfg_desa, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — Data Mentah
# ══════════════════════════════════════════════════════════════════════════════
with tab_raw:
    st.subheader("Eksplorasi Data Mentah")

    all_cols  = df.columns.tolist()
    show_cols = st.multiselect(
        "Pilih Kolom Tampilan", all_cols,
        default=all_cols[:min(15, len(all_cols))],
        key="raw_cols",
    )

    view_df = rename_display(df[show_cols] if show_cols else df)
    st.dataframe(view_df, use_container_width=True, hide_index=True)

    timestamp_raw = datetime.now().strftime("%Y%m%d_%H%M%S")

    st.download_button(
        label="Download Data Mentah (XLSX)",
        data=to_excel(view_df, sheet_name="Data Mentah"),
        file_name=f"data_mentah_{timestamp_raw}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="download_raw"
    )