import pg8000.dbapi as db
import os

from dotenv import load_dotenv
load_dotenv()



def create_db_connection():

    try:
        conn = db.connect(
            host = os.getenv("ENDPOINT"),
            port = os.getenv("PORT"),
            database = os.getenv("DB_NAME"),
            user = os.getenv("DB_USERNAME"),
            password = os.getenv("DB_PASSWORD")
        )

        return conn
    except:
        raise "unable to connect to db"


def post_event(event: dict):
    conn = create_db_connection()

    with create_db_connection() as conn:
        cur = conn.cursor()

        query = f'''INSERT INTO events (title, description, start_date)
                  VALUES 
                        (   {event["title"]}, 
                            {event["description"]}, 
                            {event["start_date"]} )'''
        cur.execute(query)

        data = cur.fetchall()

    return data

def get_all_events():

    with create_db_connection() as conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM events")
        data = cur.fetchall()

    #change
    #convert list to dict to make json seralizable
    serialized_data = [json_seralize_event(row) for row in data]
        
    return serialized_data

    
def json_seralize_event(event: list):
    return {
        "id": event[0],
        "title": event[1],
        "description": event[2],
        "date": str(event[3])
    } 


def validate_event_data(data: dict):
    #check validity of title and
    print("")