# Offline development checkpoint

**Eight engineering drafts are pushed and source-verified. Zero tasks are ready.**

The user deferred SSH and requested continued offline work. Saved SSH keys were not changed.
No native physics, full-score demonstration, Dream evaluation, media recording or upload occurred.

This branch contains development coordination only. Each task branch independently adds one folder
to upstream `7df8bd8ad8cb19df51718e5ff46d4d610a9da6f1`. Read `draft-manifest.json` for
the exact commit hashes, test counts, status and known gaps. `remote-verification.json` records the
clean-checkout audit. The 245 passing tests use synthetic states; the 35 skipped tests concern
mechanisms absent from the relevant task. USD parsing and source loading did not run a simulator.

## Draft branches

- [eight-nut-bracket](https://github.com/aryansennthilkumarGT/benchmark-tasks/tree/draft/eight-nut-bracket) — `6d630d99b4c30d3b95a8f266177554a6baa2f676`
- [fault-module-repair](https://github.com/aryansennthilkumarGT/benchmark-tasks/tree/draft/fault-module-repair) — `f10b74cf3c28bcee3094711baa0d78cd542b8376`
- [hardware-order-kit](https://github.com/aryansennthilkumarGT/benchmark-tasks/tree/draft/hardware-order-kit) — `2f6cc1a8b699e43150627c9a24bbc52f03711848`
- [hinged-chassis-drive](https://github.com/aryansennthilkumarGT/benchmark-tasks/tree/draft/hinged-chassis-drive) — `85036aa7e52e14665bb4a088038feb33cdebc69a`
- [node-service-closeout](https://github.com/aryansennthilkumarGT/benchmark-tasks/tree/draft/node-service-closeout) — `64e92f3f1f8c4a4b84483abcf0df45631935bf9a`
- [remote-battery-service](https://github.com/aryansennthilkumarGT/benchmark-tasks/tree/draft/remote-battery-service) — `64a4e23386b1d3bdffb72716d3ee6efd1f53506c`
- [switch-map-rework](https://github.com/aryansennthilkumarGT/benchmark-tasks/tree/draft/switch-map-rework) — `32b345fbcf3207ab5a379c53f0635ca5ed1e50c0`
- [twelve-cell-pack](https://github.com/aryansennthilkumarGT/benchmark-tasks/tree/draft/twelve-cell-pack) — `15a17647c5aa12986b2325e8faa2ec6ee58366c0`

## What remains

The candidates are not novelty-cleared. Generic kitting and visible-fault replacement overlap strongly
with pending tasks; more batteries or fasteners alone does not establish a distinct task. Other workflows
also have close neighbors. `novelty-search-update.json` records 294 distinct PR matches and eight
receipt/comment checks. Catalog overview checks are not exhaustive mechanism-level review.

These packages are incomplete prototypes, not polished tasks awaiting only GPU time. Flexible cables,
retaining captures, distinct module interfaces, some visual cues and task-specific expert controllers
remain unfinished. Each README and `validation.json` states its gaps. The native adapter was inspected
against a pinned source revision but has not been executed under Isaac Sim. Complete these issues and
validate native mechanics before spending model credits. The launcher rejects Dream execution until
physics and two full-score expert trials are recorded as verified.

After safe workstation verification, begin with the official station smoke test. Then validate one task
end to end before scaling: reset, reach, contacts, adversarial strategies, two expert trials, real Dream,
media inspection/upload and final exact-commit audit. Keep raw run artifacts and credentials outside Git.

## Read-only readiness check

```sh
python coordination/verify_readiness.py
python -m unittest discover -s coordination -p test_readiness.py -v
```

The first command intentionally exits 2 and explains missing evidence. It never opens PRs. The teammate
must not submit these draft revisions. The final PR titles, bodies and submission script remain pending
until the eight tasks genuinely pass all gates. The agent must not open official upstream PRs.

`development/` preserves the original offline package generator and templates. It is an engineering
snapshot, not the source of later branch edits. Running it regenerates draft files and resets their
validation metadata; do not run it over edited packages. Actual task branches are independently complete
as source snapshots and do not import anything from this coordination branch.
