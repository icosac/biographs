class Protein:
    def __init__(self, _name, _color="black", _description=""):
        self.name=_name
        self.color=_color
        self.description=_description

    def __lt__(self, other):
        return self.name<other.name

    def __eq__(self, other):
        return self.name==other.name

    def __str__(self):
        return self.name
