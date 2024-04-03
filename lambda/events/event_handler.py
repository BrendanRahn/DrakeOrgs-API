import pg8000.dbapi as db
import os
import ssl

from dotenv import load_dotenv
load_dotenv()



def create_db_connection(): 
    
    #pg8000 needs CA file to be passed to it, make sure RDS CA file is in root dir of 
    ssl_context = ssl.create_default_context()
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    ssl_context.load_verify_locations('us-east-1-bundle.pem')


    try:
        conn = db.connect(
            host = os.getenv("ENDPOINT"),
            port = os.getenv("PORT"),
            database = os.getenv("DB_NAME"),
            user = os.getenv("DB_USERNAME"),
            password = os.getenv("DB_PASSWORD"),
            ssl_context=ssl_context
        )

        return conn
    except Exception as error:
        raise error


def post_event(event: dict):

    conn = create_db_connection()

    cur = conn.cursor()
    

    

def get_all_events():

    conn = create_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM events")
    data = cur.fetchall()

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


def validate_handler_data(data: dict):
    #check validity of title and
    print("")