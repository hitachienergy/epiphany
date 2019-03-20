class ObjDict(dict):
    def __getattr__(self, name):
        if name in self:
            if type(self[name]) == dict:
                return ObjDict(self[name])
            else:
                return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        if type(value) == dict:
            self[name] = ObjDict(value)
        else:
            self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)
