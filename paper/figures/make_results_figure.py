"""Camera-ready figures for the SD-RLCD paper."""
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/mplconfig")
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np

out = Path("/Users/zhaoyuesen/Desktop/jev/paper/figures")
out.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "Times New Roman",
    "font.size": 7.5,
    "axes.labelsize": 7.5,
    "axes.titlesize": 8,
    "mathtext.fontset": "stix",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.linewidth": 0.55,
})

NAVY = "#1f4e79"
INK = "#222222"
MUTED = "#666666"
GRID = "#b8b8b8"
FILL = "#f3f3f3"
GOOD = "#d9e6f2"
BAD = "#f0d8d8"
BAD_EDGE = "#8c2f2f"
STAGE = "#eef3f8"


def box(ax, x, y, w, h, face=FILL, edge=INK, lw=0.7, radius=0.03):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.008,rounding_size={radius}",
        facecolor=face, edgecolor=edge, linewidth=lw, clip_on=False,
    )
    ax.add_patch(patch)
    return patch


def arrow(ax, p0, p1, color=INK, lw=0.8, rad=0.0, style="-|>", ms=8):
    ax.add_patch(FancyArrowPatch(
        p0, p1, arrowstyle=style, mutation_scale=ms, linewidth=lw,
        color=color, connectionstyle=f"arc3,rad={rad}", shrinkA=1, shrinkB=1,
        clip_on=False,
    ))


# ---------------------------------------------------------------------------
# Figure 1: method overview (benchmark | architecture | objectives)
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(7.0, 2.0))
TITLE_Y = 0.965
ax_a = fig.add_axes([0.000, 0.03, 0.285, 0.82])
ax_b = fig.add_axes([0.305, 0.03, 0.405, 0.82])
ax_c = fig.add_axes([0.790, 0.19, 0.200, 0.64])
for x0, label in [(0.000, "(a) Style-CalibBench"),
                  (0.305, "(b) SD-RLCD: lexicographic two-head training"),
                  (0.735, "(c) Accuracy vs. hard accuracy")]:
    fig.text(x0, TITLE_Y, label, ha="left", va="top", fontsize=7.6,
             fontweight="bold", color=INK)

# ---- (a) Style-CalibBench ----
ax_a.set_xlim(0, 3.0)
ax_a.set_ylim(0, 2.2)
ax_a.axis("off")

xs = [0.66, 1.42, 2.18]
cw, ch = 0.64, 0.50
row_y = {1: 1.30, 0: 0.50}

for xc, name in zip(xs, ["concise", "detailed", "markdown"]):
    ax_a.text(xc + cw / 2, 2.00, name, ha="center", va="center",
              fontsize=6.2, color=MUTED)
ax_a.text(0.02, row_y[1] + ch / 2, "correct\n" r"$y_c{=}1$", ha="left",
          va="center", fontsize=6.0, linespacing=1.15)
ax_a.text(0.02, row_y[0] + ch / 2, "wrong\n" r"$y_c{=}0$", ha="left",
          va="center", fontsize=6.0, linespacing=1.15)


def grid_cell(x, y, label, face, edge, lw):
    box(ax_a, x, y, cw, ch, face=face, edge=edge, lw=lw, radius=0.02)
    ax_a.text(x + cw / 2, y + ch / 2, label, ha="center", va="center",
              fontsize=7, color=INK)


for j, xc in enumerate(xs):
    grid_cell(xc, row_y[1], r"$r^+$", GOOD if j == 0 else FILL,
              NAVY if j == 0 else GRID, 1.1 if j == 0 else 0.5)
    grid_cell(xc, row_y[0], r"$r^-$", BAD if j == 2 else FILL,
              BAD_EDGE if j == 2 else GRID, 1.1 if j == 2 else 0.5)

# hard-pair arrow runs through the gap between rows
arrow(ax_a, (xs[2] + 0.04, row_y[0] + ch + 0.03),
      (xs[0] + cw - 0.04, row_y[1] - 0.03), color=NAVY, lw=0.9, ms=6)

