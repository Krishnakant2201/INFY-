"""Infosys consolidated financial dashboard. Run: streamlit run app.py"""
from pathlib import Path
from io import BytesIO
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title='Infosys | Financial Intelligence',page_icon='📊',layout='wide',initial_sidebar_state='expanded')
BLUE='#007CC3';NAVY='#102B52';CYAN='#00A5DF';GREY='#64748B'
P=Path(__file__).parent
@st.cache_data
def load():
    file = P / 'data' / 'infosys_analysed.csv'
    if not file.is_file():
        st.error('Financial dataset is missing. Upload data/infosys_analysed.csv to your GitHub repository, preserving the data folder.')
        st.stop()
    return pd.read_csv(file)
df=load()
LABELS={'revenue':'Revenue','revenue_growth':'Revenue growth','operating_profit':'Operating profit','operating_margin':'Operating margin','net_profit':'Net profit','net_margin':'Net margin','eps':'EPS','total_assets':'Total assets','total_liabilities':'Total liabilities','total_equity':'Shareholders equity (total)','roe':'ROE','roce':'ROCE','current_assets':'Current assets','current_liabilities':'Current liabilities','cash':'Cash & equivalents','investments':'Total investments','lease_debt':'Lease liabilities','current_ratio':'Current ratio','quick_ratio':'Quick ratio','gross_margin':'Gross margin','roa':'ROA','asset_turnover':'Asset turnover','receivables_turnover':'Receivables turnover','debt_to_equity':'Lease liabilities / equity','interest_coverage':'Interest coverage','cfo':'Operating cash flow','cfi':'Investing cash flow','cff':'Financing cash flow','fcf':'Free cash flow','employee_cost':'Employee costs','dividends':'Dividends paid','net_profit_growth':'Net profit growth'}
PCT={'revenue_growth','operating_margin','net_margin','roe','roce','gross_margin','roa','net_profit_growth'}
RATIOS={'current_ratio','quick_ratio','asset_turnover','receivables_turnover','debt_to_equity','interest_coverage'}
def fmt(x,k):
 if pd.isna(x):return 'N/A'
 if k=='eps':return f'₹{x:,.2f}'
 if k in PCT:return f'{x:,.2f}%'
 if k in RATIOS:return f'{x:,.2f}x'
 return f'₹{x:,.0f} Cr'
def chart(data,cols,title,kind='line'):
 long=data[['fy']+cols].melt('fy',var_name='Metric',value_name='Value').dropna()
 if long.empty:st.info('This chart cannot be calculated from the available verified data.');return
 long['Metric']=long['Metric'].map(lambda x:LABELS.get(x,x))
 fig=px.line(long,x='fy',y='Value',color='Metric',markers=True,color_discrete_sequence=[BLUE,CYAN,NAVY,'#8098B0']) if kind=='line' else px.bar(long,x='fy',y='Value',color='Metric',barmode='group',color_discrete_sequence=[BLUE,CYAN,NAVY,'#8098B0'])
 fig.update_layout(title=title,template='plotly_white',height=370,margin=dict(l=10,r=10,t=55,b=20),legend_title_text='',hovermode='x unified',xaxis_title='',yaxis_title='₹ crore / ratio / %')
 st.plotly_chart(fig,use_container_width=True)
def kpi(key,year):
 row=df[df.year==year].iloc[0];prev=df[df.year==year-1];val=row.get(key,np.nan)
 previous=prev.iloc[0].get(key,np.nan) if not prev.empty else np.nan
 delta=(val-previous)/abs(previous)*100 if pd.notna(val) and pd.notna(previous) and previous!=0 else np.nan
 st.metric(LABELS.get(key,key),fmt(val,key),f'{delta:+.1f}% YoY' if pd.notna(delta) else None)
 st.caption('Previous: '+fmt(previous,key))
