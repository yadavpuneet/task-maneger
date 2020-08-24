import os
from datetime import datetime

import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

from models import Member, TaskBoard, Task

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


def count_tasks(taskboard):
    all = len(taskboard.tasks)
    completed = 0
    today = 0
    for k in taskboard.tasks:
        if k.get().is_completed:
            completed += 1
        try:
            if k.get().completed_on.date() == datetime.now().date():
                today += 1
        except:
            pass
    return all, all - completed, completed, today


JINJA_ENVIRONMENT.globals['count_tasks'] = count_tasks


def initialize(request):
    user = users.get_current_user()
    if user:
        url = users.create_logout_url(request.uri)
        url_string = 'logout'
        email = user.email().strip()
        member_key = ndb.Key('Member', email)
        member = member_key.get()
        if member is None:
            member = Member(id=email)
            member.put()
    else:
        url = users.create_login_url(request.uri)
        url_string = 'login'
        member = None
    template_values = {
        'url': url,
        'url_string': url_string,
        'user': user,
        'member': member
    }

    return template_values


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template_values = initialize(self.request)
        for x in self.request.params:
            template_values[str(x)] = str(self.request.params[x])

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


class NewBoardHandler(webapp2.RequestHandler):
    def post(self):
        params = self.request
        template_values = initialize(self.request)
        member = template_values['member']
        taskboard_name = params.get('new_taskboard_name').strip()
        taskboard_key = ndb.Key(TaskBoard, taskboard_name)
        taskboard = taskboard_key.get()
        if taskboard is None:
            taskboard = TaskBoard(id=taskboard_name)
            taskboard.members.append(member.key)
            taskboard.put()
            member.taskboards.append(taskboard.key)
            member.put()
            template_values['report'] = 1
        else:
            template_values['report'] = -1
            template_values['new_taskboard_name'] = taskboard_name

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


class TaskBoardHandler(webapp2.RequestHandler):
    def get(self):
        params = self.request
        template_values = initialize(self.request)
        if not template_values['user']:
            self.redirect('/')
            return
        try:
            taskboard = ndb.Key(urlsafe=params.get('id')).get()
            if template_values['member'].key in taskboard.members:
                template_values['taskboard'] = taskboard
        except:
            pass
        template = JINJA_ENVIRONMENT.get_template('taskboard.html')
        self.response.write(template.render(template_values))


class InviteMemberHandler(webapp2.RequestHandler):
    def get(self):
        template_values = initialize(self.request)
        if not template_values['user']:
            self.redirect('/')
            return

    def post(self):
        params = self.request
        template_values = initialize(self.request)
        try:
            taskboard = ndb.Key(urlsafe=params.get('invite_member_taskboard')).get()
            email = params.get('invite_member_email').strip()
            member = ndb.Key(Member, email).get()
            if member is None:
                template_values['report'] = -2
                template_values['invite_member_email'] = email
            elif member.key in taskboard.members:
                template_values['report'] = -3
                template_values['invite_member_email'] = email
            else:
                taskboard.members.append(member.key)
                member.taskboards.append(taskboard.key)
                taskboard.put()
                member.put()
                template_values['report'] = 3
            template_values['taskboard'] = taskboard
        except Exception as e:
            pass

        template = JINJA_ENVIRONMENT.get_template('taskboard.html')
        self.response.write(template.render(template_values))


class AddTaskHandler(webapp2.RequestHandler):
    def get(self):
        template_values = initialize(self.request)
        if not template_values['user']:
            self.redirect('/')
            return

    def post(self):
        params = self.request
        template_values = initialize(self.request)
        try:
            taskboard = ndb.Key(urlsafe=params.get('add_task_taskboard')).get()
            name = params.get('add_task_name').strip()
            dt = params.get('add_task_date').strip()
            date = datetime.strptime(dt, '%Y-%m-%d')
            task = ndb.Key(Task, name, parent=taskboard.key).get()
            if task is None:
                task = Task(id=name, parent=taskboard.key)
                task.deadline = date
                task.put()
                taskboard.tasks.append(task.key)
                taskboard.put()
                template_values['report'] = 4
            else:
                template_values['report'] = -4
                template_values['add_task_name'] = name
                template_values['add_task_date'] = dt
            template_values['taskboard'] = taskboard
        except Exception as e:
            pass

        template = JINJA_ENVIRONMENT.get_template('taskboard.html')
        self.response.write(template.render(template_values))


class DeadlineTaskHandler(webapp2.RequestHandler):
    def get(self):
        template_values = initialize(self.request)
        if not template_values['user']:
            self.redirect('/')
            return

    def post(self):
        params = self.request
        template_values = initialize(self.request)
        try:
            taskboard = ndb.Key(urlsafe=params.get('deadline_task_taskboard')).get()
            task = ndb.Key(urlsafe=params.get('deadline_task_id')).get()
            dt = params.get('deadline_task_date').strip()
            if dt:
                task.deadline = datetime.strptime(dt, '%Y-%m-%d')
            else:
                task.deadline = None
            task.put()
            template_values['taskboard'] = taskboard
        except Exception as e:
            pass

        template = JINJA_ENVIRONMENT.get_template('taskboard.html')
        self.response.write(template.render(template_values))


