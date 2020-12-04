# GRADER - BEGIN

# 1. Preuzeti notebook kao .py datoteku i imenovati je main.py
# 2. Postaviti main.py na putanju na koju pokazuje path_root
from debug.main import path_root

if True:
    import os

    path_grader = f'grader.sh'
    os.system(f'chmod +x {path_grader}')  # Dozvola za izvršavanje
    os.system(f'bash {path_grader}')  # Pokretanje gradera

# GRADER - END
