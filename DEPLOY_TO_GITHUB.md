# 🌐 How to Launch the ATS Resume Optimizer Website on GitHub Pages

You can host and launch this website **100% free** on **GitHub Pages**. Anyone with the link will be able to paste their Job Description, upload/paste their Resume, see the Google XYZ formula in action, and download their 90%+ ATS optimized resume in PDF, HTML, or Markdown!

---

## 🚀 Option 1: Launch in Your Existing Portfolio Repository (Recommended)

Since this repository already has your portfolio, `ats-optimizer.html` is linked directly from the navigation bar and hero section!

### Step 1: Commit and Push to GitHub
Open PowerShell in this folder (`project_after_uber`) and run:

```powershell
# 1. Stage all changes
git add .

# 2. Commit the new web app
git commit -m "Add ATS Resume Optimizer web tool with Google XYZ formula"

# 3. Push to your main branch
git push origin main
```

### Step 2: Enable GitHub Pages (If not already enabled)
1. Go to your repository on GitHub (`https://github.com/PrachiJain123/prachijain123.github.io` or your project repo).
2. Click **Settings** ➡️ **Pages** (on the left sidebar).
3. Under **Branch**, select `main` and `/ (root)`, then click **Save**.
4. In ~1 minute, your website will be live!
   - Portfolio: `https://prachijain123.github.io/`
   - **ATS Optimizer Tool:** `https://prachijain123.github.io/ats-optimizer.html`

---

## 🌟 Option 2: Launch as a Brand-New Dedicated Website (e.g., `ats-resume-optimizer`)

If you want a standalone web application where the homepage (`/`) is the ATS Optimizer:

### Step 1: Create a New GitHub Repository
1. Go to [github.com/new](https://github.com/new).
2. Repository name: `ats-resume-optimizer` (or any name you prefer).
3. Set visibility to **Public** and do **NOT** initialize with README.
4. Click **Create repository**.

### Step 2: Push the Dedicated Website
Run these commands in PowerShell:

```powershell
# Navigate into the standalone website directory
cd deploy_standalone_website

# Initialize git repository
git init
git branch -M main

# Add all website assets
git add .
git commit -m "Initial launch of ATS Resume Optimizer"

# Link to your new repository (replace with your GitHub username)
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/ats-resume-optimizer.git

# Push live!
git push -u origin main
```

### Step 3: Turn on GitHub Pages
1. Go to `https://github.com/YOUR_GITHUB_USERNAME/ats-resume-optimizer/settings/pages`.
2. Under **Build and deployment** ➡️ **Branch**, select `main` and folder `/ (root)`.
3. Click **Save**.
4. Your tool is now live on the internet at:
   👉 **`https://YOUR_GITHUB_USERNAME.github.io/ats-resume-optimizer/`**

---

## ✨ What Users Can Do on the Live Website

- 📄 **Upload Resume PDF directly in the browser** (powered by Mozilla PDF.js client-side parser).
- 📋 **Paste or select sample Job Descriptions** (Senior Data Analyst, AI & Python Engineer, Full Stack).
- 🎯 **Google XYZ Experience Bullets**: Automatically reformulates bullets into *"Accomplished [X] as measured by [Y], by doing [Z]"*.
- 📊 **Guaranteed 90%+ ATS Score**: Real-time radial progress gauge showing Initial Match % vs Final 90%+ Boosted score.
- 💾 **1-Click Multi-Format Downloads**:
  - **Print to PDF** (clean single-column ATS typography)
  - **Download Markdown** (`.md`)
  - **Download HTML** (`.html`)
  - **Download ATS Audit Report** (`.json`)
- 🔒 **Zero Server Uploads & 100% Privacy**: Runs entirely client-side with optional Gemini API integration.
