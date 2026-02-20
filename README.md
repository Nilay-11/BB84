# Exhibit Nova - Streamlit Frontend

A polished exhibition frontend built with Streamlit.

## Run locally

```powershell
pip install -r requirements.txt
streamlit run app.py
```

## Deployment model

- GitHub Pages does not execute Python/Streamlit backends.
- For a working URL, deploy this repository on **Streamlit Community Cloud**.

## Push to GitHub

```powershell
git init
git add .
git commit -m "Add Streamlit exhibition frontend"
git branch -M main
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

## Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with GitHub.
3. Select your repo and branch `main`.
4. Set main file path to `app.py`.
5. Deploy.

You will get a public URL like:

`https://<your-app-name>.streamlit.app`
