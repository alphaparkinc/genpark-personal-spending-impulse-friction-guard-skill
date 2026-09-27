import sys, json
from client import PersonalSpendingImpulseGuard

def main():
    print("Testing PersonalSpendingImpulseGuard...")
    guard = PersonalSpendingImpulseGuard()
    res = guard.run_benchmark_spending_guard()
    print(json.dumps(res, indent=2))
    assert res["benchmark_status"] == "PASSED"
    assert res["scenario_impulse_cooling_hours"] >= 24
    assert res["scenario_rational_cooling_hours"] == 0
    print("All Personal Spending Impulse Guard tests passed successfully!")

if __name__ == "__main__":
    main()
