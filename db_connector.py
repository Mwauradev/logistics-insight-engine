import psycopg2
import pandas as pd
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

def get_connection():
    return psycopg2.connect(
        host = DB_HOST,
        database = DB_NAME,
        user = DB_USER,
        password = DB_PASSWORD,
        port = DB_PORT
    )
 
def fetch_trip_data() -> pd.DataFrame:
    conn = get_connection()

    query = """
        SELECT
            t.trip_date,
            r.route_name AS route,
            d.driver_name AS driver,
            v.plate_number AS vehicle, 
            t.deliveries_scheduled,
            t.deliveries_completed,
            t.fuel_cost,
            t.distance_km,
            t.delay_minutes,
            t.cargo_weight_kg
        FROM trips t
        JOIN routes r ON  t.route_id = r.id
        JOIN drivers d ON t.driver_id = d.id
        JOIN vehicles v ON t.vehicle_id = v.id
        ORDER BY t.trip_date;

    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def fetch_route_perfomance() -> pd.DataFrame:
    conn = get_connection()

    query = """
        SELECT
            r.route_name 
            ROUND(SUM(t.deliveries_completed)::numeric /
            SUM(t.deliveries_scheduled) * 100,1) AS avg_delivery_rate,
            SUM(t.fuel_cost) AS total_fuel_cost,
            ROUND(AVG(t.delay_minutes), 1) AS avg_delay,
            SUM(t.deliveries_completed) AS total_deliveries
        FROM trips t
        JOIN routes r ON  t.route_id = r.id
        GROUP BY  r.route_name
        ORDER BY avg_delivery_rate DESC;

    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def fetch_driver_perfomance() -> pd.DataFrame:
    conn = get_connection()

    query = """
        SELECT
            d.driver_name 
            ROUND(SUM(t.deliveries_completed)::numeric /
            SUM(t.deliveries_scheduled) * 100,1) AS avg_delivery_rate,
            SUM(t.delay_minutes) AS total_delay,
            SUM(t.deliveries_completed) AS total_deliveries
        FROM trips t
        JOIN drivers d ON  t.driver_id = d.id
        GROUP BY  d.driver_name
        ORDER BY avg_delivery_rate DESC;

    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

if __name__ == "__main__":
    print("Testing database connection...")
    df = fetch_trip_data()
    print(f"Fetched {len(df)} trips from database")
    print(df.head())