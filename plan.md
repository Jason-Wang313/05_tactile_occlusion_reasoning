# Paper 05 Plan: Tactile Occlusion Reasoning

## Mission
Produce a complete, runnable robotics/embodied-intelligence research paper package for `05_tactile_occlusion_reasoning`, ending with:

- a compiled anonymous ICLR-style PDF at `C:/Users/wangz/Downloads/05.pdf`
- required literature and audit documents under `docs/`
- runnable evidence code and cached outputs
- a public GitHub repository named `05_tactile_occlusion_reasoning`, or a documented push failure

## Execution Stages

1. **Resume and Environment Audit**
   - Inspect existing files, git state, available Python/LaTeX/GitHub tools, and any prior artifacts from earlier attempts.
   - Create/update `child_status.md` after each material step.

2. **Literature Landscape**
   - Build or reuse a literature retrieval script that gathers at least 1000 relevant entries across tactile perception, occlusion reasoning, robotic manipulation, haptics, visuo-tactile learning, object shape completion, active touch, and embodied physical reasoning.
   - Save `docs/related_work_matrix.csv`.
   - Create `docs/literature_map.md` summarizing a 1000-paper sweep, 300-paper skim, 200-250-paper deep read, and 100-paper hostile prior-work set.

3. **Novelty Pressure Test**
   - Extract mechanisms, hidden assumptions, fixed variables, ignored failures, novelty threats, and open gaps for important prior papers.
   - Identify at least 20 falseable field assumptions.
   - Generate candidate directions that break assumptions, reject weak moves, and choose the strongest thesis.
   - Save `docs/hostile_prior_work.md`, `docs/novelty_boundary_map.md`, `docs/novelty_decision.md`, `docs/claims.md`, and `docs/reviewer_attacks.md`.

4. **Evidence**
   - Implement a small, runnable robotics-relevant experiment that tests the chosen mechanism from first principles.
   - Prefer a synthetic manipulation/tactile-occlusion setting with cached deterministic outputs, plots, and tables.
   - Save source under `src/` or `experiments/`, outputs under `results/`, and document exact commands.

5. **Paper Writing**
   - Fetch or recreate the latest official ICLR LaTeX style available at runtime.
   - Write a complete anonymous ICLR-style paper with honest claims, related work, method, evidence, limitations, and reproducibility details.
   - Sanitize BibTeX and LaTeX text for pdfLaTeX.

6. **Build and Verify**
   - Compile with direct `pdflatex`, `bibtex`, `pdflatex`, `pdflatex` using generous timeouts.
   - Fix build failures when possible.
   - Copy only the final PDF to `C:/Users/wangz/Downloads/05.pdf`.

7. **Repository Publication**
   - Commit the complete repo.
   - Create/push public GitHub repo `05_tactile_occlusion_reasoning` if credentials/tools allow.
   - Document any failure exactly and keep the local repo runnable.

8. **Final Audit**
   - Write `docs/final_audit.md` answering all required audit questions, including the exact PDF path, GitHub URL or failure, and Desktop-copy status.

## Safety Notes

- Avoid bare probes that can abort on nonzero exit; use PowerShell guards or catch blocks.
- Use explicit long timeouts for experiments and LaTeX builds.
- Reuse useful existing artifacts from earlier attempts.
- Do not delete prior caches unless proven invalid.
