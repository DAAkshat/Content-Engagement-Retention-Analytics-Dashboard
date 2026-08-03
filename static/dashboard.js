const COLORS = { blue: "#3b82f6", purple: "#8b5cf6", grid: "#334155", text: "#94a3b8" };
const chartDefaults = {
  responsive: true,
  plugins: { legend: { labels: { color: COLORS.text } } },
  scales: {
    x: { ticks: { color: COLORS.text }, grid: { color: COLORS.grid } },
    y: { ticks: { color: COLORS.text }, grid: { color: COLORS.grid } },
  },
};

async function fetchJSON(url) {
  const r = await fetch(url);
  return r.json();
}

function renderKPIs(data) {
  document.getElementById("kpis").innerHTML = [
    ["Total Sessions", data.total_sessions.toLocaleString()],
    ["Avg DAU", data.avg_dau.toLocaleString()],
    ["Avg Completion %", data.avg_completion + "%"],
    ["Churn %", data.churn_pct + "%"],
  ].map(([l, v]) => `<div class="kpi"><div class="label">${l}</div><div class="value">${v}</div></div>`).join("");
}

function lineChart(id, labels, data, color) {
  new Chart(document.getElementById(id), {
    type: "line",
    data: { labels, datasets: [{ data, borderColor: color, backgroundColor: color + "33", fill: true, tension: 0.3 }] },
    options: { ...chartDefaults, plugins: { ...chartDefaults.plugins, legend: { display: false } } },
  });
}

function barChart(id, labels, data, color) {
  new Chart(document.getElementById(id), {
    type: "bar",
    data: { labels, datasets: [{ data, backgroundColor: color }] },
    options: { ...chartDefaults, plugins: { ...chartDefaults.plugins, legend: { display: false } } },
  });
}

function renderAB(data) {
  const el = document.getElementById("abTest");
  const groups = data.groups.map(g =>
    `<div class="ab-group"><div>Group ${g.ab_group} (${g.ab_group === "A" ? "Generic" : "Cliffhanger"})</div>
     <div class="rate">${g.rate}%</div><div style="font-size:0.8rem;color:#94a3b8">${g.re_engaged}/${g.sent} re-engaged</div></div>`
  ).join("");
  const sig = data.significant
    ? `<div class="sig yes">Significant (p=${data.p_value}, χ²=${data.chi2})</div>`
    : `<div class="sig no">Not significant (p=${data.p_value})</div>`;
  el.innerHTML = `<div class="ab-result">${groups}</div>${sig}`;
}

function heatColor(pct) {
  const r = Math.round(255 * (1 - pct / 100));
  const g = Math.round(200 * (pct / 100));
  return `rgb(${r},${g},80)`;
}

function renderHeatmap(data) {
  const rows = data.cohorts.slice(0, 12).map((cohort, i) => {
    const cells = data.values[i].map(v =>
      `<td style="background:${heatColor(v)};color:#0f172a;font-weight:600">${v}%</td>`
    ).join("");
    return `<tr><th>${cohort.slice(0, 10)}</th>${cells}</tr>`;
  }).join("");
  const headers = data.weeks.map(w => `<th>W${w}</th>`).join("");
  document.getElementById("heatmap").innerHTML =
    `<table class="heatmap"><thead><tr><th>Cohort</th>${headers}</tr></thead><tbody>${rows}</tbody></table>`;
}

async function init() {
  const [kpis, dau, genre, churn, ab, mauTrend, premium, funnel, heatmap] = await Promise.all([
    fetchJSON("/api/kpis"), fetchJSON("/api/dau"), fetchJSON("/api/genre"),
    fetchJSON("/api/churn"), fetchJSON("/api/abtest"), fetchJSON("/api/mau-trend"),
    fetchJSON("/api/premium-vs-free"), fetchJSON("/api/genre-funnel"), fetchJSON("/api/cohort-heatmap"),
  ]);

  renderKPIs(kpis);
  lineChart("dauChart", dau.map(d => d.session_date.slice(5)), dau.map(d => d.dau), COLORS.blue);
  barChart("genreChart", genre.map(g => g.genre), genre.map(g => g.avg_completion), COLORS.blue);
  barChart("churnChart", churn.map(c => c.genre), churn.map(c => c.churn_pct), "#ef4444");
  renderAB(ab);
  lineChart("mauChart", mauTrend.map(m => m.month), mauTrend.map(m => m.mau), COLORS.purple);

  const labels = premium.map(p => p.label);
  new Chart(document.getElementById("premiumChart"), {
    type: "bar",
    data: {
      labels,
      datasets: [
        { label: "Completion %", data: premium.map(p => p.avg_completion), backgroundColor: COLORS.blue },
        { label: "Duration (min)", data: premium.map(p => p.avg_duration), backgroundColor: COLORS.purple },
        { label: "Episodes", data: premium.map(p => p.avg_episodes), backgroundColor: "#10b981" },
      ],
    },
    options: chartDefaults,
  });

  const stages = ["Total", "25%", "50%", "75%", "Done"];
  const genres = Object.keys(funnel);
  const palette = ["#3b82f6", "#8b5cf6", "#10b981", "#f59e0b", "#ef4444"];
  new Chart(document.getElementById("funnelChart"), {
    type: "bar",
    data: {
      labels: stages,
      datasets: genres.map((g, i) => ({ label: g, data: funnel[g], backgroundColor: palette[i % palette.length] })),
    },
    options: chartDefaults,
  });

  renderHeatmap(heatmap);
}

init();
