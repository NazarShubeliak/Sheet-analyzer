# 📊 Sheet Analyzer
Sheet Analyzer is a modular system for collecting, normalizing, and forecasting data from Google Sheets. It automates financial data ingestion, currency normalization to EUR, model training, and next-month predictions for each country.

## ⚙️ Architecture Overview
```bash
root/
├── config/
│   └── config.py
├── ml/           
│   ├── model_runner/
│   │   └── decision_tree.py
│   ├── models/
│   │   └── decision_tree.py
│   ├── manager.py
│   └── pipeline.py 
├── modules/
│   ├── loaders/
│   │   ├── currency_api.py
│   │   └── sheet.py
│   ├── processors/
│   │   ├── currency.py
│   │   └── dataframe.py
│   └── pipeline.py 
├── run.py          
```

## 🚀 Quick Start
```bash
python run.py
```
### This runs the full pipeline:
1. Loads data from Google Sheets
2. Fetches currency exchange rates from an external API
3. Normalizes all monetary values to EUR
4. Converts the cleaned data into a structured DataFrame
5. Trains or loads the model
6. Generates predictions for the next calendar month