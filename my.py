import streamlit as st
import pandas as pd

# --- Page Layout Configuration ---
st.set_page_config(page_title="Allahabad HC Monitor", layout="wide", page_icon="⚖️")

st.title("⚖️ Allahabad High Court Dashboard & Case Monitor")
st.markdown("---")

# --- Central Data Loader ---
@st.cache_data
def load_case_data():
    # Master data sheet combining your office cases and monthly bulletin cases
    data = {
        "Case Number": [
            "WRIC No. 17230 of 2026", 
            "WRIT-C No. 24810 of 2026",
            "WRIT-A No. 19442 of 2026",
            "CRL-A No. 10224 of 2026"
        ],
        "Category": [
            "Civil / Electricity", 
            "Education (Statutory)", 
            "Education (Service)", 
            "Criminal (Appellate)"
        ],
        "Petitioner/Respondent": [
            "Smt. Munni Devi vs State of U.P. And 4 Others",
            "Dharmendra Kumar Singh vs State of U.P. and Others",
            "Management Committee vs DIOS, Prayagraj",
            "State of U.P. vs Rahul and Another"
        ],
        "Advocate (Petitioner)": [
            "Amit Dwivedi, Ramesh Chandra Dwivedi",
            "Amit Dwivedi, Ramesh Chandra Dwivedi",
            "Ramesh Chandra Dwivedi",
            "Government Advocate"
        ],
        "Advocate (Respondent)": [
            "C.S.C., Krishna Agarawal, Narendra Kumar Tiwari",
            "C.S.C.",
            "C.S.C., Amit Dwivedi",
            "Amit Dwivedi"
        ],
        "Next Hearing Date": [
            "2026-07-10",
            "Awaiting Upload",
            "2026-06-18",
            "2026-06-25"
        ],
        "Status": [
            "Adjourned / Listed as Fresh",
            "Order Passed (Bench: S.S. Shamsheri, J.)",
            "Pending / Counter Filed",
            "Listed for Bail Hearing"
        ],
        "Synopsis": [
            "Challenging DM order demanding Rs. 29,474 for shifting a tilted electric pole. Division Bench (Arindam Sinha, J. & Satya Veer Singh, J.) suggested electricity company reinforce foundation instead of charging petitioner. Put up on July 10.",
            "Heard before Hon'ble S.S. Shamsheri, J. Arguments presented regarding statutory compliance under the U.P. Intermediate Education framework. Order delivered on the bench; full text copy currently processing in the registry cache.",
            "Challenging arbitrary suspension of institutional staff under Section 16-G(7) of the U.P. Intermediate Education Act, 1921. High Court relied on settled law that DIOS must pass a reasoned, written order.",
            "Criminal appeal involving a challenge to trial court acquittal under the new Bhartiya Nyaya Sanhita (BNS) / CrPC procedural timelines. Listed for arguments on continuous structural defense."
        ]
    }
    return pd.DataFrame(data)

df = load_case_data()

# --- Navigation Tabs (Exactly Two Tabs) ---
tab1, tab2 = st.tabs(["🎯 My Cases (Amit Dwivedi & R C Dwivedi)", "🏛️ Monthly High Court Bulletin"])

# --- TAB 1: MY CASES (DEDICATED PANEL) ---
with tab1:
    st.subheader("📋 Active Office Briefs Registry")
    st.markdown("This panel displays cases actively handled or defended by **Mr. Amit Dwivedi** and **Mr. Ramesh Chandra Dwivedi**.")
    
    # Precise search strings to capture matching variants
    search_term_1 = "Amit Dwivedi"
    search_term_2 = "Ramesh Chandra Dwivedi"
    search_term_3 = "R C Dwivedi"
    
    # Filter for cases where either advocate is on record for Petitioner OR Respondent
    my_cases_df = df[
        df["Advocate (Petitioner)"].str.contains(search_term_1, case=False, na=False) |
        df["Advocate (Petitioner)"].str.contains(search_term_2, case=False, na=False) |
        df["Advocate (Petitioner)"].str.contains(search_term_3, case=False, na=False) |
        df["Advocate (Respondent)"].str.contains(search_term_1, case=False, na=False) |
        df["Advocate (Respondent)"].str.contains(search_term_2, case=False, na=False) |
        df["Advocate (Respondent)"].str.contains(search_term_3, case=False, na=False)
    ]
    
    if not my_cases_df.empty:
        # High-level Metrics for your practice this month
        m_col1, m_col2 = st.columns(2)
        m_col1.metric(label="Your Monitored Briefs", value=len(my_cases_df))
        m_col2.metric(label="Next Key Listing Date", value="2026-07-10")
        
        st.markdown("---")
        
        # Display as clean interactive tracking cards
        for idx, row in my_cases_df.iterrows():
            with st.expander(f"💼 {row['Case Number']} — {row['Petitioner/Respondent']}", expanded=True):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**Category:** `{row['Category']}`")
                    st.write(f"**Counsel for Petitioner:** {row['Advocate (Petitioner)']}")
                    st.write(f"**Counsel for Respondent:** {row['Advocate (Respondent)']}")
                with c2:
                    st.write(f"**Next Hearing Date:** `{row['Next Hearing Date']}`")
                    st.write(f"**Current Status:** {row['Status']}")
                
                st.markdown("---")
                st.info(f"📝 **Order / Judgment Synopsis:**\n{row['Synopsis']}")
    else:
        st.warning("No cases found matching the specified advocate names in the current database batch.")

# --- TAB 2: MONTHLY HIGH COURT BULLETIN ---
with tab2:
    st.subheader("🏛️ General Legal Trends: Important Educational & Criminal Matters")
    st.markdown("---")
    
    col_ed, col_crim = st.columns(2)
    
    with col_ed:
        st.markdown("### 📚 Featured Education Matters")
        st.caption("Focus on U.P. Intermediate Education Act, 1921 & Service Regulations")
        
        ed_df = df[df["Category"].str.contains("Education", case=False)]
        for idx, row in ed_df.iterrows():
            st.error(f"**{row['Case Number']}**")
            st.markdown(f"**Parties:** {row['Petitioner/Respondent']}")
            st.markdown(f"**Status:** `{row['Status']}`")
            st.markdown(f"> *Brief:* {row['Synopsis']}")
            st.markdown("---")
            
        st.markdown("💡 **Statutory Checkpoint:** Under Section 16-G(7), always ensure the DIOS has provided a reasoned order within the statutory timeline during suspension challenges.")

    with col_crim:
        st.markdown("### ⚖️ Featured Criminal Matters")
        st.caption("Focus on Appeals, Bail Applications, and Procedural Updates")
        
        crim_df = df[df["Category"].str.contains("Criminal", case=False)]
        for idx, row in crim_df.iterrows():
            st.warning(f"**{row['Case Number']}**")
            st.markdown(f"**Parties:** {row['Petitioner/Respondent']}")
            st.markdown(f"**Status:** `{row['Status']}`")
            st.markdown(f"> *Brief:* {row['Synopsis']}")
            st.markdown("---")
            
        st.markdown("💡 **Procedural Tip:** Cross-reference renumbered transition timelines for criminal procedural matters adjusting under evolving High Court rules.")