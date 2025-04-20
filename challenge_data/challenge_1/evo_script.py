import io
import os
import tempfile
from pathlib import Path
from typing import Dict, IO, Optional, Union, List
import numpy as np
import pandas as pd
import yaml
import csv
from evo.core import sync
from evo.core.trajectory import PoseTrajectory3D
from evo.core.trajectory import Plane
from evo.core.metrics import PoseRelation, Unit
from evo.tools import file_interface
import evo.main_ape as main_ape
import evo.main_rpe as main_rpe
class FileInterfaceException(Exception):
    pass

PathStrHandle = Union[str, Path, IO]

def read_tum_trajectory_matrix(
    source: PathStrHandle,
    delim: str = " ",
    comment_str: str = "#",
) -> np.ndarray:
    """
    Read a TUM‑style trajectory (.tum) into an N×8 float array:
      [timestamp, x, y, z, qx, qy, qz, qw]
    """
    raw_mat = csv_read_matrix(source, delim=delim, comment_str=comment_str)
    # every row must have exactly 8 fields
    if any(len(row) != 8 for row in raw_mat):
        raise FileInterfaceException(
            "TUM trajectory files must have 8 entries per row (no trailing delimiters)."
        )
    error_msg = ("TUM trajectory files must have 8 entries per row "
                "and no trailing delimiter at the end of the rows (space)")

    try:
        mat = np.array(raw_mat).astype(float)
    except ValueError:
        raise FileInterfaceException(error_msg)
    stamps = mat[:, 0]  # n x 1
    xyz = mat[:, 1:4]  # n x 3
    quat = mat[:, 4:]  # n x 4
    quat = np.roll(quat, 1, axis=1)  # shift 1 column -> w in front column
    return PoseTrajectory3D(xyz, quat, stamps)


def has_utf8_bom(path: Union[str, Path]) -> bool:
    """Return True if file starts with UTF‑8 BOM (0xEF,0xBB,0xBF)."""
    with open(path, "rb") as f:
        return f.read(3) == b"\xef\xbb\xbf"

# -----------------------------------------------------------------------------
# CSV → 2D list of strings
# -----------------------------------------------------------------------------
def csv_read_matrix(
    file_path: PathStrHandle,
    delim: str = ",",
    comment_str: str = "#",
) -> List[List[str]]:
    """
    Read a CSV‑like file (or handle) into a 2D list of raw strings,
    skipping any lines beginning with `comment_str`.
    """
    # file‑like case
    if isinstance(file_path, io.IOBase):
        gen = (line for line in file_path if not line.startswith(comment_str))
        return [row for row in csv.reader(gen, delimiter=delim)]

    # path case
    p = Path(file_path)
    if not p.is_file():
        raise FileInterfaceException(f"File does not exist: {p}")
    skip_bom = has_utf8_bom(p)
    with open(p, "r", encoding="utf-8") as f:
        if skip_bom:
            f.seek(3)
        gen = (line for line in f if not line.startswith(comment_str))
        return [row for row in csv.reader(gen, delimiter=delim)]


__all__ = ["TrajectoryEvaluator"]

# ---------------------------------------------------------------------------
# Defaults – feel free to override via *config*
# ---------------------------------------------------------------------------
DEFAULTS: Dict[str, object] = {
    "t_max_diff": 0.02,
    "t_offset": 0.0,
    "n_to_align": -1,
    "delta": 1,
    "unit": "m",  # "m" | "frame"
    "correct_scale": False,
    "project_to_plane": "xyz",  # "xyz" | "xy"
    # Filtering
    "enable_covariance_based_removal": False,
    "covariance_percentile_threshold": 95,
    "enable_no_motion_removal": False,
    "distance_threshold": 10.0,
    "ap20_peak_rejection": False,
    "ap20_peak_rejection_threshold": 0.1,
    "ap20_peak_rejection_trailing_window": 5,
}

# ---------------------------------------------------------------------------
# Main class
# ---------------------------------------------------------------------------


