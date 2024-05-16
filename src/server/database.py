from sqlalchemy import String, Column, select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')
session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    login = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    problems = Column(String, default="")

    async def add_problem(self, sess, new_problem):
        if self.problems != "":
            self.problems += "  "
        self.problems += new_problem
        await sess.commit()
        return "saved successfully"

    async def delete_problem(self, sess, index):
        list_of_problems = self.problems.split("  ")
        if index >= len(list_of_problems):
            return "index out of range"

        self.problems = ""
        for i in range(len(list_of_problems)):
            if i != index:
                if self.problems != "":
                    self.problems += "  "
                self.problems += list_of_problems[i]
        await sess.commit()
        return "successfully deleted"

    def check_password(self, password):
        return self.password == password

    async def change_problem(self, sess, index, new_problem_text):
        list_of_problems = self.problems.split("  ")
        if index >= len(list_of_problems):
            return "index out of range"

        self.problems = ""
        for i in range(len(list_of_problems)):
            if self.problems != "":
                self.problems += "  "
            if i == index:
                self.problems += new_problem_text
            else:
                self.problems += list_of_problems[i]
        await sess.commit()
        return "successfully changed"




async def run_database():
    async with engine.begin() as eng:
        await eng.run_sync(Base.metadata.create_all)

async def login_user(login, password):
    async with (session() as sess):
        user = await sess.scalar(select(User).where(User.login == login))
        if not user:
            return "wrong login"
        return "success" if user.check_password(password) else "wrong password"

async def register_user(login, password):
    async with session() as sess:
        user = await sess.scalar(select(User).where(User.login == login))
        if user:
            return "login is busy"
        sess.add(User(login=login, password=password))
        await sess.commit()
        return "success"

async def add_problem(login, new_problem):
    async with session() as sess:
        user = await sess.scalar(select(User).where(User.login == login))
        if not user:
            return "we have problems..."
        return await user.add_problem(sess, new_problem)

async def get_problems(login):
    async with session() as sess:
        user = await sess.scalar(select(User).where(User.login == login))
        return user.problems if user else ""

async def delete_problem(login, index):
    async with session() as sess:
        user = await sess.scalar(select(User).where(User.login == login))
        if not user:
            return "we have problems..."

        return await user.delete_problem(sess, index)

async def change_problem(login, index, problem):
    async with session() as sess:
        user = await sess.scalar(select(User).where(User.login == login))
        if not user:
            return "we have problems..."

        return await user.change_problem(sess, index, problem)

