/* ─── Tokens ─────────────────────────────────────────── */
:root {
  --bg: #0d0d0d;
  --surface: #161616;
  --surface-2: #1f1f1f;
  --border: #2a2a2a;
  --text: #f0f0f0;
  --text-muted: #888;
  --accent: #b5f03d;        /* electric lime — money, growth */
  --accent-dim: rgba(181,240,61,0.12);
  --accent-2: #3df0b5;      /* teal for secondary */
  --red: #f03d3d;
  --radius: 10px;
  --radius-sm: 6px;
  --font-display: 'Space Grotesk', sans-serif;
  --font-mono: 'Space Mono', monospace;
}

/* ─── Reset ──────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-display);
  font-size: 16px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}
a { color: inherit; text-decoration: none; }

/* ─── Layout ──────────────────────────────────────────── */
.container {
  max-width: 1080px;
  margin: 0 auto;
  padding: 0 20px;
}

/* ─── Header ─────────────────────────────────────────── */
.header {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 32px 0 48px;
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 32px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 500;
}

.logo-icon {
  width: 36px;
  height: 36px;
  background: var(--accent);
  color: #000;
  border-radius: 8px;
  display: grid;
  place-items: center;
  font-family: var(--font-mono);
  font-weight: 700;
  font-size: 20px;
  flex-shrink: 0;
}

.logo-text strong { font-weight: 700; }

.meta {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 6px;
}

.update-label { text-transform: uppercase; letter-spacing: 0.08em; }
.update-time { color: var(--accent); }

.hero-title {
  font-size: clamp(32px, 5vw, 56px);
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.02em;
  margin-bottom: 14px;
}

.accent { color: var(--accent); }

.hero-sub {
  color: var(--text-muted);
  font-size: 17px;
  font-weight: 400;
}

/* ─── Main ───────────────────────────────────────────── */
.main { padding: 40px 20px 80px; }

/* ─── Stats bar ──────────────────────────────────────── */
.stats-bar {
  display: flex;
  gap: 40px;
  padding: 24px 28px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.stat { display: flex; flex-direction: column; gap: 2px; }

.stat-num {
  font-family: var(--font-mono);
  font-size: 28px;
  font-weight: 700;
  color: var(--accent);
  line-height: 1;
}

.stat-label {
  font-size: 12px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

/* ─── Filters ────────────────────────────────────────── */
.filters {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 32px;
}

.filter-group { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }

.filter-label {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  min-width: 60px;
  flex-shrink: 0;
}

.filter-pills { display: flex; gap: 8px; flex-wrap: wrap; }

.pill {
  padding: 6px 14px;
  border-radius: 100px;
  border: 1px solid var(--border);
  background: transparent;
  color: var(--text-muted);
  font-family: var(--font-display);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}

.pill:hover {
  border-color: var(--accent);
  color: var(--text);
}

.pill.active {
  background: var(--accent);
  border-color: var(--accent);
  color: #000;
  font-weight: 600;
}

/* ─── Cards grid ─────────────────────────────────────── */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 22px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  transition: border-color 0.15s ease, transform 0.15s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.card::before {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 3px;
  height: 100%;
  background: var(--accent);
  opacity: 0;
  transition: opacity 0.15s ease;
}

.card:hover {
  border-color: #3a3a3a;
  transform: translateY(-2px);
}

.card:hover::before { opacity: 1; }

.card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
}

.card-pay {
  font-family: var(--font-mono);
  font-size: 22px;
  font-weight: 700;
  color: var(--accent);
  white-space: nowrap;
  flex-shrink: 0;
}

.card-type-badge {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 3px 8px;
  border-radius: 4px;
  background: var(--accent-dim);
  color: var(--accent);
  white-space: nowrap;
}

.card-title {
  font-size: 15px;
  font-weight: 500;
  line-height: 1.4;
  color: var(--text);
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-top: auto;
}

.card-source {
  font-size: 12px;
  color: var(--text-muted);
  font-family: var(--font-mono);
}

.card-location {
  font-size: 12px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 4px;
}

.card-location::before {
  content: '📍';
  font-size: 10px;
}

.card-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: var(--accent);
  margin-top: 4px;
  padding: 8px 16px;
  border: 1px solid var(--accent);
  border-radius: var(--radius-sm);
  transition: background 0.15s ease, color 0.15s ease;
  align-self: flex-start;
}

.card-link:hover {
  background: var(--accent);
  color: #000;
}

/* ─── Empty state ────────────────────────────────────── */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: var(--text-muted);
}

.btn-reset {
  margin-top: 16px;
  padding: 10px 24px;
  background: var(--accent);
  color: #000;
  border: none;
  border-radius: var(--radius-sm);
  font-family: var(--font-display);
  font-weight: 600;
  cursor: pointer;
}

/* ─── Sources section ────────────────────────────────── */
.sources-section {
  margin-top: 64px;
  padding-top: 40px;
  border-top: 1px solid var(--border);
}

.sources-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 24px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-family: var(--font-mono);
  font-size: 13px;
}

.sources-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 12px;
}

.source-card {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 16px 20px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  transition: border-color 0.15s ease;
}

.source-card:hover { border-color: var(--accent-2); }

.source-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--accent-2);
}

.source-desc {
  font-size: 12px;
  color: var(--text-muted);
}

/* ─── Footer ─────────────────────────────────────────── */
.footer {
  border-top: 1px solid var(--border);
  padding: 24px 0;
  text-align: center;
  color: var(--text-muted);
  font-size: 13px;
}

/* ─── Responsive ─────────────────────────────────────── */
@media (max-width: 600px) {
  .stats-bar { gap: 24px; padding: 20px; }
  .stat-num { font-size: 22px; }
  .header-inner { flex-direction: column; align-items: flex-start; gap: 12px; }
  .cards-grid { grid-template-columns: 1fr; }
  .filter-group { flex-direction: column; align-items: flex-start; }
  .filter-label { min-width: unset; }
}
