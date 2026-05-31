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

# --- Navigation Tabs (Exactly Three Specific Tabs) ---
tab1, tab2, tab3 = st.tabs([
    "🎯 RC Dwivedi and Amit dwivedi", 
    "👩‍⚖️ RC Dwivedi and Richa dwivedi", 
    "🏛️ Monthly High Court Bulletin"
])

# --- TAB 1: RC DWIVEDI AND AMIT DWIVEDI ---
with tab1:
    st.subheader("📋 Active Team Briefs: R.C. Dwivedi & Amit Dwivedi")
    
    # Filter for cases involving Amit Dwivedi
    amit_df = df[
        df["Advocate (Petitioner)"].str.contains("Amit Dwivedi", case=False, na=False) |
        df["Advocate (Respondent)"].str.contains("Amit Dwivedi", case=False, na=False)
    ]
    
    for idx, row in amit_df.iterrows():
        with st.expander(f"💼 {row['Case Number']} — {row['Petitioner/Respondent']}", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                st.write(f"**Category:** `{row['Category']}`")
                st.write(f"**Counsel for Petitioner:** {row['Advocate (Petitioner)']}")
            with c2:
                st.write(f"**Next Hearing Date:** `{row['Next Hearing Date']}`")
                st.write(f"**Current Status:** {row['Status']}")
            st.markdown("---")
            st.info(f"📝 **Order Synopsis:**\n{row['Synopsis']}")

# --- TAB 2: RC DWIVEDI AND RICHA DWIVEDI (NEW) ---
with tab2:
    st.subheader("📋 Active Team Briefs: R.C. Dwivedi & Richa Dwivedi")
    st.markdown("This panel displays high court matters argued or managed jointly by **Mr. Ramesh Chandra Dwivedi** and **Ms. Richa Dwivedi**.")
    
    # Filter for cases involving Richa Dwivedi
    richa_df = df[
        df["Advocate (Petitioner)"].str.contains("Richa Dwivedi", case=False, na=False) |
        df["Advocate (Respondent)"].str.contains("Richa Dwivedi", case=False, na=False)
    ]
    
    if not richa_df.empty:
        for idx, row in richa_df.iterrows():
            with st.expander(f"⚖️ {row['Case Number']} — {row['Petitioner/Respondent']}", expanded=True):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**Category:** `{row['Category']}`")
                    st.write(f"**Counsel on Record:** `{row['Advocate (Petitioner)']}`")
                with c2:
                    st.write(f"**Listing Timeline:** `{row['Next Hearing Date']}`")
                    st.write(f"**Registry Status:** {row['Status']}")
                st.markdown("---")
                st.success(f"📝 **Judgment / Brief Synopsis:**\n{row['Synopsis']}")
    else:
        st.warning("No active records indexed under this specific pairing.")

# --- TAB 3: MONTHLY HIGH COURT BULLETIN ---
with tab2: # Note: st.tabs assignment handles this down here
    pass # Managed dynamically by Streamlit view rendering

with tab3:
    st.subheader("🏛️ General Legal Trends: Important Educational & Criminal Matters")
    st.markdown("---")
    
    col_ed, col_crim = st.columns(2)
    with col_ed:
        st.markdown("### 📚 Featured Education Matters")
        ed_df = df[df["Category"].str.contains("Education", case=False)]
        for idx, row in ed_df.iterrows():
            st.error(f"**{row['Case Number']}**")
            st.markdown(f"**Parties:** {row['Petitioner/Respondent']}")
            st.markdown(f"**Status:** `{row['Status']}`")
            st.markdown(f"> *Brief:* {row['Synopsis']}")
            st.markdown("---")

    with col_crim:
        st.markdown("### ⚖️ Featured Criminal Matters")
        crim_df = df[df["Category"].str.contains("Criminal", case=False)]
        for idx, row in crim_df.iterrows():
            st.warning(f"**{row['Case Number']}**")
            st.markdown(f"**Parties:** {row['Petitioner/Respondent']}")
            st.markdown(f"**Status:** `{row['Status']}`")
            st.markdown(f"> *Brief:* {row['Synopsis']}")
            st.markdown("---")