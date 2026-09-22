# Jev Smart Retry test lab

This public, owner-operated repository tests the [main branch of Jev Smart Retry](https://github.com/MakonnenMak/jev-smart-retry/tree/main). Both workflow steps use `MakonnenMak/jev-smart-retry@main`, so new runs exercise the current Action code. The Action has no published release tag yet; `main` is a moving ref. Each run records the resolved Action commit in its setup log.

## Run a scenario

The repository owner adds the Actions secret `TYPESAFE_API_KEY`, then selects **Actions → Jev Smart Retry lab → Run workflow** and chooses a scenario. The workflow runs only through `workflow_dispatch` and gives `GITHUB_TOKEN` read-only contents permission. GitHub requires repository write access to dispatch it; access to this repository is currently limited to its owner for writes. The workflow and its run logs are public, so the cases contain no private test data.

| Scenario | What happens | What to look for |
| --- | --- | --- |
| `transient-network` | The command makes a real localhost connection attempt before a service is listening. The resulting `ConnectionRefusedError` starts a short-lived local service; the exact same command can succeed on retry. | At the Action's default thresholds, `attempts=2` and `recovered=true` mean Jev allowed recovery. `attempts=1` means it declined or could not get a valid decision; inspect the category and scores. |
| `deterministic-error` | Python compiles a file with a syntax error, unchanged between attempts. | `attempts=1` means Jev declined this deterministic failure. A retry is a false positive for this case and should fail again. |
| `retry-mechanics-demo` | Reuses the network case with a lab-only `0.00` retry probability threshold. | `attempts=2` and `recovered=true` demonstrate the retry mechanism. Jev must still select a retryable category with at least the default `0.75` category confidence. |

All scenarios use `max-retries=1`. The first two use the Action's default `0.90` retry probability and `0.75` category confidence thresholds. The demo changes only its own retry probability threshold; it does not change the Action's defaults. The `if: always()` result step prints `attempts`, `recovered`, `category`, `retry-probability`, and `category-confidence`, including after an expected failure. Empty classification fields may mean Jev was unavailable or returned an invalid response.

These staged cases verify the workflow and illustrate individual decisions. They do not establish accuracy on real CI failures, whose causes, logs, environments, and prevalence differ. Evaluating that requires labeled real failures and measuring both missed recoveries and harmful retries.
