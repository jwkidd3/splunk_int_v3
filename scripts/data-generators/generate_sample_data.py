#!/usr/bin/env python3
"""
Splunk Intermediate Training - Sample Data Generator
Generates web server logs, application logs, and security events for training exercises
"""

import random
import datetime
import json
import csv
import os
from pathlib import Path

# Configuration
OUTPUT_DIR = Path(__file__).parent.parent.parent / "data"
NUM_WEB_LOGS = 10000
NUM_APP_LOGS = 5000
NUM_SECURITY_EVENTS = 1000

# Sample data
USERS = ["alice", "bob", "charlie", "diana", "edward", "frank", "grace", "henry", "iris", "jack",
         "karen", "louis", "mary", "nancy", "oliver", "patricia", "quinn", "robert", "sarah", "thomas"]

PRODUCTS = ["laptop", "desktop", "tablet", "smartphone", "monitor", "keyboard", "mouse", "webcam",
            "headset", "speaker", "router", "switch", "printer", "scanner", "drive"]

CATEGORIES = ["electronics", "computers", "accessories", "networking", "peripherals"]

IP_ADDRESSES = [f"192.168.{random.randint(1,10)}.{random.randint(1,254)}" for _ in range(50)]

HTTP_METHODS = ["GET", "POST", "PUT", "DELETE"]
HTTP_STATUS = [200, 200, 200, 200, 200, 201, 204, 301, 302, 400, 401, 403, 404, 500, 503]

URLS = [
    "/", "/home", "/products", "/cart", "/checkout", "/login", "/logout", "/register",
    "/api/products", "/api/cart", "/api/orders", "/api/users", "/api/search",
    "/admin", "/admin/users", "/admin/products", "/admin/reports",
    "/products/electronics", "/products/computers", "/products/accessories"
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15"
]

LOG_LEVELS = ["DEBUG", "INFO", "INFO", "INFO", "WARN", "ERROR", "CRITICAL"]

APP_COMPONENTS = ["AuthService", "PaymentService", "InventoryService", "OrderService",
                  "SearchService", "EmailService", "NotificationService", "ReportService"]

SECURITY_EVENT_TYPES = ["login_success", "login_failure", "password_change", "privilege_escalation",
                        "file_access", "unauthorized_access", "suspicious_activity", "data_export"]

CITIES = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia",
          "San Antonio", "San Diego", "Dallas", "San Jose"]

COUNTRIES = ["USA", "Canada", "UK", "Germany", "France", "Japan", "Australia", "Brazil"]

DEPARTMENTS = ["Sales", "Engineering", "Marketing", "Finance", "HR", "Operations", "IT", "Support"]


def generate_timestamp(days_back=7):
    """Generate random timestamp within the last N days"""
    now = datetime.datetime.now()
    random_seconds = random.randint(0, days_back * 24 * 60 * 60)
    timestamp = now - datetime.timedelta(seconds=random_seconds)
    return timestamp


def generate_web_logs():
    """Generate web server access logs"""
    print(f"Generating {NUM_WEB_LOGS} web server logs...")

    logs = []
    for i in range(NUM_WEB_LOGS):
        timestamp = generate_timestamp()
        ip = random.choice(IP_ADDRESSES)
        user = random.choice(USERS) if random.random() > 0.3 else "-"
        method = random.choice(HTTP_METHODS)
        url = random.choice(URLS)

        # Add query parameters sometimes
        if random.random() > 0.7:
            url += f"?id={random.randint(1, 1000)}"

        status = random.choice(HTTP_STATUS)
        bytes_sent = random.randint(100, 50000)
        response_time = random.randint(10, 5000)
        user_agent = random.choice(USER_AGENTS)

        log_line = (
            f'{ip} - {user} [{timestamp.strftime("%d/%b/%Y:%H:%M:%S +0000")}] '
            f'"{method} {url} HTTP/1.1" {status} {bytes_sent} '
            f'response_time={response_time} "{user_agent}"'
        )
        logs.append(log_line)

    # Sort by timestamp
    logs.sort()

    output_file = OUTPUT_DIR / "web_access.log"
    with open(output_file, 'w') as f:
        f.write('\n'.join(logs))

    print(f"✓ Created {output_file}")


def generate_application_logs():
    """Generate application logs in JSON format"""
    print(f"Generating {NUM_APP_LOGS} application logs...")

    logs = []
    session_ids = [f"sess_{random.randint(100000, 999999)}" for _ in range(100)]

    for i in range(NUM_APP_LOGS):
        timestamp = generate_timestamp()
        level = random.choice(LOG_LEVELS)
        component = random.choice(APP_COMPONENTS)
        user = random.choice(USERS)
        session_id = random.choice(session_ids)

        messages = {
            "AuthService": [
                f"User {user} authenticated successfully",
                f"Failed authentication attempt for {user}",
                f"Session created for {user}",
                f"Session expired for {user}"
            ],
            "PaymentService": [
                f"Payment processed for order #{random.randint(1000, 9999)}",
                f"Payment failed for order #{random.randint(1000, 9999)}",
                f"Refund initiated for order #{random.randint(1000, 9999)}"
            ],
            "InventoryService": [
                f"Stock level updated for product {random.choice(PRODUCTS)}",
                f"Low stock alert for product {random.choice(PRODUCTS)}",
                f"Product {random.choice(PRODUCTS)} out of stock"
            ],
            "OrderService": [
                f"Order #{random.randint(1000, 9999)} created by {user}",
                f"Order #{random.randint(1000, 9999)} shipped",
                f"Order #{random.randint(1000, 9999)} delivered"
            ],
            "SearchService": [
                f"Search query: {random.choice(PRODUCTS)} by {user}",
                f"Search returned {random.randint(0, 100)} results"
            ]
        }

        message = random.choice(messages.get(component, ["Operation completed"]))

        log_entry = {
            "timestamp": timestamp.isoformat(),
            "level": level,
            "component": component,
            "user": user,
            "session_id": session_id,
            "message": message,
            "thread_id": f"thread-{random.randint(1, 50)}",
            "duration_ms": random.randint(1, 1000)
        }

        logs.append(log_entry)

    # Sort by timestamp
    logs.sort(key=lambda x: x['timestamp'])

    output_file = OUTPUT_DIR / "application.log"
    with open(output_file, 'w') as f:
        for log in logs:
            f.write(json.dumps(log) + '\n')

    print(f"✓ Created {output_file}")


