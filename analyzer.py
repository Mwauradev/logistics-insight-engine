import pandas as pd
from db_connector import fetch_trip_data, fetch_route_performance, fetch_driver_performance

def load_data():
    return fetch_trip_data()

def analyze(df: pd.DataFrame) -> dict:
    # Overall metrics
    total_deliveries_scheduled = df['deliveries_scheduled'].sum()
    total_deliveries_completed = df['deliveries_completed'].sum()
    overall_delivery_rate = round(
        total_deliveries_completed / total_deliveries_scheduled * 100, 1
    )
    total_fuel_cost = df['fuel_cost'].sum()
    total_distance = df['distance_km'].sum()
    avg_delay = round(df['delay_minutes'].mean(), 1)
    total_cargo = df['cargo_weight_kg'].sum()

    # Pull pre-aggregated data from database
    route_performance = fetch_route_performance()
    driver_performance = fetch_driver_performance()

    # Set index for compatibility
    route_performance = route_performance.set_index('route_name')
    driver_performance = driver_performance.set_index('driver_name')

    best_route = route_performance['avg_delivery_rate'].idxmax()
    worst_route = route_performance['avg_delivery_rate'].idxmin()
    most_expensive_route = route_performance['total_fuel_cost'].idxmax()
    best_driver = driver_performance['avg_delivery_rate'].idxmax()
    most_delayed_driver = driver_performance['total_delays'].idxmax()

    # Vehicle efficiency from raw data
    vehicle_efficiency = df.groupby('vehicle').agg(
        avg_cost_per_km=('fuel_cost', 'sum')
    )
    vehicle_efficiency['avg_cost_per_km'] = (
        vehicle_efficiency['avg_cost_per_km'] /
        df.groupby('vehicle')['distance_km'].sum()
    ).round(2)
    most_efficient_vehicle = vehicle_efficiency['avg_cost_per_km'].idxmin()

    return {
        'total_deliveries_scheduled': int(total_deliveries_scheduled),
        'total_deliveries_completed': int(total_deliveries_completed),
        'overall_delivery_rate': overall_delivery_rate,
        'total_fuel_cost': float(total_fuel_cost),
        'total_distance': float(total_distance),
        'avg_delay_minutes': avg_delay,
        'total_cargo_kg': float(total_cargo),
        'best_route': best_route,
        'worst_route': worst_route,
        'most_expensive_route': most_expensive_route,
        'best_driver': best_driver,
        'most_delayed_driver': most_delayed_driver,
        'most_efficient_vehicle': most_efficient_vehicle,
        'route_performance': route_performance,
        'driver_performance': driver_performance
    }

if __name__ == "__main__":
    df = load_data()
    results = analyze(df)

    print("=" * 50)
    print("   LOGISTICS PERFORMANCE ANALYSIS")
    print("   Source: PostgreSQL Database")
    print("=" * 50)
    print(f"  Delivery Rate         : {results['overall_delivery_rate']}%")
    print(f"  Total Fuel Cost       : KES {results['total_fuel_cost']:,.0f}")
    print(f"  Total Distance        : {results['total_distance']:,.0f} km")
    print(f"  Avg Delay             : {results['avg_delay_minutes']} mins")
    print(f"  Best Route            : {results['best_route']}")
    print(f"  Worst Route           : {results['worst_route']}")
    print(f"  Best Driver           : {results['best_driver']}")
    print(f"  Most Delayed Driver   : {results['most_delayed_driver']}")
    print(f"  Most Efficient Vehicle: {results['most_efficient_vehicle']}")
    print("=" * 50)