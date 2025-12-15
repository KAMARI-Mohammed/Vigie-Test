import json
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Any,Optional,Iterable

def read_json_file(file_path: str) -> Iterable[Dict[str, Any]]:
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
 

def analyse_orders(orders:Iterable[Dict[str, Any]],from_date:Optional[str] =None):
    suspicious_list: List[Dict[str,Any]] = []
    revenue_by_mp = defaultdict(int)
    total = 0

    from_dt = None
    if from_date:
        try:
            from_dt = datetime.strptime(from_date, "%Y-%m-%d")
        except ValueError as e:
            print(f"Error parsing date: {e}")

    for order in orders:
        if order.get("__parse_error__"):
            suspicious_list.append({
                "order_id": order.get("id") or order.get("order_id"),
                "reason": "JSON parse error",
                "raw": order,
            })
            continue
        
        order_id = order.get("order_id")
        created_at_str = order.get("created_at")
        dt = None
        if created_at_str:
            try:
                dt = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%SZ")
                if from_dt and dt < from_dt:
                    continue
            except ValueError:
                pass

        if from_dt and dt and dt < from_dt:
            continue 

        amount = order.get("amount") or order.get("amount_cents")
        try:
            amount = int(amount)
        except (TypeError, ValueError):
            suspicious_list.append({
            "order_id": order_id,
            "reason": "invalid_amount",
            "raw": order,
        })
            continue

        if amount < 0:
            suspicious_list.append({
                "order_id": order_id,
                "reason": "negative_amount",
                "raw": order,
            })
            continue

        marketplace = order.get("marketplace")
        if marketplace is None:
            suspicious_list.append({
                "order_id": order_id,
                "reason": "missing_marketplace",
                "raw": order,
            })
            continue
        revenue_by_mp[marketplace] += amount
        total += amount
    
    rev_mp_eur = {k: v / 100 for k, v in revenue_by_mp.items()} 
    sorted_mp = dict(sorted(rev_mp_eur.items(), key=lambda x: x[1], reverse=True))

    stats = {
        "revenue_total_eur": round(total/ 100, 2),
        "revenue_by_marketplace": sorted_mp,
        "suspicious_orders": suspicious_list,
    }    
    return stats, suspicious_list

