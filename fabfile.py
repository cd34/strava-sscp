from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd, env
from fabric.contrib.console import confirm

env.hosts = ['k1c2.mia.colo-cation.com']

def test():
    with settings(warn_only=True):
        result = local('python setup.py test', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")

def commit():
    local("git add -p && git commit")

def push():
    local("git push")

def prepare_deploy():
    test()
    commit()
    push()

def deploy():
    code_dir = '/var/www/sscp/small'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone git@github.com:sscp.git %s" % code_dir)
    with cd(code_dir):
        run("git pull")
        run("touch sscp.wsgi")
