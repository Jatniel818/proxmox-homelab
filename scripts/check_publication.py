#!/usr/bin/env python3
"""Check repository files for common accidental private-file publication.

This is a small local guard, not a comprehensive secret scanner.
It does not print matched values. Review the Git diff before publishing.
"""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
result = subprocess.run(
    ['git', 'ls-files', '-z'], cwd=ROOT, capture_output=True, check=False
)
paths = [ROOT / p.decode() for p in result.stdout.split(b'\0') if p]
if result.returncode or not paths:
    paths = [p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts]

rules = {
    'private key material': re.compile(r'-----BEGIN (?:OPENSSH |RSA |EC |DSA )?PRIVATE KEY-----'),
    'GitHub token': re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b'),
    'Tailscale auth key': re.compile(r'\btskey-(?:auth|api)-[A-Za-z0-9-]{15,}\b'),
    'temporary sign-in link': re.compile(r'https://login\.tailscale\.com/a/[A-Za-z0-9]+'),
    'live Tailscale IPv4 address': re.compile(r'\b100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.\d{1,3}\.\d{1,3}\b'),
    'personal absolute path': re.compile('/' + r'Users/[^/\s]+/'),
    'filesystem or device UUID': re.compile(r'\b[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}\b'),
}
private_suffixes = ('.img', '.qcow2', '.e2undo', '.sql', '.sql.gz', '.tar.gz', '.tgz', '.pem', '.key', '.docx')
failures = []
for path in paths:
    relative = path.relative_to(ROOT).as_posix()
    if not path.is_file():
        continue
    if path.name.startswith('.env') and path.name != '.env.example':
        failures.append((relative, 'environment file'))
    if relative.endswith(private_suffixes):
        failures.append((relative, 'private artifact type'))
    if path.stat().st_size > 1_000_000:
        failures.append((relative, 'large file requires manual review'))
        continue
    try:
        content = path.read_text()
    except UnicodeDecodeError:
        failures.append((relative, 'binary file requires manual review'))
        continue
    for label, pattern in rules.items():
        if pattern.search(content):
            failures.append((relative, label))
if failures:
    for path, reason in failures:
        print(f'REVIEW {path}: {reason}')
    sys.exit(1)
print(f'Publication check passed for {len(paths)} files. Review the diff before pushing.')
