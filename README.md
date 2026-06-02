# FamilyFood

AI meal planning, grocery-list cleanup, and household food feedback in one local-first app.

FamilyFood is built for families who want a practical weekly meal loop: generate meals around real preferences, mark what you already own, skip meals, rate what worked, and keep a spreadsheet record for the next plan.

## What It Does

- Builds weekly breakfast, lunch, and dinner plans from your family profile.
- Supports bring-your-own API keys for Google Gemini, Anthropic Claude, OpenAI, or xAI Grok.
- Tracks allergies, dislikes, favorite meals, adult count, and child count.
- Calculates the active grocery list from planned meals, skipped meals, and pantry ticks.
- Logs ratings, notes, favourites, cooked dates, estimated costs, and actual costs.
- Syncs with Google Sheets through a user-deployed Apps Script web app.
- Imports and exports Excel workbooks in the browser.
- Generates grocery helper payloads and experimental browser-console scripts for Walmart.ca, Costco Same-Day, and Instacart.
- Uses Pollinations.ai for keyless recipe images, with optional OpenAI image generation through the local proxy.

## Current Shape

This is a local-first v1, not a hosted SaaS product.

- No account system.
- No central database.
- No checkout or payment handling.
- API keys are never committed to the repo, but they are stored in your browser's local storage after you enter them.
- Non-Gemini model calls use the included local Python proxy so browser CORS does not block requests.
- Shopping scripts are helpers, not guaranteed cart automation. Store websites change often. Always review the cart manually before checkout.

## Files

| File | Purpose |
| --- | --- |
| `meal-planner.html` | Main app: profile setup, meal generation, shopping list, ratings, Excel import/export, Sheets sync |
| `server.py` | Local proxy for model and image requests |
| `google-apps-script.js` | Template for optional Google Sheets sync |
| `setup_tracker.py` | Optional workbook generator for offline Excel tracking |
| `recipes-print.html` | Printable sample recipe set |
| `AI_ONBOARDING.md` | Instructions for AI coding agents helping a user configure the app |
| `batch-images.json` | Example image-generation batch prompts |

## Quick Start

1. Clone or download this repo.
2. Start the local server:

```bash
python server.py
```

3. Open:

```text
http://localhost:8765
```

4. Complete Setup / Settings:

- Add household size.
- Add allergies and dislikes.
- Choose meal scopes.
- Add your model provider and API key.
- Choose Google Sheets or local Excel mode.

Gemini may also work from a static host because the app has a direct Gemini fallback. OpenAI, Anthropic, Grok, and OpenAI image generation need `server.py`.

## Optional Excel Workbook

The app can export Excel directly in the browser. If you want a blank starter workbook, install the optional Python dependency and run:

```bash
pip install -r requirements.txt
python setup_tracker.py --name "Family"
```

This creates `Family-Kitchen-Tracker.xlsx`.

## Optional Google Sheets Sync

1. Create a Google Sheet.
2. Open Extensions -> Apps Script.
3. Paste the contents of `google-apps-script.js`.
4. Deploy it as a Web App.
5. Set "Execute as" to "Me".
6. Set access to "Anyone".
7. Copy the Web App URL into FamilyFood settings.

Important: the app sends sync requests in `no-cors` mode, so the browser cannot verify the Apps Script response. Check the sheet after the first sync.

## Shopping Helpers

FamilyFood can generate:

- A JSON shopping payload.
- Walmart.ca helper script.
- Costco Same-Day helper script.
- Instacart helper script.

Run these only in your own browser session, while logged into the store. Review every item, size, substitution, price, and checkout step yourself. Do not use the scripts to bypass CAPTCHA, identity checks, payment steps, or store rules.

## Privacy

- Meal plans, ratings, notes, and API keys are stored in browser local storage.
- Google Sheets sync sends meal-log data to the Apps Script URL you provide.
- Model requests send your profile and prompt to the model provider you choose.
- Recipe images may be requested from Pollinations.ai or OpenAI, depending on settings.

## Known Limits

- Grocery helper scripts depend on store page markup and may break.
- Ingredient prices are estimates until you log actual costs.
- Google Sheets sync is fire-and-forget from the browser.
- The printable recipe file is a starter sample, not an automatically regenerated export from the app.
- No license file is included yet; add one before inviting broad reuse or forks.
