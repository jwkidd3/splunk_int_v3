#!/usr/bin/env python3
"""
Splunk Intermediate Training - Buttercup Games Data Generator
Generates data for the Buttercup Games e-commerce scenario
"""

import random
import datetime
import json
import csv
from pathlib import Path

# Configuration
OUTPUT_DIR = Path(__file__).parent.parent.parent / "data"
NUM_WEB_LOGS = 15000
NUM_VENDOR_SALES = 5000
NUM_SECURITY_LOGS = 2000
NUM_PROXY_LOGS = 3000
NUM_GAME_LOGS = 2000

# Buttercup Games Product Catalog
PRODUCTS = {
    "STRATEGY": [
        ("WC-SH-G01", "Mediocre Kingdoms", 39.99),
        ("WC-SH-G02", "World of Cheese", 24.99),
        ("WC-SH-G03", "Manganiello Bros.", 29.99),
        ("WC-SH-G04", "Command & Conquer", 49.99),
        ("WC-SH-G05", "Total War: Warhammer", 59.99),
    ],
    "SIMULATION": [
        ("SF-BUD-G01", "Grand Theft Scooter", 44.99),
        ("SF-BUD-G02", "The Sims 5", 49.99),
        ("SF-BUD-G03", "Cities: Skylines", 29.99),
        ("SF-BUD-G04", "Flight Simulator", 59.99),
    ],
    "ACTION": [
        ("MB-AG-G01", "Shrek Soccer", 14.99),
        ("MB-AG-G02", "Halo Infinite", 59.99),
        ("MB-AG-G03", "Call of Duty", 69.99),
        ("MB-AG-G04", "Assassin's Creed", 49.99),
    ],
    "SPORTS": [
        ("FS-FGA-G01", "Madden NFL", 59.99),
        ("FS-FGA-G02", "FIFA 24", 59.99),
        ("FS-FGA-G03", "NBA 2K24", 59.99),
    ],
    "accessories": [
        ("MB-AC-001", "Gaming Headset", 79.99),
        ("MB-AC-002", "Wireless Controller", 59.99),
        ("MB-AC-003", "Gaming Keyboard", 129.99),
        ("MB-AC-004", "Gaming Mouse", 49.99),
        ("MB-AC-005", "Mouse Pad", 19.99),
    ]
}

ACTIONS = ["view", "addtocart", "purchase", "remove", "changequantity"]
HTTP_METHODS = ["GET", "POST"]
HTTP_STATUS = [200, 200, 200, 200, 200, 201, 304, 400, 401, 403, 404, 500, 503]

USERS = ["alice", "bob", "charlie", "diana", "edward", "frank", "grace", "henry", "iris", "jack",
         "admin", "administrator", "sysadmin", "itmadmin", "sapadmin", "webadmin"]

# Vendor IDs by region
VENDOR_REGIONS = {
    "USA": (1000, 2999, ["California", "Texas", "New York", "Florida", "Washington"]),
    "Canada": (3000, 3999, ["Ontario", "Quebec", "British Columbia", "Alberta"]),
    "Mexico": (4000, 4999, ["Jalisco", "Nuevo León", "Mexico City"]),
    "Germany": (5000, 5499, ["Bavaria", "Berlin", "Hamburg"]),
    "France": (5500, 5999, ["Île-de-France", "Provence", "Aquitaine"]),
    "Italy": (6000, 6499, ["Lazio", "Lombardy", "Tuscany"]),
    "UK": (6500, 6999, ["England", "Scotland", "Wales"]),
    "Japan": (7000, 7499, ["Tokyo", "Osaka", "Kyoto"]),
    "China": (7500, 7999, ["Beijing", "Shanghai", "Guangdong"]),
    "Australia": (8000, 8499, ["New South Wales", "Victoria", "Queensland"]),
    "Brazil": (8500, 8999, ["São Paulo", "Rio de Janeiro", "Brasília"]),
    "South Africa": (9000, 9900, ["Gauteng", "Western Cape", "KwaZulu-Natal"]),
}

