from datetime import datetime

class Task:
    def __init__(self, title, description, column_id, order, id=None, date=None):
        self.id = id
        self.title = title
        self.description = description
        self.column_id = column_id
        self.order = order
        if isinstance(date, str):
            self.date = date
        else:
            self.date = (date if date is not None else datetime.utcnow()).isoformat()
