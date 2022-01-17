import os, subprocess
import datetime
all_begin = datetime.datetime.now()

def run(day_path, day_file):
    day_begin = datetime.datetime.now()
    os.chdir(day_path)
    subprocess.call(f'python {day_file}', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    print(f'{day_file.ljust(13)}: {datetime.datetime.now() - day_begin}ms')
    os.chdir('..')

path = os.walk('.')
for root, dirs, files in path:
    for day_dir in sorted(dirs):
        day_paths = os.walk(day_dir)
        for r, day_path, day_files in day_paths:
            for day_file in sorted(day_files):
                if day_file.endswith('.py'):
                    # print(f'{day_dir}/{day_file}')
                    run(day_dir, day_file)

print(f'===================================')
print(f'all together : {datetime.datetime.now() - all_begin}ms')

