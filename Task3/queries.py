import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="pythonadmin",
    password="password1234",
    database="mysql"
)
cursorObj = mydb.cursor()
username_query = "SELECT * FROM user__ WHERE username="
scrape_check = "SELECT scrape_done FROM user__ WHERE username="
all_sql = "SELECT name, work, city,favs FROM user__ WHERE username = %s"
update_sql = "UPDATE user__ SET scrape_done = %s, name=%s,work=%s,city=%s,favs=%s WHERE username=%s"