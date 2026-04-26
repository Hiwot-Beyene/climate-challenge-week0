# Notebooks

Each notebook corresponds to one task and one branch.

| Notebook | Branch | Task |
|---|---|---|
| `ethiopia_eda.ipynb` | `eda-ethiopia` | Task 2 |
| `kenya_eda.ipynb` | `eda-kenya` | Task 2 |
| `sudan_eda.ipynb` | `eda-sudan` | Task 2 |
| `tanzania_eda.ipynb` | `eda-tanzania` | Task 2 |
| `nigeria_eda.ipynb` | `eda-nigeria` | Task 2 |
| `compare_countries.ipynb` | `compare-countries` | Task 3 |

## Notebook discipline (senior rules)

1. **Restart & Run All before committing** — never commit notebooks with stale outputs or cells run out of order.
2. **Every plot gets a markdown cell below it** — interpretation is graded.
3. **No hardcoded paths** — always use `Path("data") / "ethiopia.csv"` not `/Users/yourname/...`.
4. **Import from src/**, not inline code — keeps notebooks thin and functions testable.
