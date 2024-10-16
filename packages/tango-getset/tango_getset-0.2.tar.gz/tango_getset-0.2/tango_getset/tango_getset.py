def getter(cls):
    # Überprüfe, ob es ein init gibt
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        # Rufe das Original-Init auf
        original_init(self, *args, **kwargs)

        # Durchlaufe alle Attribute, die im init übergeben wurden
        for attr, value in kwargs.items():
            # Automatisch Getter hinzufügen
            setattr(cls, attr, property(lambda self: getattr(self, f"_{attr}")))

    cls.__init__ = new_init
    return cls

def setter(cls):
    # Überprüfe, ob es ein init gibt
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        # Rufe das Original-Init auf
        original_init(self, *args, **kwargs)

        # Durchlaufe alle Attribute, die im init übergeben wurden
        for attr, value in kwargs.items():
            # Automatisch Setter hinzufügen
            setattr(cls, f"set_{attr}", lambda self, value: setattr(self, f"_{attr}", value))

    cls.__init__ = new_init
    return cls

def gettersetter(cls):
    # Überprüfe, ob es ein init gibt
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        # Rufe das Original-Init auf
        original_init(self, *args, **kwargs)

        # Durchlaufe alle Attribute, die im init übergeben wurden
        for attr, value in kwargs.items():
            # Automatisch Getter hinzufügen
            setattr(cls, attr, property(lambda self: getattr(self, f"_{attr}")))

            # Automatisch Setter hinzufügen
            setattr(cls, f"set_{attr}", lambda self, value: setattr(self, f"_{attr}", value))

    cls.__init__ = new_init
    return cls
