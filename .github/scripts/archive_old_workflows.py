from pathlib import Path
import shutil

workflow_dir = Path('.github/workflows')
archive_dir = Path('.github/workflows-disabled')
archive_dir.mkdir(parents=True, exist_ok=True)

keep = {'cleanup-old-workflows.yml'}
moved = []
for path in sorted(workflow_dir.glob('*.yml')):
    if path.name in keep:
        continue
    dest = archive_dir / path.name
    if dest.exists():
        dest.unlink()
    shutil.move(str(path), str(dest))
    moved.append(path.name)

for path in sorted(workflow_dir.glob('*.yaml')):
    if path.name in keep:
        continue
    dest = archive_dir / path.name
    if dest.exists():
        dest.unlink()
    shutil.move(str(path), str(dest))
    moved.append(path.name)

print(f'Archived {len(moved)} old workflows')
