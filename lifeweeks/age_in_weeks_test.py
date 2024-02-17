from datetime import date

d1 = date(1999, 1, 1)
d2 = date.today()
#d2 = date(2024, 2, 15)

result = (d2-d1).days//7 #1304 in actual weeks if 1 year is 52.17857 weeks or 1300 weeks if only 52 weeks
print(result)

print("-------------------")

a = d2.year - d1.year
d1 = date(d2.year, d1.month, d1.day)
b = (d2-d1).days//7
current_age = a*52+b

print(current_age)
