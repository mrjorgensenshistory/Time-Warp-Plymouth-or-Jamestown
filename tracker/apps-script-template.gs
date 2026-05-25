/**
 * Time Warp Completion Tracker v6
 * Status now distinguishes character-level from game-level completion:
 *   - "character_complete" event -> Status = "in progress" (with Completions++)
 *   - "completed" event (from hub when all chars done) -> Status = "completed"
 *   - "abandoned" event -> Status = "in progress"
 * Status is sticky: once "completed", never downgraded.
 */

const HEADERS = [
  "Period", "First Name", "Last Name",
  "Status", "Completions", "Attempts", "Restarts", "Time",
  "Game", "Last Played",
];

const COL = {
  PERIOD: 0, FIRST: 1, LAST: 2,
  STATUS: 3, COMPLETIONS: 4, ATTEMPTS: 5, RESTARTS: 6, TIME: 7,
  GAME: 8, TIMESTAMP: 9,
};

function formatTime(seconds) {
  if (seconds == null || seconds === "") return "";
  const total = Math.round(Number(seconds));
  if (isNaN(total)) return "";
  const m = Math.floor(total / 60);
  const s = total % 60;
  return m + ":" + String(s).padStart(2, "0");
}

function tabNameForGame(game) {
  if (!game) return "Untitled";
  const base = String(game).split(/\s+[—\-]\s+/)[0].trim();
  const safe = base.replace(/[\[\]\?\:\/\\\*]/g, "").substring(0, 100);
  return safe || "Untitled";
}

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
    sheet.setColumnWidth(1, 70);
    sheet.setColumnWidth(2, 110);
    sheet.setColumnWidth(3, 110);
    sheet.setColumnWidth(4, 110);
    sheet.setColumnWidth(8, 80);
    sheet.setColumnWidth(9, 240);
    sheet.setColumnWidth(10, 170);
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

// Map raw incoming status to a display string.
//   "completed"          -> game-level completion (all characters done)
//   "character_complete" -> single character finished -> "in progress"
//   "abandoned"          -> character abandoned -> "in progress"
//   anything else        -> passthrough
function displayStatus(incoming) {
  if (incoming === "completed") return "completed";
  if (incoming === "character_complete") return "in progress";
  if (incoming === "abandoned") return "in progress";
  return incoming;
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
    const rawStatus = data.status || "";
    const restarts = data.restarts == null ? 0 : data.restarts;
    const time = formatTime(data.timeSpent);
    const now = data.timestamp || new Date().toISOString();
    const game = data.game || "";

    // Only count as Completion when a character is finished
    const isCharCompletion = (rawStatus === "character_complete");

    const existingRow = findRow(sheet, period, firstName, lastName);

    if (existingRow === -1) {
      sheet.appendRow([
        period, firstName, lastName,
        displayStatus(rawStatus),
        isCharCompletion ? 1 : 0,
        1, restarts, time, game, now,
      ]);
      return jsonOut({ ok: true, action: "insert", tab: tabName });
    }

    const row = sheet.getRange(existingRow, 1, 1, HEADERS.length);
    const cur = row.getValues()[0];
    const curStatus = String(cur[COL.STATUS] || "");
    const curCompletions = Number(cur[COL.COMPLETIONS]) || 0;
    const curAttempts = Number(cur[COL.ATTEMPTS]) || 0;

    // Sticky: once "completed" (game-level), never downgrade.
    const newDisplay = displayStatus(rawStatus);
    const newStatus = (curStatus === "completed") ? "completed" : newDisplay;
    const newCompletions = curCompletions + (isCharCompletion ? 1 : 0);
    const newAttempts = curAttempts + 1;

    row.setValues([[
      period, firstName, lastName,
      newStatus, newCompletions, newAttempts,
      restarts, time,
      game || cur[COL.GAME], now,
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
    .createTextOutput("Time Warp tracker v6 — status reserved for game-level completion.")
    .setMimeType(ContentService.MimeType.TEXT);
}
