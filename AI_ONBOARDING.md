# AI Agent Onboarding Instructions

These instructions are for AI coding agents helping a user set up or customize FamilyFood.

FamilyFood is a local-first family meal planner. Keep setup practical: profile, meal scope, sync mode, API provider, starter plan, and verification. Do not expand into hosted accounts, SaaS features, payments, or new integrations unless the user explicitly asks.

## Hard Rules

- Do not write API keys, sheet URLs, addresses, payment details, or private family data into committed files.
- Do not complete grocery checkout or payment.
- Do not bypass CAPTCHA, identity checks, or store anti-bot screens.
- Do not hard-code one household's allergies, dislikes, brands, stores, or freezer inventory as product defaults.
- Keep the public repo defaults clean: no starter meals, ingredient quantities, prices, pantry ownership, brands, or printable recipes.
- Keep claims in README and UI aligned with implemented behavior.

## Step 1: Choose Storage Mode

Ask whether the user wants:

- Google Sheets sync: ratings and meal logs are sent to a user-deployed Apps Script endpoint.
- Local Excel mode: users import/export `.xlsx` workbooks from the browser.

If Google Sheets is selected:

1. Tell the user to create a Google Sheet.
2. Tell them to open Extensions -> Apps Script.
3. Tell them to paste `google-apps-script.js`.
4. Tell them to deploy it as a Web App.
5. Tell them to paste the deployed Web App URL into the app settings, not into the repository.

If local Excel is selected:

1. Use browser import/export if the app is already running.
2. Optionally run `python setup_tracker.py --name "Family"` after installing `requirements.txt`.

## Step 2: Gather Profile Details

Ask only for the details needed to make the first usable plan:

1. Household name or display name.
2. Number of adults and children.
3. Ages or appetite notes for children, if relevant.
4. Allergies.
5. Dislikes and exclusions.
6. Meals to plan: breakfast, lunch, dinner, or any combination.
7. Three to five meals the family already likes.
8. Budget or store preference, if grocery planning matters.

## Step 3: Generate A Starter Plan

Build a 7-day plan that follows the user's rules:

- No allergens.
- No excluded foods.
- Rotate proteins and textures.
- Keep weeknight meals realistic.
- Include kid-facing mitigation notes when needed.
- Estimate prices honestly and label them as estimates.

If editing `meal-planner.html` directly for a user-specific instance:

1. Populate only the user-specific instance with meals, ingredients, quantities, and prices.
2. Preserve `LOCAL_STORAGE_KEY` unless the user asks for a migration.
3. Never bake secrets into `appState`.
4. If changing baked-in defaults for an existing user, update `lastUpdatedByAgent` to a current epoch timestamp so the app can merge newer defaults while preserving logs.
5. Do not commit user-specific populated seed data back to the public default unless the user explicitly asks for a demo dataset.

## Step 4: Verify

After meaningful edits:

1. Run `python server.py`.
2. Open `http://localhost:8765`.
3. Confirm the app loads.
4. Confirm Setup / Settings opens.
5. Confirm the meal grid renders.
6. Confirm the shopping ledger updates when a meal is skipped or an ingredient is ticked.
7. Confirm Excel export works if spreadsheet changes were touched.

Report any unverified area directly. Do not imply the shopping scripts were tested against live store pages unless they actually were.
