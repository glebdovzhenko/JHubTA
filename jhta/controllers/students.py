from cement import Controller, ex
from rich.prompt import Prompt
from rich.panel import Panel
from tinydb import Query
import os


class Students(Controller):
    class Meta:
        label = 'students'
        stacked_on = 'base'
        stacked_type = 'nested'

    @ex(help='list all students')
    def list(self):
        tb = self.app.db.table('students')
        context = dict()
        context['students'] = tb.all()
        context['group_ids'] = {x['group_id']: x['group'] for x in context['students']}
        
        self.app.console.print(
            self.app.render(
                context, 'students-list.py', out=None
        ))

    @ex(help='fill students table with placeholders')
    def init(self):
        self.app.db.drop_table('students')
        tb = self.app.db.table('students')
        tb.insert({
            'name': 'Иван Иванович',
            'surname': 'Иванов',
            'group': 'ГР-000',
            'group_id': 'TEST',
            'login': 'jupyter-gr-000-ivanov'
        })
        tb.insert({
            'name': 'Пётр Петрович',
            'surname': 'Петров',
            'group': 'ГР-000',
            'group_id': 'TEST',
            'login': 'jupyter-gr-000-petrov'
        })
        tb.insert({
            'name': 'Сидор Сидорович',
            'surname': 'Сидоров',
            'group': 'ГР-000',
            'group_id': 'TEST',
            'login': 'jupyter-gr-000-sidorov'
        })

    @ex(help='add a student',
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
        ])
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
    
    @ex(help='check the database status')
    def check(self):
        ok, not_ok = [], []
        for st in self.app.db.table('students').all():
            if os.path.exists(os.path.join('/home', st['login'])):
                ok.append(st)
            else:
                not_ok.append(st)

        if not not_ok:
            self.app.console.print(
                Panel('[bold green]:green_circle: All users have home directories [/]')
            )
        else:
            self.app.console.print(
                Panel('[bold red]:x: :x: The following users have no home directories :x: :x:[/]')
            )
            context = dict()
            context['students'] = not_ok
            context['group_ids'] = {x['group_id']: x['group'] for x in context['students']}
        
            self.app.console.print(
                self.app.render(
                    context, 'students-list.py', out=None
            ))

        ok, not_ok = [], []

