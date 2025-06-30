# DM Beat It Tracker - User Guide

## 🏁 Getting Started
1. **Launch the app**:
   ```bash
   python src/DiabetesTracker.py
   ```

2. **Main Menu Options**:
   - `Add`: Log new habits (e.g., blood sugar levels)
   - `View`: Check your progress
   - `Export`: Save data to CSV

## 📝 Step-by-Step Usage
### Logging a New Entry
```
> Enter command [add/view/export/quit]: add
> Enter habit type (medication/glucose/exercise): glucose
> Enter value: 120
> Entry saved!
```

### Viewing Analytics
![Analytics Screenshot](docs/images/analytics.png)

## ❓ Troubleshooting
| Issue | Solution |
|-------|----------|
| App crashes | Run `pip install -r requirements.txt` |
| Data not saving | Check file permissions for `habits.json` |

## 📞 Support
Create an issue on [GitHub](https://github.com/NURSEIJ/dm-beat-it-tracker/issues).
