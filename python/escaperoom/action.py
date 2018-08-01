
class Action():

    def __init__(self, method, **kwargs):        
        self.method = method
        self.kwargs = kwargs

    def __str__(self):
        return "{}".format(self.method)

    
