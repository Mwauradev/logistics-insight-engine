import pandas as pd
from typing import Tuple

REQUIRED_COLUMNS = {
    'date': ['date', 'trip_date', 'tarehe'],
    'route': ['route', 'route_name', 'njia'],
    'driver': ['driver', 'driver_name', 'dereva'],
    'vehicle': ['vehicle', 'plate_number', 'gari'],
    'deliveries_scheduled': ['deliveries_scheduled', 'scheduled', 'planned'],
    'deliveries_completed': ['deliveries_completed', 'completed', 'delivered'],
    'fuel_cost': ['fuel_cost', 'fuel', 'mafuta', 'fuel_expense'],
    'distance_km': ['distance_km', 'distance', 'km', 'umbali'],
    'delay_minutes': ['delay_minutes', 'delay', 'delays', 'kuchelewa'],
    'cargo_weight_kg': ['cargo_weight_kg', 'cargo_weight', 'weight', 'cargo']
}

def detect_column_mapping(df_columns: list) -> Tuple[dict, list]:
    mapping = {}
    missing = []
    
    df_columns_lower = [col.lower().strip() for col in df_columns]
    
    for standard_name, alternatives in REQUIRED_COLUMNS.items():
        found = False
        for alt in alternatives:
            if alt.lower() in df_columns_lower:
                actual_index = df_columns_lower.index(alt.lower())
                mapping[df_columns[actual_index]] = standard_name
                found = True
                break
        if not found:
            missing.append(standard_name)
    
    return mapping, missing

def validate_csv(filepath: str) -> Tuple[pd.DataFrame, list]:
    errors = []
    
    # Check file exists and is readable
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        return None, [f"File not found: {filepath}"]
    except Exception as e:
        return None, [f"Could not read file: {str(e)}"]
    
    # Check for empty file
    if df.empty:
        return None, ["The CSV file is empty. Please provide data."]
    
    # Detect column mapping
    mapping, missing = detect_column_mapping(list(df.columns))
    
    if missing:
        found_similar = []
        for col in df.columns:
            for standard, alternatives in REQUIRED_COLUMNS.items():
                if any(alt in col.lower() for alt in alternatives):
                    found_similar.append(f"  Found '{col}' — did you mean '{standard}'?")
        
        error_msg = f"Missing required columns: {', '.join(missing)}"
        if found_similar:
            error_msg += "\n" + "\n".join(found_similar)
        error_msg += "\n\nPlease use the provided CSV template."
        errors.append(error_msg)
        return None, errors
    
    # Rename columns to standard names
    df = df.rename(columns=mapping)
    
    # Validate data types and values
    try:
        df['date'] = pd.to_datetime(df['date'])
    except Exception:
        errors.append("Column 'date' contains invalid date values. Use format YYYY-MM-DD.")
    
    numeric_columns = [
        'deliveries_scheduled', 'deliveries_completed',
        'fuel_cost', 'distance_km', 'delay_minutes', 'cargo_weight_kg'
    ]
    
    for col in numeric_columns:
        if col in df.columns:
            non_numeric = pd.to_numeric(df[col], errors='coerce').isna().sum()
            if non_numeric > 0:
                errors.append(
                    f"Column '{col}' contains {non_numeric} non-numeric value(s). "
                    f"All values must be numbers."
                )
    
    # Check for negative values
    for col in ['fuel_cost', 'distance_km', 'deliveries_scheduled']:
        if col in df.columns:
            if pd.to_numeric(df[col], errors='coerce').lt(0).any():
                errors.append(f"Column '{col}' contains negative values. Please check your data.")
    
    # Check delivery logic
    if 'deliveries_completed' in df.columns and 'deliveries_scheduled' in df.columns:
        invalid = (
            pd.to_numeric(df['deliveries_completed'], errors='coerce') >
            pd.to_numeric(df['deliveries_scheduled'], errors='coerce')
        ).sum()
        if invalid > 0:
            errors.append(
                f"{invalid} row(s) have more completions than scheduled. "
                f"Please verify your data."
            )
    
    if errors:
        return None, errors
    
    return df, []

def print_validation_report(filepath: str):
    print(f"\n  Validating: {filepath}")
    print("-" * 50)
    
    df, errors = validate_csv(filepath)
    
    if errors:
        print("  VALIDATION FAILED")
        for error in errors:
            print(f"\n  ❌ {error}")
        print("\n  Please fix the errors above and try again.")
        return None
    
    print(f"  ✅ Validation passed")
    print(f"  ✅ {len(df)} rows ready for import")
    print(f"  ✅ All required columns found")
    print(f"  ✅ Data types verified")
    return df

if __name__ == "__main__":
    print_validation_report('data/bad_trips.csv')