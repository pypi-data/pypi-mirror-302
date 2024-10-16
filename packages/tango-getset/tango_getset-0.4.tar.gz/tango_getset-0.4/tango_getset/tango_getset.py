# tango_getset.py

def make_getter(attr):
    def getter(self):
        return getattr(self, f"_{attr}")
    return getter

def make_setter(attr):
    def setter(self, value):
        setattr(self, f"_{attr}", value)
    return setter

def getter(cls):
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)

        for attr, value in kwargs.items():
            # Automatisch Getter hinzufügen mit Closure
            setattr(cls, attr, property(make_getter(attr)))

    cls.__init__ = new_init
    return cls

def setter(cls):
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)

        for attr, value in kwargs.items():
            # Automatisch Setter hinzufügen mit Closure
            setattr(cls, f"set_{attr}", make_setter(attr))

    cls.__init__ = new_init
    return cls

def gettersetter(cls):
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)

        for attr, value in kwargs.items():
            # Automatisch Getter und Setter hinzufügen mit Closure
            setattr(cls, attr, property(make_getter(attr), make_setter(attr)))

    cls.__init__ = new_init
    return cls
