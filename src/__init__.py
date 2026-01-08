
try:
    from .rootbuilder_init import createPlugins as rbPlugins
except:
    def rbPlugins(): return []
try: 
    from .profilesync_init import createPlugins as psPlugins
except: 
    def psPlugins(): return []
try:
    from .pluginfinder_init import createPlugins as pfPlugins
except:
    def pfPlugins(): return []
try:
    from .openmwplayer_init import createPlugins as ompPlugins
except:
    def ompPlugins(): return []
try:
    from .shortcutter_init import createPlugins as scPlugins
except:
    def scPlugins(): return []
try:
    from .listexporter_init import createPlugins as lePlugins
except:
    def lePlugins(): return []
try:
    from .reinstaller_init import createPlugins as riPlugins
except:
    def riPlugins(): return []
try:
    from .curationclub_init import createPlugins as ccPlugins
except:
    def ccPlugins(): return []

def createPlugins():
    plugins = []
    plugins.extend(rbPlugins())
    plugins.extend(psPlugins())
    plugins.extend(pfPlugins())
    plugins.extend(ompPlugins())
    plugins.extend(scPlugins())
    plugins.extend(lePlugins())
    plugins.extend(riPlugins())
    plugins.extend(ccPlugins())
    return plugins
