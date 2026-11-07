# ReviewGuard – AI-Powered Fake Review Detection

ReviewGuard is an AI-powered web application that analyzes Flipkart product reviews and identifies potentially fake and genuine reviews using Natural Language Processing (NLP) and a fine-tuned RoBERTa model.

## Features

- Flipkart review scraping using Playwright.
- Review cleaning and preprocessing.
- AI-based fake and genuine review classification.
- Interactive analysis dashboard.
- Fake review percentage and trust score.
- Cloudflare Turnstile protection.

## Tech Stack

- **Frontend:** React.js, Vite
- **Backend:** Python, FastAPI
- **AI Model:** RoBERTa, PyTorch, Hugging Face Transformers
- **Web Scraping:** Playwright
- **Data Processing:** Pandas
- **Security:** Cloudflare Turnstile
- **Frontend Hosting:** Vercel
- **Backend Tunneling:** Cloudflare Tunnel

## Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/gaganmandal/fake-review-detector.git
cd fake-review-detector
```

### 2. Backend Setup

Navigate to the backend folder:

```bash
cd backend
```

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
playwright install chromium
```

Create a `.env` file inside the backend folder:

```env
TURNSTILE_SECRET_KEY=your_turnstile_secret_key
```

Make sure the trained model files are available inside:

```text
backend/fake_review_model/
```

Start the backend:

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Backend API:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

### 3. Frontend Setup

Open a separate terminal and navigate to the frontend folder:

```bash
cd frontend-vite
```

Install dependencies:

```bash
npm install
```

Start the frontend:

```bash
npm run dev
```

Open the local URL displayed by Vite in your browser.

## Cloudflare Tunnel Setup

Cloudflare Tunnel exposes the locally running backend through a public URL.

### 1. Install Cloudflared

Download Cloudflared:

https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/

### 2. Start the Backend

Make sure FastAPI is running on port `8000`.

### 3. Start Cloudflare Tunnel

Open another CMD window and execute:

```bash
cloudflared tunnel --url http://127.0.0.1:8000
```

Cloudflare will generate a temporary public URL, for example:

```text
https://your-random-name.trycloudflare.com
```

### 4. Configure Vercel

Add the following environment variable in your Vercel project:

```env
VITE_API_URL=https://your-random-name.trycloudflare.com
```

Also configure:

```env
VITE_TURNSTILE_SITE_KEY=your_turnstile_site_key
```

Redeploy the frontend after updating the environment variables.

**Note:** Cloudflare Quick Tunnel URLs are temporary and may change after restarting the tunnel. The laptop, backend, and tunnel must remain running while using the application.

## How It Works

1. User submits a Flipkart product or reviews URL.
2. Cloudflare Turnstile verifies the user.
3. Playwright collects product reviews.
4. Review data is cleaned and preprocessed.
5. The RoBERTa model analyzes the reviews.
6. Reviews are classified as fake or genuine.
7. Results and trust score are displayed on the dashboard.

## Trust Score

The application calculates the trust score based on the percentage of reviews classified as genuine.

```text
Trust Score = (Genuine Reviews / Total Reviews) × 100
```

Note: Trust Score represents the proportion of reviews classified as genuine. It does not represent model accuracy.

## Live Demo

https://fake-review-detector-tawny.vercel.app

## Author

**Gagan Mandal**

GitHub: https://github.com/gaganmandal

## Future Improvements

- Support for additional e-commerce platforms.
- Improved fake review detection accuracy.
- Better review analysis and visualizations.
- Review-level explanations.
- Permanent cloud deployment of the backend.

---

*ReviewGuard – Building trust in online shopping through Artificial Intelligence.*
