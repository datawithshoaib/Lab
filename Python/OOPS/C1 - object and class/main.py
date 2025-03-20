from car import Car

car1 = Car("Mustang", 2024, "red", False)
car2 = Car("Corvette", 2025, "blue", True)
car3 = Car("Charger", 2026, "yellow", True)

print(car1) # output: <__main__.Car object at 0x000001FD0D321910>

print(car1.model) # output: Mustang
print(car1.year) # output: 2024
print(car1.color) # output: red
print(car1.for_sale) # output: False

car2.drive()
car2.stop()
car2.describe()
