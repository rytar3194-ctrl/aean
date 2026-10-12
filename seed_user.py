import sqlite3
import datetime
import bcrypt

con = sqlite3.connect('backend/eyan_ai.db')
cur = con.cursor()

now = datetime.datetime.utcnow().isoformat()
h = bcrypt.hashpw(b'123456', bcrypt.gensalt()).decode('utf-8')
h5 = bcrypt.hashpw(b'12345', bcrypt.gensalt()).decode('utf-8')

cur.execute("SELECT id FROM roles WHERE name='Admin'")
admin_role = cur.fetchone()
admin_role_id = admin_role[0] if admin_role else 1

cur.execute("""
INSERT OR REPLACE INTO users (id, username, email, password_hash, full_name, role_id, is_active, created_at, updated_at)
VALUES (3, 'dr_safwan', 'safwan@gmail.com', ?, 'د. صفوان محمد', ?, 1, ?, ?)
""", (h, admin_role_id, now, now))

cur.execute("UPDATE users SET password_hash = ? WHERE username IN ('admin', 'instructor')", (h5,))

con.commit()
print("Successfully configured users with bcrypt hashed passwords:")
for u in cur.execute("SELECT id, username, email, full_name, password_hash FROM users").fetchall():
    print(f"User {u[0]}: {u[1]} ({u[2]}) - {u[3]} - Hash: {u[4][:15]}...")
con.close()
