# Investment-Rechner

Responsives Streamlit-Dashboard für Anfangskapital, monatliche oder jährliche Sparrate, jährliche Erhöhung der Sparrate, mehrere Renditeszenarien und den Anlagehorizont.

## Lokal starten

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Kostenlos veröffentlichen

1. Dieses Projekt in ein GitHub-Repository hochladen.
2. Auf https://share.streamlit.io anmelden und **Create app** wählen.
3. Repository und Branch auswählen; als Main file `app.py` angeben.
4. Veröffentlichen. Eine eigene Domain ist nicht erforderlich.

## Rechenannahmen

- Effektive Jahresrendite wird mathematisch korrekt in eine Monatsrendite umgerechnet.
- Einzahlungen erfolgen jeweils am Monatsende.
- Die Sparrate wird nach jedem vollständigen Jahr erhöht.
- Steuern, Inflation, Gebühren und Renditeschwankungen innerhalb eines Szenarios sind nicht berücksichtigt.
