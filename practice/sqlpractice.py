import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()
# c.execute("CREATE TABLE tickets (id INTEGER, issue TEXT, status TEXT)")
# c.execute("INSERT INTO tickets VALUES (1, 'login bug', 'open')")
# c.execute("INSERT INTO tickets VALUES (2, 'slow page', 'open')")
# c.execute("INSERT INTO tickets VALUES (3, 'crash', 'closed')")
# conn.commit()

c.execute('SELECT * FROM tickets WHERE status is "open"')
print(c.fetchall())
c.execute('SELECT status, COUNT(*) FROM tickets GROUP BY status')
print(c.fetchall())