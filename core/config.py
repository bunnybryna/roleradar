from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any
import yaml


@dataclass(frozen=True)
class ProfileConfig:
    name: str
    db_path: str
    enabled_companies: List[str]


def load_profile(profile_name: str) -> ProfileConfig:
    path = Path("profiles") / f"{profile_name}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Missing profile file: {path}")

    data: Dict[str, Any] = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return ProfileConfig(
        name=profile_name,
        db_path=str(data.get("db_path", f"data/{profile_name}.sqlite")),
        enabled_companies=list(data.get("enabled_companies", [])),
    )
