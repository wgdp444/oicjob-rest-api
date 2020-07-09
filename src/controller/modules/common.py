from database import db
def search_query(Model, search_condition):
    exprs = [(getattr(Model, name) == value) 
        for name, value in search_condition.items() if value is not None]
    return db.session.query(Model).filter(*exprs).all()
