# Paper05 VLA Highlight Hardening Plan

Date: 2026-06-21

## Objective

Make `C:/Users/wangz/Downloads/05.pdf` explicitly match the visible VLA-v4
role model's boxed-link behavior while preserving the final 27-page tactile
occlusion reasoning paper:

- citation links use green one-point boxes;
- internal figure/table/equation/section links use red one-point boxes;
- URL links use green one-point boxes;
- cyan link boxes are removed;
- the final PDF is rebuilt, copied to Downloads, visually checked, and leaves
  no local `paper/main.pdf`.

## Plan-Start Evidence

Baseline artifact:

- Canonical PDF: `C:/Users/wangz/Downloads/05.pdf`
- Pages: 27
- Size: 1,040,865 bytes
- SHA256: `357BC6C52A272A578FD2452A8DCF0D27408185BA40F4728BACC00C6BBA57DAF6`
- Local `paper/main.pdf`: absent
- Repository branch: `master`

Baseline link inventory from the current Downloads PDF:

- Link pages: `[(1, 15), (2, 35), (3, 8), (4, 4), (6, 2), (7, 2), (10, 6), (11, 9), (12, 9), (13, 6)]`
- Annotation colors: green = 57, red = 9, cyan = 30
- Border widths: `(0, 0, 1)` for all link annotations

Source finding:

- `paper/main.tex` is the active manuscript source.
- The active manuscript already loads `hyperref`, but it has no explicit
  `\hypersetup` policy, so the baseline PDF contains cyan boxes that do not
  match the VLA-v4 role model.
- The target is to add the VLA role-model border policy immediately after the
  existing `\usepackage{hyperref}` line so citation/URL links remain green and
  internal links become red instead of cyan.
- Use the documented manual LaTeX flow from `paper/`: `pdflatex`, `bibtex`,
  and repeated `pdflatex` passes before export.

## Role-Model Target

Install the same explicit hyperref policy as the visible VLA-v4 role model:

```tex
\hypersetup{
  colorlinks=false,
  pdfborder={0 0 1},
  citebordercolor={0 1 0},
  linkbordercolor={1 0 0},
  urlbordercolor={0 1 0}
}
```

## Execution Plan

1. Add the VLA `\hypersetup` block in the active `paper/main.tex` preamble
   immediately after the existing `\usepackage{hyperref}`.
2. Rebuild manually from `paper/` with `pdflatex`, `bibtex`, and repeated
   `pdflatex` passes.
3. If the log asks for another pass for cross-references, run the final
   canonical pass before recording metadata.
4. Copy the rebuilt `paper/main.pdf` to `C:/Users/wangz/Downloads/05.pdf`.
5. Remove local `paper/main.pdf` after export.
6. Recompute page count, byte size, SHA256, annotation colors, border widths,
   and link pages from the final Downloads PDF.
7. Render every page that contains final link annotations into
   `tmp/pdfs/paper05_after`.
8. Visually inspect rendered affected pages:
   - green citation and URL boxes are crisp and aligned;
   - red internal-reference boxes are crisp and aligned;
   - no cyan boxes remain;
   - layout, figures, tables, headers, and page count remain stable.
9. Update README/status/audit/version/validation metadata with the new hash and
   VLA-style boxed-link inventory.
10. Validate build logs, diff hygiene, final PDF hash, expected claim markers,
    and absence of local `paper/main.pdf`.
11. Remove Paper05 temp renders, leaving only the shared role-model render
    directory.
12. Stage only Paper05 source and metadata files, commit, push, and verify a
    clean repository before moving to Paper04.

## Non-Goals

- Do not alter experiment results, claims, figures, tables, bibliography
  content, or page count.
- Do not add or remove citations, references, URLs, or template examples merely
  to change link counts.
- Do not create an additional `5.pdf`; keep the repository's canonical
  Downloads target as `05.pdf`.
- Do not leave intermediate PDFs or render folders behind.

## Completion Evidence

- Added the explicit VLA `\hypersetup` block immediately after the existing
  `\usepackage{hyperref}` in active `paper/main.tex`.
- Rebuilt from `paper/` with `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`.
- Exported canonical PDF: `C:/Users/wangz/Downloads/05.pdf`
- Pages: 27
- Size: 1,040,865 bytes
- SHA256: `BF717DB37975A5CC91C024F8936DCFE78C55C32DC6605D07BFDCBE9E6D0E570E`
- Link inventory: 96 annotations on pages `[(1, 15), (2, 35), (3, 8), (4, 4), (6, 2), (7, 2), (10, 6), (11, 9), (12, 9), (13, 6)]`; green = 87, red = 9, cyan = 0; all borders `(0, 0, 1)`.
- Visual audit: rendered pages 1, 2, 3, 4, 6, 7, 10, 11, 12, and 13; green citation/URL boxes and red internal-reference boxes are crisp and aligned.
- Local `paper/main.pdf`: removed after export.
- Duplicate `C:/Users/wangz/Downloads/5.pdf`: not created.
