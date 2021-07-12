import sqlite3 as db
from datetime import datetime


def init():
    con = db.connect("iou.db")
    cur = con.cursor()
    sql = '''
    create table if not exists expenses (
        amount number,
        category string,
        message string,
        date string
        )
    '''
    cur.execute(sql)
    con.commit()
    con.close()


def log(amount, category, message=""):
    date = str(datetime.now())
    con = db.connect("iou.db")
    cur = con.cursor()
    sql = '''
    insert into expenses values (
        {},
        '{}',
        '{}',
        '{}'
    )
        '''.format(amount, category, message, date)
    cur.execute(sql)
    con.commit()
    con.close()


def view(category=None):
    con = db.connect("iou.db")
    cur = con.cursor()
    if category:
        sql = '''
        select * from expenses where category = '{}' 
        '''.format(category)
        sql2 = '''
            select sum(amount) from expenses where category = '{}' 
            '''.format(category)
    else:
        sql = '''
            select * from expenses  
            '''.format(category)
        sql2 = '''
            select sum(amount) from expenses  
            '''.format(category)
    cur.execute(sql)
    results = cur.fetchall()
    cur.execute(sql2)
    total_amount = cur.fetchone()[0]
    
    return total_amount, results


if __name__ == '__main__':
    init()


iou_amount = input("Hur mycket pengar (sek): ")
iou_amount = iou_amount.replace(" ", "")
iou_amount = int(iou_amount)
iou_category = input("Kategori: ").lower()
iou_meddelande = input("Meddelande: ")
print()
# view_cat = input("Vilken kategori vill du se? Enter för alla: ") or "*"
log(iou_amount, iou_category, iou_meddelande)



saved = view()
print()
print(f'Total skuld: {saved[0]}kr')
print()


con = db.connect("iou.db")
cur = con.cursor()
view_cat = input("Vilken kategori vill du se? Enter för alla: ") or "*"
for row in cur.execute(f"select * from expenses where category = '{view_cat}' order by date desc"):
    print(row)
