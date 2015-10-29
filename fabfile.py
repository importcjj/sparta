# -*- coding:utf-8 -*-

from fabric.api import (
	execute,
	local,
	hosts,
	task,
	sudo,
	env,
	run,
	cd
)
from fabric.contrib.files import exists
import os

env.use_ssh_config = True

HOSTS = ['aliyun']
REMOTE_DIR = '/data/v2.sparta'
LOCAL_DIR = os.path.dirname(os.path.realpath(__file__))
FAB_PARAM = {
	'local_dir': LOCAL_DIR,
	'remote_dir':REMOTE_DIR,
	'virtualenv':'{}/env'.format(REMOTE_DIR),
	'requirements':'{}/requirements.txt'.format(REMOTE_DIR),
	'rsync_exclude':'{}/rsync_exclude.txt'.format(LOCAL_DIR),
	'services': ['sparta']
}

PYPI_ADDRESS = 'http://pypi.douban.com/simple'

def async_files(local_dir, remote_dir, rsync_exclude):
	sudo('mkdir -p {}'.format(remote_dir))
	sudo('chown {} -R {}'.format(env.user, remote_dir))
	local('rsync -azq --progress --force --delete --delay-updates'
		  ' --exclude-from={1} {3}/ {0}:{2}/'.format(
		  	env.host_string,
		  	rsync_exclude,
		  	remote_dir,
		  	local_dir))

def init_venv(virtualenv):
	# init env with virtualenv
	sudo('virtualenv {}'.format(virtualenv))
	# install and update pip and distribute
	sudo('{}/bin/pip install -U pip distribute'.format(virtualenv))

def install_requirement(remote_dir, virtualenv, requirements):
	sudo('rm -rf {}/build'.format(virtualenv))
	# install requirements in slience
	sudo('{}/bin/pip install -q -r  {}'.format(virtualenv, requirements))

def install_project(remote_dir, virtualenv):
	with cd(remote_dir):
		run('find . -name "*.pyc" -delete')
		run('rm -rf build dist')
		run('{}/bin/python setup.py sdist'.format(virtualenv))

		package = run('ls dist | grep tar')
		run('{}/bin/pip install -q dist/{}'.format(virtualenv, package))


def restart_services(services):
	for service in services:
		status = sudo('supervisorctl status {}'.format(service))
		if 'RUNNING' in status:
			sudo('supervisorctl restart {}'.format(service))
	

def common_deploy(local_dir, remote_dir, virtualenv, 
				requirements, rsync_exclude, services):
	# async necessary files to remote server
	async_files(local_dir, remote_dir, rsync_exclude)
	# init virtualenv
	if not exists(virtualenv):
		init_venv(virtualenv)
	# install requirements
	install_requirement(remote_dir, virtualenv, requirements)
	# install my project
	install_project(remote_dir, virtualenv)
	# restart
	restart_services(services)

@task
@hosts(HOSTS)
def deploy():
	execute(common_deploy, **FAB_PARAM)