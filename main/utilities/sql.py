from registry.models import Visitor


def insert_visitor(visitor_object):
    visitor = Visitor()
    visitor.fname = visitor_object.fname
    visitor.lname = visitor_object.lname
    visitor.age = visitor_object.age
    visitor.photo_path = visitor_object.photo_path
    visitor.entrance_time = visitor_object.entrance_time
    visitor.save()
    return visitor
