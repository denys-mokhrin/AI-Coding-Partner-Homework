"""
Coverage gate script — blocks push if coverage is below 80%.
Run by the pre-push hook via Claude Code settings.
"""

import subprocess
import sys

MIN_COVERAGE = 80

result = subprocess.run(
    [
        sys.executable, "-m", "pytest", "tests/",
        "--cov=agents", "--cov=integrator",
        "--cov-report=term-missing",
        f"--cov-fail-under={MIN_COVERAGE}",
        "-q",
    ],
    capture_output=True,
    text=True,
)

print(result.stdout)
if result.stderr:
    print(result.stderr, file=sys.stderr)

if result.returncode != 0:
    print(f"\n❌ PUSH BLOCKED: Coverage is below {MIN_COVERAGE}%. Fix tests before pushing.")
    sys.exit(1)

print(f"\n✅ Coverage gate passed (≥{MIN_COVERAGE}%). Push allowed.")
sys.exit(0)
