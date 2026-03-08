import { useState, useEffect, useCallback } from "react";

const API = "http://localhost:8000";

// ── tiny helpers ────────────────────────────────────────────────────────────

function buildBody(filters) {
  const body = {
    sides:      filters.sides.length      ? filters.sides      : null,
    results:    filters.results.length    ? filters.results    : null,
    openings:   filters.openings.length   ? filters.openings   : null,
    min_rating: filters.ratingRange[0] !== null ? filters.ratingRange[0] : null,
    max_rating: filters.ratingRange[1] !== null ? filters.ratingRange[1] : null,
    min_plies:  filters.pliesRange[0]  !== null ? filters.pliesRange[0]  : null,
    max_plies:  filters.pliesRange[1]  !== null ? filters.pliesRange[1]  : null,
    min_date:   filters.dateFrom || null,
    max_date:   filters.dateTo   || null,
  };
  return Object.fromEntries(Object.entries(body).filter(([_, v]) => v !== null && v !== ""));
}

const RESULT_COLORS = {
  "1-0":     { bg: "#1a3320", text: "#4ade80", border: "#166534" },
  "0-1":     { bg: "#3b1219", text: "#f87171", border: "#991b1b" },
  "1/2-1/2": { bg: "#1e2a3b", text: "#93c5fd", border: "#1e40af" },
};

// ── sub-components ───────────────────────────────────────────────────────────

function Tag({ active, onClick, children, color = "#f59e0b" }) {
  return (
    <button onClick={onClick} style={{
      padding: "4px 10px", borderRadius: 4, fontSize: 12, cursor: "pointer",
      fontFamily: "monospace", fontWeight: 600, letterSpacing: 0.5,
      border: `1px solid ${active ? color : "#334155"}`,
      background: active ? color + "22" : "transparent",
      color: active ? color : "#64748b",
      transition: "all 0.15s",
    }}>{children}</button>
  );
}

// Multi-select picker — toggles items in/out of a list
function MultiSelect({ label, options, selected, onChange }) {
  const toggle = v => onChange(selected.includes(v) ? selected.filter(x => x !== v) : [...selected, v]);
  return (
    <div style={{ marginBottom: 16 }}>
      <div style={{ fontSize: 11, color: "#94a3b8", fontFamily: "monospace", textTransform: "uppercase", letterSpacing: 1, marginBottom: 8 }}>
        {label}{selected.length > 0 && <span style={{ color: "#f59e0b", marginLeft: 4 }}>• active</span>}
      </div>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
        {options.map(o => <Tag key={o} active={selected.includes(o)} onClick={() => toggle(o)}>{o}</Tag>)}
      </div>
    </div>
  );
}

// Multi-select opening picker
function OpeningSelect({ options, selected, onChange }) {
  const [search, setSearch] = useState("");
  const filtered = options.filter(o => o.toLowerCase().includes(search.toLowerCase()));
  const toggle = v => onChange(selected.includes(v) ? selected.filter(x => x !== v) : [...selected, v]);
  return (
    <div style={{ marginBottom: 16 }}>
      <div style={{ fontSize: 11, color: "#94a3b8", fontFamily: "monospace", textTransform: "uppercase", letterSpacing: 1, marginBottom: 8 }}>
        Opening{selected.length > 0 && <span style={{ color: "#f59e0b", marginLeft: 4 }}>• active</span>}
      </div>
      <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search openings…"
        style={{ width: "100%", boxSizing: "border-box", padding: "6px 10px", marginBottom: 8, background: "#0f172a", border: "1px solid #334155", color: "#e2e8f0", borderRadius: 4, fontSize: 12, fontFamily: "monospace", outline: "none" }} />
      <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
        {filtered.map(o => <Tag key={o} active={selected.includes(o)} onClick={() => toggle(o)}>{o}</Tag>)}
      </div>
    </div>
  );
}

