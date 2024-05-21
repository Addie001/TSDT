from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/Addie001/TSDT.git'  #(1)

def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'  #(2)(3)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)  #(2)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database','static','virtualenv','source'):
        run (f'mkdir -p {site_folder}/{subfolder}')
#git pull最新原码
def _get_latest_source(source_folder):
    if exists(source_folder+'/.git'):
        run (f'cd {source_folder} && git fetch')
    else :
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit=local("git log -n 1 --format=%H",capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')
#更新配置文件
def _update_settings(source_folder,site_name):
    settings_path=source_folder+'/notes/settings.py'
    sed(settings_path,"DEBUG=True","DEBUG=False")
    sed(settings_path,'ALLOWED_HOST=.+$',
        f'ALLOWED_HOST=["{site_name}"]'
        )
    secret_key_file=source_folder+'/notes/secret_key.py'
    if not exists(secret_key_file):
        chars='abcdefghijklmnopqrstuvwyz0123456789!@#$%^&*(-_=+)'
        key=''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file,f'SECRET_KEY="{key}"')
    append(settings_path,'\nfrom .secret_key import SECRET_KEY')
#创建或更新虚拟环境
def _update_virtualenv(source_folder):
    virtualenv_folder=source_folder+'/../virtualenv'
    if not exists(virtualenv_folder+'/bin/pip'):
        run(f'python3.9 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirement.txt')
#更新静态文件
def _update_static_files(source_folder):
    run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py collectstatic --noinput'
    )
#更新数据库
def _update_database(source_folder):
    run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin//python manage.py migrate --noinput'
    )
if __name__=="__main__":
    local('fab -f /path/fabfile.py deploy')