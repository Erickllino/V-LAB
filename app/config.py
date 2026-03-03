import os
import shutil

ON_VERCEL = bool(os.environ.get('VERCEL'))
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if ON_VERCEL:
    DATA_DIR    = '/tmp/data'
    SAMPLES_DIR = '/tmp/samples'
else:
    DATA_DIR    = os.path.join(PROJECT_ROOT, 'data')
    SAMPLES_DIR = os.path.join(PROJECT_ROOT, 'samples')


def init_storage():
    """
    Garante que os diretórios de dados existem.
    No Vercel, o filesystem é read-only fora de /tmp/, então copia
    os arquivos commitados para /tmp/ na primeira execução.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(SAMPLES_DIR, exist_ok=True)

    if ON_VERCEL:
        src = os.path.join(PROJECT_ROOT, 'data', 'student_profiles.json')
        dst = os.path.join(DATA_DIR, 'student_profiles.json')
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