def insights(data):
 if data.empty:return []
 result=[]
 for k,title in [('revenue','revenue'),('net_profit','net profit')]:
  d=data.dropna(subset=[k]);
  if not d.empty:
   r=d.loc[d[k].idxmax()];result.append(f'Highest {title}: {r.fy}, {fmt(r[k],k)}.')
 d=data.dropna(subset=['revenue_growth']);
 if len(d):result.append(f'Revenue grew in {int((d.revenue_growth>0).sum())} of {len(d)} comparable years; most recent growth was {d.iloc[-1].revenue_growth:.2f}%.')
 d=data.dropna(subset=['operating_margin']);
 if len(d)>1:result.append(f'Operating margin moved from {d.iloc[0].operating_margin:.2f}% in {d.iloc[0].fy} to {d.iloc[-1].operating_margin:.2f}% in {d.iloc[-1].fy}.')
 d=data.dropna(subset=['current_ratio']);
 if len(d):result.append(f'Latest current ratio was {d.iloc[-1].current_ratio:.2f}x (current assets {fmt(d.iloc[-1].current_assets,"current_assets")}, current liabilities {fmt(d.iloc[-1].current_liabilities,"current_liabilities")}).')
 d=data.dropna(subset=['cfo','net_profit']);
 if len(d):result.append(f'Operating cash flow in {d.iloc[-1].fy} was {fmt(d.iloc[-1].cfo,"cfo")} against net profit of {fmt(d.iloc[-1].net_profit,"net_profit")}, a cash conversion of {d.iloc[-1].cash_conversion:.2f}x.')
 d=data.dropna(subset=['total_assets','total_equity']);
 if len(d):result.append(f'In {d.iloc[-1].fy}, assets of {fmt(d.iloc[-1].total_assets,"total_assets")} were supported by total equity of {fmt(d.iloc[-1].total_equity,"total_equity")}.')
 return result
st.sidebar.title('INFOSYS')
st.sidebar.caption('FINANCIAL INTELLIGENCE • CONSOLIDATED')
sections=['Executive summary','Revenue & profitability','Balance sheet','Financial ratios','Cash flows','Business performance','Insights & assessment','Data & methodology']
page=st.sidebar.radio('Navigate',sections)
all_years=df.year.astype(int).tolist()
year=st.sidebar.selectbox('Focus financial year',all_years,key='filter_year',index=len(all_years)-1,format_func=lambda y:df.loc[df.year==y,'fy'].iloc[0])
years=st.sidebar.multiselect('Comparison years',all_years,key='filter_years',default=all_years,format_func=lambda y:df.loc[df.year==y,'fy'].iloc[0])
metrics=st.sidebar.multiselect('Chart metrics',list(LABELS),key='filter_metrics',default=['revenue','net_profit'],format_func=lambda x:LABELS[x])
if st.sidebar.button('↺ Reset filters',use_container_width=True):
 for k in list(st.session_state):
  if k.startswith('filter_'):del st.session_state[k]
 st.rerun()
selected=df[df.year.isin(years)].sort_values('year')
st.title('Infosys Limited')
st.caption('Five-year financial performance | FY 2021–22 to FY 2025–26 | INR crore | Consolidated annual reports')
if not years:st.warning('Select at least one comparison year.');st.stop()
if page=='Executive summary':
 st.subheader('Executive financial scorecard')
 keys=['revenue','revenue_growth','operating_profit','operating_margin','net_profit','net_margin','eps','total_assets','total_liabilities','total_equity','roe','roce']
 for i in range(0,len(keys),4):
  cols=st.columns(4)
  for c,k in zip(cols,keys[i:i+4]):
   with c:kpi(k,year)
 chart(selected,['revenue','operating_profit','net_profit'],'Revenue and earnings trend')
 chart(selected,['revenue_growth','net_profit_growth'],'Growth rates (%)','bar')
elif page=='Revenue & profitability':
 chart(selected,['revenue'],'Five-year revenue trend');chart(selected,['operating_profit','net_profit'],'Operating and net profit');chart(selected,['revenue','operating_profit','net_profit'],'Revenue vs profit','bar');chart(selected,['operating_margin','net_margin'],'Profit margins (%)');chart(selected,['revenue_growth','net_profit_growth'],'YoY growth (%)','bar')
elif page=='Balance sheet':
 for i in range(0,8,4):
  cols=st.columns(4)
  for c,k in zip(cols,['total_assets','total_liabilities','total_equity','cash','current_assets','current_liabilities','investments','lease_debt'][i:i+4]):
   with c:kpi(k,year)
 chart(selected,['total_assets','total_liabilities','total_equity'],'Capital structure','bar');chart(selected,['current_assets','current_liabilities','cash'],'Liquidity structure');chart(selected,['investments','lease_debt'],'Investments and lease obligations')
