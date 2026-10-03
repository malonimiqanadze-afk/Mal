class CarelineEstimateCalculator:
    def __init__(self):
        # Base pricing model ($490 for 2 labor hours = $245/hr)
        self.hourly_rate = 245.00
        self.min_labor_hours = 2
        
        # Item catalog with volume (cu ft) and weight (lbs)
        self.catalog = {
            "3-Seater Sofa": {"volume": 50, "weight": 150},
            "2-Seater Loveseat": {"volume": 35, "weight": 100},
            "Armchair / Recliner": {"volume": 18, "weight": 55},
            "Coffee Table": {"volume": 12, "weight": 35}
        }
        
        # Current quantities selected by the user
        self.inventory = {item: 0 for item in self.catalog}
        
        # Vehicle capacity in cu ft
        self.vehicles = [
            {"name": "Luton / Large Sprinter Van", "capacity": 450},
            {"name": "7.5 Tonne Lorry", "capacity": 1200} # Example tier up
        ]
        
        # Packing efficiency (85% rule)
        self.packing_efficiency = 0.85 

    def update_quantity(self, item_name, quantity):
        if item_name in self.inventory and quantity >= 0:
            self.inventory[item_name] = quantity

    def calculate_totals(self):
        total_volume = 0
        total_weight = 0
        total_items = 0
        
        for item, qty in self.inventory.items():
            if qty > 0:
                total_volume += self.catalog[item]["volume"] * qty
                total_weight += self.catalog[item]["weight"] * qty
                total_items += qty
                
        return total_items, total_volume, total_weight

    def get_vehicle_recommendation(self, total_volume):
        required_capacity = total_volume / self.packing_efficiency if total_volume > 0 else 0
        
        for vehicle in self.vehicles:
            if vehicle["capacity"] >= required_capacity:
                return vehicle
        
        return {"name": "Multiple Vehicles Required", "capacity": sum(v["capacity"] for v in self.vehicles)}

    def calculate_estimate(self):
        total_items, total_volume, total_weight = self.calculate_totals()
        
        # Dynamic labor hour calculation based on volume (example scaling logic)
        labor_hours = self.min_labor_hours
        if total_volume > 200:
            # Add 1 hour for every 150 cu ft over the base 200
            extra_hours = (total_volume - 200) // 150
            labor_hours += extra_hours
            
        estimated_cost = labor_hours * self.hourly_rate
        recommended_vehicle = self.get_vehicle_recommendation(total_volume)
        usable_capacity = recommended_vehicle["capacity"] * self.packing_efficiency if recommended_vehicle["capacity"] else 0
        
        # Format the output just like the Live Estimate panel
        return {
            "live_estimate": f"${estimated_cost:,.0f}",
            "details": f"{total_items} items · {labor_hours} labour hrs",
            "total_volume": f"{total_volume} cu ft",
            "est_weight": f"{total_weight} lbs",
            "recommended_vehicle": recommended_vehicle["name"],
            "vehicle_capacity": f"{recommended_vehicle['capacity']} cu ft",
            "capacity_status": f"{(total_volume/usable_capacity*100) if usable_capacity > 0 else 0:.0f}% of rated capacity · {total_volume} cu ft packed (85% rule)"
        }

# --- Example Usage ---
calculator = CarelineEstimateCalculator()

# Simulating user clicking the "+" button on items
calculator.update_quantity("3-Seater Sofa", 1)
calculator.update_quantity("Coffee Table", 2)
calculator.update_quantity("Armchair / Recliner", 1)

# Generate the Live Estimate
dashboard_data = calculator.calculate_estimate()

for key, value in dashboard_data.items():
    print(f"{key.upper()}: {value}")