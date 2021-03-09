class Protein:
    def __init__(self, _id, _name, _color="#000000", _description=""):
        self.pid=_id
        self.name=_name
        self.color=_color
        self.description=_description

    def __lt__(self, other):
        return str(self)<str(other)

    def __eq__(self, other):
        return str(self)==str(other)

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name+str(self.pid))

    def toDic(self):
        return {"id" : self.pid, "name" : self.name, "color" : self.color, "description" : self.description}

