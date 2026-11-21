import os
import django
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from users.models import User
from events.models import Category, Event, TicketType
from bookings.models import Booking, BookingItem, Ticket, Payment
from bookings.utils import generate_qr_base64

def seed():
    print("Seeding database...")

    # 1. Create Users
    admin_user, _ = User.objects.get_or_create(
        email='admin@eventhub.com',
        defaults={
            'username': 'admin',
            'name': 'System Administrator',
            'phone': '+91 98765 43210',
            'role': 'Admin',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    admin_user.set_password('Admin@123')
    admin_user.save()

    organizer_user, _ = User.objects.get_or_create(
        email='organizer@eventhub.com',
        defaults={
            'username': 'organizer',
            'name': 'LiveNation Entertainment',
            'phone': '+91 98765 01234',
            'role': 'Organizer',
        }
    )
    organizer_user.set_password('Organizer@123')
    organizer_user.save()

    attendee_user, _ = User.objects.get_or_create(
        email='attendee@eventhub.com',
        defaults={
            'username': 'attendee',
            'name': 'Rahul Sharma',
            'phone': '+91 99887 76655',
            'role': 'Attendee',
        }
    )
    attendee_user.set_password('Attendee@123')
    attendee_user.save()

    print(f"Users created: {admin_user.email}, {organizer_user.email}, {attendee_user.email}")

    # 2. Categories
    categories_data = [
        {'name': 'Concerts', 'slug': 'concerts', 'icon': 'music'},
        {'name': 'Shows & Theatre', 'slug': 'shows-theatre', 'icon': 'theater'},
        {'name': 'Sports', 'slug': 'sports', 'icon': 'trophy'},
        {'name': 'Conferences', 'slug': 'conferences', 'icon': 'calendar'},
        {'name': 'Festivals', 'slug': 'festivals', 'icon': 'sparkles'},
        {'name': 'Events & Gaming', 'slug': 'events-gaming', 'icon': 'gamepad'},
        {'name': 'Workshops', 'slug': 'workshops', 'icon': 'users'},
    ]

    cat_map = {}
    for c in categories_data:
        cat_obj, _ = Category.objects.get_or_create(
            name=c['name'],
            defaults={'slug': c['slug'], 'icon': c['icon']}
        )
        cat_map[c['slug']] = cat_obj
    print(f"Categories seeded: {len(cat_map)}")

    # 3. Events matching UI Image precisely
    events_data = [
        {
            'title': 'The Weeknd Live in Concert',
            'category': cat_map['concerts'],
            'city': 'Kochi',
            'venue': 'National Stadium, Kochi',
            'start_datetime': timezone.now() + timedelta(days=30, hours=19),
            'end_datetime': timezone.now() + timedelta(days=30, hours=23),
            'status': 'Published',
            'is_featured': True,
            'banner_image': 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?q=80&w=1200&auto=format&fit=crop',
            'description': 'Experience the global superstar The Weeknd live in concert on his monumental world tour in Kochi. Featuring breathtaking visual effects, soaring synthesizers, and massive hits including Blinding Lights, Starboy, and Save Your Tears.',
            'ticket_types': [
                {'name': 'General Admission', 'price': 2999.00, 'total': 800},
                {'name': 'Silver Fan Pit', 'price': 4999.00, 'total': 300},
                {'name': 'VIP Lounge & After-Party', 'price': 9999.00, 'total': 100},
            ]
        },
        {
            'title': 'India vs Australia – T20',
            'category': cat_map['sports'],
            'city': 'Mumbai',
            'venue': 'Wankhede Stadium, Mumbai',
            'start_datetime': timezone.now() + timedelta(days=38, hours=19),
            'end_datetime': timezone.now() + timedelta(days=38, hours=23),
            'status': 'Published',
            'is_featured': True,
            'banner_image': 'https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?q=80&w=1200&auto=format&fit=crop',
            'description': 'Witness the epic cricketing showdown under the floodlights at the iconic Wankhede Stadium. India takes on World Champions Australia in an electric T20 international encounter with world-class rivalries.',
            'ticket_types': [
                {'name': 'North Stand (Level 3)', 'price': 1499.00, 'total': 1200},
                {'name': 'Sachin Tendulkar Stand', 'price': 2999.00, 'total': 600},
                {'name': 'Grand Pavilion Box (Hospitality)', 'price': 7499.00, 'total': 150},
            ]
        },
        {
            'title': 'Sunburn Music Festival',
            'category': cat_map['festivals'],
            'city': 'Goa',
            'venue': 'Candolim Beach, Goa',
            'start_datetime': timezone.now() + timedelta(days=36, hours=17),
            'end_datetime': timezone.now() + timedelta(days=39, hours=2),
            'status': 'Published',
            'is_featured': True,
            'banner_image': 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=1200&auto=format&fit=crop',
            'description': "Asia's premier Electronic Dance Music festival returns to the sun-soaked shores of Candolim Beach, Goa. 3 days of world-class DJ sets, hypnotic laser displays, beachside lounges, and unforgettable coastal vibes.",
            'ticket_types': [
                {'name': 'Single Day Festival Pass', 'price': 3499.00, 'total': 900},
                {'name': '3-Day Season Pass', 'price': 7999.00, 'total': 500},
                {'name': 'VIP Elevated Deck Pass', 'price': 14999.00, 'total': 100},
            ]
        },
        {
            'title': 'AI & Innovation Workshop',
            'category': cat_map['workshops'],
            'city': 'Trivandrum',
            'venue': 'Trivandrum Tech Park',
            'start_datetime': timezone.now() + timedelta(days=32, hours=9),
            'end_datetime': timezone.now() + timedelta(days=32, hours=17),
            'status': 'Published',
            'is_featured': True,
            'banner_image': 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1200&auto=format&fit=crop',
            'description': 'A hands-on, immersive masterclass on generative AI, agentic systems, multimodal intelligence, and LLM architecture. Designed for engineers, tech leads, and founders seeking practical production-grade AI deployment skills.',
            'ticket_types': [
                {'name': 'Student Access Pass', 'price': 999.00, 'total': 200},
                {'name': 'Professional Developer Pass', 'price': 1999.00, 'total': 250},
                {'name': 'Executive Hands-on Lab Pass', 'price': 3999.00, 'total': 60},
            ]
        },
        {
            'title': 'Comic Con India 2026',
            'category': cat_map['events-gaming'],
            'city': 'Bengaluru',
            'venue': 'KTPO Trade Center, Whitefield',
            'start_datetime': timezone.now() + timedelta(days=45, hours=10),
            'end_datetime': timezone.now() + timedelta(days=47, hours=20),
            'status': 'Published',
            'is_featured': False,
            'banner_image': 'https://images.unsplash.com/photo-1563089145-599997674d42?q=80&w=1200&auto=format&fit=crop',
            'description': 'The ultimate pop culture celebration! Featuring celebrity guests, comic creators, cosplay championships, gaming arenas, exclusive merchandise, and experiential zones.',
            'ticket_types': [
                {'name': 'Standard 1-Day Pass', 'price': 799.00, 'total': 1500},
                {'name': 'SuperFan 3-Day Pass', 'price': 1999.00, 'total': 500},
            ]
        },
        {
            'title': 'The Lion King – Broadway Musical',
            'category': cat_map['shows-theatre'],
            'city': 'Delhi NCR',
            'venue': 'Kingdom of Dreams Arena, Gurugram',
            'start_datetime': timezone.now() + timedelta(days=25, hours=18),
            'end_datetime': timezone.now() + timedelta(days=25, hours=21),
            'status': 'Published',
            'is_featured': False,
            'banner_image': 'https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?q=80&w=1200&auto=format&fit=crop',
            'description': "Experience the world's most acclaimed stage musical live in India. Stunning puppetry, majestic costumes, and timeless African rhythms brought to life by an award-winning international cast.",
            'ticket_types': [
                {'name': 'Balcony Seating', 'price': 1899.00, 'total': 400},
                {'name': 'Orchestra Stalls', 'price': 3499.00, 'total': 300},
                {'name': 'Royal Box Premium', 'price': 6999.00, 'total': 50},
            ]
        },
        {
            'title': 'Global Tech Leaders Conference',
            'category': cat_map['conferences'],
            'city': 'Hyderabad',
            'venue': 'HICC Novotel, HITEC City',
            'start_datetime': timezone.now() + timedelta(days=50, hours=9),
            'end_datetime': timezone.now() + timedelta(days=51, hours=18),
            'status': 'Published',
            'is_featured': False,
            'banner_image': 'https://images.unsplash.com/photo-1511578314322-379afb476865?q=80&w=1200&auto=format&fit=crop',
            'description': 'Connecting Fortune 500 CTOs, visionary startup founders, and global venture investors to discuss cloud architecture, cybersecurity, and exponential AI infrastructure.',
            'ticket_types': [
                {'name': 'Delegate Pass', 'price': 4999.00, 'total': 400},
                {'name': 'VIP All-Access & Networking Dinner', 'price': 11999.00, 'total': 100},
            ]
        }
    ]

    for edata in events_data:
        ticket_types = edata.pop('ticket_types')
        event_obj, created = Event.objects.get_or_create(
            title=edata['title'],
            defaults={**edata, 'organizer': organizer_user}
        )
        if created:
            for tt in ticket_types:
                TicketType.objects.create(
                    event=event_obj,
                    name=tt['name'],
                    price=tt['price'],
                    total_quantity=tt['total'],
                    available_quantity=tt['total']
                )
    print(f"Events seeded: {len(events_data)}")

    # 4. Seed an initial confirmed booking for attendee so "My Bookings" has immediate realistic data
    weeknd_event = Event.objects.filter(title__icontains='Weeknd').first()
    if weeknd_event and not Booking.objects.filter(user=attendee_user).exists():
        tt = weeknd_event.ticket_types.first()
        b_ref = "EH-20261120-WKD01"
        subtotal = tt.price * 2
        tax_amt = (subtotal * Decimal('0.05')).quantize(Decimal('0.01'))
        svc_fee = Decimal('40.00')
        tot_amt = subtotal + tax_amt + svc_fee

        b_booking = Booking.objects.create(
            reference=b_ref,
            user=attendee_user,
            event=weeknd_event,
            status='Confirmed',
            subtotal=subtotal,
            tax_amount=tax_amt,
            service_fee=svc_fee,
            discount_amount=Decimal('0.00'),
            total_amount=tot_amt,
            hold_expires_at=timezone.now() + timedelta(minutes=10),
            attendee_name=attendee_user.name,
            attendee_email=attendee_user.email,
            attendee_phone=attendee_user.phone
        )
        b_item = BookingItem.objects.create(
            booking=b_booking,
            ticket_type=tt,
            quantity=2,
            unit_price=tt.price
        )
        # 2 tickets with QR codes
        for idx in range(1, 3):
            tcode = f"TKT-{b_ref}-{tt.id}-{idx}"
            Ticket.objects.create(
                booking_item=b_item,
                booking=b_booking,
                code=tcode,
                qr_image=generate_qr_base64(tcode),
                is_used=False
            )
        Payment.objects.create(
            booking=b_booking,
            gateway_order_id="order_demo_1001",
            gateway_payment_id="pay_demo_2001",
            amount=b_booking.total_amount,
            status='Successful',
            method='card'
        )
        print("Sample confirmed booking seeded for attendee_user!")

    print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed()
