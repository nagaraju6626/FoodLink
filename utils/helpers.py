from datetime import datetime, timedelta
import pytz

def time_ago(dt_str):
    """
    Convert a datetime string to a relative time string (e.g., "2 hours ago").
    
    Args:
        dt_str: Datetime string in format 'YYYY-MM-DD HH:MM:SS'
    
    Returns:
        Relative time string
    """
    try:
        dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
        now = datetime.now()
        diff = now - dt
        
        if diff.days > 30:
            months = diff.days // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
        elif diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
    except:
        return "Unknown"

def expiry_countdown(expiry_str):
    """
    Calculate time remaining until expiry and return formatted string with color class.
    
    Args:
        expiry_str: Expiry datetime string in format 'YYYY-MM-DD HH:MM:SS'
    
    Returns:
        Tuple of (formatted string, color_class)
    """
    try:
        expiry = datetime.strptime(expiry_str, '%Y-%m-%d %H:%M:%S')
        now = datetime.now()
        diff = expiry - now
        
        if diff.total_seconds() <= 0:
            return "Expired", "expire-urgent"
        elif diff.total_seconds() < 7200:  # Less than 2 hours
            hours = int(diff.total_seconds() // 3600)
            minutes = int((diff.total_seconds() % 3600) // 60)
            return f"{hours}h {minutes}m", "expire-urgent"
        elif diff.total_seconds() < 21600:  # Less than 6 hours
            hours = int(diff.total_seconds() // 3600)
            return f"{hours}h", "expire-warning"
        elif diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''}", "expire-normal"
        else:
            hours = int(diff.total_seconds() // 3600)
            return f"{hours}h", "expire-normal"
    except:
        return "Unknown", "expire-normal"

def format_datetime(dt_str, format_str="%B %d, %Y at %I:%M %p"):
    """
    Format a datetime string to a readable format.
    
    Args:
        dt_str: Datetime string in format 'YYYY-MM-DD HH:MM:SS'
        format_str: Output format string
    
    Returns:
        Formatted datetime string
    """
    try:
        dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
        return dt.strftime(format_str)
    except:
        return dt_str

def get_initials(name):
    """
    Get initials from a name.
    
    Args:
        name: Full name string
    
    Returns:
        Initials (up to 2 characters)
    """
    try:
        parts = name.split()
        if len(parts) >= 2:
            return (parts[0][0] + parts[-1][0]).upper()
        else:
            return name[:2].upper()
    except:
        return "NA"

def get_avatar_color(name):
    """
    Get a color class for an avatar based on the name.
    
    Args:
        name: Name string
    
    Returns:
        CSS class name for avatar color
    """
    colors = ['avatar-green', 'avatar-blue', 'avatar-purple', 'avatar-orange']
    try:
        index = hash(name) % len(colors)
        return colors[index]
    except:
        return colors[0]

def format_quantity(quantity, unit):
    """
    Format quantity with unit.
    
    Args:
        quantity: Numeric quantity
        unit: Unit string
    
    Returns:
        Formatted quantity string
    """
    try:
        if quantity == int(quantity):
            return f"{int(quantity)} {unit}"
        else:
            return f"{quantity} {unit}"
    except:
        return f"{quantity} {unit}"

def get_status_badge_class(status):
    """
    Get CSS class for a status badge.
    
    Args:
        status: Status string
    
    Returns:
        CSS class name
    """
    status_map = {
        'Available': 'status-available',
        'Pending': 'status-pending',
        'Expired': 'status-expired',
        'Claimed': 'status-claimed',
        'Completed': 'status-completed',
        'Rejected': 'status-rejected',
        'Approved': 'status-approved'
    }
    return status_map.get(status, 'status-pending')

def calculate_percentage(value, total):
    """
    Calculate percentage.
    
    Args:
        value: Numeric value
        total: Total value
    
    Returns:
        Percentage rounded to 1 decimal place
    """
    try:
        if total == 0:
            return 0
        return round((value / total) * 100, 1)
    except:
        return 0

def format_number(num):
    """
    Format a number with commas for thousands.
    
    Args:
        num: Numeric value
    
    Returns:
        Formatted number string
    """
    try:
        return "{:,}".format(int(num))
    except:
        return str(num)

def is_expired(expiry_str):
    """
    Check if a listing is expired.
    
    Args:
        expiry_str: Expiry datetime string
    
    Returns:
        Boolean indicating if expired
    """
    try:
        expiry = datetime.strptime(expiry_str, '%Y-%m-%d %H:%M:%S')
        return datetime.now() > expiry
    except:
        return False

def get_trend_percentage(current, previous):
    """
    Calculate trend percentage between two values.
    
    Args:
        current: Current value
        previous: Previous value
    
    Returns:
        Tuple of (percentage, direction)
    """
    try:
        if previous == 0:
            return 0, 'neutral'
        change = ((current - previous) / previous) * 100
        direction = 'up' if change > 0 else 'down' if change < 0 else 'neutral'
        return round(abs(change), 1), direction
    except:
        return 0, 'neutral'

def truncate_text(text, max_length=50):
    """
    Truncate text to a maximum length with ellipsis.
    
    Args:
        text: Input string
        max_length: Maximum length
    
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def render_kpi_card(label, value, trend, icon_color, icon_svg):
    """
    Render a KPI card as a complete HTML string.
    
    Args:
        label: KPI label text
        value: KPI value (number)
        trend: Trend percentage string (e.g., "12% this week")
        icon_color: Color class for icon (green, blue, purple, amber)
        icon_svg: SVG icon string
    
    Returns:
        Complete HTML string for KPI card
    """
    return f"""
    <div class="kpi-card">
        <div class="kpi-icon kpi-icon-{icon_color}">{icon_svg}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-trend">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>
                <polyline points="17 6 23 6 23 12"></polyline>
            </svg>
            {trend}
        </div>
    </div>
    """

def render_listing_row(food_name, provider, location, quantity, status, food_type):
    """
    Render a food listing row as a complete HTML string.
    
    Args:
        food_name: Food item name
        provider: Provider name
        location: Location
        quantity: Quantity with unit
        status: Status text
        food_type: Food type for icon color
    
    Returns:
        Complete HTML string for listing row
    """
    icon_colors = {
        'Cooked Food': 'green',
        'Fruits': 'blue',
        'Vegetables': 'green',
        'Bakery': 'amber',
        'Others': 'purple'
    }
    icon_color = icon_colors.get(food_type, 'green')
    
    return f"""
    <div class="activity-row">
        <div class="activity-icon activity-icon-{icon_color}">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                <path d="M2 17l10 5 10-5"></path>
                <path d="M2 12l10 5 10-5"></path>
            </svg>
        </div>
        <div class="activity-content">
            <div class="activity-title">{food_name}</div>
            <div class="activity-subtitle">{provider} · {location} · {quantity}</div>
        </div>
        <div class="status-badge status-available">{status}</div>
    </div>
    """

def render_claim_row(receiver_name, quantity, food_name, time_ago, initial):
    """
    Render a claim row as a complete HTML string.
    
    Args:
        receiver_name: Receiver name
        quantity: Quantity claimed
        food_name: Food item name
        time_ago: Relative time string
        initial: Initial letter for avatar
    
    Returns:
        Complete HTML string for claim row
    """
    return f"""
    <div class="activity-row">
        <div class="activity-avatar">{initial}</div>
        <div class="activity-content">
            <div class="activity-title">{receiver_name}</div>
            <div class="activity-subtitle">{quantity} · {food_name} · {time_ago}</div>
        </div>
    </div>
    """

def render_cta_banner():
    """
    Render the CTA banner as a complete HTML string.
    
    Returns:
        Complete HTML string for CTA banner
    """
    return """
    <div class="cta-banner">
        <div class="cta-banner-left">
            <div class="cta-banner-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="1" y="3" width="15" height="13"></rect>
                    <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon>
                    <circle cx="5.5" cy="18.5" r="2.5"></circle>
                    <circle cx="18.5" cy="18.5" r="2.5"></circle>
                </svg>
            </div>
            <div class="cta-banner-text">
                <div class="cta-banner-title">Be a hero in someone's story</div>
                <div class="cta-banner-subtitle">Share food. Spread happiness. Save lives.</div>
            </div>
        </div>
        <button class="btn-pill">Add food listing →</button>
    </div>
    """
