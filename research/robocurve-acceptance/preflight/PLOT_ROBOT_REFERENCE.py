#!/usr/bin/env python3
"""Plot actual pinned collision-hull projections on CPU; no task geometry invented."""
from pathlib import Path
import os
import tempfile
os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir())/'robocurve-preflight-mpl'))
os.environ.setdefault('XDG_CACHE_HOME', str(Path(tempfile.gettempdir())/'robocurve-preflight-cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

from access_core import Robot, points_at


def main():
    r = Robot()
    q = r.data['ready_joint_radians'] + [-.04695, -.04695]
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), layout='constrained')
    for ax, dims, labels in zip(axes, [(0, 1), (0, 2), (1, 2)], [('x / m', 'y / m'), ('x / m', 'z / m'), ('y / m', 'z / m')]):
        for side, colour in [('left', '#2368b5'), ('right', '#e17a20')]:
            poses, _ = r.fk(q, side)
            for h in r.hulls:
                pts = points_at(h['vertices'], poses[h['link']])[:, dims]
                try:
                    outline = pts[ConvexHull(pts).vertices]
                except Exception:
                    continue
                ax.fill(outline[:, 0], outline[:, 1], color=colour, alpha=.13, linewidth=.15, edgecolor=colour)
            tcp = r.tcp(q, side)
            ax.scatter(tcp[dims[0]], tcp[dims[1]], marker='x', s=45, color=colour, label=side+' TCP')
        ax.set_xlabel(labels[0])
        ax.set_ylabel(labels[1])
        ax.set_aspect('equal', adjustable='datalim')
        ax.grid(alpha=.2)
    axes[0].legend()
    fig.suptitle('Pinned YAM collision geometry: 315 hulls/arm, actual READY pose\nProjections only; no door/seal/task geometry and no task clearance pass')
    out = Path(__file__).parent/'results/YAM_COLLISION_REFERENCE.png'
    fig.savefig(out, dpi=140)
    plt.close(fig)
    print(out)


if __name__ == '__main__':
    main()
