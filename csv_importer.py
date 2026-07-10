import pandas as pd
from sqlalchemy import text
from db_connector import get_engine
from validator import validate_csv, print_validation_report

def get_or_create(conn, table: str, column: str, value: str) -> int:
    result = conn.execute(
        text(f"SELECT id FROM {table} WHERE {column} = :value"),
        {"value": value}
    ).fetchone()
    
    if result:
        return result[0]
    
    result = conn.execute(
        text(f"INSERT INTO {table} ({column}) VALUES (:value) RETURNING id"),
        {"value": value}
    )
    conn.commit()
    return result.fetchone()[0]

def import_csv(filepath: str) -> dict:
    print(f"\n  Starting import: {filepath}")
    print("=" * 50)
    
    # Validate first
    df, errors = validate_csv(filepath)
    
    if errors:
        print("  IMPORT FAILED — Validation errors:")
        for error in errors:
            print(f"\n  ❌ {error}")
        return {'success': False, 'errors': errors, 'imported': 0}
    
    engine = get_engine()
    imported = 0
    skipped = 0
    import_errors = []
    
    with engine.connect() as conn:
        for i, row in df.iterrows():
            try:
                # Get or create foreign key IDs
                route_id = get_or_create(
                    conn, 'routes', 'route_name', str(row['route'])
                )
                driver_id = get_or_create(
                    conn, 'drivers', 'driver_name', str(row['driver'])
                )
                vehicle_id = get_or_create(
                    conn, 'vehicles', 'plate_number', str(row['vehicle'])
                )
                
                # Insert trip
                conn.execute(text("""
                    INSERT INTO trips (
                        trip_date, route_id, driver_id, vehicle_id,
                        deliveries_scheduled, deliveries_completed,
                        fuel_cost, distance_km, delay_minutes, cargo_weight_kg
                    ) VALUES (
                        :trip_date, :route_id, :driver_id, :vehicle_id,
                        :deliveries_scheduled, :deliveries_completed,
                        :fuel_cost, :distance_km, :delay_minutes, :cargo_weight_kg
                    )
                """), {
                    'trip_date': row['date'],
                    'route_id': route_id,
                    'driver_id': driver_id,
                    'vehicle_id': vehicle_id,
                    'deliveries_scheduled': int(row['deliveries_scheduled']),
                    'deliveries_completed': int(row['deliveries_completed']),
                    'fuel_cost': float(row['fuel_cost']),
                    'distance_km': float(row['distance_km']),
                    'delay_minutes': int(row['delay_minutes']),
                    'cargo_weight_kg': float(row['cargo_weight_kg'])
                })
                conn.commit()
                imported += 1
                
            except Exception as e:
                skipped += 1
                import_errors.append(f"Row {i+1}: {str(e)}")
    
    print(f"\n  IMPORT COMPLETE")
    print(f"  ✅ {imported} trips imported successfully")
    if skipped > 0:
        print(f"  ⚠️  {skipped} rows skipped")
        for err in import_errors[:5]:
            print(f"     {err}")
    
    return {
        'success': True,
        'imported': imported,
        'skipped': skipped,
        'errors': import_errors
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python csv_importer.py <path_to_csv>")
        print("Example: python csv_importer.py data/new_trips.csv")
    else:
        result = import_csv(sys.argv[1])