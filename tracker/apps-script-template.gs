/**
 * Time Warp Completion Tracker — Google Apps Script backend.
 *
 * v2: Auto-creates a separate tab per game. No manual tab setup needed.
 *
 * SETUP (one-time, 5 min):
 *  1. Create a new blank Google Sheet (Sheet1 untouched is fine — script ignores it).
 *  2. Extensions → Apps Script → paste THIS entire file as Code.gs
 *  3. Save (Ctrl+S). Click "Deploy" → "New deployment"
 *     - Type: Web app
 *     - Execute as: Me (you)
 *     - Who has access: Anyone
 *  4. Click Deploy. Authorize when prompted.
 *  5. Copy the Web app URL — paste into tracker/config.js.
 *
 * To update this script: edit, Save, Deploy → Manage deployments → edit pencil →
 *   Version: "New version" → Deploy. (URL stays the same.)
 *
 * Each game gets its own tab automatically (e.g., "Plymouth or Jamestown",
 * "Time Warp IV", etc.) with headers added on first write.
 */

const HEADERS = [
  "Timestamp", "Game", "Period", "First Name", "Last Name",
  "Status", "Score", "Restarts", "Time (min)", "Path",
];

function tabNameForGame(game) {
  if (!game) return "Untitled";
  // Strip sub-title after " — " or " - " so "Plymouth — Smith" and "Plymouth — Rolfe"
  // both write to the same "Plymouth" tab.
  const base = String(game).split(/\s+[—\-]\s+/)[0].trim();
  // Google Sheets tab-name forbidden chars: [ ] ? : / \ *
  const safe = base.replace(/[\[\]\?\:\/\\\*]/g, "").substring(0, 100);
  return safe || "Untitled";
}

function getOrCreateTab(ss, name) {
  let sheet = ss.getSheetByName(name);
  if (!sheet) {
    sheet = ss.insertSheet(name);
    sheet.appendRow(HEADERS);
    sheet.getRange(1, 1, 1, HEADERS.length).setFontWeight("bold").setBackground("#1a1410").setFontColor("#fdf6e3");
    sheet.setFrozenRows(1);
    sheet.setColumnWidth(1, 160); // Timestamp
    sheet.setColumnWidth(2, 260); // Game
    sheet.setColumnWidth(3, 90);  // Period
    sheet.setColumnWidth(6, 120); // Status
  }
  return sheet;
}

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const ss = SpreadsheetApp.getActive();
    const tabName = tabNameForGame(data.game);
    const sheet = getOrCreateTab(ss, tabName);

    const row = [
      data.timestamp || new Date().toISOString(),
      data.game || "",
      data.period || "",
      data.firstName || "",
      data.lastName || "",
      data.status || "",
      data.score == null ? "" : data.score,
      data.restarts == null ? 0 : data.restarts,
      data.timeSpent == null ? "" : Math.round(data.timeSpent / 60 * 10) / 10,
      data.path || "",
    ];
    sheet.appendRow(row);

    return ContentService
      .createTextOutput(JSON.stringify({ ok: true, tab: tabName }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ ok: false, error: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet() {
  return ContentService
    .createTextOutput("Time Warp tracker v2 is live. Per-game tabs auto-created on first POST.")
    .setMimeType(ContentService.MimeType.TEXT);
}
