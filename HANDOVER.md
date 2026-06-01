# Recipes Project — Handover
*Current as of 2026-05-31. New session: read this + `MEMORY.md` first. The original enhancement plan is archived at the bottom for history.*

## What this project is
A 3-week family meal-planning system for the **Gronning family** (2 adults + kids 16/13/6/4), Edmonton AB. Pieces:
- **`meal-planner.html`** — interactive hub. 21 dinner cards (3 week-tabs), live cost ledger, "I have it" checkboxes, "skip meal" vetoes, per-meal cost badge, 1–5 star rating + notes, favourites filter, CSV export, "📊 Open tracker" link. localStorage-persisted. Serve it at `localhost:8765` via the Preview MCP (`.claude/launch.json`, `python -m http.server 8765`).
- **`recipes-print.html`** — printable: all 21 dinners with full amounts + numbered steps + kid hacks, one recipe per page (`@media print`), plus condensed breakfast/lunch reference.
- **Plan docs**: `week-2026-05-25/` (Week 1, full recipes), `week-2026-06-01/` (Week 2, menu-level), `week-2026-06-08/` (Week 3, menu-level), `3-week-bulk-shopping.md`, `price-comparison.md`, `walmart-order-list.md`, `breakfast-rotation.md`, `lunch-salads.md`, `ground-beef-ideas.md`, `pantry-staples.md`, `deals-log.md`, `winners.md`/`retired.md`.
- **Live tracker**: Google Sheet (see below).
- **Grocery-shopping skill**: `~/.claude/skills/grocery-shopping/`.

## ✅ DONE (cumulative)
- **All 11 enhancements + 2 corrections** shipped & browser-verified (Codex-reviewed). App features, printable, deals log, grocery skill.
- **Dietary rules — enforced across app, printable, skill, memory:**
  - **No fish/seafood** (shellfish unconfirmed → avoid).
  - **No halal** (chicken thighs/drumsticks = Maple Leaf, not Mina Halal).
  - **⚠️ NUT ALLERGY** — no peanuts/tree nuts. Check the **actual ingredients list**, NOT "may contain" warnings (those are OK). **Sesame is OK.** (Walnut→sunflower seed swaps done; Thai-peanut salad → Asian cabbage slaw.)
  - **No gluten-free products** — cost/preference, not allergy. Buy regular pasta/bread/tortillas. Naturally-GF foods (rice, quinoa, produce) are fine.
  - **Ground beef from freezer stash** — never buy (until depleted).
  - **Butter**: stock salted + unsalted.
  - **Milk = 3%** (household preference, not 2%).
- **Live Google Sheets tracker** — "Gronning Family Kitchen — Tracker" in Kyle's **PERSONAL** `gronningk@gmail.com` account. ONE workbook, 3 tabs: **Meal Log** (21 dinners seeded), **Ingredient Prices** (73 items seeded; supersedes `price-comparison.md`), **Deals**. ID `1N_dke4EfsLF8WXnkuRNRFUwF6AwCErqXEXS4M5YFGyM`. **Browser-only access** — the Drive connector is the WORK account (bushelsenergy) and CANNOT see it. Read via Chrome (screenshot / CSV-export); write via the Name Box. Old work-account 3-sheet folder was trashed.
- **WEEK 1 GROCERY ORDER: PLACED + DELIVERED** ✅ (2026-05-31, Walmart.ca, "Alea G" household account, delivery to 3748 Kidd Crescent). All proper Week-1 ingredients were ordered and received — dinners (6; Wed kofta skipped), breakfast + lunch staples, and the 3 added lunches (Souvlaki chicken salad, Beet/feta/sunflower, Mexican street corn). Ground beef from stash.

## 🔑 Grocery-automation lessons (learned the hard way this session — also in the skill)
- **Tooling**: Claude-in-Chrome against Kyle's logged-in Chrome (**never Playwright**). Two Chromes/profiles connect: **Work** = bushelsenergy (Walmart cart lives here, "Alea G"), **personal** = gronningk (the tracker sheet). Use `switch_browser` to let Kyle pick.
- **Removals**: reliable via JS `.click()` on the item's "Remove" — BUT match the product name within its **item-sized container** (text < ~200 chars), or the walk-up matches a parent holding *all* names and clicks the wrong row.
- **Adds**: a search tile's "Add" button renders *before* its React handler hydrates → an immediate JS click no-ops silently. Fix: **wait ~2 s after the button appears, then click**, and **verify by re-reading the cart** (per group). Match by `aria-label="Add to cart - <name>"` with must/avoid term filters; filter out seeds/plants and the wrong variants (gluten-free, dairy-free, jerk/seasoned, pickled).
- **Verify END STATE, never action-success**: the cart item *count* and an aria-click both lied this session. Always read the actual cart contents.
- **Bot wall**: ~20+ rapid automated actions trips Walmart's "Verify Your Identity" page. **Never bypass a CAPTCHA** — stop and hand to Kyle. Go slower / smaller batches next time; lean on "Buy Again"/"My Items".
- **Leave judgment items to Kyle**: specialty proteins (whole chicken had a deceptive "jerk flattened" lookalike) and anything needing an **ingredient-panel** check (granola → nut rule).
- **Kyle always authenticates, clears bot-walls, and clicks Place Order. Claude never checks out / enters payment.**

