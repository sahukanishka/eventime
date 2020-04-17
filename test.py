class Vehicle:
    def __init__(self, cost, type):
        self.__cost = cost
        self.__type = type
        self.__premium = None          #Instance variable
   
    def calc_premium(self):
        self.__premium = 0       #Local variable
        if(self.__type == "Two Wheeler"):
            self.__premium = self.__cost * (2/100)
        elif self.__type == "Four Wheeler":
            self.__premium = self.__cost * (6/100)
        
x = Vehicle(1000, "Two Wheeler")
x.calc_premium()
print(x._Vehicle__premium)