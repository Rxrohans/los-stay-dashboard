import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="LOS and Hospital KPIs", layout="wide")

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    # ensure numeric columns
    for col in ['length_of_stay','total_charges','total_costs']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    # drop rows missing essential metrics
    df = df.dropna(subset=[c for c in ['length_of_stay','total_charges'] if c in df.columns])
    return df


DATA_PATH = "cleaned_data.csv"

df = load_data(DATA_PATH)

st.title("🏥 MediPulse AI — Hospital KPI Dashboard (2017)")
st.markdown("Interactive dashboard: select facility, filter demographics, and drill into KPIs, diagnoses and insights.")

# Sidebar filters
with st.sidebar:
    st.header("Filters / Drilldown")
    facility_list = sorted(df['facility_name'].unique().tolist())
    facility_list.insert(0, "All Facilities")
    selected_facility = st.selectbox("Facility", facility_list)
    admission_types = ["All"] + sorted(df['type_of_admission'].dropna().unique().tolist())
    selected_admission_type = st.selectbox("Type of Admission", admission_types)
    severities = ["All"] + sorted(df['apr_severity_of_illness'].dropna().unique().tolist())
    selected_severity = st.selectbox("Severity of illness", severities)
    min_los, max_los = int(df['length_of_stay'].min()), int(df['length_of_stay'].max())
    los_range = st.slider("Length of stay range (days)", min_los, max_los, (min_los, max_los))

# Apply filters
df_view = df.copy()
if selected_facility != "All Facilities":
    df_view = df_view[df_view['facility_name'] == selected_facility]
if selected_admission_type != "All":
    df_view = df_view[df_view['type_of_admission'] == selected_admission_type]
if selected_severity != "All":
    df_view = df_view[df_view['apr_severity_of_illness'] == selected_severity]
df_view = df_view[(df_view['length_of_stay'] >= los_range[0]) & (df_view['length_of_stay'] <= los_range[1])]

# KPI cards (top row)
st.markdown("### Key metrics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    admissions = int(df_view.shape[0])
    st.metric("Admissions (count)", f"{admissions:,}")
with col2:
    avg_los = df_view['length_of_stay'].mean()
    st.metric("Avg LOS (days)", f"{avg_los:.2f}")
with col3:
    total_charges = df_view['total_charges'].sum()
    st.metric("Total Charges ($)", f"{total_charges:,.0f}")
with col4:
    total_costs = df_view['total_costs'].sum() if 'total_costs' in df_view.columns else 0
    st.metric("Total Costs ($)", f"{total_costs:,.0f}")

# Main charts
st.markdown("---")
st.markdown("## Facility KPIs & Diagnostics")

# 1) Admissions by facility (if All selected)
if selected_facility == "All Facilities":
    kpi_adm = df_view.groupby('facility_name').size().reset_index(name='admissions').sort_values('admissions', ascending=False)
    fig_adm = px.bar(kpi_adm, x='facility_name', y='admissions', title="Admissions per Facility (2017)")
    fig_adm.update_layout(xaxis_tickangle=-45, height=450)
    st.plotly_chart(fig_adm, use_container_width=True)

# 2) Avg LOS by facility (if All)
if selected_facility == "All Facilities":
    kpi_los = df_view.groupby('facility_name')['length_of_stay'].mean().reset_index(name='avg_los').sort_values('avg_los', ascending=False)
    fig_los = px.bar(kpi_los, x='facility_name', y='avg_los', title="Avg Length of Stay by Facility (days)")
    fig_los.update_layout(xaxis_tickangle=-45, height=450)
    st.plotly_chart(fig_los, use_container_width=True)

# 3) Charges vs LOS scatter (always useful)
fig_scatter = px.scatter(
    df_view,
    x='length_of_stay',
    y='total_charges',
    color='facility_name' if selected_facility == "All Facilities" else None,
    hover_data=['ccs_diagnosis_description', 'type_of_admission'],
    title="Charges vs Length of Stay (each row = patient encounter)",
    trendline='ols' if df_view.shape[0] > 20 else None
)
st.plotly_chart(fig_scatter, use_container_width=True)

# 4) Top diagnoses (for current view)
st.markdown("### Top Diagnoses")
top_diag = df_view['ccs_diagnosis_description'].value_counts().head(10).reset_index()
top_diag.columns = ['ccs_diagnosis_description','count']
fig_top_diag = px.bar(top_diag, x='count', y='ccs_diagnosis_description', orientation='h', title="Top 10 Diagnoses")
fig_top_diag.update_layout(height=450)
st.plotly_chart(fig_top_diag, use_container_width=True)

# 5) LOS distribution by top diagnosis (box)
st.markdown("### LOS distribution — top diagnoses")
top_diag_list = top_diag['ccs_diagnosis_description'].tolist()
df_top = df_view[df_view['ccs_diagnosis_description'].isin(top_diag_list)]
if not df_top.empty:
    fig_box = px.box(df_top, x='ccs_diagnosis_description', y='length_of_stay', title='LOS distribution for Top Diagnoses')
    fig_box.update_layout(xaxis_tickangle=-45, height=450)
    st.plotly_chart(fig_box, use_container_width=True)
else:
    st.write("Not enough data for LOS by diagnosis in this filtered view.")

# 6) Emergency vs non-emergency
st.markdown("### Emergency vs Non-Emergency")
if 'emergency_department_indicator' in df_view.columns:
    em_counts = df_view['emergency_department_indicator'].value_counts().reset_index()
    em_counts.columns = ['emergency_department_indicator', 'count']
    fig_em = px.pie(em_counts, names='emergency_department_indicator', values='count', title="Emergency vs Non-Emergency")
    st.plotly_chart(fig_em, use_container_width=True)

# 7) Disposition distribution
st.markdown("### Patient Disposition")
disp_counts = df_view['patient_disposition'].value_counts().reset_index()
disp_counts.columns = ['patient_disposition','count']
fig_disp = px.bar(disp_counts, x='patient_disposition', y='count', title="Patient Disposition")
fig_disp.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_disp, use_container_width=True)

