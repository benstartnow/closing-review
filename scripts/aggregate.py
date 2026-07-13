#!/usr/bin/env python3
"""盘后复盘完整版 · 数据聚合脚本
读取 ts_data.json，输出 ts_agg.json（结构化报告数据）"""
import json, sys
from collections import Counter, defaultdict

def to_dicts(d, key):
    r = d.get(key, {})
    if "items" not in r: return []
    return [dict(zip(r["fields"], row)) for row in r["items"]]

def main():
    in_path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/ts_data.json"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "/tmp/ts_agg.json"
    d = json.load(open(in_path))
    out = {}

    # 1. 指数
    idx = []
    for code, v in d.get("index_daily", {}).items():
        r = v["res"]
        if "items" in r and r["items"]:
            rec = dict(zip(r["fields"], r["items"][0]))
            idx.append({"code": code, "name": v["name"], "close": rec["close"],
                        "pct": rec["pct_chg"], "amount": rec["amount"]})
    out["index"] = idx

    # 2. 市场宽度
    alls = to_dicts(d, "daily_all")
    up = sum(1 for x in alls if x.get("pct_chg") is not None and x["pct_chg"] > 0)
    down = sum(1 for x in alls if x.get("pct_chg") is not None and x["pct_chg"] < 0)
    flat = sum(1 for x in alls if x.get("pct_chg") == 0)
    up9 = sum(1 for x in alls if x.get("pct_chg") is not None and x["pct_chg"] >= 9.8)
    down9 = sum(1 for x in alls if x.get("pct_chg") is not None and x["pct_chg"] <= -9.8)
    total_amt = sum(x["amount"] for x in alls if x.get("amount"))
    out["breadth"] = {
        "total": len(alls), "up": up, "down": down, "flat": flat,
        "up_limit_approx": up9, "down_limit_approx": down9,
        "total_amount_yi": round(total_amt / 1e5, 1)
    }

    # 3. 涨停/连板梯队
    ll = to_dicts(d, "limit_list_d")
    uplist = [x for x in ll if x.get("limit") == "U"]
    downlist = [x for x in ll if x.get("limit") == "D"]
    zlist = [x for x in ll if x.get("limit") == "Z"]
    lt = Counter()
    tiers = defaultdict(list)
    for x in uplist:
        n = x.get("limit_times") or 1
        lt[n] += 1
        tiers[int(n)].append((x["name"], x.get("industry"), x.get("up_stat")))
    out["limit"] = {
        "up_count": len(uplist), "down_count": len(downlist), "zha_count": len(zlist),
        "tier_dist": dict(sorted(lt.items(), key=lambda kv: -kv[0])),
        "high_tiers": {int(k): tiers[k] for k in sorted(tiers, reverse=True)[:5]}
    }

    # 4. 行业资金流
    ind = to_dicts(d, "moneyflow_ind_dc")
    cts = Counter(x.get("content_type") for x in ind)
    out["ind_content_types"] = dict(cts)

    def pick_sorted(ct=None):
        data = [x for x in ind if (ct is None or x.get("content_type") == ct) and x.get("net_amount") is not None]
        data.sort(key=lambda x: x["net_amount"], reverse=True)
        return data

    all_ind = pick_sorted(None)
    out["ind_top_in"] = [
        {"name": x["name"], "ct": x.get("content_type"), "pct": x["pct_change"],
         "net_yi": round(x["net_amount"] / 1e8, 2)} for x in all_ind[:8]]
    out["ind_top_out"] = [
        {"name": x["name"], "ct": x.get("content_type"), "pct": x["pct_change"],
         "net_yi": round(x["net_amount"] / 1e8, 2)} for x in all_ind[-8:][::-1]]

    ind_pct = [x for x in ind if x.get("pct_change") is not None]
    ind_pct.sort(key=lambda x: x["pct_change"], reverse=True)
    out["ind_gain"] = [
        {"name": x["name"], "ct": x.get("content_type"), "pct": x["pct_change"],
         "net_yi": round((x["net_amount"] or 0) / 1e8, 2)} for x in ind_pct[:8]]
    out["ind_lose"] = [
        {"name": x["name"], "ct": x.get("content_type"), "pct": x["pct_change"],
         "net_yi": round((x["net_amount"] or 0) / 1e8, 2)} for x in ind_pct[-8:][::-1]]

    # 5. 大盘资金结构
    mkt = to_dicts(d, "moneyflow_mkt_dc")
    if mkt:
        out["mkt_flow"] = {
            "main_yi": round(mkt[0]["net_amount"] / 1e8, 1),
            "elg_yi": round(mkt[0]["buy_elg_amount"] / 1e8, 1),
            "lg_yi": round(mkt[0]["buy_lg_amount"] / 1e8, 1),
            "md_yi": round(mkt[0]["buy_md_amount"] / 1e8, 1),
            "sm_yi": round(mkt[0]["buy_sm_amount"] / 1e8, 1),
        }

    # 6. 个股资金流：跟踪个股
    mdc_name = {x["name"]: x for x in to_dicts(d, "moneyflow_dc")}
    watch_names = ["常山药业", "欢瑞世纪", "兆易创新", "中际旭创", "中科曙光", "海光信息", "歌尔股份"]
    wl = []
    for n in watch_names:
        x = mdc_name.get(n)
        if x:
            wl.append({"name": n, "pct": x["pct_change"], "close": x["close"],
                       "net_yi": round((x["net_amount"] or 0) / 1e8, 2)})
        else:
            wl.append({"name": n, "missing": True})
    out["watch"] = wl

    mall = [x for x in to_dicts(d, "moneyflow_dc") if x.get("net_amount") is not None]
    mall.sort(key=lambda x: x["net_amount"], reverse=True)
    out["stk_in"] = [{"name": x["name"], "pct": x["pct_change"], "net_yi": round(x["net_amount"] / 1e8, 2)} for x in mall[:10]]
    out["stk_out"] = [{"name": x["name"], "pct": x["pct_change"], "net_yi": round(x["net_amount"] / 1e8, 2)} for x in mall[-10:][::-1]]

    json.dump(out, open(out_path, "w"), ensure_ascii=False, indent=1)
    print(f"AGG_OK:{out_path}")
    return out_path

if __name__ == "__main__":
    main()
