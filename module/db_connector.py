import psycopg2

host = "localhost"
database = "postgres"
username = "postgres"
password = '123456'


def connect():
    conn = psycopg2.connect(host=host, database=database, user=username, password=password)

    return conn


def insert(data):
    conn = connect()

    cursor = conn.cursor()

    sql = """
            INSERT INTO user_info(fullname, phone_number, email, address)
            VALUES ('{}', '{}', '{}', '{}')
    """.format(*data)

    result = cursor.execute(sql)

    conn.commit()

    conn.close()

    print("Insert Success")


def select_by_phone(phone_number):
    conn = connect()
    cursor = conn.cursor()

    sql = """
            SELECT * FROM user_info
            WHERE phone_number = '{}'
    """.format(phone_number)

    # print(rows)

    cursor.execute(sql)
    conn.commit()

    rows = cursor.fetchall()
    conn.close()
    result = []

    if rows:
        print(phone_number, "has exist.")
        result = rows[0]

    return result


def select_by_email(email):
    conn = connect()
    cursor = conn.cursor()

    sql = """
                SELECT * FROM user_info
                WHERE email = '{}'
        """.format(email)

    cursor.execute(sql)
    conn.commit()

    rows = cursor.fetchall()
    conn.close()
    result = []

    # print(rows)

    if rows:
        print(email, "has exist.")
        result = rows[0]

    return result


