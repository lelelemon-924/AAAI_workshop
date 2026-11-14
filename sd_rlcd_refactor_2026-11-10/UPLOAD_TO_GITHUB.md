# Apply and push the manuscript refactor

This package does not authenticate to GitHub or push on your behalf. Run these commands from your local clone of `lelelemon-924/AAAI_workshop`.

```bash
# 1) Create a separate branch so the original manuscript remains recoverable.
git switch -c refactor/decision-native-audit

# 2) Back up the current source, then replace it with this package's paper/sd_rlcd.tex.
cp paper/sd_rlcd.tex paper/sd_rlcd.before-refactor.tex
cp /path/to/extracted/package/paper/sd_rlcd.tex paper/sd_rlcd.tex

# 3) Copy the accompanying review/experiment notes into the repository root.
cp /path/to/extracted/package/README.md README.md
cp /path/to/extracted/package/REFACTOR_NOTES.md .
cp /path/to/extracted/package/NEXT_EXPERIMENTS.md .
cp /path/to/extracted/package/UPLOAD_TO_GITHUB.md .

# 4) Compile from the paper directory using the AAAI-27 style files already in the repo.
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error sd_rlcd.tex
cd ..

# 5) Inspect the diff and commit.
git diff --check
git status --short
git add README.md paper/sd_rlcd.tex REFACTOR_NOTES.md NEXT_EXPERIMENTS.md UPLOAD_TO_GITHUB.md
git commit -m "Refactor style robustness manuscript"

# 6) Push the branch to GitHub.
git push -u origin refactor/decision-native-audit
```

After pushing, open a pull request from `refactor/decision-native-audit` into `main`. Do not merge until the required experiment controls and figure updates are complete.

If `latexmk` is unavailable, use the AAAI-recommended LaTeX/BibTeX sequence from inside `paper/`:
```bash
pdflatex sd_rlcd.tex
bibtex sd_rlcd
pdflatex sd_rlcd.tex
pdflatex sd_rlcd.tex
```
