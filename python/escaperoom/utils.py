# Utilities 
#

# Get a description for a list of items
#
def getListDescription(thelist):
    descr = "" 
    i = 0
    for item in thelist:
        if (isinstance(item, str)):
            descr = descr + item.lower()
        elif (item.__class__.__name__ == "Item"):      # avoid cyclic import TODO fix
            descr = descr + item.short.lower()
        else:
            raise NotImplementedError
        
        if i > 0 and i == len(thelist)-2:            
            descr = descr + ", and "
        elif i < len(thelist)-1: 
            descr = descr + ", "        
        i = i + 1
    descr = descr + "."        
    return descr 

# Get a description for a dictionary of items
#
def getDictDescription(thedict):    
    thelist = []
    for item in thedict:
        thelist.append(item)        
    return getListDescription(thelist)
