from google.appengine.ext import ndb


class Member(ndb.Model):
    taskboards = ndb.KeyProperty(repeated=True)


class Task(ndb.Model):
    name = ndb.StringProperty()
    deadline = ndb.DateProperty()
    is_completed = ndb.BooleanProperty()
    completed_on = ndb.DateTimeProperty()
    assigned_to = ndb.KeyProperty()


class TaskBoard(ndb.Model):
    tasks = ndb.KeyProperty(repeated=True)
    members = ndb.KeyProperty(repeated=True)
