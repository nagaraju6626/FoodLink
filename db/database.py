import sqlite3
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import pandas as pd

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

# ============== KPI FUNCTIONS ==============

def get_kpi_counts():
    """Get count statistics for KPI cards."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM food_listings")
    total_listings = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM providers")
    total_providers = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM receivers")
    total_receivers = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM claims")
    total_claims = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'total_listings': total_listings,
        'total_providers': total_providers,
        'total_receivers': total_receivers,
        'total_claims': total_claims
    }

def get_kpi_trends():
    """Get trend percentages for KPI cards (last 7 days vs prior 7 days)."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Listings trend
    cursor.execute('''
        SELECT COUNT(*) FROM food_listings 
        WHERE created_at >= datetime('now', '-7 days')
    ''')
    current_listings = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT COUNT(*) FROM food_listings 
        WHERE created_at >= datetime('now', '-14 days') AND created_at < datetime('now', '-7 days')
    ''')
    prior_listings = cursor.fetchone()[0]
    
    listings_trend = calculate_trend_percentage(current_listings, prior_listings)
    
    # Providers trend
    cursor.execute('''
        SELECT COUNT(*) FROM providers 
        WHERE id IN (SELECT provider_id FROM food_listings WHERE created_at >= datetime('now', '-7 days'))
    ''')
    current_providers = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT COUNT(*) FROM providers 
        WHERE id IN (SELECT provider_id FROM food_listings WHERE created_at >= datetime('now', '-14 days') AND created_at < datetime('now', '-7 days'))
    ''')
    prior_providers = cursor.fetchone()[0]
    
    providers_trend = calculate_trend_percentage(current_providers, prior_providers)
    
    # Receivers trend
    cursor.execute('''
        SELECT COUNT(*) FROM receivers 
        WHERE id IN (SELECT receiver_id FROM claims WHERE claimed_at >= datetime('now', '-7 days'))
    ''')
    current_receivers = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT COUNT(*) FROM receivers 
        WHERE id IN (SELECT receiver_id FROM claims WHERE claimed_at >= datetime('now', '-14 days') AND claimed_at < datetime('now', '-7 days'))
    ''')
    prior_receivers = cursor.fetchone()[0]
    
    receivers_trend = calculate_trend_percentage(current_receivers, prior_receivers)
    
    # Claims trend
    cursor.execute('''
        SELECT COUNT(*) FROM claims 
        WHERE claimed_at >= datetime('now', '-7 days')
    ''')
    current_claims = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT COUNT(*) FROM claims 
        WHERE claimed_at >= datetime('now', '-14 days') AND claimed_at < datetime('now', '-7 days')
    ''')
    prior_claims = cursor.fetchone()[0]
    
    claims_trend = calculate_trend_percentage(current_claims, prior_claims)
    
    conn.close()
    
    return {
        'listings_trend': listings_trend,
        'providers_trend': providers_trend,
        'receivers_trend': receivers_trend,
        'claims_trend': claims_trend
    }

def calculate_trend_percentage(current, prior):
    """Calculate trend percentage between current and prior values."""
    if prior == 0:
        return "0% this week" if current == 0 else "100% this week"
    change = ((current - prior) / prior) * 100
    if change >= 0:
        return f"{abs(change):.0f}% this week"
    else:
        return f"{abs(change):.0f}% this week"

def get_listings_trend(period='month'):
    """Get food listings trend data for charts."""
    conn = get_connection()
    
    if period == 'week':
        days = 7
    elif period == 'month':
        days = 30
    else:
        days = 90
    
    query = '''
        SELECT DATE(created_at) as date, COUNT(*) as count
        FROM food_listings
        WHERE created_at >= datetime('now', '-' || ? || ' days')
        GROUP BY DATE(created_at)
        ORDER BY date
    '''
    
    df = pd.read_sql_query(query, conn, params=(days,))
    conn.close()
    
    return df

