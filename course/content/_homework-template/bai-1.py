import json
import sys


def solve(z, lam):
    # Trả về (ridge, lasso): hai list cùng độ dài với z.
    raise NotImplementedError


if __name__ == "__main__":
    data = json.loads(sys.stdin.read())
    ridge, lasso = solve(data["z"], data["lam"])
    print(json.dumps({"ridge": ridge, "lasso": lasso}))
