import subprocess
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
pipeline_script = os.path.join(script_dir, '2_keyword_llm_pipeline.py')

print("-" * 70)
result = subprocess.run([sys.executable, pipeline_script], cwd=script_dir)
if result.returncode != 0:
    print("\nERROR")
    sys.exit(1)