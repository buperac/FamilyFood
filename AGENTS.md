# FamilyFood Agent Instructions

## Product Scope

FamilyFood is a public, local-first meal planner and grocery helper for families.

Current v1 scope:
- Generate and refine weekly meals from a household profile.
- Track allergies, dislikes, favorites, ratings, notes, skipped meals, pantry ownership, estimated cost, and actual cost.
- Keep `meal-planner.html`, `recipes-print.html`, `google-apps-script.js`, `setup_tracker.py`, `server.py`, `README.md`, and `AI_ONBOARDING.md` consistent.
- Support optional Google Sheets sync and local Excel import/export.
- Provide grocery helper payloads/scripts that users manually review before checkout.
- Ship the public instance clean. The default repo should not include starter meals, prices, ingredient amounts, brands, pantry ownership, or household-specific printable recipes.

Out of scope unless explicitly requested:
- Hosted SaaS accounts, payments, user auth, central databases, subscriptions, or analytics.
- New store integrations beyond the current helper-script model.
- Completing grocery checkout, entering payment details, bypassing CAPTCHA, or hiding store warnings.
- Hard-coding one private household's allergies, dislikes, brands, account details, or freezer inventory into public defaults.

## Source Of Truth

Read before making product claims or edits:
1. `README.md` for public product scope and user-facing claims.
2. `meal-planner.html` for actual app behavior.
3. `server.py` for model/image proxy behavior.
4. `google-apps-script.js` for Sheets sync behavior.
5. `setup_tracker.py` for workbook generation.
6. `recipes-print.html` for printable sample behavior.
7. `AI_ONBOARDING.md` for agent setup workflow.

If docs and code conflict, fix the docs or code so public claims match implemented behavior.

## Public Release Rules

- No personal names, personal Google accounts, street addresses, private trackers, or family-specific constraints in tracked product files unless framed as removable sample data.
- Do not commit API keys, Apps Script URLs, cookies, browser profiles, carts, payment details, or generated user workbooks.
- Ingredient prices and quantities must be added by the user, model, or agent after setup; do not preload them in public defaults.
- Ingredient prices must be labeled as estimates unless backed by actual logged purchases.
- Shopping scripts must be described as helpers/experimental unless they were verified live against the store.
- Warn users to manually review cart contents, substitutions, sizes, prices, delivery details, and checkout.

## Coding And Editing

- Keep the static/local workflow unless the user asks for a hosted version.
- Keep edits tightly scoped. Do not refactor unrelated code for style.
- Preserve `LOCAL_STORAGE_KEY` unless intentionally migrating user state.
- Keep seeded defaults empty for the public repo. If changing seeded defaults for a private/user-specific instance, update `lastUpdatedByAgent` only when the merge behavior is intended.
- Never write secrets into default `appState`.
- If changing recipe, ingredient, price, or portion logic, verify the meal grid, shopping list, ledger, skip toggles, pantry ticks, and Excel export.
- After meaningful UI or app edits, run the local server and verify in a browser.

## Review Style

Be source-bound and numbers-first:
- Findings before summary.
- Cite concrete files, lines, quantities, costs, and behavior.
- Separate confirmed behavior from best guesses.
- Do not invent missing features.
- If asked for failure-only output, report only evidenced failures or omissions.

## Collaboration Style

Direct answer first, then the reason.

Use concise bullets. Push back when a requested change expands beyond v1 or adds another tool/integration without a clear payoff. If the work starts drifting into v2, call it and return to the smallest public improvement that makes the repo more credible.