def get_category_distribution():
    """Get food category distribution for donut chart."""
    conn = get_connection()
    query = '''
        SELECT food_type, COUNT(*) as count
        FROM food_listings
        GROUP BY food_type
        ORDER BY count DESC
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_recent_claims(limit=5):
    """Get recent claims with receiver and food details."""
    conn = get_connection()
    query = '''
        SELECT c.id, c.quantity_claimed, c.status, c.claimed_at,
               r.name as receiver_name, r.city as receiver_city,
               f.food_name, f.food_type
        FROM claims c
        JOIN receivers r ON c.receiver_id = r.id
        JOIN food_listings f ON c.food_id = f.id
        ORDER BY c.claimed_at DESC
        LIMIT ?
    '''
    df = pd.read_sql_query(query, conn, params=(limit,))
    conn.close()
    return df

def get_recent_listings(limit=5):
    """Get recent food listings with provider details."""
    conn = get_connection()
    query = '''
        SELECT f.id, f.food_name, f.food_type, f.quantity, f.unit,
               f.location, f.expiry_time, f.status, f.image_url,
               p.name as provider_name, p.verified, p.city
        FROM food_listings f
        JOIN providers p ON f.provider_id = p.id
        ORDER BY f.created_at DESC
        LIMIT ?
    '''
    df = pd.read_sql_query(query, conn, params=(limit,))
    conn.close()
    return df

# ============== PROVIDER CRUD ==============

def create_provider(name: str, type: str, address: str, city: str, contact: str, verified: int = 0) -> int:
    """Create a new provider."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO providers (name, type, address, city, contact, verified)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, type, address, city, contact, verified))
    conn.commit()
    provider_id = cursor.lastrowid
    conn.close()
    return provider_id

def get_all_providers():
    """Get all providers."""
    conn = get_connection()
    query = "SELECT * FROM providers ORDER BY name"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_provider_by_id(provider_id: int):
    """Get provider by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM providers WHERE id = ?", (provider_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_provider(provider_id: int, name: str, type: str, address: str, city: str, contact: str, verified: int):
    """Update provider."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE providers
        SET name = ?, type = ?, address = ?, city = ?, contact = ?, verified = ?
        WHERE id = ?
    ''', (name, type, address, city, contact, verified, provider_id))
    conn.commit()
    conn.close()

def delete_provider(provider_id: int):
    """Delete provider."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM providers WHERE id = ?", (provider_id,))
    conn.commit()
    conn.close()

def verify_provider(provider_id: int):
    """Mark provider as verified."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE providers SET verified = 1 WHERE id = ?", (provider_id,))
    conn.commit()
    conn.close()

# ============== RECEIVER CRUD ==============

def create_receiver(name: str, type: str, city: str, contact: str) -> int:
    """Create a new receiver."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO receivers (name, type, city, contact)
        VALUES (?, ?, ?, ?)
    ''', (name, type, city, contact))
    conn.commit()
    receiver_id = cursor.lastrowid
    conn.close()
    return receiver_id

def get_all_receivers():
    """Get all receivers."""
    conn = get_connection()
    query = "SELECT * FROM receivers ORDER BY name"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_receiver_by_id(receiver_id: int):
    """Get receiver by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM receivers WHERE id = ?", (receiver_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_receiver(receiver_id: int, name: str, type: str, city: str, contact: str):
    """Update receiver."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE receivers
        SET name = ?, type = ?, city = ?, contact = ?
        WHERE id = ?
    ''', (name, type, city, contact, receiver_id))
    conn.commit()
    conn.close()

def delete_receiver(receiver_id: int):
    """Delete receiver."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM receivers WHERE id = ?", (receiver_id,))
    conn.commit()
    conn.close()

# ============== FOOD LISTING CRUD ==============

def claim_food_listing(food_id: int, receiver_id: int, quantity_claimed: float) -> int:
    """Create a new food claim entry for a listing."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO claims (food_id, receiver_id, quantity_claimed, status)
        VALUES (?, ?, ?, ?)
    ''', (food_id, receiver_id, quantity_claimed, 'Pending'))
    conn.commit()
    claim_id = cursor.lastrowid
    conn.close()
    return claim_id

def create_food_listing(food_name: str, food_type: str, meal_type: str, quantity: float, 
                        unit: str, provider_id: int, location: str, expiry_time: str, 
                        image_url: str = None) -> int:
    """Create a new food listing."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO food_listings (food_name, food_type, meal_type, quantity, unit, 
                                   provider_id, location, expiry_time, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (food_name, food_type, meal_type, quantity, unit, provider_id, location, expiry_time, image_url))
    conn.commit()
    food_id = cursor.lastrowid
    conn.close()
    return food_id

