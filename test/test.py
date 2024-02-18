from datetime import date, timedelta,datetime
from dtb.dtb import *
cursor.execute(f"SELECT date FROM coin WHERE discord = '824476340249821184'")
datebd = cursor.fetchone()[0]
datenow = date.today()
print(datebd)
print(datenow)
if datenow > datebd:
    print('aye')
else:
    print('lox')
