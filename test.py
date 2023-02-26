#https://gist.githubusercontent.com/FerusAndBeyond/cec616149fb74602cbed32fb2fedf3c3/raw/08ee9189c011c170ea828e45c9e58ec886c6ddf0/dividend8.py
# horizontal line
st.markdown("---")

# define all plots
div_fig = plot_data(
    stock_data,
    key="dividends",
    title="Dividends",
    yaxis_title=currency,
    type="bar"
)
pe_fig = plot_data(
    stock_data, 
    key="historical_PE", 
    title="Historical Price-to-Earnings (P/E) Ratio", 
    yaxis_title="P/E", 
    show_mean=True, 
    mean_text="Average Historical P/E",
)
yield_fig = plot_data(
    stock_data, 
    key="dividend_yield", 
    title="Dividend Yield", 
    yaxis_title="Percent %", 
    show_mean=True, 
    mean_text="Average Historical Dividend Yield",
    type="bar"
)
payout_fig = plot_data(
    stock_data, 
    key="payout_ratio", 
    title="Payout Ratio", 
    yaxis_title="Payout Ratio",
    type="bar",
    show_mean=True,
    mean_text="Average Historical Payout Ratio"
)
cps_fig = plot_data(
    stock_data, 
    key="cash_per_share", 
    title="Cash/Share", 
    yaxis_title=currency,
    type="bar"
)
fcf_fig = plot_data(
    stock_data, 
    key="free_cash_flow_per_share", 
    title="Free Cash Flow/Share", 
    yaxis_title=currency,
    type="bar"
)
eps_fig = plot_data(
    stock_data, 
    key="earnings_per_share", 
    title="Earnings/Share", 
    yaxis_title=currency,
    type="bar"
)
dte_fig = plot_data(
    stock_data,
    key="debt_to_equity",
    title="Debt-to-equity",
    yaxis_title="Debt/Equity"   
)

# align plots side by side
combos = [(div_fig, pe_fig), (eps_fig, yield_fig), (payout_fig, cps_fig), (fcf_fig, dte_fig)]
for (fig1, fig2) in combos:
    cols = st.columns(2)
    if fig1 is not None:
        cols[0].plotly_chart(fig1, use_container_width=True)
    if fig2 is not None:
        cols[1].plotly_chart(fig2, use_container_width=True)
#https://gist.githubusercontent.com/FerusAndBeyond/f1c93595bbeb4faa155637da69f8c4f6/raw/d230d92169c3794fea601686217ba19b0bb214ae/dividend7.py
def plot_data(data, key, title, yaxis_title, show_mean=False, mean_text="", type="line"):
    # getattr(px, type) if type = 'line' is px.line
    fig = getattr(px, type)(y=data[key], x=data[key].index)
    # add a historical mean if specified
    if show_mean:
        fig.add_hline(data[key].mean(), line_dash="dot", annotation_text=mean_text)
    # set title and axis-titles
    fig.update_layout(
        title=title, 
        xaxis_title="Date",
        yaxis_title=yaxis_title,
        title_x = 0.5,
        showlegend=False
    )
    return fig
#https://gist.githubusercontent.com/FerusAndBeyond/1af8d9c7525f7e9b870ab202885c634f/raw/665c12658810a34afc025c39db40f27a421b9d5f/dividend6_5.py
def get_price_data_fig(srs, moving_average, time_window, time_window_key, currency):
    # create moving average
    ma = srs.rolling(window=moving_average).mean().dropna()
    # only in time window
    start = (pd.to_datetime("today").floor("D") - time_window)
    srs = srs.loc[start:]
    ma = ma.loc[start:]
    # create figures for normal and moving average
    fig1 = px.line(y=srs, x=srs.index)
    fig1.update_traces(line_color="blue", name="Price", showlegend=True)
    fig2 = px.line(y=ma, x=ma.index)
    fig2.update_traces(line_color="orange", name=f"Moving average price ({moving_average})", showlegend=True)
    # combine and add layout
    fig = go.Figure(data = fig1.data + fig2.data)
    fig.update_layout(
        title=f"Price data last {time_window_key}",
        xaxis_title="Date",
        yaxis_title=currency,
        title_x = 0.5,
        # align labels top-left, side-by-side
        legend=dict(y=1.1, x=0, orientation="h"),
        showlegend=True
    )
    return fig
#https://gist.githubusercontent.com/FerusAndBeyond/323043d56e2a3d66fc25069249d683ba/raw/fab93d14a1650d85e0e7abe137cc1b825d9316b1/dividend6.py
# second column, graph and graph settings

