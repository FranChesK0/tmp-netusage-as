from app import create_app, db
from app.models import User, UsageRecord
from datetime import datetime, timedelta
import random

def init_db():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Create admin user
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)

        # Create test users with various usage patterns
        users = [
            ('testuser', 'test@example.com', 'test123', 'Regular user with moderate usage'),
            ('poweruser', 'power@example.com', 'power123', 'Heavy network user'),
            ('developer', 'dev@example.com', 'dev123', 'Developer with VPN access'),
            ('analyst', 'analyst@example.com', 'analyst123', 'Data analyst with high usage'),
            ('intern', 'intern@example.com', 'intern123', 'Intern with limited usage')
        ]

        created_users = []
        for username, email, password, _ in users:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            created_users.append(user)

        db.session.commit()

        # Generate usage records for the past 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        # Different usage patterns for different user types
        usage_patterns = {
            'testuser': (100, 500),      # Moderate usage: 100-500 MB per day
            'poweruser': (500, 2000),    # Heavy usage: 500-2000 MB per day
            'developer': (200, 1000),    # Variable usage: 200-1000 MB per day
            'analyst': (300, 1500),      # High usage: 300-1500 MB per day
            'intern': (50, 200)          # Limited usage: 50-200 MB per day
        }

        # Generate usage records
        current_date = start_date
        while current_date <= end_date:
            for user in created_users:
                # Skip some days randomly for more realistic data
                if random.random() < 0.1:  # 10% chance to skip a day
                    continue

                min_usage, max_usage = usage_patterns.get(user.username, (100, 500))
                
                # Generate 1-4 records per day
                daily_records = random.randint(1, 4)
                for _ in range(daily_records):
                    data_used = random.uniform(min_usage, max_usage)
                    connection_time = random.randint(30, 480)  # 30 mins to 8 hours
                    ip_address = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
                    
                    record = UsageRecord(
                        user_id=user.id,
                        timestamp=current_date + timedelta(hours=random.randint(0, 23)),
                        data_used=data_used,
                        connection_time=connection_time,
                        ip_address=ip_address
                    )
                    db.session.add(record)

            current_date += timedelta(days=1)

        db.session.commit()

if __name__ == '__main__':
    init_db()
