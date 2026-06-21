// ─── State ────────────────────────────────────────────
let allOpportunities = [];
let activeFilters = { type: 'all', location: 'all' };

// Metadata for known sources: URL + short description shown in "Sources monitored"
const SOURCE_INFO = {
  'Realtime Research': { url: 'https://rtr.com.au/projects/', desc: 'Focus groups, taste tests, surveys' },
  'Research Connections': { url: 'https://researchconnections.com.au/', desc: 'In-person market research studies' },
  'Sydney Focus Groups': { url: 'https://www.sydneyfocusgroups.com.au/', desc: 'Focus group specialists in Sydney' },
  'User Interviews': { url: 'https://app.userinterviews.com/studies', desc: 'UX research, online product testing' },
  'Prolific': { url: 'https://www.prolific.com', desc: 'Academic studies, paid per hour' },
  'Scientia Clinical Research': { url: 'https://www.scientiaclinicalresearch.com.au/find-a-study/', desc: 'Phase I clinical trials, high compensation' },
  'Clinibase': { url: 'https://clinibase.com/current-trials/', desc: 'Clinical trial aggregator AU/NZ' },
  'Gumtree': { url: 'https://www.gumtree.com.au/s-jobs/sydney/paid+research/k0c9300l3005796', desc: 'Local classifieds for paid studies' }
};

// ─── Fetch data ───────────────────────────────────────
async function loadData() {
  try {
    const res = await fetch('feed/opportunities.json?t=' + Date.now());
    const data = await res.json();

    allOpportunities = data.opportunities || [];

    // Update stats
    document.getElementById('stat-total').textContent = data.total || allOpportunities.length;

    const sources = [...new Set(allOpportunities.map(o => o.source))];
    document.getElementById('stat-sources').textContent = sources.length;

    renderCards();
    renderSources(sources);
  } catch (err) {
    console.error('Error loading data:', err);
    document.getElementById('cards-grid').innerHTML =
      '<p style="color:var(--text-muted); grid-column:1/-1;">Error loading opportunities. Check that the scraper has generated the JSON file.</p>';
  }
}

// ─── Render "Sources monitored" — only sources with active opportunities ──
function renderSources(activeSourceNames) {
  const container = document.getElementById('sources-grid');
  if (!container) return;

  const cards = activeSourceNames
    .filter(name => SOURCE_INFO[name]) // only known sources with metadata
    .map(name => {
      const info = SOURCE_INFO[name];
      return `
        <a href="${esc(info.url)}" target="_blank" class="source-card">
          <span class="source-name">${esc(name)}</span>
          <span class="source-desc">${esc(info.desc)}</span>
        </a>
      `;
    });

  container.innerHTML = cards.join('');
}

// ─── Render cards ─────────────────────────────────────
function renderCards() {
  const grid = document.getElementById('cards-grid');
  const empty = document.getElementById('empty-state');

  const filtered = allOpportunities.filter(opp => {
    const typeMatch = activeFilters.type === 'all' || opp.type === activeFilters.type;
    const locLower = (opp.location || '').toLowerCase();
    const typeLower = (opp.type || '').toLowerCase();
    const isOnline = locLower.includes('online') || locLower.includes('remote') || typeLower.includes('online');
    const locationMatch =
      activeFilters.location === 'all' ||
      (activeFilters.location === 'online' && isOnline) ||
      (activeFilters.location === 'presencial' && !isOnline);
    return typeMatch && locationMatch;
  });

  if (filtered.length === 0) {
    grid.innerHTML = '';
    empty.style.display = 'block';
    return;
  }

  empty.style.display = 'none';
  grid.innerHTML = filtered.map(opp => cardHTML(opp)).join('');
}

// ─── Card template ─────────────────────────────────────
function cardHTML(opp) {
  const isOnline = (opp.location || '').toLowerCase().includes('online');
  return `
    <div class="card">
      <div class="card-header">
        <span class="card-type-badge">${esc(opp.type)}</span>
        <span class="card-pay">${esc(opp.pay)}</span>
      </div>
      <p class="card-title">${esc(opp.title)}</p>
      <div class="card-footer">
        <span class="card-source">${esc(opp.source)}</span>
        <span class="card-location">${esc(opp.location)}</span>
      </div>
      <a href="${esc(opp.link)}" target="_blank" rel="noopener" class="card-link"
         data-source="${esc(opp.source)}" data-opp-type="${esc(opp.type)}">
        View opportunity →
      </a>
    </div>
  `;
}

function esc(str) {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ─── Filters ──────────────────────────────────────────
document.querySelectorAll('.pill').forEach(pill => {
  pill.addEventListener('click', () => {
    const filterKey = pill.dataset.filter;
    const value = pill.dataset.value;

    // Update active pill in group
    const group = pill.closest('.filter-pills');
    group.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
    pill.classList.add('active');

    activeFilters[filterKey] = value;
    renderCards();
  });
});

function resetFilters() {
  activeFilters = { type: 'all', location: 'all' };
  document.querySelectorAll('.pill').forEach(p => {
    p.classList.toggle('active', p.dataset.value === 'all');
  });
  renderCards();
}

// ─── Click tracking (Google Analytics) ────────────────
document.getElementById('cards-grid').addEventListener('click', (e) => {
  const link = e.target.closest('.card-link');
  if (!link || !window.gtag) return;
  gtag('event', 'click_opportunity', {
    source: link.dataset.source || '',
    opp_type: link.dataset.oppType || ''
  });
});

// ─── Init ─────────────────────────────────────────────
loadData();
