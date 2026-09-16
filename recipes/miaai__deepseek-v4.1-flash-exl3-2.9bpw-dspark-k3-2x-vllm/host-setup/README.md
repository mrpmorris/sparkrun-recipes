# Host setup required on BOTH nodes

The wedge that repeatedly took sparky2 down was **memory fragmentation**, not
memory exhaustion. Full evidence is in the recipe header; this directory holds
the host-side pieces, which need root and so cannot live in the recipe.

Install on **each** node (head and worker):

```bash
sudo cp dsv41-compact.service dsv41-compact.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now dsv41-compact.timer
```

Verify:

```bash
systemctl list-timers dsv41-compact.timer
grep Normal /proc/buddyinfo    # order 8+ columns should not sit at ~0
```

Compact by hand (e.g. straight after a model load):

```bash
echo 1 | sudo tee /proc/sys/vm/compact_memory
```

Do **not** instead raise `vm.min_free_kbytes` or `vm.watermark_scale_factor`.
Both were tried and are actively harmful here: raising them on a loaded box
livelocks it instantly, and at boot they break startup outright by starving the
GPU memory-utilization check.
