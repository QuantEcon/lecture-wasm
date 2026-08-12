---
title: "PROBE — which code cells actually execute?"
---

# Probe: which code cells actually execute under thebe-lite?

Temporary diagnostic page. **Not for merge.** Run the cells top to bottom, then run
the final REPORT cell — it names every cell that actually executed, so a cell that
silently did nothing is visible rather than ambiguous.

## Setup (top level — control, must work)

```{code-cell} ipython3
ran = []
ran.append("A_toplevel_setup")
print("A ok")
```

## B — top level, `%%file` magic (tests the magic independently of nesting)

```{code-cell} ipython3
%%file probe_b.txt
hello-from-B
```

```{code-cell} ipython3
import os
ran.append("C_toplevel_after_magic")
print("C: probe_b.txt exists?", os.path.exists("probe_b.txt"))
if os.path.exists("probe_b.txt"):
    print("C: contents =", open("probe_b.txt").read().strip())
```

## D — inside a GATED exercise

```{exercise-start}
:label: probe_ex
```
Prose inside the gated exercise.

```{code-cell} ipython3
ran.append("D_in_gated_exercise")
print("D ok")
```
```{exercise-end}
```

## E — inside a GATED solution

```{solution-start} probe_ex
:class: dropdown
```
```{code-cell} ipython3
ran.append("E_in_gated_solution")
print("E ok")
```
```{solution-end}
```

## F — inside a plain admonition

````{note}
```{code-cell} ipython3
ran.append("F_in_note")
print("F ok")
```
````

## REPORT (top level)

```{code-cell} ipython3
expected = ["A_toplevel_setup", "C_toplevel_after_magic",
            "D_in_gated_exercise", "E_in_gated_solution", "F_in_note"]
print("EXECUTED:", ran)
print("MISSING :", [e for e in expected if e not in ran])
import os
print("%%file worked at top level:", os.path.exists("probe_b.txt"))
```