ax_a.text(1.50, 0.30,
          r"hard pair: $p_c(r^+_{\mathrm{concise}}) > p_c(r^-_{\mathrm{md}})$",
          ha="center", va="center", fontsize=6.2, color=NAVY)
ax_a.text(1.50, 0.08, "1,327 prompts × 6 cells, typed content question",
          ha="center", va="center", fontsize=5.4, color=MUTED)

# ---- (b) SD-RLCD architecture ----
ax_b.set_xlim(0, 4.2)
ax_b.set_ylim(0, 2.2)
ax_b.axis("off")

box(ax_b, 0.02, 0.95, 0.58, 0.50, face=STAGE, edge=NAVY, lw=0.7)
ax_b.text(0.31, 1.26, r"$(x,r)$", ha="center", va="center", fontsize=7)
ax_b.text(0.31, 1.07, "state", ha="center", va="center", fontsize=5.6, color=MUTED)
arrow(ax_b, (0.60, 1.20), (0.84, 1.20), color=INK, lw=0.8, ms=6)

box(ax_b, 0.84, 0.85, 0.96, 0.70, face="#e4edf5", edge=NAVY, lw=0.9)
ax_b.text(1.32, 1.36, r"shared trunk $\theta$", ha="center", va="center", fontsize=6.4)
ax_b.text(1.32, 1.12, "Stage A", ha="center", va="center", fontsize=5.8, color=NAVY)
ax_b.text(1.32, 0.97, r"min $L_c(\theta,\phi_c)$", ha="center", va="center",
          fontsize=5.8, color=NAVY)

box(ax_b, 2.30, 1.45, 1.02, 0.52, face=GOOD, edge=NAVY, lw=1.0)
ax_b.text(2.81, 1.80, r"content head $u_c$", ha="center", va="center", fontsize=6.3)
ax_b.text(2.81, 1.59, r"Brier $L_c$, yes/no", ha="center", va="center",
          fontsize=5.6, color=MUTED)

box(ax_b, 2.30, 0.45, 1.02, 0.52, face=FILL, edge=GRID, lw=0.7)
ax_b.text(2.81, 0.80, r"style head $u_s$", ha="center", va="center", fontsize=6.3)
ax_b.text(2.81, 0.59, r"Stage B: min $L_s(\phi_s)$", ha="center", va="center",
          fontsize=5.6, color=MUTED)

arrow(ax_b, (1.80, 1.40), (2.30, 1.71), color=NAVY, lw=0.9, ms=6)
arrow(ax_b, (1.80, 1.00), (2.30, 0.71), color=MUTED, lw=0.75, ms=6)
sg_x, sg_y = 2.05, 0.855
ax_b.plot([sg_x], [sg_y], marker="o", ms=8.5, mfc="white", mec=BAD_EDGE,
          mew=1.0, zorder=5)
ax_b.plot([sg_x], [sg_y], marker="x", ms=4.2, mec=BAD_EDGE, mew=1.1, zorder=6)
ax_b.text(sg_x, 0.30, r"stop-grad: $L_s$ never updates $\theta$",
          ha="center", va="center", fontsize=5.8, color=BAD_EDGE)

box(ax_b, 3.52, 1.45, 0.66, 0.52, face="white", edge=NAVY, lw=0.9)
ax_b.text(3.85, 1.80, r"$p_c \geq t_c$", ha="center", va="center", fontsize=6.4,
          color=NAVY)
ax_b.text(3.85, 1.59, "accept/defer", ha="center", va="center", fontsize=5.4,
          color=MUTED)
arrow(ax_b, (3.32, 1.71), (3.52, 1.71), color=NAVY, lw=0.85, ms=6)

box(ax_b, 3.52, 0.45, 0.66, 0.52, face="white", edge=GRID, lw=0.6)
ax_b.text(3.85, 0.80, r"report $u_s$", ha="center", va="center", fontsize=6.2,
          color=INK)
