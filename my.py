import streamlit as st
import pandas as pd

# --- Page Layout Configuration ---
st.set_page_config(page_title="Allahabad HC Monitor", layout="wide", page_icon="⚖️")

st.title("⚖️ Allahabad High Court Dashboard & Case Monitor")
st.markdown("---")

# --- Central Data Loader ---
@st.cache_data
def load_case_data():
    # Master data sheet combining Office Briefs and General High Court Trends
    data = {
        "Case Number": [
            "WRIC No. 17230 of 2026", 
            "WRIT-C No. 24810 of 2026",
            "WRIT-A No. 1248 of 2025",
            "WRIT-A No. 44102 of 2023",
            "WRIT-A No. 19442 of 2026",
            "CRL-A No. 10224 of 2026"
        ],
        "Category": [
            "Civil / Electricity", 
            "Education (Statutory)", 
            "Education (Service)",
            "Education (Service)",
            "Education (Service)", 
            "Criminal (Appellate)"
        ],
        "Petitioner/Respondent": [
            "Smt. Munni Devi vs State of U.P. And 4 Others",
            "Dharmendra Kumar Singh vs State of U.P. and Others",
            "Sandhya Srivastava vs State Of U.P. And 3 Others",
            "Ram Naresh Prasad vs State Of U.P. And 5 Others",
            "Management Committee vs DIOS, Prayagraj",
            "State of U.P. vs Rahul and Another"
        ],
        "Advocate (Petitioner)": [
            "Amit Dwivedi, Ramesh Chandra Dwivedi",
            "Amit Dwivedi, Ramesh Chandra Dwivedi",
            "Richa Dwivedi, Ramesh Chandra Dwivedi",
            "Richa Dwivedi, R C Dwivedi",
            "Ramesh Chandra Dwivedi",
            "Government Advocate"
        ],
        "Advocate (Respondent)": [
            "C.S.C., Krishna Agarawal, Narendra Kumar Tiwari",
            "C.S.C.",
            "C.S.C.",
            "C.S.C.",
            "C.S.C., Amit Dwivedi",
            "Amit Dwivedi"
        ],
        "Next Hearing Date": [
            "2026-07-10",
            "Awaiting Upload",
            "Decided / Disposed",
            "Decided / Disposed",
            "2026-06-18",
            "2026-06-25"
        ],
        "Status": [
            "Adjourned / Listed as Fresh",
            "Order Passed (Bench: S.S. Shamsheri, J.)",
            "Disposed (Order on Merit)",
            "Disposed (Order on Merit)",
            "Pending / Counter Filed",
            "Listed for Bail Hearing"
        ],
        "Synopsis": [
            "Challenging DM order demanding Rs. 29,474 for shifting a tilted electric pole. Division Bench (Arindam Sinha, J. & Satya Veer Singh, J.) suggested electricity company reinforce foundation instead of charging petitioner. Put up on July 10.",
            "Heard before Hon'ble S.S. Shamsheri, J. Arguments presented regarding statutory compliance under the U.P. Intermediate Education framework. Order delivered on the bench; full text copy currently processing in the registry cache.",
            "Heard by Hon'ble Prakash Padia, J. Ms. Richa Dwivedi argued for the petitioner alongside lead counsel Ramesh Chandra Dwivedi regarding an arbitrary service order. High Court issued targeted binding directives to the state department.",
            "Heard by Hon'ble Vikas Budhkar, J. Ms. Richa Dwivedi held the brief of Sri R.C. Dwivedi for the writ petitioner, successfully presenting statutory protection clauses governing educational institution criteria.",
            "Challenging arbitrary suspension of institutional staff under Section 16-G(7) of the U.P. Intermediate Education Act, 1921. High Court relied on settled law that DIOS must pass a reasoned, written order.",
            "Criminal appeal involving a challenge to trial court acquittal under the new Bhartiya Nyaya Sanhita (BNS) / CrPC procedural timelines. Listed for arguments on continuous structural defense."
        ]
    }
    return pd.DataFrame(data)

df = load_case_data()

# --- Navigation Tabs (Exactly Two Combined Tabs) ---
tab1, tab2 = st.tabs([
    "🎯 RC Dwivedi, Amit dwivedi and Richa dwivedi", 
    "🏛️ Monthly High Court Bulletin"
])

# --- TAB 1: CONSOLIDATED OFFICE PANEL ---
with tab1:
    st.subheader("📋 Active Office Briefs Registry")
    st.markdown("This panel displays high court matters actively handled or defended by the joint practice team of **Mr. Ramesh Chandra Dwivedi**, **Mr. Amit Dwivedi**, and **Ms. Richa Dwivedi**.")
    st.markdown("---")
    
    # Unified filter logic to extract cases belonging to anyone on the team
    team_search_terms = ["Amit Dwivedi", "Richa Dwivedi", "Ramesh Chandra Dwivedi", "R C Dwivedi"]
    
    # Creating boolean masks for text matches
    pet_mask = df["Advocate (Petitioner)"].str.contains('|'.join(team_search_terms), case=False, na=False)
    resp_mask = df["Advocate (Respondent)"].str.contains('|'.join(team_search_terms), case=False, na=False)
    
    team_df = df[pet_mask | resp_mask]
    
    if not team_df.empty:
        # High-level metrics for the entire office
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric(label="Total Team Briefs", value=len(team_df))
        m_col2.metric(label="Active Matters", value=len(team_df[team_df["Status"].str.contains("Adjourned|Passed|Pending")]))
        m_col3.metric(label="Disposed / Closed", value=len(team_df[team_df["Status"].str.contains("Disposed")]))
        st.markdown("---")
        
        # Displaying the consolidated team cases
        for idx, row in team_df.iterrows():
            # Color indicator depending on active/disposed status
            badge = "🟢" if "Disposed" not in row["Status"] else "⚪"
            
            with st.expander(f"{badge} {row['Case Number']} — {row['Petitioner/Respondent']}", expanded=True):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**Category:** `{row['Category']}`")
                    st.write(f"**Counsel for Petitioner:** {row['Advocate (Petitioner)']}")
                    st.write(f"**Counsel for Respondent:** {row['Advocate (Respondent)']}")
                with c2:
                    st.write(f"**Next Hearing / Timeline:** `{row['Next Hearing Date']}`")
                    st.write(f"**Current Status Flag:** {row['Status']}")
                st.markdown("---")
                
                # Check which team member is highlighted and adapt the success message container
                if "Richa" in row["Advocate (Petitioner)"]:
                    st.success(f"📝 **Order Synopsis (Richa & R.C. Dwivedi):**\n{row['Synopsis']}")
                else:
                    st.info(f"📝 **Order Synopsis (Amit & R.C. Dwivedi):**\n{row['Synopsis']}")
    else:
        st.warning("No records indexed matching the office team parameters.")

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