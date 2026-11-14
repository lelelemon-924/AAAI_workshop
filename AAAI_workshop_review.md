# CC-RLCD 论文问题清单

- 仓库：https://github.com/lelelemon-924/AAAI_workshop
- 论文：`paper/sd_rlcd.tex`
- 审查日期：2026-11-12

## 一、硬伤

### 1. 训练目标与测试指标重合，缺少反方向检验

- 第 92 行的风格冲突对 \(\mathcal{P}_{\mathrm{adv}}=\{(\mathrm{con},\mathrm{det}),(\mathrm{det},\mathrm{md}),(\mathrm{con},\mathrm{md})\}\) 正好是 RM-Bench Hard 计算的三对，\(L_{\mathrm{margin}}\) 直接优化的就是测试指标。
- 训练集和测试集来自 RM-Bench 的同一分布，报告的 Hard 不能和公开榜单直接比较，但文中没有说明。
- 第 52 行的贡献列表写了会单独报告 Easy/Normal/Hard，但正文只报了 Hard。
- 没有反方向配对（markdown 正确 vs 简洁错误）的结果，无法排除模型只学会了"markdown 等于差"这种过度矫正。

### 2. Proposition 1 的形式化有错（第 70–76 行）

- \(\mu(X)\) 只依赖 prompt，预测器只依赖 prompt 和风格，同一 prompt 下的正确回答和错误回答对它来说没有区别。因此 "\(\mu(x^+)-\mu(x^-)\)" 没有定义；按现有写法，每个冲突对都会被反转，而不只是差值小于 \(2\delta\) 的那些。
- \(\mathrm{ECE}_{\mathrm{mix}}=2\delta^2/(1-2\delta)\) 只在无限细分箱（或按预测值条件）的总体 ECE 下成立，与实验用的 15 箱 ECE 不一致，文中没有注明。
- 第 70 行写成 \(P_{\mathrm{train}}(Y_c{=}1\mid X,S)\)，丢掉了回答内容，应当以 \(R\) 为条件。
- 摘要写了 "we prove"，但正文没有证明。
- 命题只构造了一个有风格偏差的预测器，没有证明它是在训练分布上用 proper score 学到的解，与摘要 "a proper-score predictor ... can achieve" 的说法不符。

### 3. 旧版本 SD-RLCD 的残留，叙事前后矛盾

- 第 158 行提到 "unmatched two-head gains"，但全文没有出现过这个结果。
- "Causal Identity Audit" 被列为一项贡献，但 stop-gradient 之后内容 logit 不变是由构造决定的，本身不构成贡献。
- Stage 2 风格头既不改变 \(p_c\)，用于 gating 时还会降低覆盖率（0.362）且不降低风险，在方法中的作用不明确。
- `README.md` 的标题仍是 "Style-Decoupled RLCD"，与论文标题不一致。
- `figures/grid.pdf`、`figures/results.pdf` 未被使用。

### 4. 基线定义不清

- RLCD 的方法细节没有公开（所引 TypeSafe 博客明确写了 "Method details not published"），而文中 "RLCD (Brier)" 的实现是 softmax 头加 Brier 损失，看不出 RL 成分，也没有说明是谁的复现、基于哪个实现。
- Readout 基线没有定义。
- Scalar RM+T 用的是 8B 的 Skywork RM，却放在 1.5B 的表里，没有说明。

### 5. 匿名性风险

- GitHub 仓库是公开的，提交记录包含真实姓名和 gmail 地址，用论文标题可以搜到。
- 正文说 "We release ... code"，但没有匿名代码链接。

## 二、其他问题

- **显著性检验对象不对**：\(p<0.001\) 只和 RLCD 比较。和最强基线 CDA 的差距（1.5B 上 ECA 0.694 vs 0.658；7B 上 0.747 vs 0.708）落在 ±5 个点的置信区间内，但没有做检验。
- **OOD 实验不够"unseen"**：Length Swap 对应的 detailed vs concise 本身就是训练轴之一。Flattery 扰动的构造方式和样本量没有说明。
- **CRC 表述过度**：
  - 对 markdown 的 ≤5% 没有理论保证，0.049 刚好压线，但摘要写成 "restoring ≤5% selective risk on markdown"。
  - 没有定义某个 cluster 里没有样本被接受时 \(\hat R_i(t)\) 的取值。
  - CRC 保证的是按 cluster 平均的风险，没有说明测试风险是否用同一口径计算。
- **算力可能不对等**：CC-RLCD 是 "2+1 epochs"，比 RLCD 多训练一轮，没有说明基线的训练预算。
- **缺少直接竞品对比**：Patterning（Wang, Donoway, Murfet 2026，arXiv:2609.00699）在 RM-Bench Hard 上报告 +14.2 个点，SteerRM（Sun et al. 2026）报告 +13.2 个点。文中只引用了 Patterning，没有说明与这两者的区别，SteerRM 没有引用。
- **"causal" 用词过度**："causal debiasing"、"Causal Identity Audit" 里的方法是反事实成对不变性，并没有识别因果效应。
- **摘要过长**：约 225 词，信息过于密集。
