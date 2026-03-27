/* ══════════════════════════════════════════
   VisaTime AI — main.js
══════════════════════════════════════════ */

// ── Set today as default date ──
document.addEventListener("DOMContentLoaded", () => {
  const dateInput = document.getElementById("app-date");
  dateInput.value = new Date().toISOString().split("T")[0];
  initCharts();
});

// ── Predict ──
async function predict() {
  const btn      = document.getElementById("predict-btn");
  const resultEl = document.getElementById("result-section");
  const errorEl  = document.getElementById("error-box");

  const wage    = document.getElementById("wage").value;
  const state   = document.getElementById("state").value;
  const occ     = document.getElementById("occupation").value;
  const appDate = document.getElementById("app-date").value;

  errorEl.classList.remove("visible");
  resultEl.classList.remove("visible");
  btn.classList.add("loading");
  btn.innerHTML = `<span class="btn-arrow">⏳</span> Estimating…`;

  try {
    const res  = await fetch("/predict", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ wage, state, occupation: occ, application_date: appDate }),
    });
    const data = await res.json();

    if (!data.success) throw new Error(data.error || "Prediction failed");

    // Populate results
    document.getElementById("r-days").textContent  = data.days;
    document.getElementById("r-weeks").innerHTML   =
      `${data.weeks}<span style="font-size:1.2rem;font-family:'Outfit',sans-serif;font-weight:400">w ${data.rem_days}d</span>`;
    document.getElementById("r-date").textContent  = data.completion.split(",")[0];
    document.getElementById("r-year").textContent  = data.completion.split(", ")[1] || "";
    document.getElementById("r-pct").textContent   = `${data.pct}% of a year`;
    document.getElementById("r-start").textContent = `📅 ${data.start}`;
    document.getElementById("r-meta").textContent  = `${data.state} · ${data.occupation}`;
    document.getElementById("r-end").textContent   = `🏁 ${data.completion}`;

    // Animate bar
    setTimeout(() => {
      document.getElementById("r-bar").style.width = `${data.pct}%`;
    }, 100);

    resultEl.classList.add("visible");
    resultEl.scrollIntoView({ behavior: "smooth", block: "nearest" });

  } catch (err) {
    errorEl.textContent = `⚠ ${err.message}`;
    errorEl.classList.add("visible");
  } finally {
    btn.classList.remove("loading");
    btn.innerHTML = `<span class="btn-arrow">⟶</span> Estimate Processing Time`;
  }
}

// ── Chart.js defaults ──
const ACCENT  = "#1a56db";
const ACCENT2 = "#0284c7";
const PURPLE  = "#7c3aed";
const MUTED   = "#94a3b8";
const BORDER  = "#e0e7f1";
const TEXT    = "#0f172a";
const SUBTEXT = "#64748b";

Chart.defaults.font.family = "'Outfit', sans-serif";
Chart.defaults.color       = SUBTEXT;

function chartBase() {
  return {
    responsive: true,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: "#ffffff",
        borderColor:     BORDER,
        borderWidth:     1,
        titleColor:      TEXT,
        bodyColor:       SUBTEXT,
        padding:         10,
        cornerRadius:    8,
      },
    },
    scales: {
      x: { grid: { color: BORDER }, ticks: { color: SUBTEXT, font: { size: 10 } } },
      y: { grid: { color: BORDER }, ticks: { color: SUBTEXT, font: { size: 10 } } },
    },
  };
}

// ── Init Charts ──
function initCharts() {
  // -- Chart 1: Processing Time Distribution --
  const distCtx = document.getElementById("chart-dist").getContext("2d");
  // Simulate plausible distribution data (replace with real server data if desired)
  const labels1 = ["0–30","31–60","61–90","91–120","121–150","151–180","181–210","211–240","240+"];
  const data1   = [120, 340, 580, 720, 490, 310, 180, 90, 50];
  new Chart(distCtx, {
    type: "bar",
    data: {
      labels: labels1,
      datasets: [{
        data:            data1,
        backgroundColor: data1.map((_, i) =>
          `rgba(26,86,219,${0.25 + 0.08 * i})`
        ),
        borderColor:     ACCENT,
        borderWidth:     0,
        borderRadius:    5,
      }],
    },
    options: {
      ...chartBase(),
      plugins: {
        ...chartBase().plugins,
        tooltip: {
          ...chartBase().plugins.tooltip,
          callbacks: { label: ctx => ` ${ctx.raw.toLocaleString()} applications` },
        },
      },
      scales: {
        x: { ...chartBase().scales.x, title: { display: true, text: "Days", color: SUBTEXT, font: { size: 10 } } },
        y: { ...chartBase().scales.y, title: { display: true, text: "Count",  color: SUBTEXT, font: { size: 10 } } },
      },
    },
  });

  // -- Chart 2: Top States --
  const statesCtx = document.getElementById("chart-states").getContext("2d");
  const stateLabels = ["CA","NY","TX","NJ","WA","IL","GA","MA"];
  const stateData   = [2800, 1900, 1600, 1400, 1100, 820, 700, 650];
  new Chart(statesCtx, {
    type: "bar",
    data: {
      labels: stateLabels,
      datasets: [{
        data:            stateData,
        backgroundColor: [ACCENT, ACCENT2, PURPLE,
          "rgba(26,86,219,0.6)","rgba(2,132,199,0.6)","rgba(124,58,237,0.6)",
          "rgba(26,86,219,0.4)","rgba(2,132,199,0.4)"],
        borderWidth:  0,
        borderRadius: 5,
      }],
    },
    options: {
      ...chartBase(),
      plugins: {
        ...chartBase().plugins,
        tooltip: {
          ...chartBase().plugins.tooltip,
          callbacks: { label: ctx => ` ${ctx.raw.toLocaleString()} apps` },
        },
      },
      scales: {
        x: { ...chartBase().scales.x },
        y: { ...chartBase().scales.y, ticks: { ...chartBase().scales.y.ticks, callback: v => `${(v/1000).toFixed(1)}k` } },
      },
    },
  });

  // -- Chart 3: Avg Time by Wage Band --
  const wageCtx = document.getElementById("chart-wage").getContext("2d");
  new Chart(wageCtx, {
    type: "bar",
    data: {
      labels: ["< $50k", "$50k–$90k", "$90k–$150k", "> $150k"],
      datasets: [{
        data:            [98, 82, 71, 58],
        backgroundColor: [PURPLE, ACCENT2, ACCENT, "rgba(26,86,219,0.5)"],
        borderWidth:     0,
        borderRadius:    5,
      }],
    },
    options: {
      ...chartBase(),
      plugins: {
        ...chartBase().plugins,
        tooltip: {
          ...chartBase().plugins.tooltip,
          callbacks: { label: ctx => ` ${ctx.raw} days avg.` },
        },
      },
      scales: {
        x: { ...chartBase().scales.x },
        y: {
          ...chartBase().scales.y,
          title: { display: true, text: "Days", color: SUBTEXT, font: { size: 10 } },
          min: 40,
        },
      },
    },
  });
}
