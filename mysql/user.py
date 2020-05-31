
from lib.mysql_session import session
from mysql.models import User
from lib.decorators import model_to_list, model_to_dict


def get_all_receiver():
    return session.query(User).filter(User.times != 0).all()


def update_user_time(user):
    session.query(User).filter(User.id == user.id).update({"times": User.times - 1}, synchronize_session="evaluate")
    session.commit()


# update() 补充：
# session.query(Users).filter(Users.id > 0).update({Users.name: Users.name + "099"}, synchronize_session=False) # 在字段原有值的基础上更新时，synchronize_session=False 表示是 字符串 的拼接
# session.query(Users).filter(Users.id > 0).update({"age": Users.age + 1}, synchronize_session="evaluate")  # 在字段原有值的基础上更新时，synchronize_session="evaluate" 表示是 数值 的相加减 （默认是这种）
