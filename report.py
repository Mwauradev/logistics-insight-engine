from analyzer import load_data, analyze
from ai_insights import generate_logistics_insight
from pdf_exporter import export_logistics_pdf

df = load_data('data/logistics_data.csv')
results = analyze(df)

print("=" * 50)
print("   LOGISTICS PERFORMANCE ANALYSIS")
print("=" * 50)
print(f"  Delivery Rate      : {results['overall_delivery_rate']}%")
print(f"  Total Fuel Cost    : KES {results['total_fuel_cost']:,}")
print(f"  Total Distance     : {results['total_distance']:,} km")
print(f"  Avg Delay          : {results['avg_delay_minutes']} mins")
print(f"  Best Route         : {results['best_route']}")
print(f"  Worst Route        : {results['worst_route']}")
print(f"  Best Driver        : {results['best_driver']}")
print(f"  Most Delayed Driver: {results['most_delayed_driver']}")
print("=" * 50)

print("\n  AI EXECUTIVE INSIGHT")
print("=" * 50)
insight = generate_logistics_insight(results)
print(insight)
print("=" * 50)

# Export PDF
print("\n  Exporting PDF report...")
export_logistics_pdf(results, insight)
print("  Report complete.")