IP_RANGES = {
    "internal": ["192.168.1.", "192.168.10.", "10.0.1.", "10.0.2."],
    "external": ["203.0.113.", "198.51.100.", "192.0.2.", "185.125.190."]
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

HTTP_CONTENT_TYPES = [
    "text/html", "text/css", "text/javascript", "application/json",
    "image/jpeg", "image/png", "image/gif", "image/webp",
    "application/pdf", "application/xml"
]

GAME_CHARACTERS = ["Warrior", "Mage", "Rogue", "Paladin", "Druid", "Hunter", "Warlock", "Priest"]
GAME_ACTIONS = ["login", "logout", "quest_complete", "item_purchased", "level_up", "pvp_battle", "dungeon_enter"]
GAME_ROLES = ["tank", "healer", "dps", "support"]


def generate_timestamp(days_back=7):
    """Generate random timestamp within the last N days"""
    now = datetime.datetime.now()
    random_seconds = random.randint(0, days_back * 24 * 60 * 60)
    timestamp = now - datetime.timedelta(seconds=random_seconds)
    return timestamp


def generate_session_id():
    """Generate a session ID"""
    import hashlib
    random_string = f"{random.random()}{datetime.datetime.now()}"
    return hashlib.md5(random_string.encode()).hexdigest()[:24].upper()


def generate_ip(ip_type="external"):
    """Generate an IP address"""
    prefix = random.choice(IP_RANGES[ip_type])
    return f"{prefix}{random.randint(1, 254)}"


def get_random_product():
    """Get a random product with category"""
    category = random.choice(list(PRODUCTS.keys()))
    product_id, product_name, price = random.choice(PRODUCTS[category])
    return category, product_id, product_name, price


def generate_web_access_logs():
    """Generate web access logs in access_combined_wcookie format"""
    print(f"Generating {NUM_WEB_LOGS} web access logs...")

    logs = []
    sessions = {}  # Track sessions for realistic behavior

    for i in range(NUM_WEB_LOGS):
        timestamp = generate_timestamp()

        # Create or reuse session
        if random.random() > 0.3 and sessions:
            session_id = random.choice(list(sessions.keys()))
            clientip, user = sessions[session_id]
        else:
            session_id = generate_session_id()
            clientip = generate_ip("external")
            user = random.choice(USERS) if random.random() > 0.4 else "-"
            sessions[session_id] = (clientip, user)

        # Generate action and related fields
        action = random.choice(ACTIONS)
        method = "POST" if action in ["purchase", "addtocart", "remove"] else "GET"

        # Get product info
        category, product_id, product_name, price = get_random_product()

        # Generate status - mostly successful
        status = random.choice(HTTP_STATUS)

        # Generate response metrics
        bytes_sent = random.randint(500, 50000)
        req_time = random.randint(50, 3000)

        # Build log line in access_combined_wcookie format
        time_str = timestamp.strftime("%d/%b/%Y:%H:%M:%S +0000")
        uri = f"/cart.do?action={action}&itemId={product_id}&product_name={product_name}&price={price}"

        log_line = (
            f'{clientip} - {user} [{time_str}] '
            f'"{method} {uri} HTTP/1.1" {status} {bytes_sent} '
            f'"{random.choice(USER_AGENTS)}" '
            f'JSESSIONID={session_id} '
            f'categoryId={category} '
            f'productId={product_id} '
            f'req_time={req_time}'
        )
        logs.append((timestamp, log_line))

    # Sort by timestamp
    logs.sort(key=lambda x: x[0])

    output_file = OUTPUT_DIR / "web_access.log"
    with open(output_file, 'w') as f:
        for _, log in logs:
            f.write(log + '\n')

    print(f"✓ Created {output_file}")


def generate_vendor_sales():
    """Generate vendor sales data"""
    print(f"Generating {NUM_VENDOR_SALES} vendor sales records...")

    sales = []
    for i in range(NUM_VENDOR_SALES):
        timestamp = generate_timestamp()

        # Select region and generate vendor ID
        region, (min_id, max_id, states) = random.choice(list(VENDOR_REGIONS.items()))
        vendor_id = random.randint(min_id, max_id)
        state = random.choice(states)

        # Get product
        category, product_id, product_name, price = get_random_product()

        # Add some variation to price
        actual_price = round(price * random.uniform(0.9, 1.1), 2)

        sales.append({
            "timestamp": timestamp.isoformat(),
            "VendorID": vendor_id,
            "VendorCountry": region,
            "VendorStateProvince": state,
            "productId": product_id,
            "product_name": product_name,
            "categoryId": category,
            "price": actual_price,
            "quantity": random.randint(1, 5)
        })

    # Sort by timestamp
    sales.sort(key=lambda x: x['timestamp'])

    output_file = OUTPUT_DIR / "vendor_sales.csv"
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=sales[0].keys())
        writer.writeheader()
        writer.writerows(sales)

    print(f"✓ Created {output_file}")


