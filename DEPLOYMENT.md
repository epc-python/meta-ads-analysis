# Streamlit Deployment Guide

## Prerequisites
- Python 3.8 or higher
- Streamlit Cloud account (free) or your own server

## Files Required for Deployment
- `streamlit_app.py` - Main application file
- `calculations.py` - Helper functions
- `requirements.txt` - Python dependencies
- `raw-data/` folder with CSV files

## Deployment Steps

### Option 1: Streamlit Cloud (Recommended)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Select `streamlit_app.py` as the main file
5. Deploy!

### Option 2: Local/Server Deployment
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   streamlit run streamlit_app.py
   ```

## Important Notes
- Make sure all CSV files are in the `raw-data/` folder
- The app will automatically load all CSV files from that folder
- Data is cached for better performance
- Error handling is included for missing files or columns

## Troubleshooting
- If you get import errors, check that all files are in the correct directory
- If data doesn't load, verify CSV files are in `raw-data/` folder
- Check that CSV files have the required columns listed in the error messages
