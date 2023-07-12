import mobase
from ..moddy_check import ModdyCheck

class ExampleCheck(ModdyCheck):

    def __init__(self, organiser=mobase.IOrganizer):
        self.organiser = organiser

    def identifier(self):
        return "ExampleCheckId"
    
    def name(self):
        return "Example Check"
    
    def description(self):
        return "An example of an implementation of a ModdyCheck."
    
    def message(self):
        return "Hi! This is just an example, you don't need to do anything."

    def level(self):
        # 3 = Critical Problem
        # 2 = Potential Issue
        # 1 = General Suggestion
        return 1

    def check(self):
        # Return true if the check fails. False otherwise.
        return False
    
    def getResolveWidget(self, dialog=QDialog):
        # Return a QWidget containing buttons for the various different options.
        baseWidget = self.actionWidget(dialog)

        firstOption = self.actionButton(baseWidget)
        firstOption.setGeometry(self.posTopLeft())

        secondOptionText = self.actionText(baseWidget)
        secondOptionText.setGeometry(self.posBtmLeft())

        secondOptionBtn = self.actionButton(baseWidget)
        secondOptionBtn.setGeometry(self.posBtmRight())
        return baseWidget