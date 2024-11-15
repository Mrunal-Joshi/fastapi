import psycopg2

try:
    conn = psycopg2.connect(
        database = "fastapi",
        user = "postgres",
        password = "2810",
        host = "localhost",
        port = "5432"
    )  # creates a new database session
    print("CONNECTED SUCCESSFULLY")

    cursor = conn.cursor()  ## alllows interaction with the server
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print("POSTS", posts)
except:
    print("DB NOT CONNECTED")