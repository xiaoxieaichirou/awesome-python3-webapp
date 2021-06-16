import os, re
from datetime import datetime

from fabric.api import *

# 服务器登陆用户名:
env.user = 'root'
# sudo用户为root:
env.sudo_user = 'root'
# 服务器地址，可以有多个，依次部署:
env.hosts = ['8.129.132.234']

# 服务器mysql用户和口令
db_user = 'root'
db_password = 'admin123'

_TAR_FILE = 'dist-awesome.tar.gz'

def build():
    includes = ['static', 'templates', 'transwarp', 'favicon.ico', '*.py']
    excludes = ['test', '.*', '*.pyc', '*.pyo']
    local(f'rm -f dist/{_TAR_FILE}')
    with lcd(os.path.join(os.path.abspath('.'), 'www')):
        cmd = ['tar', '--dereference', '-czvf', f'../dist/{_TAR_FILE}']
        cmd.extend([f'--exclude=\'{ex for ex in excludes}\''])
        cmd.extend(includes)
        local(' '.join(cmd))


_REMOTE_TMP_TAR = f'/tmp/{_TAR_FILE}'
_REMOTE_BASE_DIR = '/srv/awesome'

def deploy():
    newdir = f"www-{datetime.now().strftime('%y-%m-%d_%H.%M.%S')}"
    # 删除已有的tar文件:
    run(f'rm -f {_REMOTE_TMP_TAR}')
    #sudo(f'rm -f {_REMOTE_TMP_TAR}')
    # 上传新的tar文件:
    put('dist/%s' % _TAR_FILE, _REMOTE_TMP_TAR)
    # 创建新目录:
    with cd(_REMOTE_BASE_DIR):
        sudo(f'mkdir {newdir}')
    # 解压到新目录:
    with cd(f'{_REMOTE_BASE_DIR}/{newdir}'):
        sudo(f'tar -xzvf {_REMOTE_TMP_TAR}')
    # 重置软链接:
    with cd(_REMOTE_BASE_DIR):
        sudo('rm -f www')
        sudo(f'ln -s {newdir} www')
        sudo('chown www-data:www-data www')
        sudo(f'chown -R www-data:www-data {newdir}')
    # 重启python服务和nginx服务器:
    with settings(warn_only=True):
        sudo('supervisorctl stop awesome')
        sudo('supervisorctl start awesome')
        sudo('/etc/init.d/nginx reload')