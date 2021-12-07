import mobase, reinstaller_init, rootbuilder_init

def createPlugins():
    return set().union(reinstaller_init.createPlugins(), rootbuilder_init.createPlugins())