elif page=='Financial ratios':
 groups={'Profitability':['gross_margin','operating_margin','net_margin','roa','roe','roce'],'Liquidity':['current_ratio','quick_ratio'],'Efficiency':['asset_turnover','receivables_turnover'],'Solvency':['debt_to_equity','interest_coverage']}
 for name,ks in groups.items():
  st.subheader(name);available=[k for k in ks if k in selected and selected[k].notna().any()]
  if available:chart(selected,available,f'{name} ratios')
  for k in ks:
   if k not in selected or selected[k].isna().all():st.caption(f'{LABELS[k]}: not available from the consistently extracted disclosures / calculation inputs.')
 st.info('ROA/ROE and turnover ratios use closing balances; average-balance measures require opening FY2021 balances. Lease liabilities/equity is not a total-borrowings ratio.')
elif page=='Cash flows':
 for c,k in zip(st.columns(4),['cfo','cfi','cff','fcf']):
  with c:kpi(k,year)
 chart(selected,['cfo','cfi','cff'],'Cash flow components','bar');chart(selected,['cfo','net_profit'],'Cash flow versus accounting earnings');chart(selected,['fcf'],'Free cash flow')
 st.caption('FCF = operating cash flow + net expenditure on property, plant, equipment and intangibles (negative cash outflow).')
elif page=='Business performance':
 chart(selected,['employee_cost'],'Employee benefit expenses');chart(selected,['dividends'],'Dividend payments')
 st.info('Segment revenue, geographic mix, digital revenue, headcount/productivity and R&D are not included in the verified structured dataset; no values are inferred.')
elif page=='Insights & assessment':
 st.subheader('Evidence-based insights')
 for v in insights(selected):st.write('• '+v)
 st.subheader('Overall Financial Performance Assessment of Infosys')
 latest=selected.iloc[-1];old=selected.iloc[0]
 st.write(f'Across the selected period, reported consolidated revenue moved from {fmt(old.revenue,"revenue")} ({old.fy}) to {fmt(latest.revenue,"revenue")} ({latest.fy}); net profit moved from {fmt(old.net_profit,"net_profit")} to {fmt(latest.net_profit,"net_profit")}. The latest reported operating cash flow was {fmt(latest.cfo,"cfo")}. These figures show the direction of growth and cash generation, but do not by themselves establish future performance.')
 st.write('Key limitations: ROCE, gross margin, quick ratio, interest coverage and some FY2026 operating metrics are unavailable in the verified extract. Interpret leverage and profitability with these limitations in mind.')
elif page=='Data & methodology':
 st.subheader('Underlying data')
 st.dataframe(selected.rename(columns=LABELS),use_container_width=True,hide_index=True)
 st.subheader('Choose metrics for custom chart')
 valid=[k for k in metrics if k in selected and selected[k].notna().any()]
 if valid:chart(selected,valid,'Custom financial comparison')
 st.markdown('**Methods:** Revenue growth = annual % change; net margin = net profit / revenue; current ratio = current assets / current liabilities; ROE = net profit / closing total equity; ROA = net profit / closing assets; FCF = CFO + net capital expenditure. Operating profit uses the reported function-wise consolidated statement when available. Missing data remains N/A.')
 st.warning('PDF tables are complex; use the Source audit and the original reports for independent reconciliation before investment or management decisions.')
st.divider()
st.subheader('Export analysed data')
c1,c2=st.columns(2)
with c1:st.download_button('Download filtered CSV',selected.to_csv(index=False).encode('utf-8'),'infosys_filtered.csv','text/csv',use_container_width=True)
with c2:
 
 from io import BytesIO
 buffer=BytesIO()
 with pd.ExcelWriter(buffer,engine='openpyxl') as writer:
  selected.to_excel(writer,index=False,sheet_name='Filtered financials')
 st.download_button('Download filtered Excel workbook',buffer.getvalue(),'infosys_filtered.xlsx','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',use_container_width=True)
st.caption('Source: Infosys Integrated Annual Reports FY2022–FY2026. Preliminary extraction, not independently audited. Suspect fields are excluded; missing metrics are never estimated.')
