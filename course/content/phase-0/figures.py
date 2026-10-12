"""Chapter 0 figures — reviewed redesign source."""
from pathlib import Path
import subprocess,sys
recipe=Path(__file__).resolve().parents[2]/'figures-recipe/build.py'
if __name__=='__main__':
    raise SystemExit(subprocess.run([sys.executable,'-B','-X','utf8',str(recipe),'--apply','--phase','0']).returncode)
