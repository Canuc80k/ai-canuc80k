"""Reviewed figure redesign entry point."""
from pathlib import Path
import subprocess,sys
if __name__=='__main__':
    recipe=Path(__file__).resolve().parents[1]/'figures-recipe/build.py'
    raise SystemExit(subprocess.run([sys.executable,'-B','-X','utf8',str(recipe),'--apply']).returncode)
