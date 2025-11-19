import sqlalchemy as sa
import os

# Get DB credentials from Environment Variables (passed via Docker command later)
# Default to 'localhost' for testing outside docker, but inside Docker it must be the container name
db_host = os.environ.get('MYSQL_HOST', 'localhost') 
db_user = os.environ.get('MYSQL_USER', 'user')
db_pass = os.environ.get('MYSQL_PASSWORD', 'password')
db_name = os.environ.get('MYSQL_DATABASE', 'chatdb')

url = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}"

engine = sa.create_engine(url)
metadata = sa.MetaData()

# Define Table
user_table = sa.Table(
    "chat_data",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("room_id", sa.String(50)),
    sa.Column("timestamp", sa.String(50)),
    sa.Column("username", sa.String(50)),
    sa.Column("message", sa.Text),
)

def init_db():
    """Create tables"""
    metadata.create_all(engine)

def insert_message(room_id, timestamp, username, message):
    with engine.connect() as conn:
        query = user_table.insert().values(
            room_id=room_id, timestamp=timestamp, username=username, message=message
        )
        conn.execute(query)
        conn.commit()

def select_room(room_id):
    with engine.connect() as conn:
        query = user_table.select().where(user_table.c.room_id == room_id)
        result = conn.execute(query)
        messages = []
        for row in result:
            messages.append({
                "timestamp": row.timestamp,
                "sender": row.username,
                "text": row.message
            })
        return messages