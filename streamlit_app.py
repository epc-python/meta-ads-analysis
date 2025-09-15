from calculations import *
import glob
import os
import pandas as pd
import streamlit as st

# combine all csv files in the folder

folder_path = "./raw-data"

csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

df = pd.concat((pd.read_csv(file) for file in csv_files), ignore_index=True)

# remove columns that are not needed

columns_to_drop = ['Result type']

df = df.drop(columns_to_drop, axis=1)

# filter the data

spend_filter = df['Amount spent (USD)'] > 0

# Apply filters

df = df[spend_filter]

# add account name column

for col in df.columns:
    df['Account Name'] = df['Ad name'].apply(map_account)

# add creative type column

for col in df.columns:
    df['Creative Type'] = df['Ad name'].apply(map_creative_type)

# add hook column

for col in df.columns:
    df['Hook'] = df['Ad name'].apply(create_hook)


## ad creative name

for col in df.columns:
    df['Creative Name'] = df['Ad name'].apply(creative_name)

#### Generate the tables ####

# Set page config for better layout
st.set_page_config(
    page_title="Meta Creative Analysis",
    page_icon="📊",
    layout="wide"
)

# Main title

# Collapsible disclaimer section
with st.expander("⚠️ Disclaimer", expanded=False):
    st.info("Data is pulled manually from Meta Ads Manager every Monday morning. Your actual profitability may may vary because type is not included and EPCVIP may show different revenue. ")
    st.info("Filters: spend > $0 and impressions > 0. Tables are sorted by spend.")


st.markdown("---")

# Create three columns for side-by-side tables
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("AEF Video Hooks")

    aef_data = GroupByAccount(df, 'AEF', 'Video', 'Hook')
    st.dataframe(
        aef_data,
        use_container_width=True,
        height=400
    )
    st.caption(f"Total Hooks: {len(aef_data)}")

with col2:
    st.subheader("FLA Video Hooks")

    fla_data = GroupByAccount(df, 'FLA', 'Video', 'Hook')
    st.dataframe(
        fla_data,
        use_container_width=True,
        height=400
    )
    st.caption(f"Total Hooks: {len(fla_data)}")

with col3:
    st.subheader("FLD Video Hooks")

    fld_data = GroupByAccount(df, 'FLD', 'Video', 'Hook')
    st.dataframe(
        fld_data,
        use_container_width=True,
        height=400
    )
    st.caption(f"Total Hooks: {len(fld_data)}")

# Add some spacing
st.markdown("---")

# Optional: Add summary statistics
st.subheader("Summary Statistics")
summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:
    if not aef_data.empty:
        total_spend_aef = aef_data['amount_spent'].str.replace('$', '').str.replace(',', '').astype(float).sum()
        total_revenue_aef = aef_data['revenue'].str.replace('$', '').str.replace(',', '').astype(float).sum()
        profit_aef = total_revenue_aef - total_spend_aef
        
        st.metric("AEF Total Spend", f"${total_spend_aef:,.2f}")
        st.metric("AEF Total Revenue", f"${total_revenue_aef:,.2f}")
        
        st.metric("AEF Profit", f"${profit_aef:,.2f}")

with summary_col2:
    if not fla_data.empty:
        total_spend_fla = fla_data['amount_spent'].str.replace('$', '').str.replace(',', '').astype(float).sum()
        total_revenue_fla = fla_data['revenue'].str.replace('$', '').str.replace(',', '').astype(float).sum()
        profit_fla = total_revenue_fla - total_spend_fla
        
        st.metric("FLA Total Spend", f"${total_spend_fla:,.2f}")
        st.metric("FLA Total Revenue", f"${total_revenue_fla:,.2f}")
        
        st.metric("FLA Profit", f"${profit_fla:,.2f}")

with summary_col3:
    if not fld_data.empty:
        total_spend_fld = fld_data['amount_spent'].str.replace('$', '').str.replace(',', '').astype(float).sum()
        total_revenue_fld = fld_data['revenue'].str.replace('$', '').str.replace(',', '').astype(float).sum()
        profit_fld = total_revenue_fld - total_spend_fld
        
        st.metric("FLD Total Spend", f"${total_spend_fld:,.2f}")
        st.metric("FLD Total Revenue", f"${total_revenue_fld:,.2f}")
        
        st.metric("FLD Profit", f"${profit_fld:,.2f}")

# Exciting coming soon section
st.markdown("---")
st.markdown("### Coming soon")

# Create columns for better layout
feature_col1, feature_col2, feature_col3 = st.columns(3)

with feature_col1:
    st.markdown("• Grace Loan Advance")
    st.markdown("**🚀 Magic Score**: blendind multiple KPIs into one final score")
    st.markdown("• More charts & graphs")

with feature_col2:
    st.markdown("• Image ads")
    st.markdown("• Conditional formatting")

with feature_col3:
    st.markdown("• Typo detection")
    st.markdown("• Export capabilities")

## export csv here to sanity check
#df.to_csv("output.csv", index=False)