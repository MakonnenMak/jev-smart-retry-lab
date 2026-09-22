# Jev Smart Retry test lab

This private, manual-only repository tests the [main branch of Jev Smart Retry](https://github.com/MakonnenMak/jev-smart-retry/tree/main). Both workflow steps use `MakonnenMak/jev-smart-retry@main`, so new runs exercise the current Action code. The Action has no published release tag yet; `main` is a moving ref. Each run records the resolved Action commit in its setup log.

## Run a scenario

Add the repository Actions secret `TYPESAFE_API_KEY` in [Settings → Secrets and variables → Actions](https://github.com/MakonnenMak/jev-smart-retry-lab/settings/secrets/actions), then open [Jev Smart Retry lab](https://github.com/MakonnenMak/jev-smart-retry-lab/actions/workflows/jev-lab.yml), select **Run workflow**, and choose a scenario. The workflow runs only through `workflow_dispatch` and gives `GITHUB_TOKEN` read-only contents permission.

| Scenario | What happens | What to look for |
| --- | --- | --- |
| `transient-network` | The command makes a real localhost connection attempt before a service is listening. The resulting `ConnectionRefusedError` starts a short-lived local service; the exact same command can succeed on retry. | At the Action's default thresholds, `attempts=2` and `recovered=true` mean Jev allowed recovery. `attempts=1` means it declined or could not get a valid decision; inspect the category and scores. |
| `deterministic-error` | Python compiles a file with a syntax error, unchanged between attempts. | `attempts=1` means Jev declined this deterministic failure. A retry is a false positive for this case and should fail again. |
| `retry-mechanics-demo` | Reuses the network case with a lab-only `0.00` retry probability threshold. | `attempts=2` and `recovered=true` demonstrate the retry mechanism. Jev must still select a retryable category with at least the default `0.75` category confidence. |

All scenarios use `max-retries=1`. The first two use the Action's default `0.90` retry probability and `0.75` category confidence thresholds. The demo changes only its own retry probability threshold; it does not change the Action's defaults. The `if: always()` result step prints `attempts`, `recovered`, `category`, `retry-probability`, and `category-confidence`, including after an expected failure. Empty classification fields may mean Jev was unavailable or returned an invalid response.

## Observed runs

These are the initial runs on 2026-09-22, when `main` resolved to `8265ccd55fa65dd912b71c98262ba1d8dd4f188c`. Scores can vary on later runs.

| Scenario | Result |
| --- | --- |
| [`transient-network`](https://github.com/MakonnenMak/jev-smart-retry-lab/actions/runs/35777285360) | Real connection refusal; `network`, probability `0.41`, confidence `0.99`; declined at `0.90` (`attempts=1`). |
| [`deterministic-error`](https://github.com/MakonnenMak/jev-smart-retry-lab/actions/runs/35777308394) | Syntax error; `code_regression`, probability `0.03`, confidence `1.00`; declined (`attempts=1`). |
| [`retry-mechanics-demo`](https://github.com/MakonnenMak/jev-smart-retry-lab/actions/runs/35777526020) | Real connection refusal followed by success on the same command; `attempts=2`, `recovered=true`. |

These staged cases verify the workflow and illustrate individual decisions. They do not establish accuracy on real CI failures, whose causes, logs, environments, and prevalence differ. Evaluating that requires labeled real failures and measuring both missed recoveries and harmful retries.
