from cement import Controller, ex, shell
from rich.prompt import Prompt
from rich.panel import Panel
from tinydb import Query
from git import Repo, exc
import os


class Students(Controller):
    class Meta:
        label = 'students'
        stacked_on = 'base'
        stacked_type = 'nested'
        help = 'students list manipulation'
        arguments=[
            ([ '-g', '--group-id' ],
             {'help': 'group id',
              'action': 'store',
              'dest': 'group_id'}),
            ([ '-n', '--name' ],
             {'help': 'name',
              'action': 'store',
              'dest': 'name'}),
            ([ '-sn', '--surname' ],
             {'help': 'surname',
              'action': 'store',
              'dest': 'surname'}),
            ([ '-l', '--login' ],
             {'help': 'login',
              'action': 'store',
              'dest': 'login'}),
        ]

    def _query(self):
        tb = self.app.db.table('students')

        if self.app.pargs.group_id is not None:
            q1 = Query().group_id == self.app.pargs.group_id
        else:
            q1 = Query().group_id.exists()

        if self.app.pargs.name is not None:
            q2 = Query().name == self.app.pargs.name
        else:
            q2 = Query().name.exists()

        if self.app.pargs.surname is not None:
            q3 = Query().surname == self.app.pargs.surname
        else:
            q3 = Query().surname.exists()

        if self.app.pargs.login is not None:
            q4 = Query().login == self.app.pargs.login
        else:
            q4 = Query().login.exists()

        return tb.search(q1 & q2 & q3 & q4)

    @ex(help='list all students')
    def list(self):
        context = dict()
        context['students'] =  self._query()
        context['group_ids'] = {
            x['group_id']: x['group'] for x in context['students']
        }
        
        self.app.console.print(
            self.app.render(
                context, 'students-list.py', out=None
        ))

    @ex(help='add a student')
    def add(self):
        if self.app.pargs.group_id is not None:
            g_id = self.app.pargs.group_id
        else:
            g_id = Prompt.ask('Group ID',  console=self.app.console)
        
        g_id_match = self.app.db.table('students').search(
            Query().group_id == g_id
        )

        if g_id_match:
            g_name = g_id_match[0]['group']
        else:
            g_name = Prompt.ask('Group name',  console=self.app.console)

        if self.app.pargs.name is not None:
            name = self.app.pargs.name
        else:
            name = Prompt.ask('Name',  console=self.app.console)
        
        if self.app.pargs.surname is not None:
            surname = self.app.pargs.surname
        else:
            surname = Prompt.ask('Surname', console=self.app.console)

        if self.app.pargs.login is not None:
            login = self.app.pargs.login
        else:
            login = Prompt.ask('Login', console=self.app.console)

        student = {
            'name': name,
            'surname': surname,
            'group': g_name,
            'group_id': g_id,
            'login': login
        }
        self.app.console.print(
            self.app.render(
                student, 'student-info.py', out=None
        ))

        res = Prompt.ask('[bold]Submit?[/]', console=self.app.console)
        if res == 'y':
            tb = self.app.db.table('students')
            tb.insert(student)

    @ex(help='Initiates a user repository')
    def init_repo(self):
        for st in self._query():
            shell.cmd(
                ' && '.join((
                    'su %s' % st['login'],
                    'git init -b %s' % st['login'],
                    'git remote add origin /srv/git/studentlab.git',
                    'git config user.email %s@fake.faux' % st['login'],
                    'git config user.name %s' % st['login']
                )), 
                capture=False
            )
    
    @ex(help='check the database status')
    def check(self):
        home_ok, home_not_ok = self.check_home()
        git_ok, git_not_ok = self.check_repo(home_ok)

    def check_home(self):
        ok, not_ok = [], []
        for st in self._query():
            if os.path.exists(os.path.join('/home', st['login'])):
                ok.append(st)
            else:
                not_ok.append(st)

        if not not_ok:
            context = dict()
            context['msg'] = 'All users have home directories'
            self.app.console.print(
                self.app.render(
                    context, 'ok-msg.py', out=None
            ))
        else:
            context = dict()
            context['msg'] = 'The following users have no home directories'
            context['students'] = not_ok
            context['group_ids'] = {
                x['group_id']: x['group'] for x in context['students']
            }

            self.app.console.print(
                self.app.render(
                    context, 'err-msg.py', out=None
            ))
            self.app.console.print(
                self.app.render(
                    context, 'students-list.py', out=None
            ))
        return ok, not_ok

    def check_repo(self, usr_list=None):
        if usr_list is None:
            usr_list = self._query()
        
        ok, not_ok = [], []
        for st in usr_list:
            try:
                _ = Repo(os.path.join('/home', st['login'])).git_dir
                ok.append(st)
            except exc.InvalidGitRepositoryError:
                not_ok.append(st)
        
        if not not_ok:
            context = dict()
            context['msg'] = 'All users have valid git repos'
            self.app.console.print(
                self.app.render(
                    context, 'ok-msg.py', out=None
            ))
        else:
            context = dict()
            context['msg'] = 'The following users have no git repos'
            context['students'] = not_ok
            context['group_ids'] = {
                x['group_id']: x['group'] for x in context['students']
            }

            self.app.console.print(
                self.app.render(
                    context, 'err-msg.py', out=None
            ))
            self.app.console.print(
                self.app.render(
                    context, 'students-list.py', out=None
            ))
        return ok, not_ok

