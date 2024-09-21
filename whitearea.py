
Here’s the complete white area filter code for both Demand Zone and Supply Zone. You can paste this directly into your strategy's code where the zone validation happens.

Complete White Area Filter Code:





# Demand Zone White Area Filter (legout_open >= boring_candle_body)
def apply_white_area_filter_demand(stock_data, legout_index, boring_candle_index):
    # Calculate the body of the boring candle
    boring_candle_body = abs(stock_data['Close'].iloc[boring_candle_index] - stock_data['Open'].iloc[boring_candle_index])
    
    # Get the opening price of the legout candle
    legout_open = stock_data['Open'].iloc[legout_index]
    
    # Apply white area filter for demand zone
    if legout_open >= boring_candle_body:
        return True  # Filter passed
    else:
        return False  # Filter failed

# Supply Zone White Area Filter (legout_open <= boring_candle_body)
def apply_white_area_filter_supply(stock_data, legout_index, boring_candle_index):
    # Calculate the body of the boring candle
    boring_candle_body = abs(stock_data['Close'].iloc[boring_candle_index] - stock_data['Open'].iloc[boring_candle_index])
    
    # Get the opening price of the legout candle
    legout_open = stock_data['Open'].iloc[legout_index]
    
    # Apply white area filter for supply zone
    if legout_open <= boring_candle_body:
        return True  # Filter passed
    else:
        return False  # Filter failed





Integrating the Filters in Your Main Code:
For Demand Zone:

# Assuming 'i' is the index of the legout candle and 'i-1' is the boring candle
if scan_demand_zone_allowed and (stock_data['Close'].iloc[i] > stock_data['Open'].iloc[i]):
    # Apply the white area filter for demand zone
    if apply_white_area_filter_demand(stock_data, i, i-1):
        # Continue with your existing zone validation logic
        first_legout_candle_body = abs(stock_data['Close'].iloc[i] - stock_data['Open'].iloc[i])
        first_legout_candle_range = (stock_data['High'].iloc[i] - stock_data['Low'].iloc[i])
        
        if first_legout_candle_body >= 0.5 * first_legout_candle_range:
            condition_met = True
        else:
            condition_met = False
    else:
        condition_met = False


For Supply Zone:



# Assuming 'i' is the index of the legout candle and 'i-1' is the boring candle
if scan_supply_zone_allowed and (stock_data['Open'].iloc[i] > stock_data['Close'].iloc[i]):
    # Apply the white area filter for supply zone
    if apply_white_area_filter_supply(stock_data, i, i-1):
        # Continue with your existing zone validation logic
        first_legout_candle_body = abs(stock_data['Close'].iloc[i] - stock_data['Open'].iloc[i])
        first_legout_candle_range = (stock_data['High'].iloc[i] - stock_data['Low'].iloc[i])
        
        if first_legout_candle_body >= 0.5 * first_legout_candle_range:
            condition_met = True
        else:
            condition_met = False
    else:
        condition_met = False



How to Use:
Copy and paste the apply_white_area_filter_demand and apply_white_area_filter_supply functions into your code.
Use the respective function calls inside the zone validation logic for demand and supply zones.
This code ensures that the white area filter is applied properly based on the zone type (demand or supply).





candle behind legin





def is_candle_behind_legin(stock_data, legin_index):
    """
    This function checks if the candle just before the legin candle is opposite in color
    and covers at least 50% of the legin candle's body.
    """
    # Get the legin candle and the candle just before it
    legin_candle = stock_data.iloc[legin_index]
    previous_candle = stock_data.iloc[legin_index - 1]
    
    # Calculate body sizes (absolute difference between Close and Open)
    legin_body_size = abs(legin_candle['Close'] - legin_candle['Open'])
    previous_body_size = abs(previous_candle['Close'] - previous_candle['Open'])

    # Check for opposite color
    opposite_color = ((legin_candle['Close'] > legin_candle['Open'] and previous_candle['Close'] < previous_candle['Open']) or
                      (legin_candle['Close'] < legin_candle['Open'] and previous_candle['Close'] > previous_candle['Open']))

    # Check if the previous candle covers at least 50% of the legin candle's body
    covers_50_percent = previous_body_size >= 0.5 * legin_body_size

    # Return True if both conditions are met (opposite color and 50% body coverage)
    return opposite_color and covers_50_percent

def filter_candle_behind_legin(stock_data, legin_indexes):
    """
    This function applies the 'candle behind legin' validation to filter out candles
    that don't meet the condition. It works for both demand and supply zones.
    """
    valid_legin_indexes = []
    for legin_index in legin_indexes:
        if not is_candle_behind_legin(stock_data, legin_index):
            valid_legin_indexes.append(legin_index)
    return valid_legin_indexes

def apply_candle_behind_legin_to_zones(stock_data, demand_legin_indexes, supply_legin_indexes):
    """
    Apply 'candle behind legin' logic to both demand and supply zones.
    """
    valid_demand_legins = filter_candle_behind_legin(stock_data, demand_legin_indexes)
    valid_supply_legins = filter_candle_behind_legin(stock_data, supply_legin_indexes)

    return valid_demand_legins, valid_supply_legins


tr vs atr