def generate_security_events():
    """Generate security event logs"""
    print(f"Generating {NUM_SECURITY_EVENTS} security events...")

    logs = []
    for i in range(NUM_SECURITY_EVENTS):
        timestamp = generate_timestamp()
        event_type = random.choice(SECURITY_EVENT_TYPES)
        user = random.choice(USERS)
        src_ip = random.choice(IP_ADDRESSES)

        severity = "high" if event_type in ["unauthorized_access", "privilege_escalation", "suspicious_activity"] else "medium"
        if event_type in ["login_success", "password_change"]:
            severity = "low"

        log_entry = {
            "timestamp": timestamp.isoformat(),
            "event_type": event_type,
            "user": user,
            "src_ip": src_ip,
            "severity": severity,
            "department": random.choice(DEPARTMENTS),
            "city": random.choice(CITIES),
            "country": random.choice(COUNTRIES),
            "success": random.choice([True, True, True, False])
        }

        logs.append(log_entry)

    # Sort by timestamp
    logs.sort(key=lambda x: x['timestamp'])

    output_file = OUTPUT_DIR / "security_events.log"
    with open(output_file, 'w') as f:
        for log in logs:
            f.write(json.dumps(log) + '\n')

    print(f"✓ Created {output_file}")


def generate_product_lookup():
    """Generate product lookup CSV"""
    print("Generating product lookup table...")

    products_data = []
    for i, product in enumerate(PRODUCTS):
        products_data.append({
            "product_id": f"PROD{i+1:04d}",
            "product_name": product,
            "category": random.choice(CATEGORIES),
            "price": round(random.uniform(10, 2000), 2),
            "vendor": random.choice(["TechCorp", "DataSystems", "GlobalTech", "InnovateCo", "FutureTech"]),
            "stock_level": random.randint(0, 500)
        })

    output_file = OUTPUT_DIR / "products.csv"
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=products_data[0].keys())
        writer.writeheader()
        writer.writerows(products_data)

    print(f"✓ Created {output_file}")


def generate_user_lookup():
    """Generate user information lookup CSV"""
    print("Generating user lookup table...")

    users_data = []
    for user in USERS:
        users_data.append({
            "username": user,
            "email": f"{user}@company.com",
            "department": random.choice(DEPARTMENTS),
            "city": random.choice(CITIES),
            "country": random.choice(COUNTRIES),
            "role": random.choice(["user", "user", "user", "admin", "manager"])
        })

    output_file = OUTPUT_DIR / "users.csv"
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=users_data[0].keys())
        writer.writeheader()
        writer.writerows(users_data)

    print(f"✓ Created {output_file}")


def generate_threat_intel():
    """Generate threat intelligence lookup CSV"""
    print("Generating threat intelligence lookup table...")

    # Generate some "malicious" IPs (not real, just for training)
    threat_data = []
    for i in range(20):
        threat_data.append({
            "ip_address": f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "threat_level": random.choice(["low", "medium", "high", "critical"]),
            "threat_type": random.choice(["malware", "botnet", "scanner", "brute_force", "ddos"]),
            "last_seen": generate_timestamp(30).strftime("%Y-%m-%d"),
            "description": random.choice([
                "Known malware distribution",
                "Brute force attacks detected",
                "Part of botnet network",
                "Port scanning activity",
                "DDoS source"
            ])
        })

    output_file = OUTPUT_DIR / "threat_intel.csv"
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=threat_data[0].keys())
        writer.writeheader()
        writer.writerows(threat_data)

    print(f"✓ Created {output_file}")


def main():
    """Main function to generate all sample data"""
    print("=" * 60)
    print("Splunk Intermediate Training - Data Generator")
    print("=" * 60)
    print()

    # Create output directory if it doesn't exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate all data files
    generate_web_logs()
    generate_application_logs()
    generate_security_events()
    generate_product_lookup()
    generate_user_lookup()
    generate_threat_intel()

    print()
    print("=" * 60)
    print("✓ All sample data generated successfully!")
    print(f"✓ Output directory: {OUTPUT_DIR}")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Start your Splunk instance: scripts/start-splunk.bat")
    print("2. Log in to Splunk at http://localhost:8000")
    print("3. Create a new index called 'training'")
    print("4. Upload the data files from the 'data' directory")
    print("5. Follow the lab exercises")
    print()


if __name__ == "__main__":
    main()
