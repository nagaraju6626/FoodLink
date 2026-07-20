import sqlite3
import random
from datetime import datetime, timedelta
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), 'food_wastage.db')

def get_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize the database with all required tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create providers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS providers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            type TEXT,
            address TEXT,
            city TEXT,
            contact TEXT,
            verified INTEGER DEFAULT 0
        )
    ''')
    
    # Create receivers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS receivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            type TEXT,
            city TEXT,
            contact TEXT
        )
    ''')
    
    # Create food_listings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS food_listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_name TEXT,
            food_type TEXT,
            meal_type TEXT,
            quantity REAL,
            unit TEXT,
            provider_id INTEGER,
            location TEXT,
            expiry_time DATETIME,
            image_url TEXT,
            status TEXT DEFAULT 'Available',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (provider_id) REFERENCES providers(id)
        )
    ''')
    
    # Create claims table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_id INTEGER,
            receiver_id INTEGER,
            quantity_claimed REAL,
            status TEXT DEFAULT 'Pending',
            claimed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (food_id) REFERENCES food_listings(id),
            FOREIGN KEY (receiver_id) REFERENCES receivers(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Sample data
PROVIDER_NAMES = [
    "Green Valley Restaurant", "Fresh Harvest Kitchen", "Metro Catering Services",
    "Sunshine Bakery", "Organic Foods Co.", "City Delights Restaurant",
    "Healthy Bites Cafe", "Royal Palace Hotel", "Community Kitchen",
    "Food For All Initiative", "Sustainable Eats", "Local Harvest Market",
    "Urban Garden Restaurant", "Farm to Table Bistro", "Neighborhood Pantry",
    "Shared Meals Program", "Zero Waste Kitchen", "Compassionate Catering",
    "Food Rescue Network", "Harvest Helpers", "Community Table",
    "Nourish Network", "Good Food Collective", "Feed The City",
    "Kitchen Angels", "Meal Share Alliance", "Food Bridge",
    "Sustainable Serving", "Caring Cuisine", "Harvest Hope",
    "Plate Full Project", "Meal Makers", "Food Forward",
    "Generous Grub", "Kind Kitchen", "Abundant Appetites",
    "Sharing Spoons", "Bountiful Bowls", "Grateful Grains",
    "Heartfelt Hospitality", "Friendly Feasts", "Wholesome Wares",
    "Plentiful Plates", "Caring Cooks", "Benevolent Bites"
]

PROVIDER_TYPES = ["Restaurant", "Hotel", "Catering", "Bakery", "Grocery Store", "Community Kitchen", "NGO"]

CITIES = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]

RECEIVER_NAMES = [
    "Hope Shelter", "Food Bank Central", "Community Outreach Center", "Salvation Army",
    "Red Cross Chapter", "Local Food Pantry", "Homeless Support Network", "Senior Care Center",
    "Youth Foundation", "Children's Home", "Veterans Support Group", "Emergency Relief Fund",
    "Neighborhood Association", "Church Food Ministry", "Temple Food Program",
    "Mosque Community Kitchen", "Sikh Langar Hall", "Buddhist Temple Kitchen",
    "Hindu Temple Annadanam", "Christian Food Ministry", "Islamic Relief",
    "Jewish Family Services", "Catholic Charities", "Lutheran Services",
    "Methodist Outreach", "Baptist Mission", "Presbyterian Aid",
    "Episcopal Relief", "Unitarian Universalist", "Hindu Relief Fund",
    "Buddhist Compassion", "Sikh Humanitarian", "Muslim Aid Society",
    "Christian Aid International", "Catholic Outreach", "Lutheran World Relief",
    "Methodist Mission Society", "Baptist World Aid", "Presbyterian World Mission",
    "Episcopal Mission", "Unitarian Service", "Hindu Seva",
    "Buddhist Tzu Chi", "Sikh United", "Muslim Charity Network",
    "Christian Relief Services", "Catholic Development", "Lutheran Development",
    "Methodist Development", "Baptist Development", "Presbyterian Development",
    "Episcopal Development", "Unitarian Development", "Hindu Development",
    "Buddhist Development", "Sikh Development", "Muslim Development",
    "Christian Development", "Catholic Mission", "Lutheran Mission",
    "Methodist Relief", "Baptist Relief", "Presbyterian Relief",
    "Episcopal Relief", "Unitarian Relief", "Hindu Relief",
    "Buddhist Relief", "Sikh Relief", "Muslim Relief",
    "Christian Relief", "Catholic Aid", "Lutheran Aid",
    "Methodist Aid", "Baptist Aid", "Presbyterian Aid",
    "Episcopal Aid", "Unitarian Aid", "Hindu Aid",
    "Buddhist Aid", "Sikh Aid", "Muslim Aid",
    "Christian Aid", "Catholic Support", "Lutheran Support",
    "Methodist Support", "Baptist Support", "Presbyterian Support",
    "Episcopal Support", "Unitarian Support", "Hindu Support",
    "Buddhist Support", "Sikh Support", "Muslim Support"
]

RECEIVER_TYPES = ["Shelter", "Food Bank", "NGO", "Community Center", "Religious Organization", "Senior Center", "Youth Center"]

FOOD_TYPES = ["Cooked Food", "Fruits", "Vegetables", "Bakery", "Others"]
FOOD_TYPE_WEIGHTS = [35, 22, 16, 14, 13]  # Percentage distribution

MEAL_TYPES = ["Breakfast", "Lunch", "Dinner", "Snacks", "Mixed"]

FOOD_NAMES = {
    "Cooked Food": ["Rice and Curry", "Pasta with Sauce", "Chicken Biryani", "Vegetable Stir Fry", "Dal and Rice", 
                   "Sambar and Rice", "Curry and Roti", "Fried Rice", "Noodles", "Soup and Bread",
                   "Grilled Chicken", "Fish Curry", "Beef Stew", "Pork Chops", "Lamb Curry",
                   "Mixed Vegetables", "Pulao", "Khichdi", "Upma", "Dosa"],
    "Fruits": ["Apples", "Bananas", "Oranges", "Grapes", "Mangoes", "Watermelon", "Papaya", "Pineapple",
              "Strawberries", "Blueberries", "Pears", "Peaches", "Plums", "Kiwi", "Melon"],
    "Vegetables": ["Tomatoes", "Potatoes", "Onions", "Carrots", "Cabbage", "Spinach", "Broccoli",
                  "Cauliflower", "Bell Peppers", "Cucumbers", "Eggplant", "Zucchini", "Green Beans",
                  "Peas", "Corn"],
    "Bakery": ["Bread Loaves", "Croissants", "Muffins", "Cookies", "Cakes", "Pastries", "Donuts",
              "Bagels", "Biscuits", "Brownies", "Pies", "Tarts", "Rolls", "Scones", "Cupcakes"],
    "Others": ["Milk", "Yogurt", "Cheese", "Butter", "Eggs", "Rice Bags", "Flour", "Sugar",
              "Oil", "Pulses", "Spices", "Nuts", "Dried Fruits", "Canned Goods", "Snacks"]
}

UNITS = ["kg", "liters", "pieces", "boxes", "packs", "bags"]

LOCATIONS = ["Downtown", "Midtown", "Uptown", "Westside", "Eastside", "Northside", "Southside", "Central", "Suburb", "Industrial Area"]

CLAIM_STATUSES = ["Pending", "Approved", "Completed", "Rejected"]

def generate_random_datetime(days_back=30):
    """Generate a random datetime within the last N days."""
    now = datetime.now()
    random_days = random.randint(0, days_back)
    random_hours = random.randint(0, 23)
    random_minutes = random.randint(0, 59)
    return now - timedelta(days=random_days, hours=random_hours, minutes=random_minutes)

def seed_providers(count=45):
    """Seed providers table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    for i in range(count):
        name = PROVIDER_NAMES[i % len(PROVIDER_NAMES)] + f" {i+1}" if i >= len(PROVIDER_NAMES) else PROVIDER_NAMES[i]
        provider_type = random.choice(PROVIDER_TYPES)
        city = random.choice(CITIES)
        address = f"{random.randint(100, 999)} {random.choice(['Main St', 'Oak Ave', 'Pine Rd', 'Maple Dr', 'Cedar Ln'])}"
        contact = f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        verified = random.choice([0, 1, 1])  # 66% verified
        
        cursor.execute('''
            INSERT INTO providers (name, type, address, city, contact, verified)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, provider_type, address, city, contact, verified))
    
    conn.commit()
    conn.close()
    print(f"✓ Seeded {count} providers")

