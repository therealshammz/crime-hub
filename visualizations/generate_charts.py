import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

os.makedirs("/home/therealshammz/bdata/visualizations", exist_ok=True)
OUT = "/home/therealshammz/bdata/visualizations/"

# --- 1. Crimes by Year ---
df = pd.read_csv("/home/therealshammz/bdata/output/crime_by_year.tsv", sep="\t", header=None, names=["Year","Count"])
df = df.sort_values("Year")
fig, ax = plt.subplots(figsize=(12,5))
ax.plot(df["Year"], df["Count"], marker="o", linewidth=2, color="#e63946")
ax.fill_between(df["Year"], df["Count"], alpha=0.1, color="#e63946")
ax.set_title("Chicago Crime Trend (2001–2026)", fontsize=14, fontweight="bold")
ax.set_xlabel("Year"); ax.set_ylabel("Number of Crimes")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"{int(x):,}"))
ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout(); plt.savefig(OUT+"crime_by_year.png", dpi=150); plt.close()
print("Saved crime_by_year.png")

# --- 2. Top 15 Crime Types ---
df = pd.read_csv("/home/therealshammz/bdata/output/crime_by_type.tsv", sep="\t", header=None, names=["Type","Count"])
df = df.sort_values("Count", ascending=True).tail(15)
fig, ax = plt.subplots(figsize=(10,7))
bars = ax.barh(df["Type"], df["Count"], color="#457b9d")
ax.set_title("Top 15 Crime Types in Chicago", fontsize=14, fontweight="bold")
ax.set_xlabel("Number of Crimes")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"{int(x):,}"))
ax.grid(axis="x", linestyle="--", alpha=0.5)
plt.tight_layout(); plt.savefig(OUT+"crime_by_type.png", dpi=150); plt.close()
print("Saved crime_by_type.png")

# --- 3. Arrest Rate by Crime Type (top 15 by volume) ---
df = pd.read_csv("/home/therealshammz/bdata/output/arrest_rate.tsv", sep="\t", header=None, names=["Type","Total","Arrests","Rate"])
df["Rate"] = df["Rate"].str.replace("%","").astype(float)
df = df.sort_values("Total", ascending=False).head(15).sort_values("Rate")
fig, ax = plt.subplots(figsize=(10,7))
colors = ["#2a9d8f" if r >= 50 else "#e76f51" for r in df["Rate"]]
ax.barh(df["Type"], df["Rate"], color=colors)
ax.axvline(50, color="gray", linestyle="--", linewidth=1)
ax.set_title("Arrest Rate by Crime Type (Top 15 by Volume)", fontsize=14, fontweight="bold")
ax.set_xlabel("Arrest Rate (%)")
ax.grid(axis="x", linestyle="--", alpha=0.5)
plt.tight_layout(); plt.savefig(OUT+"arrest_rate.png", dpi=150); plt.close()
print("Saved arrest_rate.png")

# --- 4. Crimes by Hour ---
df = pd.read_csv("/home/therealshammz/bdata/output/crimes_by_hour.csv")
df = df.dropna().astype(int).sort_values("Hour")
fig, ax = plt.subplots(figsize=(12,5))
ax.bar(df["Hour"], df["Count"], color="#6a4c93", width=0.7)
ax.set_title("Crime Distribution by Hour of Day", fontsize=14, fontweight="bold")
ax.set_xlabel("Hour (24h)"); ax.set_ylabel("Number of Crimes")
ax.set_xticks(range(0,24))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"{int(x):,}"))
ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout(); plt.savefig(OUT+"crimes_by_hour.png", dpi=150); plt.close()
print("Saved crimes_by_hour.png")

# --- 5. Crimes by Month ---
df = pd.read_csv("/home/therealshammz/bdata/output/crimes_by_month.csv")
df = df.dropna().astype(int).sort_values("Month")
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
fig, ax = plt.subplots(figsize=(10,5))
ax.bar(months, df["Count"], color="#f4a261")
ax.set_title("Crime Distribution by Month", fontsize=14, fontweight="bold")
ax.set_ylabel("Number of Crimes")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"{int(x):,}"))
ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout(); plt.savefig(OUT+"crimes_by_month.png", dpi=150); plt.close()
print("Saved crimes_by_month.png")

# --- 6. Crimes by Day of Week ---
df = pd.read_csv("/home/therealshammz/bdata/output/crimes_by_dow.csv")
df = df.dropna().astype(int).sort_values("DayOfWeek")
days = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]
fig, ax = plt.subplots(figsize=(8,5))
ax.bar(days, df["Count"], color="#2a9d8f")
ax.set_title("Crime Distribution by Day of Week", fontsize=14, fontweight="bold")
ax.set_ylabel("Number of Crimes")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"{int(x):,}"))
ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout(); plt.savefig(OUT+"crimes_by_dow.png", dpi=150); plt.close()
print("Saved crimes_by_dow.png")

# --- 7. Domestic vs Non-Domestic ---
df = pd.read_csv("/home/therealshammz/bdata/output/domestic_vs_nondomestic.csv")
labels = ["Non-Domestic", "Domestic"]
sizes = df.sort_values("Domestic")["Count"].tolist()
fig, ax = plt.subplots(figsize=(6,6))
ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=["#457b9d","#e63946"],
       startangle=90, wedgeprops={"edgecolor":"white","linewidth":2})
ax.set_title("Domestic vs Non-Domestic Crimes", fontsize=14, fontweight="bold")
plt.tight_layout(); plt.savefig(OUT+"domestic_pie.png", dpi=150); plt.close()
print("Saved domestic_pie.png")

# --- 8. Model Feature Importance (New) ---
if os.path.exists("/home/therealshammz/bdata/output/feature_importance.csv"):
    df = pd.read_csv("/home/therealshammz/bdata/output/feature_importance.csv")
    df = df.sort_values("Importance", ascending=True)
    fig, ax = plt.subplots(figsize=(10,6))
    ax.barh(df["Feature"], df["Importance"], color="#f4a261")
    ax.set_title("Crime Type Prediction: Feature Importance", fontsize=14, fontweight="bold")
    ax.set_xlabel("Importance Score")
    ax.grid(axis="x", linestyle="--", alpha=0.5)
    plt.tight_layout(); plt.savefig(OUT+"feature_importance.png", dpi=150); plt.close()
    print("Saved feature_importance.png")

print("\nAll 8 charts generated.")