def generate_linux_secure():
    """Generate Linux secure authentication logs"""
    print(f"Generating {NUM_SECURITY_LOGS} security logs...")

    logs = []
    for i in range(NUM_SECURITY_LOGS):
        timestamp = generate_timestamp()
        src_ip = generate_ip("external")
        user = random.choice(USERS)

        # Generate different types of events
        event_type = random.choice([
            "session opened", "session opened", "session opened",
            "failed password", "failed password",
            "authentication failure", "invalid user"
        ])

        port = random.randint(50000, 60000)

        time_str = timestamp.strftime("%b %d %H:%M:%S")
        hostname = "buttercup-web-01"

        if event_type == "session opened":
            log_line = f"{time_str} {hostname} sshd[{port}]: session opened for user {user} from {src_ip}"
            vendor_action = "session opened"
        elif event_type == "failed password":
            log_line = f"{time_str} {hostname} sshd[{port}]: Failed password for {user} from {src_ip} port {port} ssh2"
            vendor_action = "failed password"
        elif event_type == "authentication failure":
            log_line = f"{time_str} {hostname} sshd[{port}]: authentication failure; user={user} rhost={src_ip}"
            vendor_action = "authentication failure"
        else:
            log_line = f"{time_str} {hostname} sshd[{port}]: Invalid user {user} from {src_ip}"
            vendor_action = "invalid user"

        logs.append((timestamp, log_line))

    # Sort by timestamp
    logs.sort(key=lambda x: x[0])

    output_file = OUTPUT_DIR / "linux_secure.log"
    with open(output_file, 'w') as f:
        for _, log in logs:
            f.write(log + '\n')

    print(f"✓ Created {output_file}")


def generate_cisco_wsa_squid():
    """Generate Cisco WSA Squid proxy logs"""
    print(f"Generating {NUM_PROXY_LOGS} proxy logs...")

    logs = []
    for i in range(NUM_PROXY_LOGS):
        timestamp = generate_timestamp()
        elapsed = random.randint(10, 5000)
        src_ip = generate_ip("internal")

        result_code = random.choice(["TCP_HIT", "TCP_MISS", "TCP_REFRESH_HIT", "TCP_CLIENT_REFRESH_MISS"])
        status = random.choice(HTTP_STATUS)
        sc_bytes = random.randint(1000, 500000)
        method = random.choice(HTTP_METHODS)
        url = random.choice([
            "http://www.buttercupgames.com/",
            "http://www.buttercupgames.com/cart.do",
            "http://cdn.buttercupgames.com/images/products/",
            "http://www.social-media.com/",
            "http://www.news-site.com/",
            "http://www.gaming-forum.com/"
        ])
        cs_username = random.choice(USERS)
        hierarchy_code = "DIRECT"
        content_type = random.choice(HTTP_CONTENT_TYPES)

        # Cisco WSA Squid format
        epoch_time = int(timestamp.timestamp())
        log_line = (
            f"{epoch_time} {elapsed} {src_ip} {result_code}/{status} {sc_bytes} "
            f"{method} {url} {cs_username} {hierarchy_code}/- {content_type}"
        )

        logs.append((timestamp, log_line))

    # Sort by timestamp
    logs.sort(key=lambda x: x[0])

    output_file = OUTPUT_DIR / "cisco_wsa_squid.log"
    with open(output_file, 'w') as f:
        for _, log in logs:
            f.write(log + '\n')

    print(f"✓ Created {output_file}")