ax_b.text(3.85, 0.59, "not gated", ha="center", va="center", fontsize=5.4,
          color=MUTED)
arrow(ax_b, (3.32, 0.71), (3.52, 0.71), color=MUTED, lw=0.7, ms=6)

# ---- (c) Scalarization vs constraint ----
k_acc, k_hard = 0.739, 0.683
ax_c.set_xlim(0.695, 0.753)
ax_c.set_ylim(0.52, 0.70)
ax_c.set_xticks([0.70, 0.72, 0.74])
ax_c.set_yticks([0.55, 0.60, 0.65, 0.70])
ax_c.set_xlabel("content accuracy", fontsize=6.2, labelpad=1)
ax_c.set_ylabel("hard accuracy", fontsize=6.2, labelpad=1)
ax_c.tick_params(length=2, labelsize=5.6, pad=1)
ax_c.spines["top"].set_visible(False)
ax_c.spines["right"].set_visible(False)

ax_c.add_patch(Rectangle((0.695, 0.52), k_acc - 0.695, k_hard - 0.52,
                         facecolor=NAVY, alpha=0.07, edgecolor="none", zorder=0))
ax_c.plot([0.695, k_acc, k_acc], [k_hard, k_hard, 0.52], color=NAVY,
          lw=0.5, ls=":", zorder=0)

acc = np.array([0.731, 0.736, 0.722, 0.701])
hard = np.array([0.536, 0.589, 0.638, 0.659])
ax_c.plot(acc, hard, color=GRID, lw=0.9, zorder=1)
ax_c.scatter(acc, hard, s=20, c="#8d8d8d", edgecolors=INK, linewidths=0.4, zorder=2)
for a, h, lab, dx, dy, ha, va in [
    (0.731, 0.536, r"$\lambda{=}1$", -0.0015, 0.0, "right", "center"),
    (0.736, 0.589, r"$0.75$", -0.0015, 0.0, "right", "center"),
    (0.722, 0.638, r"$0.50$", 0.0015, -0.004, "left", "top"),
    (0.701, 0.659, r"$0.25$", 0.0012, 0.006, "left", "bottom"),
]:
    ax_c.text(a + dx, h + dy, lab, fontsize=5.4, color=MUTED, ha=ha, va=va)

ax_c.scatter([0.748], [0.560], s=16, facecolors="white", edgecolors=INK,
             linewidths=0.6, marker="s", zorder=2)
ax_c.text(0.748, 0.568, "SFT", fontsize=5.4, color=INK, ha="center", va="bottom")
ax_c.scatter([0.721], [0.649], s=16, facecolors="white", edgecolors=BAD_EDGE,
             linewidths=0.7, marker="D", zorder=2)
ax_c.text(0.7230, 0.6505, "w/o stop-grad", fontsize=5.2, color=BAD_EDGE,
          ha="left", va="bottom")
ax_c.scatter([k_acc], [k_hard], s=60, c=NAVY, marker="*",
             edgecolors=INK, linewidths=0.35, zorder=3)
ax_c.text(k_acc - 0.002, k_hard + 0.004, "constraint", fontsize=5.8,
          color=NAVY, ha="right", va="bottom")

fig.savefig(out / "grid.pdf", bbox_inches="tight", pad_inches=0.02)

# ---------------------------------------------------------------------------
# Figure 2: results
# ---------------------------------------------------------------------------
hard_names = ["Readout", "Scalar RM", "RLCD", "SFT", "SD-RLCD"]
hard = [0.358, 0.412, 0.536, 0.560, 0.683]
hard_se = [0.029, 0.030, 0.031, 0.030, 0.029]

ece_names = ["Readout", "RM", "SFT", "RLCD", "SD-\nRLCD"]
ece = [0.248, 0.221, 0.168, 0.089, 0.096]
ece_md = [0.331, 0.294, 0.226, 0.171, 0.104]

fig, axes = plt.subplots(1, 3, figsize=(7.05, 2.15),
                         gridspec_kw={"width_ratios": [1.15, 1.0, 1.0]})

