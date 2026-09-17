from __future__ import annotations

import altair as alt
import pandas as pd
import streamlit as st

from calculator import simulate


st.set_page_config(page_title="Investment-Rechner", page_icon="📈", layout="wide")


def euro(value: float) -> str:
    return f"{value:,.0f} €".replace(",", "X").replace(".", ",").replace("X", ".")


def parse_returns(raw: str) -> list[float]:
    values: list[float] = []
    for part in raw.replace(";", ",").split(","):
        part = part.strip().replace("%", "").replace(" ", "")
        if part:
            value = float(part.replace(",", "."))
            if value <= -100:
                raise ValueError
            if value not in values:
                values.append(value)
    if not values:
        raise ValueError
    return values


st.title("Investment-Rechner")
st.caption("Vergleiche mehrere Renditeszenarien mit monatlicher Verzinsung und wachsender Sparrate.")

with st.sidebar:
    st.header("Deine Angaben")
    initial = st.number_input("Anfangskapital (€)", min_value=0.0, value=10_000.0, step=500.0)
    saving = st.number_input("Sparrate (€)", min_value=0.0, value=500.0, step=50.0)
    saving_period = st.radio("Sparrate gilt", ["pro Monat", "pro Jahr"], horizontal=True)
    increase = st.number_input("Jährliche Steigerung der Sparrate (%)", min_value=-99.0, value=5.0, step=0.5)
    returns_raw = st.text_input("Renditeszenarien pro Jahr (%)", value="5, 7, 10")
    years = st.slider("Anlagehorizont (Jahre)", min_value=1, max_value=60, value=30)
    st.caption("Annahme: Die Sparrate wird jeweils am Monatsende eingezahlt; Steuern und Gebühren sind nicht berücksichtigt.")

try:
    returns = parse_returns(returns_raw)
except ValueError:
    st.error("Bitte Renditen als Zahlen eingeben, zum Beispiel: 5, 7, 10")
    st.stop()

monthly_saving = saving if saving_period == "pro Monat" else saving / 12
all_results = {
    rate: simulate(initial, monthly_saving, increase, rate, years) for rate in returns
}

st.subheader(f"Ergebnis nach {years} Jahren")
metric_columns = st.columns(min(len(returns), 4))
for index, rate in enumerate(returns):
    final = all_results[rate][-1]
    gain = final.value - final.contributed
    with metric_columns[index % len(metric_columns)]:
        st.metric(f"{rate:g} % Rendite", euro(final.value))
        st.caption(f"Renditegewinn: {euro(gain)} · Eingezahlt: {euro(final.contributed)}")

chart_rows = []
for rate, rows in all_results.items():
    for row in rows:
        chart_rows.append({"Jahr": row.year, "Wert": row.value, "Szenario": f"{rate:g} % Rendite"})

for row in all_results[returns[0]]:
    chart_rows.append({"Jahr": row.year, "Wert": row.contributed, "Szenario": "Eigene Einzahlungen"})

chart_data = pd.DataFrame(chart_rows)
chart = (
    alt.Chart(chart_data)
    .mark_line(strokeWidth=3)
    .encode(
        x=alt.X("Jahr:Q", title="Jahre", axis=alt.Axis(tickMinStep=1)),
        y=alt.Y("Wert:Q", title="Vermögen (€)", axis=alt.Axis(format="~s")),
        color=alt.Color("Szenario:N", title=None),
        tooltip=[alt.Tooltip("Jahr:Q", format=".0f"), "Szenario:N", alt.Tooltip("Wert:Q", format=",.0f")],
    )
    .properties(height=430)
    .interactive()
)
st.altair_chart(chart, use_container_width=True)

table = pd.DataFrame({"Jahr": range(years + 1)})
table["Eigene Einzahlungen"] = [row.contributed for row in all_results[returns[0]]]
for rate in returns:
    table[f"Vermögen bei {rate:g} %"] = [row.value for row in all_results[rate]]

st.subheader("Jahresübersicht")
st.dataframe(
    table.style.format({column: euro for column in table.columns if column != "Jahr"}),
    use_container_width=True,
    hide_index=True,
)
st.download_button(
    "Tabelle als CSV herunterladen",
    data=table.to_csv(index=False, decimal=",", sep=";").encode("utf-8-sig"),
    file_name="investment-szenarien.csv",
    mime="text/csv",
)

st.info("Die Berechnung ist eine Modellrechnung und keine Anlageberatung. Tatsächliche Marktrenditen schwanken.")
