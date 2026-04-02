from board import Board
from row import Row
from visualize import show
import argparse

def build_modules():
    RB3 = Board("RB", 3)
    RB6 = Board("RB", 6)
    RB7 = Board("RB", 7)
    PB1 = Board("PB", 1)
    PB2 = Board("PB", 2)

    M3 = RB3 + PB1
    M6 = RB6 + PB2
    M7 = RB7 + PB2

    return M3, M6, M7


def row_recurse(row, m3, m6, m7, results=None, under_tol=None):
    if results is None:
        results = []
    if under_tol is None:
        under_tol = []

    if row.over_tolerance:
        return results, under_tol

    if row.in_tolerance["RB"] or row.in_tolerance["PB"]:
        results.append(row)
        return results, under_tol

    under_tol.append(row)

    for module in [m3, m6, m7]:
        next_row = Row(row.modules + [module], row.row_index, row.R, row.tol)
        row_recurse(next_row, m3, m6, m7, results, under_tol)

    return results, under_tol


def prune(results):
    seen = set()
    pruned = []
    for row in results:
        modules = row.modules
        first = modules[0].label
        last = modules[-1].label
        middle = tuple(sorted(m.label for m in modules[1:-1]))
        key = (first, last, middle)
        if key not in seen:
            seen.add(key)
            pruned.append(row)
    return pruned


def print_results(results, title=None):
    n = 102
    print("\n" * 3)
    if title:
        print(title)
    print("+" + "-" * n + "+")
    for row in results:
        print(row)
    print("+" + "-" * n + "+")


if __name__ == "__main__":

    argParser = argparse.ArgumentParser(description="Argument parser")
    argParser.add_argument('--row', action='store', type=int, default=0, help="Row to optimize (0 to 25)")
    argParser.add_argument('--radius', action='store', type=int, default=1000, help="Keep out radius (mm)")
    argParser.add_argument('--tol', action='store', type=float, default=5, help="Tolerance to keepout radius (mm)")
    argParser.add_argument('--visualize', action='store_true', default=False, help="Visualize results in Pygame window")
    argParser.add_argument('--prune', action='store_true', help="Remove duplicates (two solutions with same first and last module that just mix up the order in between)")
    args = argParser.parse_args()

    M3, M6, M7 = build_modules()

    starting_row_M3 = Row([M3], args.row, args.radius, args.tol)
    starting_row_M6 = Row([M6], args.row, args.radius, args.tol)
    starting_row_M7 = Row([M7], args.row, args.radius, args.tol)

    M3_results, M3_under = row_recurse(starting_row_M3, M3, M6, M7)
    M6_results, M6_under = row_recurse(starting_row_M6, M3, M6, M7)
    M7_results, M7_under = row_recurse(starting_row_M7, M3, M6, M7)

    sorted_M3_results = sorted(M3_results)[::-1]
    sorted_M6_results = sorted(M6_results)[::-1]
    sorted_M7_results = sorted(M7_results)[::-1]

    sorted_M3_under = sorted(M3_under)[::-1]
    sorted_M6_under = sorted(M6_under)[::-1]
    sorted_M7_under = sorted(M7_under)[::-1]

    if args.prune:
        sorted_M3_results = prune(sorted_M3_results)
        sorted_M6_results = prune(sorted_M6_results)
        sorted_M7_results = prune(sorted_M7_results)

        sorted_M3_under = prune(sorted_M3_under)
        sorted_M6_under = prune(sorted_M6_under)
        sorted_M7_under = prune(sorted_M7_under)

    all_results = sorted_M3_results + sorted_M6_results + sorted_M7_results
    all_results_under = sorted_M3_under[:10] + sorted_M6_under[:10] + sorted_M7_under[:10]

    if len(all_results + all_results_under) > 0:
        print_results(all_results, "Results (In tolerance)")
        print_results(all_results_under, "Results (Under tolerance)")
    else:
        print("No results in tolerance or under tolerance")

    if args.visualize and len(all_results + all_results_under) != 0:
        show(all_results + all_results_under, args.row)
    elif args.visualize:
        print("No results to visualize")