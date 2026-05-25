/* completionTracker.js — universal Time Warp completion tracker
 * Usage in a game HTML:
 *   <script src="tracker/completionTracker.js"></script>
 *   <script>
 *     TimeWarp.init({
 *       game: "Time Warp: Plymouth or Jamestown — Smith",
 *       webhookUrl: "https://script.google.com/macros/s/XXXXX/exec",
 *       requireIdentity: true   // shows modal on first load
 *     });
 *     // anywhere in your game:
 *     TimeWarp.recordRestart();
 *     TimeWarp.recordScore(85);          // for quizzes
 *     TimeWarp.recordPath("Smith");      // optional path/character tag
 *     TimeWarp.submit("completed");      // "completed" | "failed" | "abandoned"
 *   </script>
 */
(function () {
  const LS_KEY = "timewarp_identity";
  const STATE_KEY = "timewarp_state";
  const CHARS_KEY = "timewarp_characters_complete";  // per-game key, see charsKey()
  const PERIODS = ["Period 1","Period 2","Period 3","Period 4","Period 5","Period 6","Period 7"];

  let cfg = { game: "Unknown Game", webhookUrl: "", requireIdentity: true };
  let identity = null;     // {period, firstName, lastName}
  let state = { restarts: 0, score: null, path: null, startTime: Date.now() };

  // ---------- identity (modal at start) ----------
  function loadIdentity() {
    try { identity = JSON.parse(localStorage.getItem(LS_KEY)) || null; } catch (e) { identity = null; }
    return identity;
  }
  function saveIdentity(i) {
    identity = i;
    localStorage.setItem(LS_KEY, JSON.stringify(i));
  }
  function showIdentityModal() {
    return new Promise(resolve => {
      const wrap = document.createElement("div");
      wrap.id = "tw-id-modal";
      wrap.innerHTML = `
        <div class="tw-id-backdrop"></div>
        <div class="tw-id-card">
          <h2>Before you begin</h2>
          <p>Enter your info so your teacher knows you completed this.</p>
          <label>Class Period
            <select id="tw-period">
              <option value="">— select —</option>
              ${PERIODS.map(p => `<option value="${p}">${p}</option>`).join("")}
            </select>
          </label>
          <label>First Name<input id="tw-first" type="text" autocomplete="given-name"></label>
          <label>Last Name<input id="tw-last" type="text" autocomplete="family-name"></label>
          <button id="tw-go" disabled>START GAME</button>
        </div>
      `;
      const style = document.createElement("style");
      style.textContent = `
        #tw-id-modal { position: fixed; inset: 0; z-index: 99999; font-family: 'Bangers', sans-serif, system-ui; }
        .tw-id-backdrop { position: absolute; inset: 0; background: rgba(0,0,0,.85); }
        .tw-id-card { position: relative; max-width: 460px; margin: 8vh auto; background: #fdf6e3; color: #2b1810;
          padding: 32px; border-radius: 14px; box-shadow: 0 12px 40px rgba(0,0,0,.6); border: 3px solid #b8860b; }
        .tw-id-card h2 { margin: 0 0 8px 0; font-size: 32px; letter-spacing: 2px; color: #8b2c2c; }
        .tw-id-card p { margin: 0 0 18px 0; font-family: Georgia, serif; }
        .tw-id-card label { display: block; margin: 10px 0; font-size: 20px; letter-spacing: 1px; }
        .tw-id-card input, .tw-id-card select { display: block; width: 100%; padding: 10px; font-size: 18px;
          margin-top: 4px; border: 2px solid #b8860b; border-radius: 6px; background: #fff; font-family: Georgia, serif; }
        .tw-id-card button { margin-top: 18px; width: 100%; padding: 14px; font-size: 24px; letter-spacing: 2px;
          background: #b8860b; color: #000; border: none; border-radius: 8px; cursor: pointer; font-family: 'Bangers', sans-serif; }
        .tw-id-card button:disabled { background: #aaa; cursor: not-allowed; }
        .tw-id-card button:not(:disabled):hover { filter: brightness(1.1); }
      `;
      document.head.appendChild(style);
      document.body.appendChild(wrap);

      const per = wrap.querySelector("#tw-period");
      const fn  = wrap.querySelector("#tw-first");
      const ln  = wrap.querySelector("#tw-last");
      const go  = wrap.querySelector("#tw-go");
      const validate = () => {
        go.disabled = !(per.value && fn.value.trim() && ln.value.trim());
      };
      [per, fn, ln].forEach(el => el.addEventListener("input", validate));
      go.addEventListener("click", () => {
        const i = { period: per.value, firstName: fn.value.trim(), lastName: ln.value.trim() };
        saveIdentity(i);
        wrap.remove();
        resolve(i);
      });
    });
  }

  // ---------- state ----------
  function loadState() {
    try {
      const s = JSON.parse(sessionStorage.getItem(STATE_KEY));
      if (s) state = s;
    } catch (e) {}
  }
  function saveState() { sessionStorage.setItem(STATE_KEY, JSON.stringify(state)); }

  // ---------- submit ----------
  async function submit(status) {
    const payload = {
      timestamp: new Date().toISOString(),
      game: cfg.game,
      period: identity ? identity.period : "(unknown)",
      firstName: identity ? identity.firstName : "(unknown)",
      lastName: identity ? identity.lastName : "(unknown)",
      status: status || "completed",
      score: state.score,
      restarts: state.restarts,
      timeSpent: Math.round((Date.now() - state.startTime) / 1000),
      path: state.path,
    };
    showSubmitOverlay("Saving...");
    if (!cfg.webhookUrl) {
      console.warn("[TimeWarp] No webhookUrl set — payload:", payload);
      showSubmitOverlay("⚠ Tracker not configured — show your teacher", payload);
      return { ok: false, payload };
    }
    try {
      await fetch(cfg.webhookUrl, {
        method: "POST",
        mode: "no-cors",
        headers: { "Content-Type": "text/plain" }, // text/plain avoids CORS preflight
        body: JSON.stringify(payload),
      });
      showSubmitOverlay("✓ Saved!");
      sessionStorage.removeItem(STATE_KEY);
      return { ok: true, payload };
    } catch (e) {
      showSubmitOverlay("⚠ Couldn't reach server — show this screen to your teacher", payload);
      return { ok: false, payload, error: e.message };
    }
  }
  function showSubmitOverlay(msg, payload) {
    let overlay = document.getElementById("tw-submit");
    if (!overlay) {
      overlay = document.createElement("div");
      overlay.id = "tw-submit";
      overlay.innerHTML = `<div class="tw-sub-card"><div id="tw-sub-msg"></div><pre id="tw-sub-pre" style="display:none"></pre></div>`;
      const s = document.createElement("style");
      s.textContent = `
        #tw-submit { position: fixed; inset: 0; z-index: 99998; background: rgba(0,0,0,.75); display: flex; align-items: center; justify-content: center; font-family: 'Bangers', sans-serif, system-ui; }
        .tw-sub-card { background: #fdf6e3; color: #2b1810; padding: 28px 40px; border-radius: 12px; border: 3px solid #b8860b; max-width: 540px; text-align: center; }
        #tw-sub-msg { font-size: 28px; letter-spacing: 2px; }
        #tw-sub-pre { text-align: left; font-family: monospace; font-size: 12px; background: #fff; padding: 12px; border-radius: 6px; margin-top: 14px; max-height: 240px; overflow: auto; }
      `;
      document.head.appendChild(s);
      document.body.appendChild(overlay);
    }
    overlay.querySelector("#tw-sub-msg").textContent = msg;
    if (payload) {
      const pre = overlay.querySelector("#tw-sub-pre");
      pre.style.display = "block";
      pre.textContent = JSON.stringify(payload, null, 2);
    }
  }

  // ---------- multi-character progress ----------
  function charsKey() {
    // namespace by game prefix so different Time Warps don't collide
    const prefix = (cfg.game || "game").split(":")[0].trim().replace(/\s+/g, "_");
    return CHARS_KEY + ":" + prefix;
  }
  function getCompletedCharacters() {
    try { return JSON.parse(localStorage.getItem(charsKey())) || []; } catch (e) { return []; }
  }
  function recordCharacterComplete(name) {
    const list = getCompletedCharacters();
    if (!list.includes(name)) {
      list.push(name);
      localStorage.setItem(charsKey(), JSON.stringify(list));
    }
    return list;
  }
  function isFullyComplete(required) {
    const done = getCompletedCharacters();
    return required.every(c => done.includes(c));
  }
  function clearProgress() {
    localStorage.removeItem(charsKey());
    sessionStorage.removeItem(STATE_KEY);
  }

  // ---------- public API ----------
  window.TimeWarp = {
    init(opts) {
      cfg = Object.assign(cfg, opts || {});
      loadState();
      // restart startTime if it's a fresh session
      if (!sessionStorage.getItem(STATE_KEY)) {
        state.startTime = Date.now();
        saveState();
      }
      if (cfg.requireIdentity !== false) {
        if (!loadIdentity()) return showIdentityModal();
      }
      return Promise.resolve(identity);
    },
    recordRestart() { state.restarts += 1; saveState(); },
    recordScore(n) { state.score = n; saveState(); },
    recordPath(p) { state.path = p; saveState(); },
    getIdentity() { return identity; },
    getState() { return Object.assign({}, state); },
    clearIdentity() { localStorage.removeItem(LS_KEY); identity = null; },
    clearProgress,
    recordCharacterComplete,
    getCompletedCharacters,
    isFullyComplete,
    submit,
  };
})();
