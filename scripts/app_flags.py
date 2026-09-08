"""Validated, build-time feature flags shared by every site generator.

The values live in ``config/app-flags.json`` because an emergency switch should be a one-character
reviewable diff, not an edit inside a template. Metadata lives here so the local Flags app and the
generators cannot disagree about a flag's name, meaning or group.

Only integer 0 and 1 are accepted. Python's ``bool`` is a subclass of ``int``, so the explicit type
check is important: JSON ``true`` may look equivalent in code, but it defeats the control panel's
one visual vocabulary and makes reviews needlessly ambiguous.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATH = ROOT / "config" / "app-flags.json"
SCHEMA_PATH = ROOT / "config" / "app-flags.schema.json"
ENV_NAME = "AAA_APP_FLAGS"


@dataclass(frozen=True)
class FlagSpec:
    key: str
    group: str
    name: str
    description: str
    off_effect: str


class FlagError(ValueError):
    """A configuration that is unsafe to render or overwrite."""


def load_specs(path: Path | str = SCHEMA_PATH) -> tuple[FlagSpec, ...]:
    source = Path(path)
    try:
        document = json.loads(source.read_text(encoding="utf-8"))
    except OSError as exc:
        raise FlagError(f"cannot read {source}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise FlagError(f"invalid JSON in {source} at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc
    if type(document) is not dict or document.get("schema_version") != 1:
        raise FlagError(f"{source} must be an application-flag schema with schema_version 1")
    app = document.get("application")
    if type(app) is not dict or not all(type(app.get(k)) is str and app[k].strip()
                                        for k in ("id", "name", "description")):
        raise FlagError(f"{source} has invalid application metadata")
    raw_specs = document.get("flags")
    if type(raw_specs) is not list or not raw_specs:
        raise FlagError(f"{source} must contain a non-empty flags array")
    fields = ("key", "group", "name", "description", "off_effect")
    specs = []
    for number, item in enumerate(raw_specs, 1):
        if type(item) is not dict or set(item) != set(fields):
            raise FlagError(f"flag {number} in {source} must contain exactly: {', '.join(fields)}")
        if not all(type(item[field]) is str and item[field].strip() for field in fields):
            raise FlagError(f"flag {number} in {source} has an empty or non-text field")
        specs.append(FlagSpec(**{field: item[field] for field in fields}))
    keys = [spec.key for spec in specs]
    if len(keys) != len(set(keys)):
        raise FlagError(f"{source} contains duplicate flag keys")
    return tuple(specs)


try:
    SPECS = load_specs()
except FlagError as exc:
    raise SystemExit(f"Application flag schema is invalid: {exc}") from exc

BY_KEY = {spec.key: spec for spec in SPECS}


def active_path() -> Path:
    """Return the build input, allowing a disposable candidate file for local previews."""
    override = os.environ.get(ENV_NAME, "").strip()
    return Path(override).expanduser().resolve() if override else DEFAULT_PATH


def validate(values: object) -> dict[str, int]:
    if type(values) is not dict:
        raise FlagError("the top level must be a JSON object")
    keys = set(values)
    expected = set(BY_KEY)
    missing = sorted(expected - keys)
    unknown = sorted(keys - expected)
    if missing:
        raise FlagError("missing flag" + ("s" if len(missing) != 1 else "") + ": " + ", ".join(missing))
    if unknown:
        raise FlagError("unknown flag" + ("s" if len(unknown) != 1 else "") + ": " + ", ".join(unknown))
    invalid = [key for key in BY_KEY if type(values[key]) is not int or values[key] not in (0, 1)]
    if invalid:
        details = ", ".join(f"{key}={values[key]!r}" for key in invalid)
        raise FlagError("every value must be the integer 1 (ON) or 0 (OFF / DISABLED); invalid: " + details)
    # Schema order makes the file and every payload stable even if an editor reordered the input.
    return {key: values[key] for key in BY_KEY}


def load(path: Path | str | None = None) -> dict[str, int]:
    source = Path(path) if path is not None else active_path()
    try:
        raw = source.read_text(encoding="utf-8")
    except OSError as exc:
        raise FlagError(f"cannot read {source}: {exc}") from exc
    try:
        return validate(json.loads(raw))
    except json.JSONDecodeError as exc:
        raise FlagError(f"invalid JSON in {source} at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc


def serialise(values: object) -> str:
    valid = validate(values)
    return json.dumps(valid, indent=2, ensure_ascii=False) + "\n"


def revision(path: Path | str = DEFAULT_PATH) -> str:
    source = Path(path)
    try:
        return hashlib.sha256(source.read_bytes()).hexdigest()
    except OSError as exc:
        raise FlagError(f"cannot read {source}: {exc}") from exc


def write(values: object, expected_revision: str, path: Path | str = DEFAULT_PATH) -> str:
    """Atomically replace *path*, refusing to overwrite a newer editor's changes."""
    destination = Path(path)
    current = revision(destination)
    if not expected_revision or expected_revision != current:
        raise FlagError("the flags changed after this screen loaded; reload before saving so newer changes are not lost")
    payload = serialise(values)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="\n", delete=False,
                                         dir=destination.parent,
                                         prefix=destination.name + ".", suffix=".tmp") as handle:
            temporary = Path(handle.name)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
    except OSError as exc:
        raise FlagError(f"cannot write {destination}: {exc}") from exc
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    return revision(destination)


def browser_json(values: dict[str, int] | None = None) -> str:
    """A safe script literal: keys are fixed ASCII and values are validated integers."""
    return json.dumps(validate(FLAGS if values is None else values), separators=(",", ":"))


try:
    FLAGS = load()
except FlagError as exc:
    raise SystemExit(f"Application flags are invalid: {exc}") from exc
