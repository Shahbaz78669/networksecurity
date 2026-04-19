# Network Security — Phishing URL Detection API

A machine-learning-powered FastAPI service that classifies URLs as **phishing** or **legitimate**.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Local Development](#local-development)
3. [Deployment Guide (GitHub Student Developer Pack)](#deployment-guide-github-student-developer-pack)
   - [Free Services Used](#free-services-used)
   - [Step 1 — MongoDB Atlas (free database)](#step-1--mongodb-atlas-free-database)
   - [Step 2 — Docker Hub (free image registry)](#step-2--docker-hub-free-image-registry)
   - [Step 3 — Deploy to Render.com (free hosting)](#step-3--deploy-to-rendercom-free-hosting)
   - [Step 4 — GitHub Actions CI/CD (automatic deploys)](#step-4--github-actions-cicd-automatic-deploys)
   - [Alternative — Deploy to Railway.app](#alternative--deploy-to-railwayapp)
4. [API Endpoints](#api-endpoints)
5. [Environment Variables Reference](#environment-variables-reference)

---

## Project Overview

| Component | Technology |
|-----------|-----------|
| API framework | FastAPI |
| ML library | scikit-learn |
| Database | MongoDB Atlas |
| Experiment tracking | MLflow + DagShub |
| Containerisation | Docker |
| CI/CD | GitHub Actions |

---

## Local Development

```bash
# 1. Clone the repo
git clone https://github.com/Shahbaz78669/networksecurity.git
cd networksecurity

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
pip install -e .

# 4. Set environment variables
cp .env.example .env
# Edit .env and fill in your MONGODB_URL_KEY and other values

# 5. Run the API server
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# Open http://localhost:8000/docs in your browser
```

---

## Deployment Guide (GitHub Student Developer Pack)

> **No credit card required.** Every service below has a free tier that works with your [GitHub Student Developer Pack](https://education.github.com/pack).

### Free Services Used

| Service | Purpose | Credit card? |
|---------|---------|-------------|
| [MongoDB Atlas](https://www.mongodb.com/atlas/database) | Database (M0 free cluster) | ❌ Not required |
| [Docker Hub](https://hub.docker.com) | Container image registry | ❌ Not required |
| [Render.com](https://render.com) | Host the FastAPI app | ❌ Not required |
| GitHub Actions | CI/CD pipeline | ❌ Already included |

---

### Step 1 — MongoDB Atlas (free database)

1. Go to <https://www.mongodb.com/atlas/database> and sign up with your GitHub account.
2. Choose the **free M0 cluster** (M0 is MongoDB Atlas's permanently free tier — 512 MB storage, no credit card required).
3. Under **Security > Database Access**, create a user with a strong password.
4. Under **Security > Network Access**, click **Allow Access from Anywhere** (`0.0.0.0/0`).
   > ⚠️ **Security note:** Allowing all IPs is convenient for getting started but is not recommended for production. Once everything works, replace `0.0.0.0/0` with the specific IP address(es) of your hosting service for a safer setup.
5. Click **Connect > Drivers** and copy the connection string. It looks like:
   ```
   mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
   ```
6. Save this — you will need it as `MONGODB_URL_KEY`.

---

### Step 2 — Docker Hub (free image registry)

1. Go to <https://hub.docker.com> and create a free account.
2. Note your **Docker Hub username** — you need it in Step 4.

---

### Step 3 — Deploy to Render.com (free hosting)

1. Go to <https://render.com> and sign up with your GitHub account.
2. Click **New + → Web Service → Connect a Repository**.
3. Choose this repository (`Shahbaz78669/networksecurity`).
4. Render auto-detects `render.yaml`. Review the settings and click **Create Web Service**.
5. Under **Environment**, add your secret environment variables:

   | Key | Value |
   |-----|-------|
   | `MONGODB_URL_KEY` | Your Atlas connection string from Step 1 |

6. Click **Save Changes** — Render will build and deploy the Docker image automatically.
7. Your API will be live at `https://networksecurity-api.onrender.com` (URL shown in the dashboard).

> **Note:** The free Render instance **spins down after 15 minutes of inactivity** and takes ~30 seconds to wake up on the next request. This is normal behaviour for the free plan.

---

### Step 4 — GitHub Actions CI/CD (automatic deploys)

Every time you push to `main`, GitHub Actions will:
1. Lint the code.
2. Build a Docker image and push it to Docker Hub.
3. Trigger a fresh deploy on Render.

**Set up the required secrets in your repository:**

Go to **Settings → Secrets and variables → Actions → New repository secret** and add:

| Secret name | Where to get it |
|-------------|----------------|
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_PASSWORD` | Docker Hub → **Account Settings → Security → New Access Token** |
| `RENDER_SERVICE_ID` | Render dashboard → Your service → URL contains the ID, e.g. `srv-xxxx` |
| `RENDER_API_KEY` | Render → **Account Settings → API Keys → Create API Key** |

After adding the secrets, push any commit to `main` to trigger the pipeline.

---

### Alternative — Deploy to Railway.app

[Railway.app](https://railway.app) is also available through the Student Developer Pack with **$5/month free credit**.

```bash
# Install the Railway CLI
npm install -g @railway/cli

# Login and link to this repository
railway login
railway link

# Set environment variables
railway variables set MONGODB_URL_KEY="your_connection_string"

# Deploy
railway up
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Redirects to interactive API docs (`/docs`) |
| `GET` | `/health` | Health check — reports model file availability |
| `GET` | `/train` | Runs the full training pipeline |
| `POST` | `/predict` | Upload a CSV file and get phishing predictions |

**Example prediction request:**

```bash
curl -X POST "https://<your-render-url>/predict" \
  -F "file=@your_data.csv"
```

---

## Environment Variables Reference

See [`.env.example`](.env.example) for a full list with descriptions.

| Variable | Required | Description |
|----------|----------|-------------|
| `MONGODB_URL_KEY` | ✅ Yes | MongoDB Atlas connection string |
| `PORT` | No (default `8080`) | Port the server listens on |
| `MLFLOW_TRACKING_URI` | Only for training | DagShub MLflow URI |
| `MLFLOW_TRACKING_USERNAME` | Only for training | DagShub username |
| `MLFLOW_TRACKING_PASSWORD` | Only for training | DagShub token |
| `AWS_ACCESS_KEY_ID` | Only for S3 sync | AWS credentials |
| `AWS_SECRET_ACCESS_KEY` | Only for S3 sync | AWS credentials |
| `AWS_BUCKET_NAME` | Only for S3 sync | S3 bucket name |