## ▶️ NEXT SESSION — start here
1. **Collect Week-1 feedback** after the family eats: ratings/notes go in `meal-planner.html` (in Kyle's Work Chrome at `localhost:8765`). To sync into the tracker: read the app's `localStorage` key `bushels-meal-plan-v1` via Claude-in-Chrome (same Work profile/origin), then write rows into the **Meal Log** tab (personal Chrome).
2. **True-up Ingredient Prices** tab with actual prices from the delivered Week-1 order; **fix the "Milk 2%" cell → "Milk 3%"** (still says 2%; browser-only edit on the personal-account sheet).
3. **Log the Week-1 order** in the tracker (Meal Log: date cooked / actual cost as the week runs; Deals tab: any stock-up finds).
4. **Plan / refine Week 2** — apply the grocery lessons (smaller, slower, verify-by-reading). Week 2 dinners are menu-level in `week-2026-06-01/meal-plan.md`; full recipes already exist in `recipes-print.html`.
5. **(Optional) Apps Script auto-sync** — designed, not built. Bind to the tracker workbook, `getSheetByName('Meal Log')`, deploy as a Web App from `gronningk@gmail.com`, then add a `fetch()` in `meal-planner.html` so ratings POST themselves. Kyle must do the deploy/auth.
6. **Gemini key + billing** for the remaining Week 2/3 card images (free-tier image quota = 0; W2 mon/tue/wed exist, rest fall back to emoji). Image prompts archived below.

## Process reminders
- **Codex** = recurring second-opinion collaborator on plans/code (caught real bugs + recipe-quantity issues this session).
- Family prefs: wife wants interesting salads; breakfast = eggs backbone + variety; leftovers welcome; cost-conscious AND quality-conscious.

---
---
## 📦 ARCHIVE — original enhancement plan & image prompts (historical)

### Week 2 & 3 image prompts (Kyle generates in Antigravity, save as `images/<id>.png`, ~3:2)
**Shared style suffix:** *"Professional appetizing food photography, 45-degree angle, soft natural window light, rustic ceramic dishware on a warm wooden table, shallow depth of field, vibrant fresh ingredients, cozy home-kitchen mood, no text, no words, no people."*

**Week 2** (w2mon/tue/wed already generated):
- `w2thu.png` — Honey-garlic chicken thighs: glossy sticky glazed thighs over white rice, sesame + green onion.
- `w2fri.png` — Calzones: golden folded pizza pockets, one cut open showing melted cheese + pepperoni, marinara for dipping.
- `w2sat.png` — Smashburgers: two thin crispy-edged cheeseburgers on potato buns with dill spears, oven fries beside.
- `w2sun.png` — Pork tenderloin roast: sliced roasted pork tenderloin with crispy potatoes + green beans on a platter.

**Week 3:**
- `w3mon.png` — Italian wedding soup: brothy soup with tiny meatballs, small pasta + greens, parmesan, crusty bread.
- `w3tue.png` — Chicken quesadillas: golden crisp wedges oozing cheese, with rice + beans, salsa + sour cream.
- `w3wed.png` — Chicken souvlaki bowls: lemon-garlic chicken over rice with tzatziki, cucumber, tomato, red onion, feta.
- `w3thu.png` — BBQ chicken drumsticks: sticky glazed drumsticks with corn on the cob + creamy coleslaw.
- `w3fri.png` — Homemade pizza fresh from the oven, bubbling cheese + toppings on a wooden board (vary toppings from Week 1).
- `w3sat.png` — Beef tacos: soft tortillas with seasoned beef, queso fresco, quick-brined red onion, cilantro, lime, avocado.
- `w3sun.png` — Roast chicken dinner: golden whole roast chicken with crispy potatoes + vegetables (encore).

*(The original 11-enhancement plan that drove this project is preserved in git history / earlier versions of this file; all items are now complete.)*