def get_all_food_listings():
    """Get all food listings."""
    conn = get_connection()
    query = '''
        SELECT f.*, p.name as provider_name, p.verified
        FROM food_listings f
        JOIN providers p ON f.provider_id = p.id
        ORDER BY f.created_at DESC
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_food_listing_by_id(food_id: int):
    """Get food listing by ID."""
    conn = get_connection()
    query = '''
        SELECT f.*, p.name as provider_name, p.verified, p.contact as provider_contact
        FROM food_listings f
        JOIN providers p ON f.provider_id = p.id
        WHERE f.id = ?
    '''
    df = pd.read_sql_query(query, conn, params=(food_id,))
    conn.close()
    return dict(df.iloc[0]) if not df.empty else None

def get_food_listings_by_provider(provider_id: int):
    """Get food listings by provider."""
    conn = get_connection()
    query = "SELECT * FROM food_listings WHERE provider_id = ? ORDER BY created_at DESC"
    df = pd.read_sql_query(query, conn, params=(provider_id,))
    conn.close()
    return df

def update_food_listing(food_id: int, food_name: str, food_type: str, meal_type: str, 
                        quantity: float, unit: str, location: str, expiry_time: str, 
                        image_url: str = None, status: str = None):
    """Update food listing."""
    conn = get_connection()
    cursor = conn.cursor()
    
    if status:
        cursor.execute('''
            UPDATE food_listings
            SET food_name = ?, food_type = ?, meal_type = ?, quantity = ?, unit = ?,
                location = ?, expiry_time = ?, image_url = ?, status = ?
            WHERE id = ?
        ''', (food_name, food_type, meal_type, quantity, unit, location, expiry_time, image_url, status, food_id))
    else:
        cursor.execute('''
            UPDATE food_listings
            SET food_name = ?, food_type = ?, meal_type = ?, quantity = ?, unit = ?,
                location = ?, expiry_time = ?, image_url = ?
            WHERE id = ?
        ''', (food_name, food_type, meal_type, quantity, unit, location, expiry_time, image_url, food_id))
    
    conn.commit()
    conn.close()

def delete_food_listing(food_id: int):
    """Delete food listing."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM food_listings WHERE id = ?", (food_id,))
    conn.commit()
    conn.close()

def update_food_status(food_id: int, status: str):
    """Update food listing status."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE food_listings SET status = ? WHERE id = ?", (status, food_id))
    conn.commit()
    conn.close()

# ============== CLAIM CRUD ==============

def create_claim(food_id: int, receiver_id: int, quantity_claimed: float) -> int:
    """Create a new claim."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO claims (food_id, receiver_id, quantity_claimed)
        VALUES (?, ?, ?)
    ''', (food_id, receiver_id, quantity_claimed))
    conn.commit()
    claim_id = cursor.lastrowid
    conn.close()
    return claim_id

def get_all_claims():
    """Get all claims."""
    conn = get_connection()
    query = '''
        SELECT c.*, r.name as receiver_name, f.food_name, f.food_type
        FROM claims c
        JOIN receivers r ON c.receiver_id = r.id
        JOIN food_listings f ON c.food_id = f.id
        ORDER BY c.claimed_at DESC
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_claim_by_id(claim_id: int):
    """Get claim by ID."""
    conn = get_connection()
    query = '''
        SELECT c.*, r.name as receiver_name, f.food_name
        FROM claims c
        JOIN receivers r ON c.receiver_id = r.id
        JOIN food_listings f ON c.food_id = f.id
        WHERE c.id = ?
    '''
    df = pd.read_sql_query(query, conn, params=(claim_id,))
    conn.close()
    return dict(df.iloc[0]) if not df.empty else None

def update_claim_status(claim_id: int, status: str):
    """Update claim status."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE claims SET status = ? WHERE id = ?", (status, claim_id))
    conn.commit()
    conn.close()

def delete_claim(claim_id: int):
    """Delete claim."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM claims WHERE id = ?", (claim_id,))
    conn.commit()
    conn.close()

# ============== ANALYTICS FUNCTIONS ==============

def get_food_type_distribution():
    """Get distribution of food types."""
    conn = get_connection()
    query = '''
        SELECT food_type, COUNT(*) as count,
               ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM food_listings), 1) as percentage
        FROM food_listings
        GROUP BY food_type
        ORDER BY count DESC
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_meal_type_distribution():
    """Get distribution of meal types."""
    conn = get_connection()
    query = '''
        SELECT meal_type, COUNT(*) as count
        FROM food_listings
        GROUP BY meal_type
        ORDER BY count DESC
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_top_locations(limit=10):
    """Get top locations by food listings."""
    conn = get_connection()
    query = '''
        SELECT location, COUNT(*) as count
        FROM food_listings
        GROUP BY location
        ORDER BY count DESC
        LIMIT ?
    '''
    df = pd.read_sql_query(query, conn, params=(limit,))
    conn.close()
    return df

def get_claims_trend(period='month'):
    """Get claims trend over time."""
    conn = get_connection()
    
    if period == 'week':
        days = 7
    elif period == 'month':
        days = 30
    else:
        days = 90
    
    query = '''
        SELECT DATE(claimed_at) as date, COUNT(*) as count
        FROM claims
        WHERE claimed_at >= datetime('now', '-' || ? || ' days')
        GROUP BY DATE(claimed_at)
        ORDER BY date
    '''
    
    df = pd.read_sql_query(query, conn, params=(days,))
    conn.close()
    return df

def get_claim_status_distribution():
    """Get distribution of claim statuses."""
    conn = get_connection()
    query = '''
        SELECT status, COUNT(*) as count
        FROM claims
        GROUP BY status
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