# Assuming 'i' is the index of the legout candle and 'i-1' is the boring candle
def apply_tr_vs_atr_filter(stock_data, legin_candle_index, legout_candle_index, boring_candle_index):
    # Calculate TR for legin, legout, and boring candles
    def calculate_tr(row):
        tr1 = abs(row['High'] - row['Low'])
        tr2 = abs(row['High'] - row['previous_close'])
        tr3 = abs(row['Low'] - row['previous_close'])
        return max(tr1, tr2, tr3)

    # Calculate TR for legin, legout, and boring candles
    legin_tr = calculate_tr(stock_data.iloc[legin_candle_index])
    legout_tr = calculate_tr(stock_data.iloc[legout_candle_index])
    boring_tr = calculate_tr(stock_data.iloc[boring_candle_index])

    # Get ATR for the corresponding candles
    legin_atr = stock_data['ATR'].iloc[legin_candle_index]
    legout_atr = stock_data['ATR'].iloc[legout_candle_index]
    boring_atr = stock_data['ATR'].iloc[boring_candle_index]

    # Apply the filter: legin_tr > legin_atr, legout_tr > legout_atr, boring_tr < boring_atr
    if (legin_tr > legin_atr) and (legout_tr > legout_atr) and (boring_tr < boring_atr):
        return True  # Filter passed
    else:
        return False  # Filter failed






tr vs atr


# Assuming 'i' is the index of the legout candle and 'i-1' is the boring candle
def apply_tr_vs_atr_filter(stock_data, legin_candle_index, legout_candle_index, boring_candle_index):
    # Calculate TR for legin, legout, and boring candles
    def calculate_tr(row):
        tr1 = abs(row['High'] - row['Low'])
        tr2 = abs(row['High'] - row['previous_close'])
        tr3 = abs(row['Low'] - row['previous_close'])
        return max(tr1, tr2, tr3)

    # Calculate TR for legin, legout, and boring candles
    legin_tr = calculate_tr(stock_data.iloc[legin_candle_index])
    legout_tr = calculate_tr(stock_data.iloc[legout_candle_index])
    boring_tr = calculate_tr(stock_data.iloc[boring_candle_index])

    # Get ATR for the corresponding candles
    legin_atr = stock_data['ATR'].iloc[legin_candle_index]
    legout_atr = stock_data['ATR'].iloc[legout_candle_index]
    boring_atr = stock_data['ATR'].iloc[boring_candle_index]

    # Apply the filter: legin_tr > legin_atr, legout_tr > legout_atr, boring_tr < boring_atr
    if (legin_tr > legin_atr) and (legout_tr > legout_atr) and (boring_tr < boring_atr):
        return True  # Filter passed
    else:
        return False  # Filter failed





How to Integrate This Filter:
Identify the indices for the legin, legout, and boring candles in your strategy.
Apply the TR vs ATR Filter within the zone validation logic.
Here’s an example of how you can apply this filter during zone validation:

Integrating Into the Zone Validation:
python
Copy code
# Assuming 'legin_candle_index', 'legout_candle_index', and 'i-1' (boring_candle) are already identified

# Apply the TR vs ATR filter
if apply_tr_vs_atr_filter(stock_data, legin_candle_index, i, i-1):
    # Proceed with the rest of the validation (like white area filter and ATR checks)
    condition_met = True
else:
    condition_met = False
Explanation:
legin_candle_index: Index of the legin candle (before the base).
i: Index of the legout candle (breakout candle).
i-1: Index of the boring candle (small base candle).
This will ensure the filter checks that TR > ATR for legin and legout candles, and TR < ATR for boring candles






To implement the **"formation of legout"** validation, we need to calculate the range of the **legin** candle and compare it to the opening price of the **legout** candle. The condition will vary for demand and supply zones:

- **Demand Zone**: The legout's opening price should not be more than **twice the range** of the legin.
- **Supply Zone**: The legout's opening price should not be **less than twice** the range of the legin.

If the conditions are violated, we'll filter out such zones.

### Here's how to implement this validation in Python:

1. **Calculate the Range of the Legin Candle**:
   The range of the legin candle is the difference between its **high** and **low** prices.
   
2. **Apply the Validation for Demand and Supply Zones**:
   - **Demand**: If the legout's opening price is more than twice the legin's range, filter it out.
   - **Supply**: If the legout's opening price is less than twice the legin's range, filter it out.

Here’s the Python code to add this validation:

```python
def validate_formation_of_legout(zones):
    validated_zones = []

    for zone in zones:
        legin_high = zone['legin_high']
        legin_low = zone['legin_low']
        legout_open = zone['legout_open']
        zone_type = zone['zone_type']  # 'demand' or 'supply'
        
        # Calculate the legin range
        legin_range = legin_high - legin_low

        # Validation for demand zone
        if zone_type == 'demand':
            if legout_open <= 2 * legin_range:
                validated_zones.append(zone)
            else:
                print(f"Filtered out demand zone: {zone['symbol']} (Legout open too high)")

        # Validation for supply zone
        elif zone_type == 'supply':
            if legout_open >= 2 * legin_range:
                validated_zones.append(zone)
            else:
                print(f"Filtered out supply zone: {zone['symbol']} (Legout open too low)")

    return validated_zones
```

### Explanation:
- **legin_range**: The difference between the **high** and **low** of the legin candle.
- **Demand Validation**: If the legout's opening price is **more** than twice the legin range, it's filtered out.
- **Supply Validation**: If the legout's opening price is **less** than twice the legin range, it's filtered out.

### How to Integrate This:
You can call this `validate_formation_of_legout` function in the part of your code where the zones are being processed before further analysis (e.g., backtesting or displaying).

Example usage:

```python
zones = [
    {'symbol': 'AAPL', 'zone_type': 'demand', 'legin_high': 150, 'legin_low': 140, 'legout_open': 285},
    {'symbol': 'TSLA', 'zone_type': 'supply', 'legin_high': 700, 'legin_low': 680, 'legout_open': 1390},
    # Add more zones here
]

validated_zones = validate_formation_of_legout(zones)

# Now, validated_zones contains only the zones that passed the "formation of legout" validation
```

### What’s Next?
- Let me know if you'd like to integrate this directly into your existing code, or if you need help modifying your current zone processing logic to include this validation.
- If you need any changes or further explanation, feel free to ask!