def generate_simcube_beta():
    """Generate SimCube Beta game logs (comma-delimited)"""
    print(f"Generating {NUM_GAME_LOGS} game telemetry logs...")

    logs = []
    for i in range(NUM_GAME_LOGS):
        timestamp = generate_timestamp()
        time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        src_ip = generate_ip("external")
        version = random.choice(["1.0", "1.1", "1.2", "2.0"])
        misc = random.randint(1000, 9999)
        user = random.choice(USERS)
        character_name = random.choice(GAME_CHARACTERS)
        action = random.choice(GAME_ACTIONS)
        role = random.choice(GAME_ROLES)

        # Comma-delimited format
        log_line = f"{time_str},{src_ip},{version},{misc},{user},{character_name},{action},{role}"

        logs.append((timestamp, log_line))

    # Sort by timestamp
    logs.sort(key=lambda x: x[0])

    output_file = OUTPUT_DIR / "simcube_beta.csv"
    with open(output_file, 'w') as f:
        # Write header
        f.write("time,src,version,misc,user,CharacterName,action,role\n")
        for _, log in logs:
            f.write(log + '\n')

    print(f"✓ Created {output_file}")


def generate_http_status_lookup():
    """Generate HTTP status code lookup"""
    print("Generating HTTP status lookup table...")

    status_codes = [
        (200, "OK", "Success"),
        (201, "Created", "Success"),
        (204, "No Content", "Success"),
        (301, "Moved Permanently", "Redirection"),
        (302, "Found", "Redirection"),
        (304, "Not Modified", "Redirection"),
        (400, "Bad Request", "Client Error"),
        (401, "Unauthorized", "Client Error"),
        (403, "Forbidden", "Client Error"),
        (404, "Not Found", "Client Error"),
        (500, "Internal Server Error", "Server Error"),
        (502, "Bad Gateway", "Server Error"),
        (503, "Service Unavailable", "Server Error"),
    ]

    output_file = OUTPUT_DIR / "http_status_lookup.csv"
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["status", "status_description", "status_type"])
        writer.writerows(status_codes)

    print(f"✓ Created {output_file}")


def generate_product_catalog():
    """Generate product catalog lookup"""
    print("Generating product catalog...")

    catalog = []
    for category, products in PRODUCTS.items():
        for product_id, product_name, price in products:
            catalog.append({
                "productId": product_id,
                "product_name": product_name,
                "categoryId": category,
                "price": price
            })

    output_file = OUTPUT_DIR / "product_catalog.csv"
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["productId", "product_name", "categoryId", "price"])
        writer.writeheader()
        writer.writerows(catalog)

    print(f"✓ Created {output_file}")


def main():
    """Main function to generate all Buttercup Games data"""
    print("=" * 60)
    print("Splunk Intermediate Training - Buttercup Games Data Generator")
    print("=" * 60)
    print()

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate all data files
    generate_web_access_logs()
    generate_vendor_sales()
    generate_linux_secure()
    generate_cisco_wsa_squid()
    generate_simcube_beta()
    generate_http_status_lookup()
    generate_product_catalog()

    print()
    print("=" * 60)
    print("✓ All Buttercup Games data generated successfully!")
    print(f"✓ Output directory: {OUTPUT_DIR}")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Start Splunk: scripts/start-splunk.bat")
    print("2. Log in to Splunk at http://localhost:8000")
    print("3. Create 4 indexes: web, security, network, games")
    print()
    print("4. Upload data files to appropriate indexes:")
    print("   INDEX: web")
    print("   - web_access.log → sourcetype=access_combined_wcookie")
    print("   - web_access.log → sourcetype=access_combined (also)")
    print("   - vendor_sales.csv → sourcetype=vendor_sales")
    print()
    print("   INDEX: security")
    print("   - linux_secure.log → sourcetype=linux_secure")
    print()
    print("   INDEX: network")
    print("   - cisco_wsa_squid.log → sourcetype=cisco_wsa_squid")
    print()
    print("   INDEX: games")
    print("   - simcube_beta.csv → sourcetype=SimCubeBeta")
    print()
    print("5. Upload lookup files (Settings → Lookups → Lookup table files):")
    print("   - http_status_lookup.csv")
    print("   - product_catalog.csv")
    print()
    print("See DATA_LOADING_GUIDE.md for detailed instructions.")
    print()


if __name__ == "__main__":
    main()