class TrajectoryEvaluator:
    """Tiny wrapper around *evo* that hides all boilerplate.

    Parameters
    ----------
    reference, estimated : str | IO | None, optional
        Paths to ``.tum`` files **or** already opened file‑like objects.  Can be
        left *None* and supplied later to :py:meth:`evaluate`.
    config : dict | str | None, optional
        Dict or path to a YAML/JSON config file.  Missing keys fall back to
        sane :pydata:`DEFAULTS`.

    Example
    -------
    >>> ev = TrajectoryEvaluator("ref.tum", "est.tum", {"delta": 5})
    >>> metrics = ev.evaluate()      # {"ATE": ..., "RTE": ..., "last_error": ...}
    """

    # .....................................................................
    # Construction helpers
    # .....................................................................

    def __init__(
        self,
        reference: Optional[Union[str, IO]] = None,
        estimated: Optional[Union[str, IO]] = None,
        config: Optional[Union[str, Dict]] = None,
    ) -> None:
        self._reference_source = reference
        self._estimated_source = estimated
        self.config: Dict[str, object] = DEFAULTS.copy()
        if config is not None:
            self.update_config(config)

    # ..................................................................
    # Public helpers
    # ..................................................................

    def update_config(self, cfg: Union[str, Dict]) -> None:
        """Merge *cfg* into the current configuration."""
        if isinstance(cfg, str):
            with open(cfg, "r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f)
        if not isinstance(cfg, dict):
            raise TypeError("config must be dict or path to YAML/JSON file")
        self.config.update(cfg)

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # Internal implementation
    # ------------------------------------------------------------------

    # -- compute --------------------------------------------------------

    def evaluate(self, traj_ref: str, traj_est: str) -> Dict[str, float]:
        cfg = self.config
        delta_unit_enum = Unit.meters if cfg["unit"] == "m" else Unit.frames
        if cfg["unit"] not in ("m", "frame"):
            raise ValueError("config['unit'] must be 'm' or 'frame'")

        plane_param = None if cfg["project_to_plane"] == "xyz" else Plane.XY

        self._apply_filters(traj_ref, traj_est)

        traj_ref, traj_est = sync.associate_trajectories(
            traj_ref, traj_est, cfg["t_max_diff"], cfg["t_offset"]
        )

        ape = main_ape.ape(
            traj_ref,
            traj_est,
            est_name="estimated",
            ref_name="RTS",
            pose_relation=PoseRelation.point_distance,
            align=True,
            align_origin=False,
            n_to_align=cfg["n_to_align"],
            correct_scale=cfg["correct_scale"],
            project_to_plane=plane_param,
        )

        rpe = main_rpe.rpe(
            traj_ref,
            traj_est,
            est_name="estimated",
            ref_name="RTS",
            pose_relation=PoseRelation.point_distance,
            delta=cfg["delta"],
            delta_unit=delta_unit_enum,
            all_pairs=False,
            align=True,
            correct_scale=cfg["correct_scale"],
            n_to_align=cfg["n_to_align"],
            project_to_plane=plane_param,
            support_loop=False,
        )

        return {
            "ATE": float(ape.stats["rmse"]),
            "RTE": float(rpe.stats["rmse"]),
            "LE": float(ape.np_arrays["error_array"][-1]),
        }

    # -- filters --------------------------------------------------------

    def _apply_filters(self, traj_ref, traj_est: str):
        cfg = self.config
        if cfg["enable_no_motion_removal"]:
            self._filter_no_motion(traj_est, cfg["distance_threshold"])
        if cfg["ap20_peak_rejection"]:
            self._filter_ap20(
                traj_ref,
                cfg["ap20_peak_rejection_threshold"],
                cfg["ap20_peak_rejection_trailing_window"],
            )

    @staticmethod
    def _filter_no_motion(traj_est, threshold: float):
        d = np.linalg.norm(traj_est.positions_xyz - traj_est.positions_xyz[0], axis=1)
        traj_est.reduce_to_ids(np.where(d > threshold)[0])

    @staticmethod
    def _filter_ap20(traj_ref, thresh: float, trailing: int):
        t_diff = np.diff(traj_ref.timestamps)
        idx_remove = np.where(t_diff > thresh)[0]
        extended = set(idx_remove)
        for i in idx_remove:
            extended.update(range(max(0, i - trailing), i + trailing))
        traj_ref.reduce_to_ids(np.setdiff1d(np.arange(len(traj_ref.positions_xyz)), list(extended)))