import pandas as pd

def load_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date'])
    df['delivery_rate'] = (df['deliveries_completed'] / 
                          df['deliveries_scheduled'] * 100).round(1)
    df['cost_per_km'] = (df['fuel_cost'] / 
                        df['distance_km']).round(2)
    df['cost_per_delivery'] = (df['fuel_cost'] / 
                              df['deliveries_completed']).round(2)
    return df

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

    # Best and worst routes
    route_performance = df.groupby('route').agg(
        avg_delivery_rate=('delivery_rate', 'mean'),
        total_fuel_cost=('fuel_cost', 'sum'),
        avg_delay=('delay_minutes', 'mean'),
        total_deliveries=('deliveries_completed', 'sum')
    ).round(2)

    best_route = route_performance['avg_delivery_rate'].idxmax()
    worst_route = route_performance['avg_delivery_rate'].idxmin()
    most_expensive_route = route_performance['total_fuel_cost'].idxmax()

    # Driver performance
    driver_performance = df.groupby('driver').agg(
        avg_delivery_rate=('delivery_rate', 'mean'),
        total_delays=('delay_minutes', 'sum'),
        total_deliveries=('deliveries_completed', 'sum')
    ).round(2)

    best_driver = driver_performance['avg_delivery_rate'].idxmax()
    most_delayed_driver = driver_performance['total_delays'].idxmax()

    # Vehicle efficiency
    vehicle_efficiency = df.groupby('vehicle').agg(
        avg_cost_per_km=('cost_per_km', 'mean'),
        total_distance=('distance_km', 'sum')
    ).round(2)

    most_efficient_vehicle = vehicle_efficiency['avg_cost_per_km'].idxmin()

    return {
        'total_deliveries_scheduled': total_deliveries_scheduled,
        'total_deliveries_completed': total_deliveries_completed,
        'overall_delivery_rate': overall_delivery_rate,
        'total_fuel_cost': total_fuel_cost,
        'total_distance': total_distance,
        'avg_delay_minutes': avg_delay,
        'total_cargo_kg': total_cargo,
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
    df = load_data('data/logistics_data.csv')
    results = analyze(df)
    
    print("=" * 50)
    print("   LOGISTICS PERFORMANCE ANALYSIS")
    print("=" * 50)
    print(f"  Delivery Rate      : {results['overall_delivery_rate']}%")
    print(f"  Total Fuel Cost    : KES {results['total_fuel_cost']:,}")
    print(f"  Total Distance     : {results['total_distance']:,} km")
    print(f"  Avg Delay          : {results['avg_delay_minutes']} mins")
    print(f"  Total Cargo        : {results['total_cargo_kg']:,} kg")
    print(f"  Best Route         : {results['best_route']}")
    print(f"  Worst Route        : {results['worst_route']}")
    print(f"  Best Driver        : {results['best_driver']}")
    print(f"  Most Delayed Driver: {results['most_delayed_driver']}")
    print(f"  Most Efficient Vehicle: {results['most_efficient_vehicle']}")
    print("=" * 50)

    print("\n  ROUTE PERFORMANCE BREAKDOWN")
    print("-" * 50)
    print(results['route_performance'].to_string())
    
    print("\n  DRIVER PERFORMANCE BREAKDOWN")
    print("-" * 50)
    print(results['driver_performance'].to_string())
    print("=" * 50)