class AssignTaskHandler(webapp2.RequestHandler):
    def get(self):
        template_values = initialize(self.request)
        if not template_values['user']:
            self.redirect('/')
            return

    def post(self):
        params = self.request
        template_values = initialize(self.request)
        try:
            taskboard = ndb.Key(urlsafe=params.get('assign_task_taskboard')).get()
            task = ndb.Key(urlsafe=params.get('assign_task_id')).get()
            m = params.get('assign_task_member')
            if m:
                member = ndb.Key(urlsafe=m).get()
                task.assigned_to = member.key
            else:
                task.assigned_to = None
            task.put()
            template_values['taskboard'] = taskboard
        except Exception as e:
            pass

        template = JINJA_ENVIRONMENT.get_template('taskboard.html')
        self.response.write(template.render(template_values))


class CompleteTaskHandler(webapp2.RequestHandler):
    def get(self):
        template_values = initialize(self.request)
        if not template_values['user']:
            self.redirect('/')
            return

    def post(self):
        params = self.request
        template_values = initialize(self.request)
        try:
            taskboard = ndb.Key(urlsafe=params.get('complete_task_taskboard')).get()
            task = ndb.Key(urlsafe=params.get('complete_task_id')).get()
            if params.get('complete_task_state') == 'on':
                task.is_completed = True
                task.completed_on = datetime.now()
            else:
                task.is_completed = False
                task.completed_on = None
            task.put()
            template_values['taskboard'] = taskboard
        except Exception as e:
            pass

        template = JINJA_ENVIRONMENT.get_template('taskboard.html')
        self.response.write(template.render(template_values))


class DeleteTaskHandler(webapp2.RequestHandler):
    def get(self):
        template_values = initialize(self.request)
        if not template_values['user']:
            self.redirect('/')
            return

    def post(self):
        params = self.request
        template_values = initialize(self.request)
        try:
            taskboard = ndb.Key(urlsafe=params.get('delete_task_taskboard')).get()
            task = ndb.Key(urlsafe=params.get('delete_task_id')).get()
            taskboard.tasks.remove(task.key)
            taskboard.put()
            task.key.delete()
            template_values['taskboard'] = taskboard
        except Exception as e:
            pass

        template = JINJA_ENVIRONMENT.get_template('taskboard.html')
        self.response.write(template.render(template_values))


class RenameBoardHandler(webapp2.RequestHandler):
    def get(self):
        template_values = initialize(self.request)
        if not template_values['user']:
            self.redirect('/')
            return

    def post(self):
        params = self.request
        template_values = initialize(self.request)
        member = template_values['member']
        try:
            tb = ndb.Key(urlsafe=params.get('rename_taskboard_id')).get()
            taskboard_name = params.get('rename_taskboard_name').strip()
            taskboard_key = ndb.Key(TaskBoard, taskboard_name)
            taskboard = taskboard_key.get()
            if taskboard is None:
                taskboard = TaskBoard(id=taskboard_name)
                taskboard.members = tb.members
                for key in tb.tasks:
                    task = Task(id=key.id(), parent=taskboard.key)
                    task.deadline = key.get().deadline
                    task.is_completed = key.get().is_completed
                    task.completed_on = key.get().completed_on
                    task.assigned_to = key.get().assigned_to
                    task.put()
                    taskboard.tasks.append(task.key)
                taskboard.put()
                for key in taskboard.members:
                    key.get().taskboards.remove(tb.key)
                    key.get().taskboards.append(taskboard.key)
                    key.get().put()
                tb.key.delete()
                template_values['report'] = 5
                template_values['taskboard'] = taskboard
            else:
                template_values['report'] = -5
                template_values['rename_taskboard_name'] = taskboard_name
                template_values['taskboard'] = tb

        except Exception as e:
            pass

        template = JINJA_ENVIRONMENT.get_template('taskboard.html')
        self.response.write(template.render(template_values))


class RemoveMemberHandler(webapp2.RequestHandler):
    def get(self):
        template_values = initialize(self.request)
        if not template_values['user']:
            self.redirect('/')
            return

    def post(self):
        params = self.request
        template_values = initialize(self.request)
        try:
            taskboard = ndb.Key(urlsafe=params.get('remove_member_taskboard')).get()
            member = ndb.Key(urlsafe=params.get('remove_member_id')).get()
            taskboard.members.remove(member.key)
            for key in taskboard.tasks:
                if key.get().assigned_to == member.key:
                    key.get().assigned_to = None
                    key.get().put()
            taskboard.put()
            member.taskboards.remove(taskboard.key)
            member.put()
            template_values['taskboard'] = taskboard
        except Exception as e:
            pass

        template = JINJA_ENVIRONMENT.get_template('taskboard.html')
        self.response.write(template.render(template_values))


class DeleteBoardHandler(webapp2.RequestHandler):
    def get(self):
        template_values = initialize(self.request)
        if not template_values['user']:
            self.redirect('/')
            return

    def post(self):
        params = self.request
        template_values = initialize(self.request)
        try:
            taskboard = ndb.Key(urlsafe=params.get('delete_taskboard_id')).get()
            taskboard.members[0].get().taskboards.remove(taskboard.key)
            taskboard.members[0].get().put()
            taskboard.key.delete()
        except Exception as e:
            pass

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/new-board', NewBoardHandler),
    ('/taskboard', TaskBoardHandler),
    ('/invite-member', InviteMemberHandler),
    ('/add-task', AddTaskHandler),
    ('/assign-task', AssignTaskHandler),
    ('/complete-task', CompleteTaskHandler),
    ('/delete-task', DeleteTaskHandler),
    ('/rename-board', RenameBoardHandler),
    ('/remove-member', RemoveMemberHandler),
    ('/delete-board', DeleteBoardHandler),
    ('/deadline-task', DeadlineTaskHandler),
], debug=True)