# empty() functions as a placeholder,
# that is, after I later add items to this placeholder,
# the items will appear here before elements that are
# added later. 
graph_placeholder = overview_columns[1].empty()
# The reason a placeholder is used is because I would like
# to show the graph options beneath the graph, but they
# need to be set first so that their returned values can
# be used when constructing the graph

# here I add an empty graph to avoid the elements from
# jumping around when updating the graph
graph_placeholder.plotly_chart(go.Figure(), use_container_width=True)

# options that will dictate the graph:

# radio buttons for what time window to display the stock price
time_window_key = overview_columns[1].radio("Time window", TIME_DIFFS.keys(), index=len(TIME_DIFFS)-1, horizontal=True)
# select the value from the key, i.e. the pd.DateOffset
time_window = TIME_DIFFS[time_window_key]

# slider to select the moving average to display in the graph
moving_average = overview_columns[1].slider("Moving average", min_value=2, max_value=500, value=30)

# Use above to construct the graph:

# show the graph
fig = get_price_data_fig(stock_data["stock_closings"], moving_average, time_window, time_window_key, currency)
# add to placeholder to be displayed before options
graph_placeholder.plotly_chart(fig, use_container_width=True)
#https://gist.githubusercontent.com/FerusAndBeyond/91e08647f58b10d09ef1015ce4191036/raw/0cb715830a18e9ff3469e158e711dc7e7ae1dc38/dividend4.py
info = stock_data["info"]
currency = info["currency"]

# Title
st.title(f"{info['companyName']} ({info['symbol']})")

# Add changes for different periods
close = stock_data["stock_closings"]
latest_price = close.iloc[-1]
# should all be displayed on the same row
change_columns = st.columns(len(TIME_DIFFS))
today = pd.to_datetime("today").floor("D")
for i, (name, difference) in enumerate(TIME_DIFFS.items()):
    # go back to the date <difference> ago
    date = (today - difference)
    # if there is no data back then, then use the earliest
    if date < close.index[0]:
        date = close.index[0]
    # if no match, get the date closest to it back in time, e.g. weekend to friday
    previous_price = close.iloc[close.index.get_loc(date,method='ffill')]
    # calculate change in percent
    change = 100*(latest_price - previous_price) / previous_price
    # show red if negative, green if positive
    color = "red" if change < 0 else "green"

    # color can be displayed as :red[this will be red] in markdown
    change_columns[i].markdown(f"{name}: :{color}[{round(change, 2)}%]")
#https://gist.githubusercontent.com/FerusAndBeyond/96fc34458abeb1a36fb007d29c66e744/raw/bc1276e8f970cd1642d5ced8c775af11095d9bfd/dividend3.py
# create 3 columns and add a text_input
# in the second/center column
ticker = st.columns(3)[1].text_input("Ticker")

if ticker != "":
    stock_data = load_data(ticker)
#https://gist.githubusercontent.com/FerusAndBeyond/2d547d4f26c1ffcaea62b20c1bb6ed8b/raw/8a17b3cde98873bec7d1057fa8fee2f1383d11eb/dividend2.py
# save for 5 hours
@st.cache(ttl=60*60*5)
def load_data(ticker):
    # load data
    profile = fa.profile(ticker, FA_API_KEY)
    key_metrics_annually = fa.key_metrics(ticker, FA_API_KEY, period="annual")
    stock_data = fa.stock_data(ticker, period="5y", interval="1d")
    financial_ratios_annually = fa.financial_ratios(ticker, FA_API_KEY, period="annual")
    income_statement_annually = fa.income_statement(ticker, FA_API_KEY, period="annual")
    try:
        dividends = fa.stock_dividend(ticker, FA_API_KEY)
        dividends.index = pd.to_datetime(dividends.index)
        dividends = dividends["adjDividend"].resample("1Y").sum().sort_index()
    except:
        dividends = pd.Series(0, name="Dividends")

    # return information of interest
    return {
        "stock_closings": stock_data["close"].sort_index(),
        "historical_PE": key_metrics_annually.loc["peRatio"].sort_index(),
        "payout_ratio": financial_ratios_annually.loc["payoutRatio"].sort_index(),
        "dividend_yield": 100*financial_ratios_annually.loc["dividendYield"].sort_index(),
        "cash_per_share": key_metrics_annually.loc["cashPerShare"].sort_index(),
        "debt_to_equity": key_metrics_annually.loc["debtToEquity"].sort_index(),
        "free_cash_flow_per_share": key_metrics_annually.loc["freeCashFlowPerShare"].sort_index(),
        "dividends": dividends,
        "earnings_per_share": income_statement_annually.loc["eps"].sort_index(),
        "info": profile.iloc[:, 0]
    }
