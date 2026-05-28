#!/usr/bin/env python3
"""Apply target-only skill group labels for Codex/Claude discoverability.

This intentionally patches copied target SKILL.md files, not the Skillshare source
repo, so upstream/vendor skill updates stay clean. Re-run after `skillshare sync -g`.
"""

from __future__ import annotations

from pathlib import Path

TARGETS = [
    Path.home() / ".codex" / "skills",
    Path.home() / ".claude" / "skills",
]

GROUPS = {
    "Taste Skill": {
        "ui-ux__brandkit_Leonxlnx": "Brand-kit and visual identity guidance from the Taste Skill collection.",
        "ui-ux__industrial-brutalist-ui_Leonxlnx": "Industrial/brutalist interface direction from the Taste Skill collection.",
        "ui-ux__gpt-taste_Leonxlnx": "Awwwards-level UI and motion direction from the Taste Skill collection.",
        "ui-ux__image-to-code_Leonxlnx": "Image-to-frontend implementation from the Taste Skill collection.",
        "ui-ux__imagegen-frontend-mobile_Leonxlnx": "Mobile frontend image-prompting from the Taste Skill collection.",
        "ui-ux__imagegen-frontend-web_Leonxlnx": "Web frontend image-prompting from the Taste Skill collection.",
        "ui-ux__minimalist-ui_Leonxlnx": "Minimalist interface direction from the Taste Skill collection.",
        "meta-tools__full-output-enforcement_Leonxlnx": "Completion/output discipline from the Taste Skill collection.",
        "ui-ux__redesign-existing-projects_Leonxlnx": "Existing-product redesign direction from the Taste Skill collection.",
        "ui-ux__high-end-visual-design_Leonxlnx": "High-end visual design direction from the Taste Skill collection.",
        "ui-ux__stitch-design-taste_Leonxlnx": "Stitch-style design taste direction from the Taste Skill collection.",
        "ui-ux__design-taste-frontend_Leonxlnx": "Frontend design taste direction from the Taste Skill collection.",
        "ui-ux__design-taste-frontend-v1_Leonxlnx": "Earlier frontend design taste direction from the Taste Skill collection.",
    },
    "Impeccable": {
        "ui-ux__impeccable_anthropic": "Production UI design, critique, polish, animation, and frontend craft from the Impeccable skill group.",
    },
}


def frontmatter_bounds(text: str) -> tuple[int, int] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    return 4, end


def replace_description(frontmatter: str, prefix: str, fallback: str) -> str:
    lines = frontmatter.splitlines()
    out: list[str] = []
    i = 0
    changed = False
    while i < len(lines):
        line = lines[i]
        if line.startswith("description:"):
            raw = line.split(":", 1)[1].strip().strip('"')
            continuation: list[str] = []
            i += 1
            while i < len(lines) and (lines[i].startswith(" ") or not lines[i].strip()):
                if lines[i].strip():
                    continuation.append(lines[i].strip())
                i += 1
            if raw in {">", "|", "|-", ">-"} or not raw:
                desc = " ".join(continuation) or fallback
            else:
                desc = " ".join([raw, *continuation]).strip()
            for old in ("[Taste Skill] ", "[Impeccable] "):
                if desc.startswith(old):
                    desc = desc[len(old):]
            out.append(f'description: "[{prefix}] {desc}"')
            changed = True
            continue
        out.append(line)
        i += 1
    if not changed:
        out.append(f'description: "[{prefix}] {fallback}"')
    return "\n".join(out) + "\n"


def ensure_metadata_group(frontmatter: str, group: str) -> str:
    if "skill_group:" in frontmatter:
        return frontmatter
    lines = frontmatter.rstrip("\n").splitlines()
    insert_at = len(lines)
    lines[insert_at:insert_at] = ["skill_group: " + group]
    return "\n".join(lines) + "\n"


def patch_skill(path: Path, group: str, fallback: str) -> bool:
    skill = path / "SKILL.md"
    if not skill.exists():
        return False
    text = skill.read_text()
    bounds = frontmatter_bounds(text)
    if not bounds:
        return False
    start, end = bounds
    frontmatter = text[start:end]
    patched = replace_description(frontmatter, group, fallback)
    patched = ensure_metadata_group(patched, group)
    new_text = text[:start] + patched.rstrip("\n") + text[end:]
    if new_text == text:
        return False
    skill.write_text(new_text)
    return True


def main() -> None:
    changed: list[str] = []
    missing: list[str] = []
    for target in TARGETS:
        for group, skills in GROUPS.items():
            for folder, fallback in skills.items():
                path = target / folder
                if not path.exists():
                    missing.append(str(path))
                    continue
                if patch_skill(path, group, fallback):
                    changed.append(str(path / "SKILL.md"))
    print(f"changed={len(changed)} missing={len(missing)}")
    for path in changed:
        print(f"changed: {path}")
    for path in missing:
        print(f"missing: {path}")


if __name__ == "__main__":
    main()
