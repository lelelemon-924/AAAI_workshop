# P0/P1 experiment plan before submission

## P0 — required to make the current claims defensible

### 1. Stage-A / Stage-B identity audit
Use the exact same Stage-A checkpoint and inference path.

- Save content logits for every test instance immediately after Stage A.
- Run Stage B with the shared trunk detached/frozen.
- Save content logits again.
- Report `max_abs_diff`, `mean_abs_diff`, and the count of changed predictions.
- Expected under the written method: differences are zero up to numerical tolerance.
- If they are not, inspect checkpoint loading, dropout/eval mode, tokenizer/template, LoRA target modules, optimizer parameter groups, and inference preprocessing.

### 2. Matched Stage-A-only dual-head control
Match the final two-head run on:
- base checkpoint and tokenizer revision;
- initialization of the shared trunk and content head;
- training examples and sample order;
- optimizer, scheduler, batch size, epochs, and random seeds;
- inference prompt and yes/no token extraction.

The Stage-A-only content logits should match the final two-head model's logits. Report this row explicitly. Do not attribute any difference from single-head RLCD to Stage B.

### 3. Correct benchmark metrics
For every method, report:
- Overall accuracy, AUROC, Brier, NLL, ECE;
- ECE by concise/detailed/markdown style;
- official RM-Bench Easy / Normal / Hard from the official evaluation implementation;
- ECA as a separate additional metric;
- style-flip rate and confidence inflation.

Keep the evaluation script and exact version/commit in the repository.

### 4. Statistical analysis
- Use paired bootstrap resampling at the prompt/pair level, not at the six-instance level.
- Report 95% confidence intervals for accuracy, official Hard, ECA, ECE, Markdown ECE, and flip rate.
- Report seed-level mean and standard deviation separately.
- Use a predeclared non-inferiority margin for content accuracy if claiming no accuracy loss.

### 5. Selective prediction audit
- Choose the threshold on calibration data only.
- Freeze it before test evaluation.
- Report test coverage and observed selective risk with confidence intervals.
- If claiming a formal risk guarantee, implement and cite a valid risk-control/conformal procedure.

## P1 — strongly recommended

### 6. Strong baselines
At minimum add:
- Counterfactual Data Augmentation (CDA) using style-swapped positive/negative responses;
- one shared-parameter multi-task baseline such as PCGrad or MGDA;
- temperature scaling as a calibration-only post-processing baseline.

If compute is constrained, prioritize CDA and PCGrad over adding many weaker baselines.

### 7. Semantic-preservation audit
Sample 200–300 prompts stratified by domain and label. Have at least two independent annotators assess whether each style rewrite preserves the task-relevant content. Report agreement (e.g., Cohen's kappa or Krippendorff's alpha), drift categories, and exclusions.

### 8. Domain and split accounting
Generate the train/calibration/test counts directly from the split manifest:
- total prompts per domain;
- train prompts per domain;
- calibration prompts per domain;
- test prompts per domain.

Explain whether the split is hash-random or stratified. Do not infer domain counts from a plot.

### 9. Generalization
Test at least two unseen style transformations (e.g., formal tone, jargon-heavy wording, bullet structure, paraphrase). Keep the test transformations out of training and hyperparameter selection.

### 10. Reproducibility release
Include:
- model and tokenizer revisions;
- package versions and hardware;
- full configs and random seeds;
- run IDs and checkpoints;
- exact split manifest/hash;
- evaluation scripts;
- logs sufficient to regenerate every table cell.
