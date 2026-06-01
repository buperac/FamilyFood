# Weekly Family Meal Planning (Gronning Family)

A rolling weekly meal planning system for a family of 6 (eats like 4).

## Family

| Member  | Age | Notes (update over time) |
|---------|-----|--------------------------|
| Adult 1 | -   | Calorie target: ~2,200/day |
| Adult 2 | -   | Calorie target: ~2,000/day |
| Kid     | 16  | Eats adult portions |
| Kid     | 13  | Eats near-adult portions |
| Kid     | 6   | Half portions, picky/preference notes TBD |
| Kid     | 4   | Small portions, picky/preference notes TBD |

## How this works

Each week lives in its own folder: `week-YYYY-MM-DD` (the Monday of that week).

Inside each weekly folder:
- **`meal-plan.md`** — 7 dinners with recipes, calories per adult serving, kid-appeal notes
- **`shopping-list.md`** — split into a Costco list and a Walmart.ca list, with quantities and "best value" notes
- **`feedback.md`** — fill this in after each meal: rating, who ate what, actual cost, what to change

## The loop

1. **Sunday before**: Claude drafts the week's plan + shopping list
2. **Same Sunday**: Codex (codex-rescue subagent) does a second-opinion pass — calorie reality check, kid-acceptance audit, cost/SKU corrections. Critique gets saved alongside the plan as `codex-review.md` so we can see what was flagged.
3. **Sunday/Monday**: Order groceries (Walmart.ca + Costco Sameday) — Claude drives the Claude-in-Chrome extension against Kyle's logged-in Chrome session. Kyle watches, approves checkout, and confirms payment.
4. **Each night**: Cook the meal, family rates it in `feedback.md`. Log actuals (cost, leftovers, who ate what).
5. **Next Sunday**: Claude reads the feedback, dispatches Codex to look at the data and recommend retire/rotate/adjust calls, then drafts week N+1.
   - Meals rated 4+/5 by both adults AND both little kids → `winners.md` rotation
   - Meals where the 4yo or 6yo refused → adjust seasoning/format and retry once. Retire after 2 failed attempts → `retired.md`.
   - Cost overruns get flagged and the next plan adjusts

**Pattern**: Claude drafts → Codex critiques → Claude integrates → deliver. Codex isn't ceremony — it has measurably caught calorie underestimates, price errors, and kid-acceptance blind spots on the first pass.

## Ordering

Kyle stays logged into Walmart.ca and Costco Sameday in his regular Chrome browser. The right tool is therefore the **Claude in Chrome MCP** (Chrome extension based), not Playwright — because the extension attaches to the existing browser session, so logins, saved addresses, and saved payment methods are all already available.

**Flow per order**:
1. Claude calls `list_connected_browsers` to confirm Chrome is wired up
2. Claude navigates to the search bar (Walmart.ca grocery or Costco Sameday)
3. For each item on the shopping list: search → verify the right SKU/size → add to cart
4. Kyle reviews the cart in his own browser tabs (he's watching live)
5. Kyle approves checkout + delivery options himself (Claude does not enter payment info)

If for any reason Chrome MCP isn't connected when we need it, fallback is a copy-paste-ready shopping list organized in the order each site's nav is structured.

## Meal scope

We plan all three meals, but with different levels of structure:

- **Dinner** — fully planned. 7 recipes/week, all in `meal-plan.md`. Kyle (and sometimes spouse) cooks. Leftovers are *expected and welcome*.
- **Breakfast** — backbone of eggs (Kyle's default) plus 2-3 variations for variety. Pulled from `breakfast-rotation.md`. Sunday batch-prep (overnight oats, egg muffins) carries weekdays.
- **Lunch (wife)** — 4 "interesting salads" per week, pulled from `lunch-salads.md`. Other days she pulls from dinner leftovers or makes her own call.
- **Lunch (others)** — kids' school lunches and Kyle's work meals are out of scope of this system unless he wants to add them later.

## Constraints & philosophy

- **Cost-conscious but quality-conscious** — we'll save where it makes sense (Costco bulk, store-brand condiments), but won't sacrifice quality on key items (Costco salmon, real parmesan, no jarred lemon juice).
- **Leftovers are a feature, not a bug** — many dinners are intentionally over-portioned so they become lunch the next day or a make-ahead meal Wed.
- **Ground beef is plentiful** — Kyle has a stash. Plan 1-2 ground beef meals/week from `ground-beef-ideas.md` until depleted. Don't buy more ground beef.
- **Busy household** — most weeknight dinners under 40 min; weekend slower meals OK.
