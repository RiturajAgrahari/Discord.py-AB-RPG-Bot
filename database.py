import os
import mysql.connector
from datetime import date
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("MY_SQL_HOST")
USER = os.getenv("MY_SQL_USER")
PASSWORD = os.getenv("MY_SQL_PASSWORD")
DATABASE = os.getenv("MY_SQL_DATABASE")


def open_database():
    mydb = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
        auth_plugin="mysql_native_password"
    )
    return mydb


# Need to add multiple coulmns and conditions!
async def select_query(column:str, table:str, condition_column:str=None, condition_value:str | int=None):
    if condition_column is None or condition_value is None:
        condition = ""
    else:
        if type(condition_value) is str:
            condition = f" WHERE {condition_column} = '{condition_value}'"
        else:
            condition = f" WHERE {condition_column} = {condition_value}"

    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f"SELECT {column} FROM {table}{condition}"
    # print(f'(sql select query): {sql}')
    mycursor.execute(sql)
    output = mycursor.fetchall()
    mydb.close()
    return output


# Not working!
async def insert_query(columns:tuple, values:tuple):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f"INSERT INTO {columns} VALUES {values}"
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()


# Need to add multiple conditions!
async def update_query(table:str, key_value:dict, condition_column:str=None, condition_value:str | int=None, operation:str='equal'):
    # {'koens': 100}
    if condition_column is None or condition_value is None:
        condition = ""
    else:
        if type(condition_value) is str or type(condition_value) is None:
            condition = f" WHERE {condition_column} = '{condition_value}'"
        else:
            condition = f" WHERE {condition_column} = {condition_value}"

    set = ""

    for key, value in key_value.items():
        if type(value) is str:
            set += f", {key} = '{value}'"

        elif type(value) is int:
            if operation == 'equal':
                set += f", {key} = {value}"
            elif operation == 'addition':
                set += f", {key} = {key} + {value}"
            elif operation == 'subtraction':
                set += f", {key} = {key} - {value}"
            else:
                print('wrong operation!')
        else:
            print('wrong value datatype')

    set = set.lstrip(',')

    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f"UPDATE {table} SET{set}{condition}"
    # print(f"(sql update query): {sql}")
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()


'''
INEFFICIENT WORK :
'''


async def creating_main_profile(interaction):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = "INSERT INTO profile (name, discord_id) VALUES (%s, %s)"
    val = [(interaction.user.name, interaction.user.mention)]
    mycursor.executemany(sql, val)
    mydb.commit()
    mydb.close()


async def create_inventory(uid):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = 'INSERT INTO inventory (uid) VALUES (%s)'
    val = [(uid)]
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()


async def create_events(uid):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = 'INSERT INTO events (uid) VALUES (%s)'
    val = [(uid)]
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()


async def create_updated_db():
    user_data = await select_query(column="uid, storage", table="events")
    print(user_data)
    data_transfer_status = "OK"
    counter = 0
    for user_storage in user_data:
        counter += 1
        try:
            await update_query(table="inventory", key_value={"storage": str(user_storage[1])}, condition_column="uid", condition_value=user_storage[0])
        except:
            data_transfer_status = "ERROR"
            print(f"{counter} : error updating storage of user with UID: {user_storage[0]}")

    if data_transfer_status is "OK":
        mydb = open_database()
        mycursor = mydb.cursor()
        sql = 'ALTER TABLE events DROP COLUMN storage'
        mycursor.execute(sql)
        mydb.commit()
        mydb.close()
        print("Data is completely transfered!")

    else:
        print("Data is not completely transfered!")



async def bot_uses(today_date):
    await update_query(table="bot_info", key_value={"rpg_bot": 1}, condition_column="date",
                       condition_value=str(today_date), operation="addition")
