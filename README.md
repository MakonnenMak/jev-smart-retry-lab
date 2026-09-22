# Jev Smart Retry lab

This private, manual-only workflow exercises [Jev Smart Retry](https://github.com/MakonnenMak/jev-smart-retry) at commit `8265ccd55fa65dd912b71c98262ba1d8dd4f188c`. Add the repository Actions secret `TYPESAFE_API_KEY`, then run **Actions → Jev Smart Retry lab → Run workflow** and choose a scenario. Each Action invocation allows one additional attempt. The first two choices use the Action's default `0.90` retry probability and `0.75` category confidence thresholds.

- **transient-network:** The command really connects to localhost before anything is listening, producing a `ConnectionRefusedError`. It then starts a short-lived local service. A retry of the exact same command can connect successfully. `attempts=2` and `recovered=true` show that Jev allowed this staged recovery. `attempts=1` means the Action declined or could not obtain a valid Jev decision; inspect the category and scores.
- **deterministic-error:** Python compiles a file with a syntax error. The file is unchanged across attempts. `attempts=1` shows Jev declined a deterministic failure. If it retries, the compile command should fail again; a retry here is a false positive for this example.
- **retry-mechanics-demo:** Uses the same network case with a lab-only `0.50` retry probability threshold. Use it to exercise the successful retry path if Jev declines the network case at `0.90`. Category confidence stays at its default `0.75`; Jev can still decline. This does not change the Action's production defaults.

The final step prints `attempts`, `recovered`, `category`, `retry-probability`, and `category-confidence` even when the Action step fails. Empty category or score fields can mean Jev was unavailable or returned an invalid response; they do not establish a classification.

These two staged failures check the workflow's mechanics and a couple of decisions. They do **not** establish accuracy on real CI failures, which vary in logs, causes, environments, and prevalence. Calibration requires labeled real failures and measuring both missed recoveries and harmful retries.
