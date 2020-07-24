from database import db
from flask import make_response
def search_query(Model, search_condition):
    exprs = []
    for name, value in search_condition.items():
        if value is None:
            continue
        if type(value) == str:
            exprs.append(getattr(Model, name).like(f"%{value}%"))
        else:
            exprs.append((getattr(Model, name) == value))
    # 完全一致検索ならこっち
    # exprs = [(getattr(Model, name) == value) 
    #     for name, value in search_condition.items() if value is not None]
    return db.session.query(Model).filter(*exprs).all()


