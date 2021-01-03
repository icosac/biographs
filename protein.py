class Protein:
    def __init__(self, _id, _name, _color="black", _description=""):
        self.id=_id
        self.name=_name
        self.color=_color
        self.description=_description

    def __lt__(self, other):
        return self.name<other.name

    def __eq__(self, other):
        return self.name==other.name

    def __str__(self):
        return self.name

    def toDic(self):
        return {"id" : self.id, "name" : self.name, "color" : self.color, "description" : self.description}

