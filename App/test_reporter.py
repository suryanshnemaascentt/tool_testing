import json
import os
from datetime import datetime


class TestReporter:
    def __init__(self, goal: str, url: str):
        self.goal       = goal
        self.url        = url
        self.start_time = None
        self.end_time   = None
        self.result     = "UNKNOWN"
        self.reason     = ""
        self.steps      = []

    # ─────────────────────────────────────────────
    # Lifecycle
    # ─────────────────────────────────────────────

    def start(self):
        self.start_time = datetime.now()
        print(f"\n📋 TEST STARTED  — {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Goal : {self.goal}")
        print(f"   URL  : {self.url}\n")

    def finish(self, result: str, reason: str = ""):
        self.end_time = datetime.now()
        self.result   = result
        self.reason   = reason

    # ─────────────────────────────────────────────
    # Step logging
    # ─────────────────────────────────────────────

    def log_step(self, step_num: int, action: dict, current_url: str):
        self.steps.append({
            "step"       : step_num,
            "timestamp"  : datetime.now().strftime("%H:%M:%S"),
            "action"     : action.get("action", "?"),
            "selector"   : action.get("selector", ""),
            "text"       : action.get("text", ""),
            "url"        : current_url,
            "success"    : None,   # filled by update_last_step
        })

    def update_last_step(self, success: bool):
        if self.steps:
            self.steps[-1]["success"] = success

    # ─────────────────────────────────────────────
    # Console summary
    # ─────────────────────────────────────────────

    def print_summary(self):
        duration = (
            (self.end_time - self.start_time).total_seconds()
            if self.start_time and self.end_time else 0
        )
        passed = sum(1 for s in self.steps if s["success"] is True)
        failed = sum(1 for s in self.steps if s["success"] is False)

        icon = "✅" if self.result == "PASS" else "❌"
        print("\n" + "=" * 55)
        print(f"  {icon}  TEST {self.result}")
        print("=" * 55)
        print(f"  Goal     : {self.goal}")
        print(f"  Duration : {duration:.1f}s")
        print(f"  Steps    : {len(self.steps)}  (✅ {passed}  ❌ {failed})")
        if self.reason:
            print(f"  Reason   : {self.reason}")
        print("=" * 55 + "\n")

    # ─────────────────────────────────────────────
    # Save reports
    # ─────────────────────────────────────────────

    def save_report(self, output_dir: str = "reports"):
        os.makedirs(output_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")

        # JSON
        json_path = os.path.join(output_dir, f"report_{ts}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self._to_dict(), f, indent=2)
        print(f"💾 JSON report saved  → {json_path}")

        # HTML
        html_path = os.path.join(output_dir, f"report_{ts}.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(self._build_html())
        print(f"🌐 HTML report saved  → {html_path}")

    # ─────────────────────────────────────────────
    # Internal helpers
    # ─────────────────────────────────────────────

    def _to_dict(self):
        duration = (
            round((self.end_time - self.start_time).total_seconds(), 2)
            if self.start_time and self.end_time else None
        )
        return {
            "goal"        : self.goal,
            "url"         : self.url,
            "result"      : self.result,
            "reason"      : self.reason,
            "started_at"  : self.start_time.isoformat() if self.start_time else None,
            "ended_at"    : self.end_time.isoformat()   if self.end_time   else None,
            "duration_sec": duration,
            "total_steps" : len(self.steps),
            "steps"       : self.steps,
        }

    def _build_html(self):
        d        = self._to_dict()
        color    = "#16a34a" if self.result == "PASS" else "#dc2626"
        bg_badge = "#dcfce7" if self.result == "PASS" else "#fee2e2"
        icon     = "✅" if self.result == "PASS" else "❌"
        duration = f"{d['duration_sec']}s" if d['duration_sec'] is not None else "—"

        rows = ""
        for s in self.steps:
            ok      = s["success"]
            s_color = "#16a34a" if ok is True else ("#dc2626" if ok is False else "#6b7280")
            s_icon  = "✅" if ok is True else ("❌" if ok is False else "⏳")
            detail  = s["selector"] or s["text"] or "—"
            rows += f"""
            <tr>
              <td class="cell num">{s['step']}</td>
              <td class="cell">{s['timestamp']}</td>
              <td class="cell"><span class="badge action">{s['action']}</span></td>
              <td class="cell mono small">{detail[:80]}</td>
              <td class="cell url small">{s['url'][:60]}…</td>
              <td class="cell" style="color:{s_color};font-weight:600">{s_icon}</td>
            </tr>"""

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Test Report — {self.result}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
          background: #f8fafc; color: #1e293b; padding: 32px 24px; }}
  h1   {{ font-size: 1.6rem; font-weight: 700; margin-bottom: 4px; }}
  .sub {{ color: #64748b; font-size: .9rem; margin-bottom: 28px; }}

  .card {{
    background: #fff; border-radius: 12px; padding: 24px;
    box-shadow: 0 1px 4px rgba(0,0,0,.08); margin-bottom: 24px;
  }}

  .meta-grid {{
    display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px;
  }}
  .meta-item label {{ font-size: .75rem; color: #64748b; text-transform: uppercase;
                       letter-spacing: .05em; display: block; margin-bottom: 4px; }}
  .meta-item span  {{ font-size: 1rem; font-weight: 600; }}

  .result-badge {{
    display: inline-block; padding: 6px 18px; border-radius: 999px;
    font-weight: 700; font-size: 1rem;
    color: {color}; background: {bg_badge};
  }}

  table  {{ width: 100%; border-collapse: collapse; font-size: .875rem; }}
  th     {{ text-align: left; padding: 10px 12px; background: #f1f5f9;
             color: #475569; font-weight: 600; font-size: .75rem;
             text-transform: uppercase; letter-spacing: .05em; }}
  .cell  {{ padding: 10px 12px; border-bottom: 1px solid #f1f5f9; vertical-align: top; }}
  .num   {{ color: #94a3b8; width: 40px; }}
  .mono  {{ font-family: monospace; }}
  .small {{ font-size: .8rem; color: #475569; }}
  .url   {{ max-width: 220px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
  tr:hover td {{ background: #f8fafc; }}

  .badge {{
    display: inline-block; padding: 2px 10px; border-radius: 999px;
    font-size: .75rem; font-weight: 600;
  }}
  .badge.action {{ background: #ede9fe; color: #6d28d9; }}

  .reason {{ margin-top: 12px; padding: 12px 16px; background: #f1f5f9;
              border-radius: 8px; font-size: .9rem; color: #334155; }}
</style>
</head>
<body>

<h1>🤖 Automation Test Report</h1>
<p class="sub">Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

<div class="card">
  <div class="meta-grid">
    <div class="meta-item">
      <label>Result</label>
      <span><span class="result-badge">{icon} {self.result}</span></span>
    </div>
    <div class="meta-item">
      <label>Goal</label>
      <span>{self.goal}</span>
    </div>
    <div class="meta-item">
      <label>Duration</label>
      <span>{duration}</span>
    </div>
    <div class="meta-item">
      <label>Total Steps</label>
      <span>{len(self.steps)}</span>
    </div>
    <div class="meta-item">
      <label>Started</label>
      <span>{d['started_at'] or '—'}</span>
    </div>
    <div class="meta-item">
      <label>URL</label>
      <span class="small">{self.url}</span>
    </div>
  </div>
  {f'<div class="reason">📝 {self.reason}</div>' if self.reason else ''}
</div>

<div class="card">
  <table>
    <thead>
      <tr>
        <th>#</th><th>Time</th><th>Action</th>
        <th>Detail</th><th>URL</th><th>Status</th>
      </tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
</div>

</body>
</html>"""