# Host setup required on BOTH nodes

The wedge that repeatedly took sparky2 down was **memory fragmentation**, not
memory exhaustion. Full evidence is in the recipe header; this directory holds
the host-side pieces, which need root and so cannot live in the recipe.

Install on **each** node (head and worker):

```bash
sudo cp dsv41-compact.service dsv41-compact.timer dsv41-compact-watch.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now dsv41-compact.timer dsv41-compact-watch.service
```

That gives two triggers:

* **dsv41-compact-watch.service** — waits on `docker events` and compacts 60 s
  after any `sparkrun_*` container starts, i.e. right after the model loads.
* **dsv41-compact.timer** — every 2 min thereafter, as the safety net.

Verify:

```bash
systemctl status dsv41-compact-watch.service
systemctl list-timers dsv41-compact.timer
grep Normal /proc/buddyinfo     # order 8+ columns should not sit at ~0
```

Health metric: in `/proc/buddyinfo`, zone Normal, the columns for order 8 and
above. Near zero means a wedge is coming. Compact by hand with:

```bash
echo 1 | sudo tee /proc/sys/vm/compact_memory
```

Do **not** instead raise `vm.min_free_kbytes` or `vm.watermark_scale_factor`.
Both were tried and are actively harmful here: raising them on a loaded box
livelocks it instantly, and at boot they break startup outright by starving the
GPU memory-utilization check.

Note `CMA 0` in `/proc/pagetypeinfo`: after a load, ~86% of zone Normal's
pageblocks are UNMOVABLE, so compaction only works within the ~14% that remain
movable. A boot-time `cma=` reservation would be the structural fix if the
timer ever proves insufficient — untested, and only helps if the NVIDIA driver
routes these allocations through CMA.
