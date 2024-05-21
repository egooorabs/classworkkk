from peewee import SqliteDatabase, Model, ForeignKeyField, TextField, TimeField, IntegerField

dbb = SqliteDatabase('sqlite.db')

class DB(Model):
    class Meta:
        database = dbb

class User(DB):
    tg_user = IntegerField()
    time = TimeField(null=True)

class Image(DB):
    url = TextField()

class Send(DB):
    user = ForeignKeyField(User)
    image = ForeignKeyField(Image)

class UserDoesNotExist(Exception):
    pass



dbb.connect()
dbb.create_tables([User, Image, Send], safe=True)
User.create(tg_user=1, time=None)
dbb.close()