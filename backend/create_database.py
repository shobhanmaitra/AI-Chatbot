"""
Tourism Chatbot Database Creator
This script creates a SQLite database with tourism data
"""

import sqlite3
import os

print("=" * 50)
print("🚀 TOURISM CHATBOT DATABASE CREATOR")
print("=" * 50)
print()

# Step 1: Check if database already exists
if os.path.exists('tourism_chatbot.db'):
    print("⚠️  Database already exists!")
    choice = input("Do you want to DELETE and recreate it? (yes/no): ")
    if choice.lower() == 'yes':
        os.remove('tourism_chatbot.db')
        print("🗑️  Old database deleted!")
    else:
        print("❌ Exiting... Database not modified.")
        exit()

print()
print("📦 Step 1: Creating new database...")

# Step 2: Create database connection
# This creates a file called 'tourism_chatbot.db'
conn = sqlite3.connect('tourism_chatbot.db')
cursor = conn.cursor()

print("✅ Database file created: tourism_chatbot.db")
print()
print("📊 Step 2: Creating tables...")

# Step 3: Create DESTINATIONS table
cursor.execute('''
CREATE TABLE IF NOT EXISTS destinations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    state TEXT NOT NULL,
    description TEXT,
    best_season TEXT,
    rating REAL
)
''')
print("✅ Table 'destinations' created")

# Step 4: Create HOTELS table
cursor.execute('''
CREATE TABLE IF NOT EXISTS hotels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    destination_id INTEGER,
    price INTEGER,
    rating REAL,
    amenities TEXT,
    FOREIGN KEY (destination_id) REFERENCES destinations(id)
)
''')
print("✅ Table 'hotels' created")

# Step 5: Create ATTRACTIONS table
cursor.execute('''
CREATE TABLE IF NOT EXISTS attractions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    destination_id INTEGER,
    entry_fee INTEGER,
    timing TEXT,
    type TEXT,
    FOREIGN KEY (destination_id) REFERENCES destinations(id)
)
''')
print("✅ Table 'attractions' created")

# Step 6: Create PACKAGES table
cursor.execute('''
CREATE TABLE IF NOT EXISTS packages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    destination_id INTEGER,
    duration TEXT,
    price INTEGER,
    includes TEXT,
    FOREIGN KEY (destination_id) REFERENCES destinations(id)
)
''')
print("✅ Table 'packages' created")

print()
print("📝 Step 3: Inserting sample data...")
print()

# Step 7: Insert DESTINATIONS data
print("   Adding destinations...")
destinations_data = [
    ('Jaipur', 'Rajasthan', 'The Pink City - Capital of Rajasthan with magnificent forts and palaces', 'October to March', 4.5),
    ('Udaipur', 'Rajasthan', 'The City of Lakes - Known for beautiful lakes and romantic ambiance', 'September to March', 4.7),
    ('Jaisalmer', 'Rajasthan', 'The Golden City - Famous for sand dunes and desert safari', 'October to February', 4.6),
    ('Jodhpur', 'Rajasthan', 'The Blue City - Known for Mehrangarh Fort and blue houses', 'October to March', 4.4),
    ('Pushkar', 'Rajasthan', 'Holy City - Famous for Brahma Temple and annual camel fair', 'October to March', 4.3),
    ('Mount Abu', 'Rajasthan', 'Only Hill Station in Rajasthan - Famous for Dilwara Temples', 'November to February', 4.2),
    ('Bikaner', 'Rajasthan', 'Desert City - Known for Junagarh Fort and camel breeding farm', 'October to March', 4.1)
]

for dest in destinations_data:
    cursor.execute('INSERT INTO destinations (name, state, description, best_season, rating) VALUES (?, ?, ?, ?, ?)', dest)
    print(f"      ✓ {dest[0]}")

