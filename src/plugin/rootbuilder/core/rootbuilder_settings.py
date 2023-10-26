import mobase
from ....base.base_settings import BaseSettings

class RootBuilderSettings(BaseSettings):
    """ Root Builder settings module. Used to load various plugin settings. """

    def __init__(self, organiser:mobase.IOrganizer):
        super().__init__("RootBuilder", organiser)

    def cache(self):
        """ Determines whether to cache game file hashes. """
        return self.setting("cache")

    def backup(self):
        """ Determines whether to take a full game backup. """
        return self.setting("backup")
        
    def hash(self):
        """ Determines if change tracking should use hashes or not."""
        return self.setting("hash")

    def autobuild(self):
        """ Determines whether to build automatically on run. """
        return self.setting("autobuild")

    def exclusions(self):
        """ Files to be excluded from all operations. """
        return str(self.setting("exclusions")).split(",")

    def redirect(self):
        """ Whether to redirect apps launched from mod root folders. """
        return self.setting("redirect")

    def installer(self):
        """ Enables the installer plugin. """
        return self.setting("installer")

    def priority(self):
        """ The priority of the installer module for installing root mods. """
        return self.setting("priority")
    
    def copyfiles(self):
        """Wildcard supporting list of files that should be copied."""
        return str(self.setting("copyfiles")).split(",")
    
    def copypriority(self):
        """Priority order for files to be copied."""
        return self.setting("copypriority")
    
    def linkfiles(self):
        """Wildcard supporting list of files that should be linked."""
        return str(self.setting("linkfiles")).split(",")
    
    def linkpriority(self):
        """Priority order for files to be linked."""
        return self.setting("linkpriority")
    
    def usvfsfiles(self):
        """Wildcard supporting list of files that should be handled by usvfs."""
        return str(self.setting("usvfsfiles")).split(",")
    
    def usvfspriority(self):
        """Priority order for files to be mapped."""
        return self.setting("usvfspriority")