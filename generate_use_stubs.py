import sys
import shutil
import subprocess
from pathlib import Path

import pxr

"""
Generate USD Stubs by hubbas
https://gist.github.com/hubbas/ba27e8e9b41a27a6e206f9fb15368a63

"""


def in_virtualenv() -> bool:
    base_prefix_compat = getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix
    return base_prefix_compat != sys.prefix


def main() -> int:
    print('in main')
    # assert in_virtualenv(), "You are not running the script inside a virtual env"
    
    # Install mypy for stubgen
    if subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "mypy"]) != 0:
        print("Failed installing mypy")
        return 1
    
    # Generate stubs for package 'pxr' (from usd-core)
    if subprocess.check_call(["stubgen","-v", "-p", "pxr", "-o", "out"]) != 0:
        print("Failed generating stubs for package 'pxr'. Make sure that you have 'usd-core' installed")
        return 1
    
    # Rename every file that was generated
    # We only care about the files starting with ONE _ (underscore)
    output_path = Path("./out/pxr")
    pyis = list(output_path.rglob("**/*.pyi"))
    filtered = [i for i in pyis if i.stem.startswith("_") and i.stem != "__init__"]
    for p in pyis:
        if p in filtered:
            continue
        p.unlink()
    for f in filtered:
        f.rename(f.parent / "__init__.pyi")

    # Copy generated stubs to where we have the package installed
    pxr_package_dir = Path(pxr.__file__).parent
    shutil.copytree(output_path, pxr_package_dir, dirs_exist_ok=True)
    shutil.rmtree(output_path.parent)

    print(f"Done! Copied stubs to '{pxr_package_dir}'")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
