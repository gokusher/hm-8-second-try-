import sqlite3


def execute_query(connection, query, parameters=None):
    try:
        cursor = connection.cursor()
        cursor.execute(query, parameters)
        connection.commit()
    except sqlite3.Error as e:
        print(e)


def fetch_all(connection, query, parameters=None):
    try:
        cursor = connection.cursor()
        cursor.execute(query, parameters)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(e)
        return []


def create_connection(db_name):
    try:
        return sqlite3.connect(db_name)
    except sqlite3.Error as e:
        print(e)
        return None


def main():
    db_file = 'students.db'
    connect = create_connection(db_file)

    if connect:
        print("Connected to the database.")

        # Uncomment the lines below for initial setup
        # execute_query(connect, countries)
        # execute_query(connect, cities)
        # execute_query(connect, students)

        # Uncomment the lines below to add initial data
        countries_to_add = ['Kyrgyzstan', 'Russia', 'Italy', 'France', 'Spain', 'Japan']
        for country in countries_to_add:
            execute_query(connect, 'INSERT INTO countries (title) VALUES (?)', (country,))

        cities_to_add = [('Bishkek', 3.2, 1), ('Osh', 2.7, 1), ('Moscow', 8.7, 2), ('Novosibirsk', 2.5, 2),
                         ('Krasnoyarsk', 5.9, 2),
                         ('Rome', 4.9, 3), ('Venice', 3.8, 3), ('Paris', 4.5, 4), ('Madrid', 6.6, 5),
                         ('Tokyo', 13.5, 6),
                         ('Berlin', 5.0, 4), ('Beijing', 16.8, 5), ('London', 5.6, 6), ('New York', 12.4, 0),
                         ('Mumbai', 603.4, 0),
                         ('Sydney', 12.4, 0), ('Cairo', 606.0, 0)]
        for city in cities_to_add:
            execute_query(connect, 'INSERT INTO cities (title, area, country_id) VALUES (?, ?, ?)', city)

        students_to_add = [('Bailando', 'Puta', 3), ('Gordon', 'Ramsy', 1), ('Mice', 'Miller', 5),
                           ('Maybe', 'Baby', 1), ('Peter', 'Parker', 7), ('Harold', 'Veryaskina', 3),
                           ('Eva', 'Elvion', 7), ('Adol', 'Meta', 2), ('Nikita', 'Saharov', 3),
                           ('Umar', 'Zhumaev', 1), ('Malik', 'Abdurahmanov', 1), ('Ivan', 'Vernovsky', 6),
                           ('Natalya', 'Valueva', 5), ('Jinny', 'Minter', 7), ('Keros', 'Faster', 6),
                           ('Anna', 'Smith', 8), ('John', 'Doe', 9), ('Sakura', 'Yamamoto', 10),
                           ('Pablo', 'Gomez', 11), ('Sophie', 'Dupont', 12), ('Hiroshi', 'Tanaka', 13),
                           ('Olga', 'Ivanova', 14), ('Carlos', 'Garcia', 15)]
        for student in students_to_add:
            execute_query(connect, 'INSERT INTO students (first_name, last_name, city_id) VALUES (?, ?, ?)', student)

        cities = fetch_all(connect, 'SELECT id, title FROM cities')
        print("\nList of cities:")
        for city in cities:
            print(f"{city[0]}. {city[1]}")

        while True:
            city_id = input('\nEnter the city id to display students (0 to exit): ')
            if city_id == '0':
                print('You have successfully exited the program.')
                break
            else:
                display_students_by_city_id(connect, city_id)

        connect.close()
        print("Connection closed.")


def display_students_by_city_id(connection, city_id):
    students = fetch_all(connection, '''
        SELECT st.first_name, st.last_name, co.title AS country, ci.title AS city, ci.area
        FROM students AS st
        INNER JOIN cities AS ci ON st.city_id = ci.id
        INNER JOIN countries AS co ON ci.country_id = co.id
        WHERE ci.id = ?
    ''', (city_id,))

    if students:
        print(f'\nList of students in the selected city (ID {city_id}):')
        for student in students:
            print(
                f'Name: {student[0]}, Last Name: {student[1]}, Country: {student[2]}, City: {student[3]}, Area: {student[4]} million sq. km')
    else:
        print(f'No students found in the selected city (ID {city_id}).')


if __name__ == "__main__":
    main()