# 8) Severity & Mortality overview
st.markdown("### Severity & Mortality")
if 'apr_severity_of_illness' in df_view.columns:
    fig_sev = px.histogram(df_view, x='apr_severity_of_illness', title='APR Severity of Illness Distribution')
    st.plotly_chart(fig_sev, use_container_width=True)
if 'apr_risk_of_mortality' in df_view.columns:
    fig_mor = px.histogram(df_view, x='apr_risk_of_mortality', title='APR Risk of Mortality Distribution')
    st.plotly_chart(fig_mor, use_container_width=True)

# 9) Automated insights (simple rule-based)
st.markdown("---")
st.markdown("## Automated Insights")
# compute facility-level kpis for the current filtered universe (or single facility)
kpi_fac = pd.DataFrame({
    'admissions': [df_view.shape[0]],
    'avg_los': [df_view['length_of_stay'].mean()],
    'total_charges': [df_view['total_charges'].sum()]
})

ins = []
# admissions anomaly (vs overall)
overall_adm = df.groupby('facility_name').size()
if selected_facility != "All Facilities" and selected_facility in overall_adm.index:
    fac_adm = df_view.shape[0]
    mean_adm = overall_adm.mean()
    std_adm = overall_adm.std()
    if std_adm > 0 and abs(fac_adm - mean_adm) / std_adm > 2:
        ins.append(f"⚠️ Admissions for {selected_facility} ({fac_adm}) is more than 2σ away from mean ({mean_adm:.0f}).")
# LOS anomaly (compare facility to all)
overall_los = df.groupby('facility_name')['length_of_stay'].mean()
if selected_facility != "All Facilities" and selected_facility in overall_los.index:
    fac_los = df_view['length_of_stay'].mean()
    mean_los = overall_los.mean()
    std_los = overall_los.std()
    if std_los > 0 and abs(fac_los - mean_los) / std_los > 2:
        ins.append(f"⚠️ Avg LOS for {selected_facility} ({fac_los:.1f}d) is >2σ from mean ({mean_los:.1f}d). Consider reviewing discharge workflow.")
# Cost anomaly
overall_costs = df.groupby('facility_name')['total_charges'].sum()
if selected_facility != "All Facilities" and selected_facility in overall_costs.index:
    fac_costs = df_view['total_charges'].sum()
    mean_costs = overall_costs.mean()
    std_costs = overall_costs.std()
    if std_costs > 0 and abs(fac_costs - mean_costs) / std_costs > 2:
        ins.append(f"⚠️ Total charges for {selected_facility} (${fac_costs:,.0f}) is >2σ from mean. Investigate case-mix or billing.")

if len(ins) == 0:
    st.success("No strong anomalies detected for the current view. KPIs are within expected range.")
else:
    for s in ins:
        st.warning(s)

st.markdown("### Data preview (filtered)")
st.dataframe(df_view.head(200))
