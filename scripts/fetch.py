#!/usr/bin/env python3
"""盘后复盘完整版 · 数据获取脚本
从 Tushare Pro 拉取：指数日线 / 全市场个股 / 涨跌停 / 行业资金流 / 大盘资金结构
环境变量: TUSHARE_TOKEN, TRADE_DATE (YYYYMMDD)"""
import os, sys, json, time, requests

URL = "http://api.tushare.pro"

def call(api, params, fields=""):
    token = os.environ.get("TUSHARE_TOKEN", "")
    payload = {"api_name": api, "token": token, "params": params, "fields": fields}
    for _ in range(3):
        try:
            r = requests.post(URL, json=payload, timeout=40)
            d = r.json()
            if d.get("code") == 0:
                return {"fields": d["data"]["fields"], "items": d["data"]["items"]}
            return {"error": d.get("msg"), "code": d.get("code")}
        except Exception as e:
            time.sleep(1)
            last = repr(e)
    return {"error": last}

def main():
    td = os.environ.get("TRADE_DATE", "")
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "/tmp"
    data = {}
    
    # 1. 六大指数日线
    idx_map = {"000001.SH":"上证指数","399001.SZ":"深证成指","399006.SZ":"创业板指",
               "000300.SH":"沪深300","000688.SH":"科创50","899050.BJ":"北证50"}
    data["index_daily"] = {}
    for code, name in idx_map.items():
        data["index_daily"][code] = {"name": name, "res": call("index_daily", {"ts_code": code, "start_date": td, "end_date": td})}
    
    # 2. 全市场个股日线
    data["daily_all"] = call("daily", {"trade_date": td})
    
    # 3. 涨跌停列表
    data["limit_list_d"] = call("limit_list_d", {"trade_date": td})
    
    # 4. 行业资金流（东财）
    data["moneyflow_ind_dc"] = call("moneyflow_ind_dc", {"trade_date": td})
    
    # 5. 个股资金流
    data["moneyflow_dc"] = call("moneyflow_dc", {"trade_date": td})
    
    # 6. 大盘资金流（超大单/大单结构）
    data["moneyflow_mkt_dc"] = call("moneyflow_mkt_dc", {"trade_date": td})
    
    path = os.path.join(out_dir, "ts_data.json")
    json.dump(data, open(path, "w"), ensure_ascii=False)
    print(f"FETCH_OK:{path}")
    return path

if __name__ == "__main__":
    main()
