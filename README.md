# AI Meal Planner & Grocery Shopping Hub

A premium, customizable, and open-source weekly meal planner that adapts to your family's sizes, preferences, allergies, and dislikes. It integrates with your chosen LLM (Gemini, Claude, ChatGPT, or Grok) to generate custom weekly menus, logs ratings and notes to Google Sheets or Excel, and automatically generates browser automation scripts to populate your online grocery carts.

## Key Features
- **Dynamic Onboarding & Profiles**: Define your name, number of adults/kids, favorite meals, allergies, and dislikes.
- **Choose Your AI Brain**: Plug in your own API key for **Google Gemini**, **Anthropic Claude**, **OpenAI ChatGPT**, or **xAI Grok**.
- **Free Keyless Images**: Automatically spins up high-quality mouthwatering recipe photos using Pollinations.ai (with DALL-E 3 fallback).
- **Interactive Ratings & Replacements**: Skip meals (which deducts ingredients from your shopping list), rate meals, or replace individual meals on the fly.
- **Double Sync Connectors**:
  - **Google Sheets Web App**: Sync ratings, notes, and costs in real-time.
  - **Offline Excel**: Upload an `.xlsx` file to sync price indexes or ratings, and export a clean spreadsheet copy client-side.
- **Browser Shopping Console Injector**: Instantly generates browser console scripts to load ingredients directly into your shopping cart on **Walmart.ca**, **Costco Same-Day**, and **Instacart**.

---

## Getting Started

### 1. Run the Local Server
Since web browsers restrict calling APIs like OpenAI or Anthropic directly from raw local HTML files due to Cross-Origin Resource Sharing (CORS) rules, we provide a zero-dependency Python server.

Run this command in your terminal inside the project directory:
```bash
python server.py
```
This will start a local server at **`http://localhost:8765`**. Open this address in your web browser.

*(If you are host it on a static server like GitHub Pages, you can still use Google Gemini directly since Google supports CORS for browser clients, but for other providers, the local proxy server is recommended.)*

---

## Integrations Setup

### 2. Connect to Google Sheets (Optional)
To log your history, ratings, and track prices over time in a spreadsheet:
1. Open a new Google Sheet.
2. Go to **Extensions** -> **Apps Script**.
3. Copy the code from [google-apps-script.js](file:///c:/Users/kyle/Recipes/google-apps-script.js) and paste it in.
4. Click Save.
5. Click **Deploy** -> **New Deployment**.
6. Under "Select type", choose **Web App**.
7. Set "Execute as" to **Me** (your email).
8. Set "Who has access" to **Anyone** (this allows the client-side app to send sync payloads).
9. Click **Deploy**. Authorize the script when prompted.
10. Copy the generated **Web App URL** and paste it into the **Sync Integrations** step of the planner's settings wizard!

### 3. Connect to Excel (Optional)
If you prefer offline spreadsheets:
1. In the settings, switch storage mode to **Local Excel Mode**.
2. Click **Export Excel** to download the meal log and ingredient list as a `.xlsx` file.
3. Update prices or log entries in Excel.
4. Click **Import Excel** to upload the spreadsheet back and sync your ratings/pantry inventory.

---

## How the AI Personalization Works (The Memory Loop)
When generating weekly plans or replacements, the app reads your saved ratings (1-5 stars) and favorites from local storage. It appends these to the system prompt (e.g., *"Liked: Tacos (5 stars), Avoid: Tikka Chicken (1 star)"*) so the LLM continuously refines its meal suggestions to suit your family's tastes.

---

## Online Grocery Shopping Automation
1. Navigate to the **Shopping List** section.
2. Ensure items you already have in stock are checked (they will be struck-through and removed from the total).
3. Click **Shop Online**.
4. Select your preferred store (**Walmart**, **Costco**, or **Instacart**) and copy the generated console script.
5. Open your grocery store page in another tab and log in.
6. Open browser DevTools by pressing **F12** (or right-click -> Inspect) and go to the **Console** tab.
7. Paste the copied script and hit **Enter**. Watch the browser search and add items to your checkout cart! Review and place the order manually.
