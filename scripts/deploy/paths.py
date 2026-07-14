"""Resolved filesystem paths for the backend repo."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    """Root and well-known directories for the backend repo."""

    project_root: Path
    scripts_dir: Path
    src_dir: Path
    utils_dir: Path
    env_file: Path
    local_cache_root: Path
    local_image_cache_dir: Path
    input_hash_script: Path

    @classmethod
    def from_deploy_package(cls) -> ProjectPaths:
        deploy_dir = Path(__file__).resolve().parent
        scripts_dir = deploy_dir.parent
        project_root = scripts_dir.parent
        return cls(
            project_root=project_root,
            scripts_dir=scripts_dir,
            src_dir=project_root / "src",
            utils_dir=project_root / "utils",
            env_file=project_root / ".env",
            local_cache_root=project_root / ".deploy-cache",
            local_image_cache_dir=project_root / ".deploy-cache" / "images",
            input_hash_script=scripts_dir / "docker_inputs_hash.py",
        )
