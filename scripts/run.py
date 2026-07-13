#!/usr/bin/env python3
"""盘后复盘完整版 · 一键生成入口
用法：
  TUSHARE_TOKEN=xxx python run.py [trade_date] [output_dir]

trade_date 默认今天 (YYYYMMDD), output_dir 默认当前目录
"""
import os, sys, subprocess, json
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    today = datetime.now().strftime("%Y%m%d")
    td = sys.argv[1] if len(sys.argv) > 1 else today
    out_dir = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()

    os.environ["TRADE_DATE"] = td
    token = os.environ.get("TUSHARE_TOKEN", "")

    if not token:
        print("ERROR: need TUSHARE_TOKEN env var", file=sys.stderr)
        sys.exit(1)

    venv_python = os.environ.get("VENV_PYTHON", "/Users/ben/.workbuddy/binaries/python/envs/default/bin/python")

    # Step 1: Fetch
    print(f"[1/3] Fetching data for {td}...")
    r = subprocess.run([venv_python, os.path.join(SCRIPT_DIR, "fetch.py"), out_dir],
                       capture_output=True, text=True, env=os.environ)
    if r.returncode != 0:
        print(f"FETCH FAILED:\n{r.stderr}", file=sys.stderr)
        sys.exit(1)
    data_path = r.stdout.strip().split("FETCH_OK:")[-1].strip()
    print(f"  → {data_path}")

    # Step 2: Aggregate
    print("[2/3] Aggregating data...")
    agg_path = os.path.join(out_dir, f"ts_agg_{td}.json")
    r = subprocess.run([venv_python, os.path.join(SCRIPT_DIR, "aggregate.py"), data_path, agg_path],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(f"AGG FAILED:\n{r.stderr}", file=sys.stderr)
        sys.exit(1)
    print(f"  → {agg_path}")

    # Step 3: Build HTML
    print("[3/3] Building HTML report...")
    html_path = os.path.join(out_dir, f"盘后复盘与次日策略_{td}.html")
    weekday_map = ["周一","周二","周三","周四","周五","周六","周日"]
    try:
        dt = datetime.strptime(td, "%Y%m%d")
        date_label = f"{dt.year}-{dt.month:02d}-{dt.day:02d}"
        weekday_label = weekday_map[dt.weekday()]
    except:
        date_label = td
        weekday_label = ""

    r = subprocess.run([venv_python, os.path.join(SCRIPT_DIR, "build_report.py"),
                        agg_path, html_path, date_label, weekday_label],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(f"BUILD FAILED:\n{r.stderr}", file=sys.stderr)
        sys.exit(1)
    print(f"  → {html_path}")
    print(f"\nDONE: {html_path}")

    # Cleanup temp files
    for f in [data_path, agg_path]:
        try:
            os.remove(f)
        except:
            pass

if __name__ == "__main__":
    main()