def seed_receivers(count=78):
    """Seed receivers table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    for i in range(count):
        name = RECEIVER_NAMES[i % len(RECEIVER_NAMES)] + f" {i+1}" if i >= len(RECEIVER_NAMES) else RECEIVER_NAMES[i]
        receiver_type = random.choice(RECEIVER_TYPES)
        city = random.choice(CITIES)
        contact = f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        
        cursor.execute('''
            INSERT INTO receivers (name, type, city, contact)
            VALUES (?, ?, ?, ?)
        ''', (name, receiver_type, city, contact))
    
    conn.commit()
    conn.close()
    print(f"✓ Seeded {count} receivers")

def seed_food_listings(count=128):
    """Seed food_listings table with weighted food types."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get provider IDs
    cursor.execute("SELECT id FROM providers")
    provider_ids = [row[0] for row in cursor.fetchall()]
    
    for i in range(count):
        # Weighted random selection for food type
        food_type = random.choices(FOOD_TYPES, weights=FOOD_TYPE_WEIGHTS)[0]
        food_name = random.choice(FOOD_NAMES[food_type])
        meal_type = random.choice(MEAL_TYPES)
        quantity = round(random.uniform(1, 50), 1)
        unit = random.choice(UNITS)
        provider_id = random.choice(provider_ids)
        location = random.choice(LOCATIONS)
        
        # Expiry time between 1 hour and 7 days from creation
        created_at = generate_random_datetime(30)
        expiry_hours = random.randint(1, 168)
        expiry_time = created_at + timedelta(hours=expiry_hours)
        
        # Image URL (placeholder)
        image_url = f"https://via.placeholder.com/150?text={food_name.replace(' ', '+')}"
        
        # Status based on expiry
        if expiry_time < datetime.now():
            status = "Expired"
        else:
            status = random.choice(["Available", "Claimed", "Available", "Available"])  # 75% available
        
        cursor.execute('''
            INSERT INTO food_listings (food_name, food_type, meal_type, quantity, unit, 
                                       provider_id, location, expiry_time, image_url, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (food_name, food_type, meal_type, quantity, unit, provider_id, location, 
              expiry_time.strftime('%Y-%m-%d %H:%M:%S'), image_url, status, 
              created_at.strftime('%Y-%m-%d %H:%M:%S')))
    
    conn.commit()
    conn.close()
    print(f"✓ Seeded {count} food listings")

def seed_claims(count=96):
    """Seed claims table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get food IDs and receiver IDs
    cursor.execute("SELECT id, quantity FROM food_listings WHERE status = 'Available'")
    food_data = cursor.fetchall()
    
    cursor.execute("SELECT id FROM receivers")
    receiver_ids = [row[0] for row in cursor.fetchall()]
    
    for i in range(count):
        if not food_data:
            break
        
        food_id, max_quantity = random.choice(food_data)
        receiver_id = random.choice(receiver_ids)
        quantity_claimed = round(random.uniform(0.5, max_quantity), 1)
        status = random.choice(CLAIM_STATUSES)
        
        # Claimed at within last 30 days
        claimed_at = generate_random_datetime(30)
        
        cursor.execute('''
            INSERT INTO claims (food_id, receiver_id, quantity_claimed, status, claimed_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (food_id, receiver_id, quantity_claimed, status, claimed_at.strftime('%Y-%m-%d %H:%M:%S')))
        
        # Update food status if claim is approved or completed
        if status in ["Approved", "Completed"]:
            cursor.execute("UPDATE food_listings SET status = 'Claimed' WHERE id = ?", (food_id,))
    
    conn.commit()
    conn.close()
    print(f"✓ Seeded {count} claims")

def main():
    """Main function to seed all data."""
    print("Initializing database...")
    init_database()
    
    print("Seeding data...")
    seed_providers(45)
    seed_receivers(78)
    seed_food_listings(128)
    seed_claims(96)
    
    print("\n✓ Database seeding completed successfully!")
    print("\nSummary:")
    print("  - 45 providers")
    print("  - 78 receivers")
    print("  - 128 food listings")
    print("  - 96 claims")

if __name__ == "__main__":
    main()
