"""Streamlit UI. Run with:  streamlit run app.py"""

import streamlit as st

from src import analysis, storage

st.set_page_config(page_title="Stock Analysis", page_icon="📈")
st.title("📈 Stock Analysis")

def render_result(result:dict) -> None:
    """Display an analysis stored in session state."""
    data = result["data"]
    ticker = result["ticker"]
    if result["analysis_type"] == "filings":
        st.subheader(f"Financial statements for {ticker}")
        for name, df in data.items():
            st.write(f"**{name}**")
            if df is None or df.empty:
                st.write("No data available.")
            else:
                st.dataframe(df)
    
    elif result["analysis_type"] == "news":
        st.subheader(f"Latest news for {ticker}")
        for i, article in enumerate(data, 1):
            st.write(f"**{i}. {article['title']}**")
            st.write(article["description"])
    
    else:  # stock price ratings
        price, ratings = data
        st.subheader(f"Price and ratings for {ticker}")
        st.metric("Current price (USD)", f"{price:,.2f}")
        st.write("**Analyst recommendations**")
        st.dataframe(ratings)

@st.dialog("Saved analysis", width="large")
def show_saved_analysis(filename:str) -> None:
    """Pop-up showing a saved analysis rendered as Markdown."""
    try:
        st.markdown(storage.read_analysis(filename))
    except OSError as e:
        st.error(f"Could not open {filename}: {e}")


ticker = st.text_input("Ticker symbol", value="MU", placeholder="e.g. MU, GOOG, AAPL")
analysis_type = st.selectbox(
    "Analysis type", ["filings", "news", "stock price ratings"]
)

if st.button("Run"):
    st.session_state["result"] = None
    try:
        with st.spinner("Fetching data from Yahoo Finance..."):
            clean = analysis.clean_ticker(ticker)
            if analysis_type == "filings":
                data = analysis.get_financials(ticker)
                params = {"statements": ", ".join(data)}
            elif analysis_type == "news":
                data = analysis.get_news(ticker)
                params = {"articles": len(data)}
            else:  # stock price ratings
                data = (analysis.get_price(ticker), analysis.get_analyst_ratings(ticker))
                params = {"recent recommendations": len(data[1])}
        st.session_state["result"] = {
            "ticker": clean,
            "analysis_type": analysis_type,
            "params": params,
            "data": data
        }
    
    except ValueError as e:
        # Expected problems: empty input, no data found
        st.warning(str(e))
    except Exception as e:
        # Anything else: network issues, invalid ticker, Yahoo errors
        st.error(f"Something went wrong: {e}")

# Results live in session_state so they survive the rerun triggered by clicking Save.
result = st.session_state.get("result")
if result:
    render_result(result)
    if st.button("Save Analysis"):
        try:
            body = storage.build_body(result["analysis_type"], result["data"])
            filename = storage.save_analysis(result["ticker"], result["analysis_type"], result["params"], body)
            st.success(f"Analysis saved as {filename} in analyses-data/.")
        except OSError as e:
            st.error(f"Could not save the analysis: {e}")

st.divider()
st.header("Previous Analyses")
try:
    saved = storage.list_analyses()
except OSError as e:
    saved = []
    st.error(f"Could not read saved analyses: {e}")
else:
    if not saved:
        st.info("No analyses saved yet. Run an analysis and click Save Analysis to keep it here.")

if saved:
    selected = st.selectbox("Saved analyses (newest first)", saved, format_func=storage.label_for)
    if st.button("Show"):
        show_saved_analysis(selected)
