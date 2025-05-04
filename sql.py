import pymysql
from pymysql import IntegrityError
from datetime import datetime

username = ''

connect = pymysql.connect(
    host='<YOURHOST>',
    port=3306,
    user='<USERNAME>',
    passwd='<PASSWORD>',
    db='<DATABASE>'
)

cursor = connect.cursor()

class AccountInfo:
    def __init__(self):
        self.version = '0.0.1beta'
        self.function = ('getASIKey', '')

    def getASIKey(self, username):
        cursor.execute(f"select keyMD from `license` where username = '{username}'")
        result = cursor.fetchone()
        if result is not None:
            return result[0]
        return 'Not found'


class SignIn:
    def __init__(self):
        self.version = '0.0.1beta'
        self.function = ('login', 'IsExistUser')

    def login(self, username, password):
        cursor.execute("select password from acps where username = %s", (username,))
        password_get = cursor.fetchone()
        if password_get[0] == password:
            return True
        return False

    def IsExistUser(self, username):
        cursor.execute("select username from acps where username = %s", (username,))
        username_get = cursor.fetchone()
        if username_get is not None:
            return True
        return False


class SignUp:
    def __init__(self):
        self.version = '0.0.1beta'
        self.function = ('register', 'IsExistUser', 'init')

    def register(self, username, password):
        try:
            cursor.execute("insert into acps (username, password) values (%s, %s)", (username, password))
            cursor.execute(f"insert into license (username, keyMD) values ('{username}', MD5('{username}'));")
            connect.commit()
            cursor.execute(f"create table `{username}_agd` (datetime datetime primary key not null, title varchar(31) not null, description text, state tinyint(1) not null);")
            return True
        except IntegrityError:
            print("Primary key already exists")
            return False

    def IsExistUser(self, username):
        cursor.execute("select username from acps where username = %s", (username,))
        username_get = cursor.fetchone()
        if username_get is not None:
            return True
        return False

    def init(self, username):
        try:
            description = 'Thanks for your choice to Agenda. More usage tips in introduction.'
            cursor.execute(f"insert into `{username}_agd` (datetime, title, description, state) values (%s, %s, %s, %s)", (datetime.now(), 'Welcome to Agenda', description, 0))
            connect.commit()
        except Exception as e:
            print(e)

class Tool:
    def __init__(self):
        self.version = '0.0.1beta'
        self.function = ('IsKey',)

    def IsKey(self, username, key):
        cursor.execute(f"select keyMD from `license` where username = '{username}'")
        key_get = cursor.fetchone()
        if key_get is not None:
            if key_get[0] == key:
                return True
        return False

class GetInfo:
    def __init__(self):
        self.version = '0.0.1beta'
        self.function = ('getTable',)

    def getTable(self, username):
        cursor.execute(f"select * from `{username}_agd`")
        data = cursor.fetchall()
        if data is not None:
            return data
        return False

class InsertInfo:
    def __init__(self):
        self.version = '0.0.1beta'
        self.function = ('insertTable',)

    def insertTable(self, username, pack):
        try:
            cursor.execute(f"insert into `{username}_agd` (datetime, title, description, state) values (%s, %s, %s, %s);", pack)
            connect.commit()
            return True
        except pymysql.err.IntegrityError:
            return False, 'Primary key already exists'
        except pymysql.err.DataError:
            return False, "Data too long for column 'title'"

class ModifyInfo:
    def __init__(self):
        self.version = '0.0.1beta'
        self.function = ('ModifyTable', 'markAsComplete', 'markAsIncomplete', 'deleteItem')

    def ModifyTable(self, username, pack, orintime):
        try:
            cursor.execute(f"delete from `{username}_agd` where datetime = %s", (orintime,))
            cursor.execute(f"insert into `{username}_agd` (datetime, title, description, state) values (%s, %s, %s, %s);", pack)
            connect.commit()
            return True
        except pymysql.err.IntegrityError:
            return False, 'Primary key already exists'
        except pymysql.err.DataError:
            return False, "Data too long for column 'title'"

    def markAsComplete(self, username, datetime):
        try:
            cursor.execute(f"update `{username}_agd` set state = 0 where datetime = %s", (datetime,))
            connect.commit()
            return True
        except:
            return False

    def markAsIncomplete(self, username, datetime):
        try:
            cursor.execute(f"update `{username}_agd` set state = 1 where datetime = %s", (datetime,))
            connect.commit()
            return True
        except:
            return False

    def deleteItem(self, username, datetime):
        try:
            cursor.execute(f"delete from `{username}_agd` where datetime = %s", (datetime,))
            connect.commit()
            return True
        except:
            return False


if __name__ =='__main__':
    signup = SignUp()
    signup.register(username='aaaa', password='bbbb')