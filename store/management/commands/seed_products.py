import requests
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from store.models import Product, ProductImage

PRODUCTS = [
    # =========================
    # RINGS
    # =========================
    {
        "name": "Royal Diamond Party Ring",
        "description": "Exquisite gold ring with a luxurious diamond design, perfect for parties and special occasions.",
        "price": 35000,
        "category": "Rings",
        "collection": "Party Wear",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/8891950/pexels-photo-8891950.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },
    {
        "name": "Classic Gold Daily Ring",
        "description": "Elegant gold ring with a simple and comfortable design for everyday wear.",
        "price": 18500,
        "category": "Rings",
        "collection": "Daily Wear",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/94843/pexels-photo-94843.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },
    {
        "name": "Diamond Bridal Ring",
        "description": "Beautiful diamond ring crafted for brides and memorable wedding celebrations.",
        "price": 46000,
        "category": "Rings",
        "collection": "Bridal Wear",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/9420323/pexels-photo-9420323.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },
    {
        "name": "Elegant Men's Gold Ring",
        "description": "Premium gold ring with a bold and sophisticated design for modern men.",
        "price": 32000,
        "category": "Rings",
        "collection": "Office Wear",
        "gender": "male",
        "images": [
            "https://images.pexels.com/photos/15727980/pexels-photo-15727980.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },

    # =========================
    # PENDANTS
    # =========================
    {
        "name": "Royal Emerald Pendant",
        "description": "Elegant gold pendant featuring a beautiful gemstone design for festive occasions.",
        "price": 32000,
        "category": "Pendants",
        "collection": "Special Festival",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/13292930/pexels-photo-13292930.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },
    {
        "name": "Minimal Gold Heart Pendant",
        "description": "Delicate gold heart pendant with a minimal design suitable for everyday styling.",
        "price": 15500,
        "category": "Pendants",
        "collection": "Daily Wear",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/12217206/pexels-photo-12217206.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },
    {
        "name": "Diamond Leaf Pendant",
        "description": "Graceful diamond-inspired pendant designed to add elegance to formal outfits.",
        "price": 42000,
        "category": "Pendants",
        "collection": "Office Wear",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/8768536/pexels-photo-8768536.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },
    {
        "name": "Ruby Celebration Pendant",
        "description": "Stylish gold pendant with a rich gemstone look designed for celebrations and festivals.",
        "price": 38500,
        "category": "Pendants",
        "collection": "Party Wear",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/4735888/pexels-photo-4735888.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },

    # =========================
    # CHAINS
    # =========================
    {
        "name": "Classic Men's Gold Chain",
        "description": "Strong and stylish gold chain designed for sophisticated everyday men's fashion.",
        "price": 45000,
        "category": "Chains",
        "collection": "Daily Wear",
        "gender": "male",
        "images": [
            "https://images.pexels.com/photos/14111392/pexels-photo-14111392.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },
    {
        "name": "Royal Gold Rope Chain",
        "description": "Luxurious rope-style gold chain with a premium finish for special occasions.",
        "price": 48000,
        "category": "Chains",
        "collection": "Party Wear",
        "gender": "male",
        "images": [
            "https://images.pexels.com/photos/14111396/pexels-photo-14111396.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },
    {
        "name": "Elegant Women's Gold Chain",
        "description": "Delicate gold chain designed to complement modern women's outfits with subtle elegance.",
        "price": 36000,
        "category": "Chains",
        "collection": "Office Wear",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/29557145/pexels-photo-29557145.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },
    {
        "name": "Premium Designer Chain",
        "description": "Statement gold chain featuring a refined designer finish for festive styling.",
        "price": 49000,
        "category": "Chains",
        "collection": "Special Festival",
        "gender": "male",
        "images": [
            "https://images.pexels.com/photos/18819278/pexels-photo-18819278.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },

    # =========================
    # EARRINGS
    # =========================
    {
        "name": "Elegant Gold Hoop Earrings",
        "description": "Classic gold hoop earrings with a modern finish, perfect for daily fashion.",
        "price": 22000,
        "category": "Earrings",
        "collection": "Daily Wear",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/12144990/pexels-photo-12144990.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },
    {
        "name": "Royal Diamond Earrings",
        "description": "Premium gold earrings with sparkling diamond details designed for elegant parties.",
        "price": 48000,
        "category": "Earrings",
        "collection": "Party Wear",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/16055232/pexels-photo-16055232.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },
    {
        "name": "Bridal Pearl Earrings",
        "description": "Traditional pearl and gold earrings created to complement bridal jewellery collections.",
        "price": 36000,
        "category": "Earrings",
        "collection": "Bridal Wear",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/13595292/pexels-photo-13595292.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },
    {
        "name": "Modern Geometric Earrings",
        "description": "Contemporary geometric gold earrings designed for stylish office and formal outfits.",
        "price": 19500,
        "category": "Earrings",
        "collection": "Office Wear",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/12145058/pexels-photo-12145058.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },

    # =========================
    # NECKLACES
    # =========================
    {
        "name": "Royal Bridal Necklace",
        "description": "Grand traditional necklace designed for bridal ceremonies and luxurious wedding looks.",
        "price": 49000,
        "category": "Necklaces",
        "collection": "Bridal Wear",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/29502955/pexels-photo-29502955.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },
    {
        "name": "Classic Gold Necklace",
        "description": "Timeless gold necklace with an elegant design suitable for everyday traditional wear.",
        "price": 45000,
        "category": "Necklaces",
        "collection": "Daily Wear",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/29502923/pexels-photo-29502923.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },
    {
        "name": "Luxury Pearl Necklace",
        "description": "Sophisticated pearl jewellery design with a premium finish for elegant celebrations.",
        "price": 47000,
        "category": "Necklaces",
        "collection": "Party Wear",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/6716445/pexels-photo-6716445.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },
    {
        "name": "Festive Gold Statement Necklace",
        "description": "Beautiful statement necklace designed to enhance traditional and festive outfits.",
        "price": 48500,
        "category": "Necklaces",
        "collection": "Special Festival",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/29502924/pexels-photo-29502924.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },

    # =========================
    # BRACELETS
    # =========================
    {
        "name": "Diamond Tennis Bracelet",
        "description": "Elegant diamond-inspired bracelet with a luxurious design for premium occasions.",
        "price": 49500,
        "category": "Bracelets",
        "collection": "Party Wear",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/25810584/pexels-photo-25810584.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },
    {
        "name": "Classic Gold Bracelet",
        "description": "Minimal gold bracelet designed for comfortable everyday styling.",
        "price": 42000,
        "category": "Bracelets",
        "collection": "Daily Wear",
        "gender": "male",
        "images": [
            "https://images.pexels.com/photos/12124662/pexels-photo-12124662.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },
    {
        "name": "Elegant Chain Bracelet",
        "description": "Stylish chain bracelet with a refined gold finish for modern fashion.",
        "price": 38000,
        "category": "Bracelets",
        "collection": "Office Wear",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/12155925/pexels-photo-12155925.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },
    {
        "name": "Royal Gemstone Bracelet",
        "description": "Luxurious gold bracelet decorated with colourful gemstone accents for festive occasions.",
        "price": 46000,
        "category": "Bracelets",
        "collection": "Special Festival",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/12194337/pexels-photo-12194337.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },

    # =========================
    # BANGLES
    # =========================
    {
        "name": "Traditional Gold Bangles",
        "description": "Beautiful traditional gold bangles crafted to complement festive Indian outfits.",
        "price": 47000,
        "category": "Bangles",
        "collection": "Special Festival",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/37485314/pexels-photo-37485314.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },
    {
        "name": "Designer Diamond Bangles",
        "description": "Elegant diamond-inspired bangles with a luxurious finish for bridal celebrations.",
        "price": 49000,
        "category": "Bangles",
        "collection": "Bridal Wear",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/17521716/pexels-photo-17521716.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },
    {
        "name": "Minimal Gold Bangle",
        "description": "Simple and elegant gold bangle designed for comfortable daily wear.",
        "price": 28000,
        "category": "Bangles",
        "collection": "Daily Wear",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/12194239/pexels-photo-12194239.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },
    {
        "name": "Royal Party Bangles",
        "description": "Glamorous gold bangles with a sophisticated design for parties and celebrations.",
        "price": 48000,
        "category": "Bangles",
        "collection": "Party Wear",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/13284499/pexels-photo-13284499.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },

    # =========================
    # SOLITAIRES
    # =========================
    {
        "name": "Classic Solitaire Diamond Ring",
        "description": "Timeless solitaire-inspired diamond ring designed for elegant and memorable occasions.",
        "price": 49000,
        "category": "Solitaires",
        "collection": "Diamond collection",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/37769382/pexels-photo-37769382.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },
    {
        "name": "Premium Men's Solitaire Ring",
        "description": "Bold solitaire-style ring crafted for men who prefer a refined luxury look.",
        "price": 48000,
        "category": "Solitaires",
        "collection": "Diamond collection",
        "gender": "male",
        "images": [
            "https://images.pexels.com/photos/8891950/pexels-photo-8891950.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },
    {
        "name": "Royal Solitaire Engagement Ring",
        "description": "Elegant solitaire engagement ring designed to celebrate unforgettable moments.",
        "price": 49500,
        "category": "Solitaires",
        "collection": "Diamond collection",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/9420323/pexels-photo-9420323.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    },
    {
        "name": "Luxury Diamond Solitaire",
        "description": "Premium solitaire jewellery piece featuring a sophisticated luxury design for special occasions.",
        "price": 49900,
        "category": "Solitaires",
        "collection": "Diamond collection",
        "gender": "female",
        "images": [
            "https://images.pexels.com/photos/15727980/pexels-photo-15727980.jpeg?auto=compress&cs=tinysrgb&w=1200"
        ]
    }
]


class Command(BaseCommand):
    help = "Seed database with sample products under 50000 using unique image URLs"

    def download_image(self, url):
        response = requests.get(url)
        return ContentFile(response.content)

    def handle(self, *args, **kwargs):
        for item in PRODUCTS:
            image_urls = item.pop("images")
            
            # Remove duplicate URLs from the list automatically
            image_urls = list(dict.fromkeys(image_urls))
            
            if not image_urls:
                continue

            first_url = image_urls[0]

            product = Product(**item)
            image_content = self.download_image(first_url)
            filename = first_url.split("/")[-1].split("?")[0]
            product.image.save(filename, image_content, save=True)

            # Add extra images only if they are unique and not same as first_url
            for extra_url in image_urls[1:]:
                if extra_url != first_url:
                    ProductImage.objects.create(product=product, image_url=extra_url)

            self.stdout.write(self.style.SUCCESS(f"Created: {product.name} (₹{product.price})"))