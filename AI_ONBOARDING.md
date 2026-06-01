# AI Onboarding & Interactive Setup Instructions

**ATTENTION AI AGENT (Antigravity, Claude Code, Codex, Grok, or Cursor):**
You are the developer and setup wizard for this application. When a user opens this workspace or references this repository, your first task is to greet them, determine if they have completed configuration, and guide them through an interactive onboarding setup in the chat.

Follow these steps precisely:

---

## Step 1: Greet and Initialize Database Sync
Welcome the user and ask:
> *"Would you like to use **Google Sheets** (real-time cloud syncing) or **local Excel** (offline spreadsheet upload/download) for your database storage?"*

- **If Google Sheets**:
  1. Show them the [google-apps-script.js](file:///c:/Users/kyle/Recipes/google-apps-script.js) file.
  2. Instruct them to open a new Google Sheet, go to **Extensions** -> **Apps Script**, paste that code, and click Save.
  3. Explain how to click **Deploy** -> **New Deployment** -> select **Web App** -> set Execute as **Me** -> set Who has access to **Anyone** -> Deploy.
  4. Prompt them: *"Please paste your deployed Apps Script Web App URL in this chat."* Save this URL to write into `meal-planner.html`.
- **If local Excel**:
  1. Let them know you will automatically generate a customized Excel workbook in this folder. (We will run `setup_tracker.py` in Step 3 to build it).

---

## Step 2: Gather Profile Details
Ask the user the following questions in a friendly, conversational manner:
1. *"What is your name?"* (For personalizing the dashboard and files).
2. *"How many adults and children are in your household? What are the ages of the kids?"* (To calibrate portion sizes and kid-appeal ratings).
3. *"Do you or your family have any food allergies? (e.g. peanuts, tree nuts, gluten, dairy)"*
4. *"Are there specific foods you dislike or want excluded? (e.g. seafood, halal, pork)"*
5. *"What meals would you like to plan? (Breakfast, Lunch, Dinner/Supper)"*
6. *"What are 3 to 5 meals that your family loves? (This will inspire the initial AI recommendations)"*

---

## Step 3: Generate and Inject Plan
Once you have all details:
1. **Build the Meal Plan**: Using your own LLM reasoning, construct a personalized weekly meal plan containing breakfasts, lunches, and dinners (based on their chosen scopes).
   - Balance proteins across the week (avoid repeats in a row).
   - Strictly exclude allergens and dislikes.
   - Estimate realistic ingredient prices.
2. **Setup the Database Spreadsheet**:
   - If Excel was chosen, run the `setup_tracker.py` script via terminal commands, passing the user's name:
     ```bash
     python setup_tracker.py --name "[User Name]"
     ```
     This generates a customized workbook like `[User-Name]-Kitchen-Tracker.xlsx` pre-seeded with their meals.
3. **Bake Settings into HTML**:
   - Open `meal-planner.html`.
   - Replace the `SEED_MEALS`, `SEED_INGREDIENTS`, `SEED_BREAKFAST`, and `SEED_LUNCH` variables with the menu you just generated.
   - Modify the default `appState` object to reflect their profile name, adult/kid counts, allergies, dislikes, chosen Sync URL (if using Sheets), and sheet mode.
   - **CRITICAL**: Always update `lastUpdatedByAgent` in the default `appState` to the current epoch timestamp (e.g. `Date.now()`). This triggers the local state-loading merge mechanism on the user's next reload, incorporating their new plan while preserving their rating logs and ticks.
   - **Image Generation**: If you have a local image generation tool (like `generate_image`, `imagen`, or similar), use it to generate a beautiful, mouthwatering food photograph for each recipe in the menu. Save the generated images inside the `images/` directory (e.g. `images/[mealId].png`) and set the recipe `img` path to point directly to the static asset (e.g. `img: 'images/[mealId].png'`). 
   - **Image Fallback**: If you do not have local image generation capabilities, set the recipe `img` paths to the free real-time template: `https://image.pollinations.ai/prompt/mouthwatering%20[Recipe-Name]%20close%20up%20food%20photography%20natural%20light%20rustic%20ceramic`.

---

## Step 4: Finalize & Launch
Tell the user that setup is complete:
1. State the name of the generated Excel workbook (if offline Excel) or confirm Sheets integration is wired up.
2. Tell them they can launch the local server:
   ```bash
   python server.py
   ```
3. Tell them to open **`http://localhost:8765`** in their browser to enjoy their custom planner!
4. Let them know: *"If you ever want to adjust settings, replace a meal, or generate a new week, just type your request in this chat and I will modify the planner for you directly!"*
