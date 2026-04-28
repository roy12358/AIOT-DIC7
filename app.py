"""
CRISP-DM Linear Regression — Interactive Streamlit App
Layout: chart first, CRISP-DM details in expanders below.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# ─────────────────────────────────────────────
st.set_page_config(page_title="CRISP-DM · Linear Regression", page_icon="📈", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .topbar {
        display: flex; align-items: center;
        background: linear-gradient(135deg, #0f2027, #2c5364);
        border-radius: 12px; padding: 0.8rem 1.5rem;
        margin-bottom: 0.8rem; color: white;
    }
    .topbar h1 { font-size: 1.3rem; font-weight: 700; margin: 0; }
    .topbar p  { font-size: 0.82rem; opacity: 0.75; margin: 0.2rem 0 0; }

    .metric-row { display: flex; gap: 0.7rem; margin: 0.5rem 0 0.8rem; }
    .metric-card {
        flex: 1; background: linear-gradient(135deg, #1a1a2e, #16213e);
        border-radius: 10px; padding: 0.65rem 0.8rem; color: white;
        text-align: center; box-shadow: 0 3px 10px rgba(0,0,0,0.3);
    }
    .metric-card .label { font-size: 0.68rem; opacity: 0.6; letter-spacing: 0.07em; text-transform: uppercase; }
    .metric-card .value { font-size: 1.5rem; font-weight: 700; margin-top: 0.1rem; }
    .metric-card .value.green { color: #56ab2f; }
    .metric-card .value.blue  { color: #4fc3f7; }
    .metric-card .value.gold  { color: #f7b731; }
    .metric-card .value.red   { color: #ff5370; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Parameters")
    st.markdown("**Equation:** `y = a·x + b + noise`")
    st.markdown("---")
    a        = st.slider("Slope  (a)",       -50.0, 50.0,   10.0, 0.5)
    b        = st.slider("Intercept  (b)",  -100.0, 100.0,  30.0, 1.0)
    sigma    = st.slider("Noise σ",            0.0, 100.0,  10.0, 1.0)
    n_points = st.slider("Sample size  (n)",    50, 5000,   1000,  50)
    test_size = st.slider("Test split (%)",     10,   40,     20,   5) / 100
    seed     = st.number_input("Random seed",    0, 9999,    42,    1)
    st.markdown("---")
    st.caption("Powered by scikit-learn · Streamlit · Matplotlib")

# ── Generate data ────────────────────────────
rng    = np.random.default_rng(int(seed))
x_raw  = rng.uniform(-10, 10, size=n_points)
noise_ = rng.normal(0, sigma, size=n_points)
y_raw  = a * x_raw + b + noise_
df     = pd.DataFrame({"x": x_raw, "y": y_raw})

X = x_raw.reshape(-1, 1)
X_train, X_test, y_train, y_test = train_test_split(
    X, y_raw, test_size=test_size, random_state=int(seed))

model     = LinearRegression().fit(X_train, y_train)
learned_a = model.coef_[0]
learned_b = model.intercept_

y_pred_train = model.predict(X_train)
y_pred_test  = model.predict(X_test)
mse_train    = mean_squared_error(y_train, y_pred_train)
mse_test     = mean_squared_error(y_test,  y_pred_test)
r2_train     = r2_score(y_train, y_pred_train)
r2_test      = r2_score(y_test,  y_pred_test)
rmse_test    = float(np.sqrt(mse_test))

# ── Top bar ──────────────────────────────────
st.markdown(f"""
<div class="topbar">
  <div>
    <h1>📈 CRISP-DM · Linear Regression Explorer</h1>
    <p>y = {a:+.1f}·x {b:+.1f} + N(0, {sigma:.1f})
       &nbsp;→&nbsp; ŷ = {learned_a:+.3f}·x {learned_b:+.3f}</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Metrics row ───────────────────────────────
st.markdown(f"""
<div class="metric-row">
  <div class="metric-card">
    <div class="label">Train MSE</div>
    <div class="value blue">{mse_train:.2f}</div>
  </div>
  <div class="metric-card">
    <div class="label">Test MSE</div>
    <div class="value blue">{mse_test:.2f}</div>
  </div>
  <div class="metric-card">
    <div class="label">Test RMSE</div>
    <div class="value gold">{rmse_test:.2f}</div>
  </div>
  <div class="metric-card">
    <div class="label">Train R²</div>
    <div class="value green">{r2_train:.4f}</div>
  </div>
  <div class="metric-card">
    <div class="label">Test R²</div>
    <div class="value {'green' if r2_test >= 0.9 else 'red'}">{r2_test:.4f}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Main chart ────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 5))
fig.patch.set_facecolor("#0f2027")
ax.set_facecolor("#16213e")

ax.scatter(x_raw, y_raw, color="#4fc3f7", alpha=0.35, s=14,
           label="Data points", zorder=2, rasterized=True)

x_line = np.linspace(-10, 10, 400)
y_line = model.predict(x_line.reshape(-1, 1))
ax.plot(x_line, y_line, color="#ff5370", linewidth=2.5,
        label=f"Fitted: ŷ = {learned_a:.2f}x + {learned_b:.2f}", zorder=3)

ax.set_xlabel("x", color="#e0e0e0", fontsize=12)
ax.set_ylabel("y", color="#e0e0e0", fontsize=12)
ax.set_title("Data & Regression Line", color="white", fontsize=14, fontweight="bold")
ax.tick_params(colors="#e0e0e0")
for sp in ax.spines.values():
    sp.set_color("#2c5364")
ax.legend(facecolor="#1a1a2e", edgecolor="#2c5364", labelcolor="white", fontsize=10)

st.pyplot(fig, use_container_width=True)
plt.close(fig)

# ── CRISP-DM details (collapsed) ─────────────
st.markdown("---")
st.markdown("#### 📚 CRISP-DM Phase Details")
col1, col2 = st.columns(2)

with col1:
    with st.expander("Phase 1 · Business Understanding"):
        st.markdown(f"Recover **a** and **b** from noisy data via OLS.  \n"
                    f"True: `y = {a}·x + {b} + N(0,{sigma})`")
    with st.expander("Phase 2 · Data Understanding"):
        st.dataframe(df.head(8), use_container_width=True, hide_index=True)
        st.dataframe(df.describe().round(3), use_container_width=True)
    with st.expander("Phase 3 · Data Preparation"):
        st.markdown(f"- Train: **{len(X_train):,}** ({int((1-test_size)*100)}%)  \n"
                    f"- Test: **{len(X_test):,}** ({int(test_size*100)}%)")

with col2:
    with st.expander("Phase 4 · Modelling"):
        st.markdown(f"- Slope: true **{a}** → learned **{learned_a:.4f}**  \n"
                    f"- Intercept: true **{b}** → learned **{learned_b:.4f}**")
    with st.expander("Phase 5 · Evaluation"):
        st.markdown(
            f"| Metric | Train | Test |\n|---|---|---|\n"
            f"| MSE | {mse_train:.2f} | {mse_test:.2f} |\n"
            f"| RMSE | {float(np.sqrt(mse_train)):.2f} | {rmse_test:.2f} |\n"
            f"| R² | {r2_train:.4f} | {r2_test:.4f} |"
        )
    with st.expander("Phase 6 · Deployment"):
        st.markdown("This dashboard is the deployed artefact. "
                    "Adjust sliders to re-train in real time.")
