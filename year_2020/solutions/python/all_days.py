import os
import subprocess

from year_2020.solutions.python.utils.files import PYTHON_SOLUTIONS_DIRECTORY

if __name__ == '__main__':
    for day_file in sorted([f for f in os.listdir(PYTHON_SOLUTIONS_DIRECTORY)
                              if f.startswith('day_') and f.endswith('.py')]):
        day_module = day_file.split('.')[0]
        day_number: int = int(day_module.split('_')[1])
        print(f"\n******* Day {day_number} *******\n")
        subprocess.run(['python', '-m', f'year_2020.solutions.python.{day_module}'])
