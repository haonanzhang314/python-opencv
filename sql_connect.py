# import mysql.connector
#
# mydb = mysql.connector.connect(
#     host="124.221.206.185",
#     user="face",
#     passwd="qwe123ASD",
#     database='face'
# )
# mycursor = mydb.cursor()
# mycursor.execute("select * from student where id ='20214132132'")
#
# for x in mycursor:
#     print(x)

import mysql.connector
name = 202134
mydb = mysql.connector.connect(
    host="124.221.206.185",
    user="face",
    passwd="qwe123ASD",
    database='face'
)
mycursor = mydb.cursor()
mycursor.execute("select * from student where id = '%s'"%(name))

for x in mycursor:
    print(x)

# 数据库命令
# 显示数据库show databases
# 创建数据库 create databases
# 显示表 show table
# 创建表 create table
# 创建表中的行 CREATE TABLE student (id int auto_increment primary key,name varchar(10),passwd varchar(10))")
# INT AUTO_INCREMENT PRIMARY KEY表示主键