function RangeSlider({ label, min, max, value, onChange }) {
  return (
    <div style={{ marginBottom: 16 }}>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
        <span style={{ fontSize: 11, color: "#94a3b8", fontFamily: "monospace", textTransform: "uppercase", letterSpacing: 1 }}>{label}</span>
        <span style={{ fontSize: 11, color: "#e2e8f0", fontFamily: "monospace" }}>{value[0]} – {value[1]}</span>
      </div>
      <div style={{ position: "relative", height: 20, display: "flex", alignItems: "center" }}>
        <div style={{ position: "absolute", width: "100%", height: 3, background: "#1e293b", borderRadius: 2 }} />
        <div style={{ position: "absolute", left: `${((value[0]-min)/(max-min))*100}%`, right: `${100-((value[1]-min)/(max-min))*100}%`, height: 3, background: "#f59e0b", borderRadius: 2 }} />
        {[0, 1].map(i => (
          <input key={i} type="range" min={min} max={max} value={value[i]}
            onChange={e => { const v = +e.target.value; const next = [...value]; next[i] = i === 0 ? Math.min(v, value[1]-1) : Math.max(v, value[0]+1); onChange(next); }}
            style={{ position: "absolute", width: "100%", opacity: 0, cursor: "pointer", zIndex: 2, height: 20 }} />
        ))}
        {value.map((v, i) => (
          <div key={i} style={{ position: "absolute", left: `${((v-min)/(max-min))*100}%`, transform: "translateX(-50%)", width: 14, height: 14, borderRadius: "50%", background: "#f59e0b", border: "2px solid #fbbf24", boxShadow: "0 0 8px #f59e0b88", zIndex: 1 }} />
        ))}
      </div>
    </div>
  );
}

function ErrorBadge({ count, color }) {
  if (!count) return <span style={{ color: "#334155", fontSize: 11 }}>—</span>;
  return <span style={{ display: "inline-block", minWidth: 20, textAlign: "center", padding: "1px 6px", borderRadius: 3, fontSize: 11, background: color + "22", color, border: `1px solid ${color}44`, fontFamily: "monospace", fontWeight: 700 }}>{count}</span>;
}

function ColHeader({ label, col, sortCol, sortDir, onSort, align = "left" }) {
  const active = sortCol === col;
  return (
    <th onClick={() => onSort(col)} style={{ padding: "10px 12px", textAlign: align, cursor: "pointer", userSelect: "none", fontSize: 10, fontFamily: "monospace", textTransform: "uppercase", letterSpacing: 1.5, color: active ? "#f59e0b" : "#475569", whiteSpace: "nowrap", borderBottom: "1px solid #1e293b", background: active ? "#0f1929" : "transparent" }}>
      {label} {active ? (sortDir === "asc" ? "↑" : "↓") : <span style={{ opacity: 0.3 }}>↕</span>}
    </th>
  );
}

// ── main component ───────────────────────────────────────────────────────────

const DEFAULT_FILTERS = {
  sides:       [],
  results:     [],
  openings:    [],
  ratingRange: [0, 3000],
  pliesRange:  [0, 300],
  dateFrom:    "",
  dateTo:      "",
};

