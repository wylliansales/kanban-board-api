class Column:
    def __init__(self, name, user_id, id=None, tasks=None):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.tasks = tasks if tasks is not None else []
