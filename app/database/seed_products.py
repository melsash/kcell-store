import logging

from app.database.db import SessionLocal
from app.models.product import Product

logger = logging.getLogger(__name__)

DEMO_PRODUCTS = [
    {
        "name": "iPhone 16 Pro",
        "description": "6.3-inch ProMotion display, A18 Pro chip, titanium design, and advanced camera system.",
        "price": 699_990,
        "image": "https://placehold.co/600x600/1d1d1f/ffffff/png?text=iPhone+16+Pro",
    },
    {
        "name": "iPhone 16",
        "description": "6.1-inch Super Retina XDR display, A18 chip, Dynamic Island, and all-day battery life.",
        "price": 549_990,
        "image": "https://placehold.co/600x600/1d1d1f/ffffff/png?text=iPhone+16",
    },
    {
        "name": "Samsung Galaxy S25 Ultra",
        "description": "200 MP camera, S Pen support, Snapdragon flagship performance, and 5000 mAh battery.",
        "price": 649_990,
        "image": "https://placehold.co/600x600/1428a0/ffffff/png?text=Galaxy+S25+Ultra",
    },
    {
        "name": "Samsung Galaxy S25",
        "description": "Compact flagship with vivid AMOLED display, pro-grade AI features, and fast charging.",
        "price": 449_990,
        "image": "https://placehold.co/600x600/1428a0/ffffff/png?text=Galaxy+S25",
    },
    {
        "name": "Google Pixel 9 Pro",
        "description": "Best-in-class computational photography, pure Android, and seven years of updates.",
        "price": 499_990,
        "image": "https://placehold.co/600x600/4285f4/ffffff/png?text=Pixel+9+Pro",
    },
    {
        "name": "Apple Watch Series 10",
        "description": "Thinner design, brighter Always-On display, advanced health sensors, and fast charging.",
        "price": 249_990,
        "image": "https://placehold.co/600x600/1d1d1f/ffffff/png?text=Watch+Series+10",
    },
    {
        "name": "AirPods Pro 2",
        "description": "Active Noise Cancellation, Adaptive Audio, USB-C case, and personalized spatial sound.",
        "price": 129_990,
        "image": "https://placehold.co/600x600/1d1d1f/ffffff/png?text=AirPods+Pro+2",
    },
    {
        "name": "iPad Air M3",
        "description": "11-inch Liquid Retina display, M3 chip, Apple Pencil Pro support, and all-day productivity.",
        "price": 399_990,
        "image": "https://placehold.co/600x600/1d1d1f/ffffff/png?text=iPad+Air+M3",
    },
]


def seed_products_if_empty() -> None:
    db = SessionLocal()
    try:
        if db.query(Product).first() is not None:
            logger.info("Products table already has data; skipping demo seed.")
            return

        for item in DEMO_PRODUCTS:
            db.add(Product(**item))

        db.commit()
        logger.info("Seeded %d demo products.", len(DEMO_PRODUCTS))
    finally:
        db.close()
