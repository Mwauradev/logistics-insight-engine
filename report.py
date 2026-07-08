from analyzer import load_data, analyze
from ai_insights import generate_logistics_insight
from pdf_exporter import export_logistics_pdf

print("  Connecting to database...")
df = load_data()
print(f"  Loaded {len(df)} trips from PostgreSQL\n")

results = analyze(df)

print("=" * 50)
print("   LOGISTICS PERFORMANCE REPORT")
print("   Powered by PostgreSQL + Groq AI")
print("=" * 50)
print(f"  Delivery Rate         : {results['overall_delivery_rate']}%")
print(f"  Total Fuel Cost       : KES {results['total_fuel_cost']:,.0f}")
print(f"  Total Distance        : {results['total_distance']:,.0f} km")
print(f"  Avg Delay             : {results['avg_delay_minutes']} mins")
print(f"  Total Cargo           : {results['total_cargo_kg']:,.0f} kg")
print(f"  Best Route            : {results['best_route']}")
print(f"  Worst Route           : {results['worst_route']}")
print(f"  Best Driver           : {results['best_driver']}")
print(f"  Most Delayed Driver   : {results['most_delayed_driver']}")
print(f"  Most Efficient Vehicle: {results['most_efficient_vehicle']}")
print("=" * 50)

print("\n  ROUTE PERFORMANCE")
print("-" * 50)
print(results['route_performance'].to_string())

print("\n  DRIVER PERFORMANCE")
print("-" * 50)
print(results['driver_performance'].to_string())
print("=" * 50)

print("\n  Generating AI insight...")
insight = generate_logistics_insight(results)
print("\n  AI EXECUTIVE INSIGHT")
print("=" * 50)
print(insight)
print("=" * 50)

print("\n  Exporting PDF report...")
export_logistics_pdf(results, insight)
print("  Pipeline complete. Database → Analysis → AI → PDF")