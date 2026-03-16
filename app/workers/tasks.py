from redis import Redis
from rq import Queue

redis_conn = Redis()
queue = Queue(connection=redis_conn)

def run_scraper():

    from app.services.property_scraper import get_properties

    return get_properties()
