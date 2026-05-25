# Time Warp Completion Tracker — Setup (5 minutes, one-time)

## 1. Create the Google Sheet
1. Go to [sheets.google.com](https://sheets.google.com), click **+ Blank**.
2. Rename the sheet **"Time Warp Completions"** (top-left corner).
3. Rename the bottom tab **Sheet1 → Log** (right-click the tab).
4. In row 1, paste this header row:

```
Timestamp	Game	Period	First Name	Last Name	Status	Score	Restarts	Time (min)	Path
```

(Tab-separated — pastes cleanly into 10 columns. Bold the row + freeze it via View → Freeze → 1 row.)

## 2. Deploy the Apps Script
1. In your new sheet: **Extensions → Apps Script**.
2. Delete the placeholder `function myFunction() {}` code.
3. Open `apps-script-template.gs` (in this `tracker/` folder), copy ALL of it, paste into the Apps Script editor.
4. Click the floppy-disk **Save** icon (or Ctrl+S). Name the project "Time Warp Tracker".
5. Click **Deploy → New deployment** (top-right).
6. Gear icon → choose **Web app**.
7. Fill in:
   - Description: *Time Warp tracker v1*
   - Execute as: **Me (your email)**
   - Who has access: **Anyone**
8. Click **Deploy**.
9. Authorize when prompted:
   - Click "Authorize access"
   - Choose your Google account
   - You'll see "Google hasn't verified this app" — that's fine, it's YOUR script.
   - Click **Advanced → Go to Time Warp Tracker (unsafe)**
   - Click **Allow**
10. **Copy the Web app URL** that appears. It looks like:
    `https://script.google.com/macros/s/AKfycby.../exec`

## 3. Plug the URL into the games
The URL needs to be added to each Time Warp HTML file. In the `<script>` tag where
`TimeWarp.init({...})` is called, set `webhookUrl: "PASTE_URL_HERE"`.

You can either:
- (a) Tell me the URL and I'll bake it into every Time Warp, OR
- (b) Edit one constant in `tracker/config.js` (centralized — recommended)

## 4. Test it
1. Open any Time Warp HTML in Chrome.
2. The identity modal appears: enter Period / First / Last, click START.
3. Play through to the end.
4. On completion, you should see "✓ Saved!"
5. Open your Google Sheet — a new row should appear within 1-2 seconds.

## Troubleshooting
- **"⚠ Couldn't reach server"** → check the webhook URL is pasted correctly, and the Apps Script is deployed as "Anyone" access.
- **Sheet shows blank rows** → the script ran but `data.field` was undefined. Open Apps Script → Executions to see the error.
- **Want to reset identity** (e.g. a student typed wrong name) → open browser DevTools → Console → `TimeWarp.clearIdentity()` then refresh.

## What if a student is offline / submission fails?
The game shows a screen with the payload visible. They show you the screen; you enter the row manually. Future enhancement: queue failed submits in localStorage and retry.
