class Employee(object):
    def __init__(self, id, importance, subordi):
        self.id = id
        self.importance = importance
        self.subordi = subordi
        
def getImportance(employees, id):
    table = {emp.id: emp for emp in employees}

    def dfs(emp):
        if emp.subordis == []:
            return emp.importance
        else:
            value = emp.importance
            for sub in emp.subordis:
                value += dfs(table[sub])
            return value
    
    return dfs(table[id])