# Step 8: Insert HOTELS data
print("   Adding hotels...")
hotels_data = [
    ('Hotel Raj Palace', 1, 2500, 4.2, 'WiFi, Pool, Restaurant, Parking'),
    ('Pink City Inn', 1, 1800, 4.0, 'WiFi, Breakfast, AC'),
    ('Heritage Haveli', 1, 3200, 4.5, 'Heritage Property, Pool, Spa'),
    
    ('Lake View Resort', 2, 3500, 4.6, 'Lake View, Pool, Spa, Restaurant'),
    ('Udaipur Palace Hotel', 2, 2200, 4.3, 'WiFi, Restaurant, City View'),
    ('Romantic Retreat', 2, 4500, 4.8, 'Luxury, Lake View, Fine Dining'),
    
    ('Desert Camp Jaisalmer', 3, 1500, 4.4, 'Desert Safari, Cultural Show, Bonfire'),
    ('Golden Fort Hotel', 3, 2000, 4.2, 'WiFi, Rooftop Restaurant, Fort View'),
    ('Sand Dunes Resort', 3, 2800, 4.5, 'Desert View, Pool, Camel Safari'),
    
    ('Blue City Inn', 4, 1600, 4.1, 'WiFi, City View, Breakfast'),
    ('Mehrangarh View Hotel', 4, 2800, 4.5, 'Fort View, Pool, Restaurant'),
    ('Jodhpur Heritage', 4, 2200, 4.3, 'Traditional Decor, WiFi, Terrace'),
    
    ('Pushkar Palace', 5, 1400, 4.0, 'WiFi, Temple View, Vegetarian Food'),
    ('Lake Side Resort', 5, 1800, 4.2, 'Lake View, Garden, Restaurant'),
    
    ('Mount Abu Resort', 6, 2500, 4.3, 'Hill View, Garden, Restaurant'),
    ('Hill Top Hotel', 6, 3000, 4.4, 'Panoramic View, Pool, Spa'),
    
    ('Bikaner Fort Hotel', 7, 1700, 4.0, 'Fort View, WiFi, Traditional Cuisine')
]

for hotel in hotels_data:
    cursor.execute('INSERT INTO hotels (name, destination_id, price, rating, amenities) VALUES (?, ?, ?, ?, ?)', hotel)
print(f"      ✓ {len(hotels_data)} hotels added")

# Step 9: Insert ATTRACTIONS data
print("   Adding attractions...")
attractions_data = [
    # Jaipur (id=1)
    ('Hawa Mahal', 1, 200, '9:00 AM - 5:00 PM', 'Monument'),
    ('Amber Fort', 1, 500, '8:00 AM - 6:00 PM', 'Fort'),
    ('City Palace Jaipur', 1, 400, '9:00 AM - 5:00 PM', 'Palace'),
    ('Jantar Mantar', 1, 200, '9:00 AM - 5:00 PM', 'Observatory'),
    ('Jal Mahal', 1, 0, 'Always Open', 'Palace'),
    
    # Udaipur (id=2)
    ('Lake Pichola', 2, 0, 'Always Open', 'Lake'),
    ('City Palace Udaipur', 2, 300, '9:00 AM - 5:00 PM', 'Palace'),
    ('Jag Mandir', 2, 250, '10:00 AM - 6:00 PM', 'Island Palace'),
    ('Saheliyon Ki Bari', 2, 100, '9:00 AM - 6:00 PM', 'Garden'),
    
    # Jaisalmer (id=3)
    ('Jaisalmer Fort', 3, 250, '9:00 AM - 6:00 PM', 'Fort'),
    ('Sam Sand Dunes', 3, 0, 'Always Open', 'Desert'),
    ('Patwon Ki Haveli', 3, 150, '9:00 AM - 6:00 PM', 'Heritage'),
    ('Gadisar Lake', 3, 0, 'Always Open', 'Lake'),
    
    # Jodhpur (id=4)
    ('Mehrangarh Fort', 4, 600, '9:00 AM - 5:00 PM', 'Fort'),
    ('Jaswant Thada', 4, 50, '9:00 AM - 5:00 PM', 'Memorial'),
    ('Umaid Bhawan Palace', 4, 100, '9:00 AM - 5:00 PM', 'Palace'),
    
    # Pushkar (id=5)
    ('Brahma Temple', 5, 0, '6:00 AM - 9:00 PM', 'Temple'),
    ('Pushkar Lake', 5, 0, 'Always Open', 'Lake'),
    ('Savitri Temple', 5, 0, '5:00 AM - 9:00 PM', 'Temple'),
    
    # Mount Abu (id=6)
    ('Dilwara Temples', 6, 0, '12:00 PM - 6:00 PM', 'Temple'),
    ('Nakki Lake', 6, 0, 'Always Open', 'Lake'),
    ('Guru Shikhar', 6, 0, 'Always Open', 'View Point'),
    
    # Bikaner (id=7)
    ('Junagarh Fort', 7, 200, '10:00 AM - 5:00 PM', 'Fort'),
    ('Karni Mata Temple', 7, 50, '6:00 AM - 10:00 PM', 'Temple'),
]

