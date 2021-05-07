import psycopg2

host = "localhost"
database = "postgres"
username = "postgres"
password = '123456'


def connect():
    conn = psycopg2.connect(host=host, database=database, user=username, password=password)

    return conn


def insert(data):
    sql = """
            INSERT INTO user_info(fullname, phone_number, email, address)
            VALUES ('{}', '{}', '{}', '{}')
    """.format(*data)

    execute(sql, "insert")


def select_by_phone(phone_number):
    sql = """
            SELECT * FROM user_info
            WHERE phone_number = '{}'
    """.format(phone_number)

    return execute(sql, "select")


def select_by_email(email):
    sql = """
                SELECT * FROM user_info
                WHERE email = '{}'
        """.format(email)

    return execute(sql, "select")


def select_by_address(address):
    sql = """
                    SELECT * FROM user_info
                    WHERE address = '{}'
            """.format(address)

    return execute(sql, "select")


def select_all():
    sql = """
            SELECT * FROM user_info
                        
        """

    return execute(sql, "select")


def check_exist(fullname, phone_number, email, address):
    sql = """
                SELECT * FROM user_info
                WHERE fullname = '{}' AND phone_number = '{}' AND email = '{}' AND address = '{}' 
            """.format(fullname, phone_number, email, address)

    return execute(sql, "select")


def group_by_address():
    sql = """
        SELECT address, count(*) as number FROM user_info
        GROUP BY address
    """

    return execute(sql, "select")


def update(fullname, phone_number, email, address, status):
    sql = """
        UPDATE user_info
        SET fullname = '{}',
            phone_number = '{}',
            email = '{}',
            address = '{}',
            status = '{}'
        WHERE phone_number = '{}'
    """.format(fullname, phone_number, email, address, status, phone_number)

    return execute(sql, "update")


def group_by_status():
    sql = """
            SELECT status, count(*) as number FROM user_info
            GROUP BY status
        """

    return execute(sql, "select")
def execute(sql, type):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(sql)
    conn.commit()
    result = []
    if type == "select":
        result = cursor.fetchall()

    conn.close()
    if (result):
        return result

    else:
        return None
