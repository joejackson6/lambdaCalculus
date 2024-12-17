import re
from typing import Dict

def parse_lambda_expr(expr: str) -> str:
    return expr.replace(' ', '').replace('λ', '\\')

def beta_reduce(expr: str, substitutions: Dict[str, str] = None) -> str:
    if substitutions is None:
        substitutions = {}
    def reduce(current_expr):
        match = re.search(r'\\([^.]+)\\.([^)]+)\\s*\\(([^)]+)\\)', current_expr)
        if match:
            var, body, arg = match.groups()
            return reduce(body.replace(var, arg))
        return current_expr
    return reduce(expr)

def eta_reduce(expr: str) -> str:
    match = re.match(r'\\([^.]+)\\.(([^)]+)\\s*\\1)', expr)
    return match.groups()[2] if match else expr

def normalize_lambda_expr(expr: str) -> str:
    prev_expr, current_expr = None, expr
    while prev_expr != current_expr:
        prev_expr = current_expr
        current_expr = eta_reduce(beta_reduce(current_expr))
    return current_expr

def solve_lambda_expr(expr: str) -> str:
    return normalize_lambda_expr(parse_lambda_expr(expr))

def apply_substitution(expr: str, var: str, value: str) -> str:
    return beta_reduce(expr, {var: value})

def are_lambda_exprs_equivalent(expr1: str, expr2: str) -> bool:
    return normalize_lambda_expr(expr1) == normalize_lambda_expr(expr2)

def main():
    tests = {
        "Identity Function": solve_lambda_expr(r"\\x.x"),
        "Self Application": solve_lambda_expr(r"(\\x.x x)"),
        "Beta Reduction (\\x.\\y.x a)": solve_lambda_expr(r"(\\x.\\y.x a)"),
        "Eta Reduction (\\x.(f x))": solve_lambda_expr(r"\\x.(f x)"),
        "Alpha Equivalence (\\x.x, \\y.y)": are_lambda_exprs_equivalent(r"\\x.x", r"\\y.y"),
        "Non-equivalence (\\x.x, \\x.y)": are_lambda_exprs_equivalent(r"\\x.x", r"\\x.y"),
        "Complex Reduction": solve_lambda_expr(r"((\\x.\\y.x) a b)"),
    }

    print("Extended Lambda Calculus Solver Tests:")
    for test_name, result in tests.items():
        print(f"{test_name}: {result}")

if __name__ == "__main__":
    main()