ax = axes[0]
y = range(len(hard_names))
colors = ["#c4c4c4", "#c4c4c4", "#8d8d8d", "#8d8d8d", NAVY]
hatches = ["", "", "", "", "///"]
bars = ax.barh(list(y), hard, xerr=hard_se, color=colors, height=0.62,
               capsize=2, error_kw={"lw": 0.6, "ecolor": INK}, zorder=2)
for bar, hatch in zip(bars, hatches):
    bar.set_hatch(hatch)
    bar.set_edgecolor(INK)
    bar.set_linewidth(0.4)
ax.axvline(0.5, color=MUTED, ls="--", lw=0.7, zorder=1)
ax.text(0.62, 0.0, "chance", color="#555555", fontsize=7, va="center")
for i, (v, se) in enumerate(zip(hard, hard_se)):
    ax.text(v + se + 0.015, i, f"{v:.2f}", va="center", ha="left",
            fontsize=7, color=INK, zorder=3,
            bbox=dict(boxstyle="square,pad=0.05", fc="white", ec="none"))
ax.set_yticks(list(y), hard_names)
ax.set_xlim(0, 0.92)
ax.set_xlabel("Hard accuracy")
ax.set_title("(a) Style opposed to content", loc="left", fontsize=8)
ax.tick_params(length=2)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax = axes[1]
idx = np.arange(len(ece_names))
w = 0.36
ax.bar(idx - w / 2, ece, w, color="#d0d0d0", edgecolor=INK, linewidth=0.4,
       label="Overall ECE")
ax.bar(idx + w / 2, ece_md, w, color=NAVY, edgecolor=INK, linewidth=0.4,
       label="Markdown ECE", hatch="///")
ax.set_xticks(idx, ece_names)
ax.set_ylabel("ECE")
ax.set_ylim(0, 0.42)
ax.set_title("(b) Where the calibration goes", loc="left", fontsize=8)
ax.tick_params(length=2)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(frameon=False, ncol=1, loc="upper right", fontsize=6.5,
          bbox_to_anchor=(1.0, 1.02), borderaxespad=0)
ax.tick_params(axis="x", labelsize=6.5)

# (c) hard accuracy, single-head RLCD -> constraint, per slice
ax = axes[2]
slices = [
    ("Chat", 0.516, 0.677),
    ("Code", 0.611, 0.759),
    ("Math", 0.466, 0.603),
    ("Safety, refuse", 0.542, 0.708),
    ("Safety, respond", 0.558, 0.674),
    ("0.5B model", 0.501, 0.629),
    ("Held-out length", 0.544, 0.618),
]
ys = np.arange(len(slices))[::-1].astype(float)
ys[-2:] -= 0.45
for yv, (name, before, after) in zip(ys, slices):
    ax.plot([before, after], [yv, yv], color=GRID, lw=1.4, zorder=1,
            solid_capstyle="round")
    ax.scatter([before], [yv], s=16, c="white", edgecolors=INK,
               linewidths=0.6, zorder=2)
    ax.scatter([after], [yv], s=18, c=NAVY, edgecolors=INK,
               linewidths=0.4, zorder=3)
    ax.text(after + 0.012, yv, f"+{after - before:.2f}", va="center",
            ha="left", fontsize=6, color=NAVY)
ax.axhline((ys[4] + ys[5]) / 2, color="#cccccc", lw=0.5)
ax.axvline(0.5, color=MUTED, ls="--", lw=0.7, zorder=0)
ax.set_yticks(ys, [s[0] for s in slices])
ax.tick_params(axis="y", labelsize=6.5)
ax.set_xlim(0.44, 0.83)
ax.set_xlabel("Hard accuracy")
ax.set_title("(c) Gain by slice", loc="left", fontsize=8)
ax.tick_params(length=2)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout(w_pad=1.0)
fig.savefig(out / "results.pdf", bbox_inches="tight", pad_inches=0.03)
print("wrote", out / "grid.pdf")
print("wrote", out / "results.pdf")
