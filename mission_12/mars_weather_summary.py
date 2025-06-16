import csv
import mysql.connector

class MySQLHelper:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def insert_weather_data(self, date, temp, storm):
        query = (
            'INSERT INTO mars_weather (mars_date, temp, storm) '
            'VALUES (%s, %s, %s)'
        )
        self.cursor.execute(query, (date, temp, storm))

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()

def read_csv_and_insert(filename, db_helper):
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            mars_date = row[0]
            temp = int(row[1])
            storm = int(row[2])
            db_helper.insert_weather_data(mars_date, temp, storm)
        db_helper.commit()

def main():
    db = MySQLHelper(
        host='localhost',
        user='your_username',
        password='your_password',
        database='your_database'
    )
    read_csv_and_insert('mars_weathers_data.csv', db)
    db.close()

if __name__ == '__main__':
    main()
