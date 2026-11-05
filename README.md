# Infosys Financial Intelligence Dashboard

A Python-only Streamlit dashboard for FY2022–FY2026 Infosys consolidated financial data.

## Deploy to Streamlit Community Cloud

1. Create a **public** GitHub repository named `infosys-financial-dashboard`.
2. Upload the **contents of this folder** to the repository root (not the enclosing folder).
3. Open https://share.streamlit.io/ and sign in with GitHub.
4. Choose **Create app**, select `Krishnakant2201/infosys-financial-dashboard`, branch `main`, main file `app.py`.
5. Click **Deploy**. Streamlit will give you a public shareable URL.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Files

- `app.py`: dashboard, charts, filters, insights, CSV and Excel exports.
- `data/infosys_analysed.csv`: preliminary consolidated figures.
- `data/source_audit.csv`: extraction audit and source-page references.
- `.streamlit/config.toml`: corporate blue and navy theme.
- `requirements.txt`: Python dependencies.

## Important data limitations

The extracted dataset has not been fully independently reconciled against the source PDFs. Some automatically extracted fields were demonstrably implausible (for example, cash balances of ₹2.9 crore) and have been removed rather than presented as factual. EPS, ROCE, segment and geographical revenue, and FY2026 operating profit remain unavailable pending verification. ROA/ROE use closing balances. This dashboard is a preliminary analytical tool, not an audited restatement or investment recommendation.
