# Dev Log — CRISP-DM Linear Regression Streamlit App

**Project:** AIOT-DIC7  
**Date:** 2026-04-28  
**Author:** roy12358  
**Live:** https://aiot-dic7.streamlit.app

---

## Iteration History

### v1 — Plain Python Script
- Generated 1,000 random data points: `x ~ Uniform(-10, 10)`
- Defined `y = 10x + 30 + N(0, 10)`
- Fitted `sklearn.linear_model.LinearRegression`
- Evaluated with MSE and R²
- Visualised with matplotlib: blue scatter + red regression line

### v2 — Convert to Streamlit (Basic)
Converted to Streamlit following the CRISP-DM structure:
- **Sidebar sliders:** slope `a`, intercept `b`, noise σ, sample size `n`, test split %, random seed
- **Phase 1–6** CRISP-DM sections rendered as page sections
- Dark-mode premium design (deep navy palette, gradient hero)

### v3 — Enhanced Visuals (7 charts)
Added a 7-panel matplotlib dashboard (3×3 GridSpec):

| Panel | Chart |
|-------|-------|
| ① | Data & Regression Line (scatter + fitted + true line) |
| ② | True vs Learned Coefficients (bar chart) |
| ③ | Residual Scatter with rolling mean |
| ④ | Residual Distribution (histogram + normal curve) |
| ⑤ | Q-Q Plot |
| ⑥ | Actual vs Predicted |
| ⑦ | Learning Curve (5-fold CV) |

Dependencies added: `scipy`

### v4 — Layout Restructure ("chart first")
User feedback: *"一進去就看到圖"* — chart should be visible without scrolling.

Restructured page:
- **Slim topbar** (shows equation + learned formula inline)
- **Metric cards row** (Train MSE, Test MSE, RMSE, Train R², Test R²)
- **Main chart** — fills remaining viewport
- **CRISP-DM Phase Details** — collapsed in `st.expander` sections below

### v5 — Simplify Back to One Chart
User feedback: *"表就跟之前一樣 保留最必要的"*

Reverted to a single clean chart:
- Blue scatter points
- Red regression line with learned equation in legend
- Kept the v4 layout (topbar + metrics + chart visible on load)
- CRISP-DM phases remain in expanders

### v6 — GitHub Push + Docs
- Created `devlog.md` and `conversation.md`
- Initialized git repo, added remote `https://github.com/roy12358/AIOT-DIC7.git`
- Committed and pushed all files
- Created `README.md` with screenshot, feature table, CRISP-DM breakdown, local setup guide
- Captured `screenshot.png` of local app for README embed
- Committed README + screenshot and pushed

### v7 — Streamlit Cloud Deployment + Fix
- User deployed app via Streamlit Cloud at https://aiot-dic7.streamlit.app
- **Bug:** `ModuleNotFoundError: matplotlib` — `requirements.txt` was not committed (write failed silently during previous session)
- **Fix:** Recreated `requirements.txt`, force-added, committed, pushed
- Streamlit Cloud auto-redeployed — app now live and fully functional

---

## Final Architecture

```
app.py
├── st.set_page_config        # wide layout
├── CSS (custom dark theme)
├── Sidebar sliders           # a, b, σ, n, test%, seed
├── Data generation           # numpy RNG
├── Model training            # sklearn LinearRegression
├── Evaluation                # MSE, RMSE, R²
├── Topbar (HTML)             # slim gradient header
├── Metrics row (HTML)        # 5 metric cards
├── Main chart (matplotlib)   # scatter + regression line
└── Expanders                 # 6 CRISP-DM phase details
```

## Project Structure

```
AIOT-DIC7/
├── app.py
├── requirements.txt
├── screenshot.png
├── README.md
├── devlog.md
├── conversation.md
└── .gitignore
```

## Dependencies

```
streamlit / scikit-learn / matplotlib / pandas / numpy / scipy
```

## Key Design Decisions

- **Chart-first layout**: visualization above text — immediate visual feedback on load
- **CRISP-DM in expanders**: keeps screen uncluttered, details accessible on demand  
- **Dark navy palette**: `#0f2027` / `#16213e` / `#2c5364` — premium feel
- **Reactive**: every slider re-generates data, re-trains, re-renders instantly
