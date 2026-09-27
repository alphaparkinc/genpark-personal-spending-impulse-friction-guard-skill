import sys, json
from client import PersonalSpendingImpulseGuard

def main():
    guard = PersonalSpendingImpulseGuard()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(guard.run_benchmark_spending_guard(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            params = req.get("params", {})
            rid = req.get("id")

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "evaluate_purchase_intent", "description": "Assess purchase for impulse risk and work hours cost."},
                        {"name": "calculate_work_hour_equivalence", "description": "Convert dollar amount into required labor hours."},
                        {"name": "run_benchmark_spending_guard", "description": "Run spending guard tests."}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "evaluate_purchase_intent":
                    out = guard.evaluate_purchase_intent(
                        args.get("item_name", "item"),
                        args.get("price", 0.0),
                        args.get("net_hourly_wage", 30.0),
                        args.get("current_hour_24", 14),
                        args.get("user_emotion", "neutral")
                    )
                elif tname == "calculate_work_hour_equivalence":
                    out = guard.calculate_work_hour_equivalence(args.get("price", 0.0), args.get("net_hourly_wage", 30.0))
                elif tname == "run_benchmark_spending_guard":
                    out = guard.run_benchmark_spending_guard()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
