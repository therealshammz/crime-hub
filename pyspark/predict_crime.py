import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

OUT = "/home/therealshammz/bdata/visualizations/"
os.makedirs(OUT, exist_ok=True)

# Load year data — exclude 2026 (incomplete year)
df = pd.read_csv("/home/therealshammz/bdata/output/crime_by_year.tsv",
                 sep="\t", header=None, names=["Year","Count"])
df = df[df["Year"] < 2026].sort_values("Year").reset_index(drop=True)

X = df["Year"].values.reshape(-1, 1)
y = df["Count"].values

# --- Train/test split: train on 2001-2019, test on 2020-2025 ---
train_mask = df["Year"] <= 2019
X_train, y_train = X[train_mask], y[train_mask]
X_test,  y_test  = X[~train_mask], y[~train_mask]

model = LinearRegression()
model.fit(X_train, y_train)

y_pred_test = model.predict(X_test)

# --- Forecast 2026-2030 ---
future_years = np.array([2026, 2027, 2028, 2029, 2030]).reshape(-1, 1)
y_future = model.predict(future_years)

# --- Metrics ---
mae  = mean_absolute_error(y_test, y_pred_test)
r2   = r2_score(y_test, y_pred_test)
slope = model.coef_[0]

print("=== Linear Regression Crime Forecast ===")
print(f"Training period : 2001–2019")
print(f"Test period     : 2020–2025")
print(f"R² score        : {r2:.4f}")
print(f"MAE             : {mae:,.0f} crimes/year")
print(f"Trend slope     : {slope:,.0f} crimes/year change")
print()
print("Forecast (2026–2030):")
for yr, val in zip(future_years.flatten(), y_future):
    print(f"  {yr}: {max(0,int(val)):,}")

# Save forecast CSV
forecast_df = pd.DataFrame({
    "Year": future_years.flatten(),
    "Predicted_Count": [max(0, int(v)) for v in y_future]
})
forecast_df.to_csv("/home/therealshammz/bdata/output/crime_forecast.csv", index=False)

# --- Plot ---
all_years_pred = model.predict(X)

fig, ax = plt.subplots(figsize=(13, 6))

# Actual data
ax.plot(df["Year"], df["Count"], marker="o", linewidth=2,
        color="#e63946", label="Actual Crimes", zorder=3)

# Regression line over historical data
ax.plot(df["Year"], all_years_pred, linestyle="--", linewidth=1.5,
        color="#457b9d", label="Regression Fit", zorder=2)

# Test period highlight
ax.axvspan(2019.5, 2025.5, alpha=0.08, color="orange", label="Test Period")

# Forecast
ax.plot(future_years.flatten(), y_future, marker="s", linestyle="--",
        linewidth=2, color="#2a9d8f", label="Forecast (2026–2030)", zorder=3)

# Confidence band on forecast (±1 std of residuals)
residual_std = np.std(y_train - model.predict(X_train))
ax.fill_between(future_years.flatten(),
                y_future - residual_std,
                y_future + residual_std,
                alpha=0.15, color="#2a9d8f", label="±1σ Confidence Band")

ax.set_title("Chicago Crime Trend & Linear Regression Forecast (2001–2030)",
             fontsize=14, fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Crimes")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"{int(x):,}"))
ax.legend(loc="upper right")
ax.grid(axis="y", linestyle="--", alpha=0.4)

# Annotate R²
ax.text(0.02, 0.05, f"R² = {r2:.3f}  |  MAE = {mae:,.0f}  |  Slope = {slope:,.0f}/yr",
        transform=ax.transAxes, fontsize=9, color="gray")

plt.tight_layout()
plt.savefig(OUT + "crime_forecast.png", dpi=150)
plt.close()
print("\nSaved crime_forecast.png")
