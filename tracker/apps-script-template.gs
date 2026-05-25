/**
 * Time Warp Completion Tracker — Google Apps Script backend.
 * v4: Reordered columns - Period | First | Last leftmost. Game/Timestamp on right.
 *     Period is just the number (no "Period " prefix) so filter dropdowns are clean.
 *
 * SETUP / UPDATE:
 *  - Paste this entire file into Apps Script editor (Ctrl+A → Delete → Paste).
 *  - Save (Ctrl+S).
 *  - Deploy → Manage deployments → pencil → Version: "New version" → Deploy.
 *  - URL stays the same.
 *  - DELETE THE EXISTING "Plymouth or Jamestown" TAB so the new column layout takes effect
 *    (the script will auto-recreate it with the new schema on next submit).
 *
 * Column layout (10 columns):
 *   A: Period   B: First Name   C: Last Name   D: Status   E: Completions
 *   F: Attempts   G: Restarts   H: Time (min)   I: Game   J: Last Played
 */

const HEADERS = [
  "Period", "First Name", "Last Name",
  "Status", "Completions", "Attempts", "Restarts", "Time (min)",
  "Game", "Last Played",
];

const COL = {
  PERIOD: 0, FIRST: 1, LAST: 2,
  STATUS: 3, COMPLETIONS: 4, ATTEMPTS: 5, RESTARTS: 6, TIME: 7,
  GAME: 8, TIMESTAMP: 9,
};

function tabNameForGame(game) {
  if (!game) return "Untitled";
  const base = String(game).split(/\s+[—\-]\s+/)[0].trim();
  const safe = base.replace(/[\[\]\?\:\/\\\*]/g, "").substring(0, 100);
  return safe || "Untitled";
}

// Strip "Period " prefix so the cell holds just the number (1-7).
function normalizePeriod(p) {
  if (p == null) return "";
  const m = String(p).match(/(\d+)/);
  return m ? Number(m[1]) : String(p).trim();
}

function getOrCreateTab(ss, name) {
  let sheet = ss.getSheetByName(name);
  if (!sheet) {
    sheet = ss.insertSheet(name);
    sheet.appendRow(HEADERS);
    sheet.getRange(1, 1, 1, HEADERS.length)
      .setFontWeight("bold")
      .setBackground("#1a1410")
      .setFontColor("#fdf6e3");
    sheet.setFrozenRows(1);
    sheet.setColumnWidth(1, 70);   // Period (small)
    sheet.setColumnWidth(2, 110);  // First
    sheet.setColumnWidth(3, 110);  // Last
    sheet.setColumnWidth(4, 110);  // Status
    sheet.setColumnWidth(9, 240);  // Game
    sheet.setColumnWidth(10, 170); // Last Played
  }
  return sheet;
}

function findRow(sheet, period, firstName, lastName) {
  const last = sheet.getLastRow();
  if (last < 2) return -1;
  const data = sheet.getRange(2, 1, last - 1, HEADERS.length).getValues();
  const p = String(period).trim();
  const f = String(firstName).trim().toLowerCase();
  const l = String(lastName).trim().toLowerCase();
  for (let i = 0; i < data.length; i++) {
    if (String(data[i][COL.PERIOD]).trim() === p &&
        String(data[i][COL.FIRST]).trim().toLowerCase() === f &&
        String(data[i][COL.LAST]).trim().toLowerCase() === l) {
      return i + 2;
    }
  }
  return -1;
}

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const ss = SpreadsheetApp.getActive();
    const tabName = tabNameForGame(data.game);
    const sheet = getOrCreateTab(ss, tabName);

    const period = normalizePeriod(data.period);
    const firstName = data.firstName || "";
    const lastName = data.lastName || "";
    const status = data.status || "";
    const restarts = data.restarts == null ? 0 : data.restarts;
    const timeMin = data.timeSpent == null ? "" : Math.round(data.timeSpent / 60 * 10) / 10;
    const now = data.timestamp || new Date().toISOString();
    const game = data.game || "";

    const isCompletion = (status === "character_complete" || status === "completed");

    const existingRow = findRow(sheet, period, firstName, lastName);

    if (existingRow === -1) {
      sheet.appendRow([
        period, firstName, lastName,
        isCompletion ? "completed" : status,
        isCompletion ? 1 : 0,
        1,
        restarts,
        timeMin,
        game,
        now,
      ]);
      return jsonOut({ ok: true, action: "insert", tab: tabName });
    }

    const row = sheet.getRange(existingRow, 1, 1, HEADERS.length);
    const cur = row.getValues()[0];
    const curStatus = String(cur[COL.STATUS] || "");
    const curCompletions = Number(cur[COL.COMPLETIONS]) || 0;
    const curAttempts = Number(cur[COL.ATTEMPTS]) || 0;

    const newStatus = (curStatus === "completed") ? "completed"
                    : (isCompletion ? "completed" : status);
    const newCompletions = curCompletions + (isCompletion ? 1 : 0);
    const newAttempts = curAttempts + 1;

    row.setValues([[
      period, firstName, lastName,
      newStatus,
      newCompletions,
      newAttempts,
      restarts,
      timeMin,
      game || cur[COL.GAME],
      now,
    ]]);

    return jsonOut({ ok: true, action: "update", row: existingRow, tab: tabName });
  } catch (err) {
    return jsonOut({ ok: false, error: err.message });
  }
}

function jsonOut(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function doGet() {
  return ContentService
    .createTextOutput("Time Warp tracker v4 (reordered columns) is live.")
    .setMimeType(ContentService.MimeType.TEXT);
}
