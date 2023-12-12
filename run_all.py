import os, subprocess
import datetime
import sys

all_begin = datetime.datetime.now()


def run(day_path, day_file):
    day_begin = datetime.datetime.now()
    os.chdir(day_path)
    result = subprocess.run(f'python3 {day_file}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if result.returncode:
        print(result.stderr)
    print(f'{day_file.ljust(13)}: {datetime.datetime.now() - day_begin}ms')
    os.chdir('../..')


path = os.walk('2023') if len(sys.argv) == 1 else os.walk(sys.argv[1])
sys.path.append('./aopython')
for root, dirs, files in path:
    for day_dir in sorted(dirs):
        day_paths = os.walk(f'{root}/{day_dir}')
        for r, day_path, day_files in day_paths:
            for day_file in sorted(day_files):
                if day_file.endswith('.py'):
                    # print(f'{day_dir}/{day_file}')
                    run(r, day_file)

print(f'===================================')
print(f'all together : {datetime.datetime.now() - all_begin}ms')
