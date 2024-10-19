import sys, os
from datetime import datetime
from multiprocessing import Pool
from subprocess import Popen, DEVNULL, PIPE

def info(*args, file=sys.stdout):
    pref = datetime.now().strftime('[%H:%M:%S]')
    if file != sys.stdout:
        print(pref, *args, file=file, flush=True)
    print(pref, *args, file=sys.stdout, flush=True)

def create_readme(argv, outdir):
    readmepath = os.path.join(outdir, 'README.txt')
    SEP = '##########################################################'
    os.system('echo "{}" >> "{}"'.format(SEP, readmepath))
    if os.path.isdir('.git'):
        os.system('printf "git commit: " >> "{}"'.format(readmepath))
        os.system('git rev-parse  HEAD >> "{}"'.format(readmepath))
    else:
        os.system('echo "Not a git repository"')

    os.system('printf "machine: " >> "{}"'.format(readmepath))
    os.system('hostname >> "{}"'.format(readmepath))

    os.system('echo "python {}" >> "{}" # Call '.format(' '.join(argv), readmepath))
    os.system('printf "Started: " >> {}'.format(readmepath))
    os.system('date +"%Y-%m-%d %H:%M:%S" >> "{}"'.format(readmepath))
    os.system(f'echo "" >> "{readmepath}"')

    return readmepath

def append_to_file(text, file):
    info('{}'.format(text))
    os.system('echo "{}" >> "{}"'.format(text, file))

def parallelize(func, nprocs, argsconcat):
    if nprocs == 1:
        return [ func(*args) for args in argsconcat ]
    else:
        info('Running in parallel ({} procs)'.format(nprocs))
        with Pool(processes=nprocs) as pool:
            return pool.starmap(func, argsconcat)

def run_bash_cmd(cmd, verb=True, sync=True):
    if verb: info(cmd)
    if sync:
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        if verb:
            info('OUTPUT:{}, ERR:{}'.format(
                output.decode('utf-8'), err.decode('utf-8')))
        return output
    else:
        Popen(cmd, shell=True, stdout=DEVNULL, stderr=DEVNULL)
        return '' # Nothing is returned