export default function App() {
  const [meta, setMeta] = useState({ openings: [] });
  const [games, setGames] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [filters, setFilters] = useState(DEFAULT_FILTERS);
  const [sortCol, setSortCol] = useState("date");
  const [sortDir, setSortDir] = useState("desc");
  const [page, setPage] = useState(1);
  const PAGE_SIZE = 15;

  // Load available openings from /options/opening on mount
  useEffect(() => {
    fetch(`${API}/options/opening`)
      .then(r => r.json())
      .then(data => setMeta({ openings: data }))
      .catch(() => setError("Could not connect to API at " + API));
  }, []);

  // Fetch games via POST whenever filters change
  const fetchGames = useCallback(() => {
    setLoading(true);
    setError(null);
    fetch(`${API}/games/filtered`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(buildBody(filters)),
    })
      .then(r => r.json())
      .then(data => { const list = Array.isArray(data) ? data : (data.games ?? []); setGames(list); setTotal(Array.isArray(data) ? list.length : (data.total ?? list.length)); setPage(1); })
      .catch(() => setError("Failed to load games."))
      .finally(() => setLoading(false));
  }, [filters]);

  useEffect(() => { fetchGames(); }, [fetchGames]);

  const setFilter = (key, val) => setFilters(f => ({ ...f, [key]: val }));

  const sorted = [...games].sort((a, b) => {
    const av = a[sortCol] ?? ""; const bv = b[sortCol] ?? "";
    return sortDir === "asc" ? (av > bv ? 1 : -1) : (av < bv ? 1 : -1);
  });
  const pageGames = sorted.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);
  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));

  const handleSort = col => { if (sortCol === col) setSortDir(d => d === "asc" ? "desc" : "asc"); else { setSortCol(col); setSortDir("desc"); } };
  const activeFilterCount = [filters.sides, filters.results, filters.openings].filter(a => a.length > 0).length;

  return (
    <div style={{ minHeight: "100vh", background: "#080e18", color: "#e2e8f0", fontFamily: "'Georgia', serif", display: "flex", flexDirection: "column" }}>
      {/* Header */}
      <div style={{ borderBottom: "1px solid #1e293b", padding: "20px 32px", background: "linear-gradient(180deg, #0d1826 0%, #080e18 100%)", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div>
          <div style={{ display: "flex", alignItems: "baseline", gap: 12 }}>
            <span style={{ fontSize: 22, fontWeight: 700, letterSpacing: -0.5, color: "#f1f5f9" }}>♟ chelyzer</span>
            <span style={{ fontSize: 11, fontFamily: "monospace", color: "#475569", letterSpacing: 2, textTransform: "uppercase" }}>game explorer</span>
          </div>
          <div style={{ fontSize: 12, color: "#475569", fontFamily: "monospace", marginTop: 3 }}>
            {loading ? "Loading…" : `${total} games`}
            {activeFilterCount > 0 && <span style={{ color: "#f59e0b", marginLeft: 8 }}>· {activeFilterCount} filter{activeFilterCount > 1 ? "s" : ""} active</span>}
          </div>
        </div>
        {activeFilterCount > 0 && (
          <button onClick={() => setFilters(DEFAULT_FILTERS)}
            style={{ padding: "6px 14px", background: "transparent", border: "1px solid #334155", color: "#94a3b8", borderRadius: 4, cursor: "pointer", fontSize: 12, fontFamily: "monospace" }}>
            Clear filters
          </button>
        )}
      </div>

      {error && <div style={{ padding: "12px 32px", background: "#3b1219", color: "#f87171", fontSize: 13, fontFamily: "monospace" }}>⚠ {error}</div>}

      <div style={{ display: "flex", flex: 1 }}>
        {/* Sidebar */}
        <div style={{ width: 260, flexShrink: 0, borderRight: "1px solid #1e293b", padding: "24px 20px", overflowY: "auto", background: "linear-gradient(180deg, #0a1220 0%, #080e18 100%)" }}>
          <div style={{ fontSize: 10, fontFamily: "monospace", textTransform: "uppercase", letterSpacing: 2, color: "#334155", marginBottom: 20 }}>Filters</div>

          <MultiSelect
            label="Side"
            options={["White", "Black"]}
            selected={filters.sides}
            onChange={v => setFilter("sides", v)}
          />

          <div style={{ borderTop: "1px solid #1e293b", margin: "4px 0 16px" }} />

          <MultiSelect
            label="Result"
            options={["1:0", "½:½", "0:1", "+:-", "-:+"]}
            selected={filters.results}
            onChange={v => setFilter("results", v)}
          />

          <div style={{ borderTop: "1px solid #1e293b", margin: "4px 0 16px" }} />

          <OpeningSelect
            options={meta.openings}
            selected={filters.openings}
            onChange={v => setFilter("openings", v)}
          />

          <div style={{ borderTop: "1px solid #1e293b", margin: "0 0 16px" }} />

          <RangeSlider label="Rating range" min={0} max={3000}
            value={filters.ratingRange} onChange={v => setFilter("ratingRange", v)} />

          <RangeSlider label="Plies range" min={0} max={300}
            value={filters.pliesRange} onChange={v => setFilter("pliesRange", v)} />

          <div style={{ marginBottom: 16 }}>
            <div style={{ fontSize: 11, color: "#94a3b8", fontFamily: "monospace", textTransform: "uppercase", letterSpacing: 1, marginBottom: 8 }}>Date range</div>
            {[["From", "dateFrom"], ["To", "dateTo"]].map(([lbl, key]) => (
              <div key={key} style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 6 }}>
                <span style={{ width: 28, fontSize: 10, color: "#475569", fontFamily: "monospace" }}>{lbl}</span>
                <input type="date" value={filters[key]} onChange={e => setFilter(key, e.target.value)}
                  style={{ flex: 1, padding: "5px 8px", background: "#0f172a", border: "1px solid #334155", color: "#e2e8f0", borderRadius: 4, fontSize: 11, fontFamily: "monospace", outline: "none" }} />
              </div>
            ))}
          </div>
        </div>

        {/* Table */}
        <div style={{ flex: 1, overflowX: "auto", paddingBottom: 32 }}>
          <table style={{ width: "100%", borderCollapse: "collapse", minWidth: 800 }}>
            <thead>
              <tr style={{ background: "#0a1220" }}>
                {[["date","Date"],["white","White"],["white_rating","Elo"],["black","Black"],["black_rating","Elo"],["result","Result"],["opening","Opening"],["event","Event"],["plies","Plies"],["blunders","Blunders"],["mistakes","Mistakes"],["inaccuracies","Inaccuracies"],["termination","End"]].map(([col, label]) => (
                  <ColHeader key={col} col={col} label={label} sortCol={sortCol} sortDir={sortDir} onSort={handleSort} align={["white_rating","black_rating","plies","blunders","mistakes","inaccuracies"].includes(col) ? "right" : ["result"].includes(col) ? "center" : "left"} />
                ))}
              </tr>
            </thead>
            <tbody>
              {pageGames.length === 0 ? (
                <tr><td colSpan={13} style={{ padding: 48, textAlign: "center", color: "#334155", fontFamily: "monospace", fontSize: 13 }}>
                  {loading ? "Loading games…" : "No games match the current filters"}
                </td></tr>
              ) : pageGames.map((g, i) => {
                const rc = RESULT_COLORS[g.result] || { bg: "#1e293b", text: "#94a3b8", border: "#334155" };
                return (
                  <tr key={i}
                    style={{ background: i % 2 === 0 ? "transparent" : "#0a1220", borderBottom: "1px solid #0f172a" }}
                    onMouseEnter={e => e.currentTarget.style.background = "#111d2e"}
                    onMouseLeave={e => e.currentTarget.style.background = i % 2 === 0 ? "transparent" : "#0a1220"}>
                    <td style={{ padding: "9px 12px", fontSize: 12, color: "#475569", fontFamily: "monospace", whiteSpace: "nowrap" }}>{g.date}</td>
                    <td style={{ padding: "9px 12px", fontSize: 13, color: "#e2e8f0", whiteSpace: "nowrap" }}>{g.white}</td>
                    <td style={{ padding: "9px 12px", fontSize: 12, color: "#94a3b8", fontFamily: "monospace", textAlign: "right" }}>{g.white_rating}</td>
                    <td style={{ padding: "9px 12px", fontSize: 13, color: "#e2e8f0", whiteSpace: "nowrap" }}>{g.black}</td>
                    <td style={{ padding: "9px 12px", fontSize: 12, color: "#94a3b8", fontFamily: "monospace", textAlign: "right" }}>{g.black_rating}</td>
                    <td style={{ padding: "9px 12px", textAlign: "center" }}>
                      <span style={{ display: "inline-block", padding: "2px 8px", borderRadius: 3, fontSize: 11, fontFamily: "monospace", fontWeight: 700, background: rc.bg, color: rc.text, border: `1px solid ${rc.border}`, whiteSpace: "nowrap" }}>{g.result}</span>
                    </td>
                    <td style={{ padding: "9px 12px", fontSize: 12, color: "#94a3b8", maxWidth: 180, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{g.opening}</td>
                    <td style={{ padding: "9px 12px", fontSize: 11, color: "#475569", fontFamily: "monospace", whiteSpace: "nowrap" }}>{g.event}</td>
                    <td style={{ padding: "9px 12px", fontSize: 12, color: "#475569", fontFamily: "monospace", textAlign: "right" }}>{g.plies}</td>
                    <td style={{ padding: "9px 12px", textAlign: "center" }}><ErrorBadge count={g.blunders} color="#f87171" /></td>
                    <td style={{ padding: "9px 12px", textAlign: "center" }}><ErrorBadge count={g.mistakes} color="#fb923c" /></td>
                    <td style={{ padding: "9px 12px", textAlign: "center" }}><ErrorBadge count={g.inaccuracies} color="#fbbf24" /></td>
                    <td style={{ padding: "9px 12px", fontSize: 11, color: "#475569", fontFamily: "monospace", whiteSpace: "nowrap" }}>{g.termination}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>

          {totalPages > 1 && (
            <div style={{ display: "flex", justifyContent: "center", alignItems: "center", gap: 8, padding: "24px 0 0", fontFamily: "monospace" }}>
              <button onClick={() => setPage(p => Math.max(1, p-1))} disabled={page === 1}
                style={{ padding: "5px 12px", background: "transparent", border: "1px solid #334155", color: page===1?"#1e293b":"#94a3b8", borderRadius: 4, cursor: page===1?"default":"pointer", fontSize: 12 }}>←</button>
              {Array.from({ length: Math.min(7, totalPages) }, (_, i) => {
                const p = totalPages <= 7 ? i+1 : page <= 4 ? i+1 : page >= totalPages-3 ? totalPages-6+i : page-3+i;
                return <button key={p} onClick={() => setPage(p)} style={{ padding: "5px 10px", borderRadius: 4, fontSize: 12, cursor: "pointer", border: p===page?"1px solid #f59e0b":"1px solid #334155", background: p===page?"#f59e0b22":"transparent", color: p===page?"#f59e0b":"#64748b" }}>{p}</button>;
              })}
              <button onClick={() => setPage(p => Math.min(totalPages, p+1))} disabled={page===totalPages}
                style={{ padding: "5px 12px", background: "transparent", border: "1px solid #334155", color: page===totalPages?"#1e293b":"#94a3b8", borderRadius: 4, cursor: page===totalPages?"default":"pointer", fontSize: 12 }}>→</button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
