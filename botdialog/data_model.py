class UserProfile:
    def __init__(self):
        self.name = "" 
        self.first = ""
        self.second = ""
        self.firsttime = ""
        self.secondtime = ""
        self.clickdiff= ""


    @property
    def Name(self):
        return self.name
    @Name.setter
    def Name(self,name:str):
        self.name = name
    
    @property
    def First(self):
        return self.first
    @First.setter
    def First(self,first:str):
        self.first = first

    @property
    def Second(self):
        return self.second
    @Second.setter
    def Second(self,second:str):
        self.second = second

    @property
    def Firsttime(self):
        return self.firsttime
    @Firsttime.setter
    def Firsttime(self,firsttime:str):
        self.firsttime = firsttime

    @property
    def Secondtime(self):
        return self.secondtime
    @Secondtime.setter
    def Secondtime(self,secondtime:str):
        self.secondtime = secondtime


    @property
    def Clickdiff(self):
        return self.clickdiff
    @Clickdiff.setter
    def Clickdiff(self,clickdiff:str):
        self.clickdiff = clickdiff
       