for attr in attractions_data:
    cursor.execute('INSERT INTO attractions (name, destination_id, entry_fee, timing, type) VALUES (?, ?, ?, ?, ?)', attr)
print(f"      ✓ {len(attractions_data)} attractions added")

# Step 10: Insert PACKAGES data
print("   Adding tour packages...")
packages_data = [
    ('Jaipur Heritage Tour', 1, '2 Days / 1 Night', 8000, 'Hotel Stay, Breakfast, All Fort Entries, Guide, Transport'),
    ('Jaipur Complete Experience', 1, '3 Days / 2 Nights', 12000, 'Hotel Stay, All Meals, All Entries, Guide, Transport'),
    
    ('Udaipur Romance Package', 2, '3 Days / 2 Nights', 15000, 'Luxury Hotel, Boat Ride, Candlelight Dinner, Guide'),
    ('Lake City Explorer', 2, '2 Days / 1 Night', 9000, 'Hotel Stay, Breakfast, Palace Entries, Boat Ride, Guide'),
    
    ('Desert Adventure Jaisalmer', 3, '2 Days / 1 Night', 7000, 'Desert Camp, Camel Safari, Cultural Show, All Meals'),
    ('Golden City Package', 3, '3 Days / 2 Nights', 11000, 'Hotel + Desert Camp, Safari, All Entries, Guide'),
    
    ('Blue City Special', 4, '2 Days / 1 Night', 8500, 'Hotel Stay, Fort Entry, Breakfast, Guide, Transport'),
    ('Jodhpur Heritage', 4, '3 Days / 2 Nights', 13000, 'Hotel Stay, All Meals, All Entries, Village Tour, Guide'),
    
    ('Pushkar Spiritual Tour', 5, '1 Day', 3000, 'Temple Visits, Aarti, Lunch, Guide'),
    ('Pushkar Festival Package', 5, '3 Days / 2 Nights', 9000, 'Hotel Stay, Festival Access, Camel Fair, All Meals'),
    
    ('Mount Abu Hill Retreat', 6, '2 Days / 1 Night', 8000, 'Hotel Stay, Temple Visit, Lake Boating, Guide'),
    
    ('Bikaner Fort & Culture', 7, '2 Days / 1 Night', 7500, 'Hotel Stay, Fort Entry, Camel Farm Visit, Guide'),
    
    ('Rajasthan Complete Tour', 1, '7 Days / 6 Nights', 35000, 'Jaipur-Udaipur-Jaisalmer, Hotels, All Meals, Guide, AC Transport')
]

for pkg in packages_data:
    cursor.execute('INSERT INTO packages (name, destination_id, duration, price, includes) VALUES (?, ?, ?, ?, ?)', pkg)
print(f"      ✓ {len(packages_data)} packages added")

# Step 11: Save (commit) all changes
conn.commit()
print()
print("💾 Step 4: Saving all changes to database...")

# Step 12: Verify data was inserted
cursor.execute('SELECT COUNT(*) FROM destinations')
dest_count = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM hotels')
hotel_count = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM attractions')
attr_count = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM packages')
pkg_count = cursor.fetchone()[0]

# Step 13: Close database connection
conn.close()

# Step 14: Display success message
print("✅ All changes saved!")
print()
print("=" * 50)
print("🎉 DATABASE CREATED SUCCESSFULLY!")
print("=" * 50)
print()
print("📊 DATABASE SUMMARY:")
print(f"   📍 Destinations: {dest_count}")
print(f"   🏨 Hotels: {hotel_count}")
print(f"   🎯 Attractions: {attr_count}")
print(f"   📦 Packages: {pkg_count}")
print(f"   📁 Total Records: {dest_count + hotel_count + attr_count + pkg_count}")
print()
print("📍 Database Location: backend/tourism_chatbot.db")
print("📏 Database Size: ~100 KB")
print()
print("=" * 50)
print("✅ NEXT STEP: Run 'python app.py' to start chatbot!")
print("=" * 50)