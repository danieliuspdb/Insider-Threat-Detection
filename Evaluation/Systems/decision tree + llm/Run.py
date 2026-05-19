import subprocess
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

result = subprocess.run([sys.executable, 'combined_detector.py'], cwd=script_dir)

if result.returncode == 0:
    print("\n" + "="*70)
    print("="*70)
else:
    print("\n" + "="*70)
    print("ERROR")
    print("="*70)
    sys.exit(1)
