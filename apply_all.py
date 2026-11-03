import subprocess, sys, os, glob
os.chdir(os.path.dirname(os.path.abspath(__file__)))
steps = []
if os.path.exists('add_format.py'):
    steps.append('add_format.py')
steps += sorted(glob.glob('site_patches/*.py'))
bad = 0
for f in steps:
    r = subprocess.run([sys.executable, f], capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip()
    print('[' + f + ']', out)
    if r.returncode != 0 or 'nahi mili' in out.lower():
        bad += 1
print('KUL', len(steps), 'step, gadbad:', bad)
