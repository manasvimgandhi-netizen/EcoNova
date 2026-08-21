# data.py
"""
EcoNova: Mock Datasets for Smart City Waste Platform
"""

citizens = [
    {
        "id": "c1",
        "name": "Aarav Sharma",
        "neighborhood": "Kothrud, Sector 4",
        "points": 65,
        "streak": 4,
        "badge": "🍃 Leaf Guardian",
        "co2_total": 12.4,
    },
    {
        "id": "c2",
        "name": "Ananya Patel",
        "neighborhood": "Kothrud, Sector 4",
        "points": 180,
        "streak": 12,
        "badge": "🌳 Tree Protector",
        "co2_total": 28.5,
    },
    {
        "id": "c3",
        "name": "Rohan Gupta",
        "neighborhood": "Shivajinagar Hub",
        "points": 30,
        "streak": 2,
        "badge": "🌱 Seedling Scout",
        "co2_total": 5.1,
    },
]

eco_reels = [
    {
        "id": "reel_1",
        "title": "How I turned 5 plastic bottles into a vertical planter 🌱",
        "category": "DIY Reuse",
        "creator": "@rewild.pune",
        "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
        "likes": "1,240",
        "comments": "86",
        "shares": "312",
        "caption": "Never discard empty plastic bottles! Cut a 4-inch side opening, drill drainage holes, and hang them up as a vertical herb wall."
    },
    {
        "id": "reel_2",
        "title": "Why Aluminium Cans are 100% Infinitely Recyclable ♻️",
        "category": "Waste Facts",
        "creator": "@zerowaste.lab",
        "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
        "likes": "3,581",
        "comments": "142",
        "shares": "890",
        "caption": "Recycling an aluminium can takes 95% less energy than mining virgin bauxite. It can be remelted and back on shelves in 60 days!"
    }
]

hotspots = [
    {
        "id": "H1",
        "location": "Main Market Fruit Stall Lane",
        "lat": 18.5204,
        "lng": 73.8567,
        "waste_type": "Mixed Plastic & Organic",
        "notes": "Large overflow behind stall #4 blocking sidewalk",
        "status": "Pending",
        "reported_by": "Aarav Sharma",
    },
    {
        "id": "H2",
        "location": "Station Road Bus Depot Gate",
        "lat": 18.5314,
        "lng": 73.8446,
        "waste_type": "Plastic Bottles & Wrappers",
        "notes": "Unsegregated dry waste pile near pedestrian crossing",
        "status": "Pending",
        "reported_by": "Ananya Patel",
    },
    {
        "id": "H3",
        "location": "Green Park Gate 2 Corner",
        "lat": 18.5100,
        "lng": 73.8620,
        "waste_type": "Dry Cardboard Boxes",
        "notes": "Scattered packaging boxes after weekly farmers market",
        "status": "Resolved",
        "reported_by": "Rohan Gupta",
    },
]