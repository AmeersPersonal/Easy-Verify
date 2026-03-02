import sqlite3
connection = sqlite3.connect('EasyVerifyDB.sqlite')
cursor = connection.cursor()

insert_query = """
INSERT INTO Verifications (Result, Method, Policy, Confidence)
VALUES (?, ?, ?, ?);
"""
new_record =(1, "manual_test", "standard_policy", 98)

cursor.execute(insert_query, new_record)
connection.commit()

# 6. Close the connection
connection.close()