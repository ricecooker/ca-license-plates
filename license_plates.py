#
# Streamlit viewer for FOI request for personlized license plates flagged for additional review
# from https://github.com/veltman/ca-license-plates
#

import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache()
def fetch_data():
    url = 'https://raw.githubusercontent.com/veltman/ca-license-plates/master/applications.csv'

    applications_df = pd.read_csv(url).query('review_reason_code in ["1", "2", "3", "4", "5", "6", "7"]')

    reasons_df = pd.DataFrame([
        dict(code='1', reason='sexual'),
        dict(code='2', reason='hostile'),
        dict(code='3', reason='obscene'),
        dict(code='4', reason='neg group'),
        dict(code='5', reason='neg law'),
        dict(code='6', reason='deleted'),
        dict(code='7', reason='foreign'),
    ]).rename(columns={'code': 'review_reason_code'}).set_index('review_reason_code')

    result_df = applications_df.set_index('review_reason_code')\
        .join(reasons_df, how='left')\
        .reset_index()\
        .drop(columns='review_reason_code')

    return result_df


st.markdown("# Rejected CA License Plates")
df = fetch_data()

st.markdown("## Random")
random_set = df.sample(3).to_dict(orient='records')
for row in random_set:
    st.markdown(f'''
        ## {row["plate"]}
        * Customer Explanation: {row["customer_meaning"]}
        * Flag Reason: {row["reason"]}
        * Reviewer Comments: {row["reviewer_comments"]}
        * __{"REJECTED" if row["status"] == "N" else "APPROVED"}__
''')
st.button("Try Another!")

st.markdown("## Summary Stats")
st.write(df.describe())

st.markdown("## Approvals")
st.plotly_chart(px.histogram(df.query('status in ["Y", "N"]'), x='status', title='Approved?'))

st.markdown("## Common Flags")
st.plotly_chart(
    px.histogram(df, x='reason', title='Flagging'))

st.markdown("## Data")
st.dataframe(df, width=1000, height=1200)
