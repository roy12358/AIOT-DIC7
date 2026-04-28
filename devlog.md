# Dev Log — CRISP-DM Linear Regression Streamlit App

**Project:** AIOT-DIC7  
**Date:** 2026-04-28  
**Author:** roy12358  

---

## Overview

Built an interactive Streamlit app that demonstrates the full CRISP-DM data mining framework applied to a simple linear regression problem. Users can tune all key parameters via sidebar sliders and see the model update in real time.

---

## Iteration History

### v1 — Plain Python Script
- Generated 1,000 random data points: `x ~ Uniform(-10, 10)`
- Defined `y = 10x + 30 + N(0, 10)`
- Fitted `sklearn.linear_model.LinearRegression`
- Evaluated with MSE and R²
- Visualised with matplotlib: blue scatter + red regression line

### v2 — Convert to Streamlit (Basic)
Converted the script to a Streamlit app following the CRISP-DM structure:
- **Sidebar sliders:** slope `a`, intercept `b`, noise σ, sample size `n`, test split %, random seed
- **Phase 1** Business Understanding — equation display  
- **Phase 2** Data Understanding — dataset preview + descriptive stats  
- **Phase 3** Data Preparation — train/test split info  
- **Phase 4** Modelling — learned coefficients vs true values  
- **Phase 5** Evaluation — MSE / R² metric cards  
- **Phase 6** Deployment — scatter plot + regression line  
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

## Dependencies

```
streamlit
scikit-learn
matplotlib
pandas
numpy
scipy
```

---

## Key Design Decisions

- **Chart-first layout**: visualization above all text — immediate visual feedback
- **All CRISP-DM text in expanders**: keeps screen uncluttered, accessible on demand  
- **Dark navy palette**: `#0f2027` / `#16213e` / `#2c5364` for a premium feel
- **Reactive**: every slider change re-generates data, re-trains, and re-renders instantly
