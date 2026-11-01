"""Seed content for PELIVET.

Edit these lists to change what appears on the site, then re-run `python seed.py`
(or hit /admin and use "Reseed content"). Keeping copy here means content lives
in version control alongside the code.
"""

SERVICES = [
    {
        "slug": "wellness-exams", "title": "Wellness exams", "icon": "pulse",
        "summary": "Head-to-tail checkups that catch problems early and keep your pet thriving through every life stage.",
        "description": "A wellness exam is the single most valuable thing you can do for your pet's long-term health. Our veterinarians perform a calm, unhurried head-to-tail assessment — eyes, ears, teeth, skin, heart, lungs, joints and weight — and talk you through what we find in plain language. Because we see your pet regularly, we spot subtle changes early, when they're easiest and most affordable to treat.",
        "includes": "Full physical examination\nWeight and body-condition scoring\nLife-stage and breed-specific advice\nParasite and vaccination review\nA written summary you can keep",
    },
    {
        "slug": "vaccinations", "title": "Vaccinations", "icon": "syringe",
        "summary": "Core and lifestyle vaccines on a schedule tailored to your pet's age, breed and daily adventures.",
        "description": "Vaccines are a simple, proven way to protect your companion from serious, often fatal diseases. We build a schedule around your pet — their age, breed, and how they actually live, whether that's a city apartment or weekends on the trail — so they get exactly the protection they need and nothing they don't.",
        "includes": "Core vaccines (rabies, distemper, parvo)\nLifestyle vaccines (kennel cough, leptospirosis)\nPuppy and kitten starter courses\nAnnual boosters with reminders\nVaccination certificate for travel and boarding",
    },
    {
        "slug": "dental-care", "title": "Dental care", "icon": "tooth",
        "summary": "Cleanings, extractions and at-home coaching to protect those teeth — and fresher, healthier breath.",
        "description": "Dental disease is the most common health problem in cats and dogs, and it's about far more than bad breath — untreated, it causes pain and affects the heart, liver and kidneys. We offer thorough cleanings under safe anaesthesia, extractions when needed, and practical coaching so you can keep those teeth healthy between visits.",
        "includes": "Dental assessment and charting\nScale and polish under safe anaesthesia\nDigital dental X-rays\nExtractions and pain management\nAt-home dental care plan",
    },
    {
        "slug": "surgery", "title": "Surgery", "icon": "cross",
        "summary": "Spays, neuters and soft-tissue procedures in a sterile suite, with pain management and gentle recovery.",
        "description": "From routine spays and neuters to soft-tissue procedures, our surgical suite is fully equipped and sterile, with modern monitoring at every step. Your pet's comfort and safety come first — individualised anaesthesia, proactive pain management, and a calm recovery with clear aftercare so you know exactly what to expect at home.",
        "includes": "Spay and neuter procedures\nSoft-tissue surgery\nMass and lump removals\nPre-anaesthetic bloodwork\nMulti-step pain management and recovery plan",
    },
    {
        "slug": "diagnostics-lab", "title": "Diagnostics & lab", "icon": "search",
        "summary": "On-site digital X-ray, ultrasound and bloodwork mean fast answers when every minute matters.",
        "description": "When your pet isn't themselves, waiting days for results is agonising. Our on-site laboratory and imaging mean we can run bloodwork, take digital X-rays and perform ultrasound during your visit — so we reach a diagnosis quickly and start the right treatment sooner.",
        "includes": "In-house blood chemistry and haematology\nDigital X-ray imaging\nUltrasound scanning\nUrinalysis and microscopy\nRapid tests for common conditions",
    },
    {
        "slug": "emergency-urgent", "title": "Emergency & urgent", "icon": "heart-pulse",
        "summary": "Sudden scare? Our team is ready with rapid triage and around-the-clock guidance when you need it most.",
        "description": "Emergencies don't keep office hours. If something's wrong, call our 24/7 line and a trained team member will triage over the phone and get you seen fast. From poisoning and injuries to sudden illness, we move quickly and keep you informed every step of the way.",
        "includes": "24/7 emergency phone line\nRapid triage and stabilisation\nUrgent same-day appointments\nCritical-care monitoring\nClear updates throughout",
    },
    {
        "slug": "parasite-nutrition", "title": "Parasite & nutrition", "icon": "shield",
        "summary": "Flea, tick and worm protection plus tailored diet plans to keep your companion at a healthy weight.",
        "description": "Prevention is the easiest medicine. We set up year-round protection against fleas, ticks and worms, and build a realistic nutrition plan around your pet's age, breed and goals — whether that's trimming a few kilos or supporting a growing puppy.",
        "includes": "Flea, tick and worm prevention\nWeight-management plans\nLife-stage nutrition advice\nPrescription and therapeutic diets\nFeeding guidance you can actually follow",
    },
    {
        "slug": "grooming-spa", "title": "Grooming & spa", "icon": "scissors",
        "summary": "Baths, nail trims and coat care in a calm, low-stress setting that leaves pets feeling great.",
        "description": "Good grooming isn't just about looking sharp — it's part of staying healthy and comfortable. Our gentle groomers work at your pet's pace in a calm, low-stress setting, keeping coats, nails and skin in great shape and flagging anything that needs a vet's attention.",
        "includes": "Bath and blow-dry\nBreed-specific clips and trims\nNail trims and ear cleaning\nDe-shedding treatments\nSkin and coat health checks",
    },
]

TEAM = [
    {"name": "Dr. Amina Karanja", "role": "Lead Veterinarian", "initials": "AK",
     "color": "#12304F", "bio": "15 years in small-animal medicine, with a soft spot for senior pets and a gift for calming anxious owners."},
    {"name": "Dr. David Otieno", "role": "Surgeon", "initials": "DO",
     "color": "#159AA8", "bio": "Precise hands and a calm manner that puts nervous owners at ease before, during and after surgery."},
    {"name": "Priya Mehta", "role": "Veterinary Nurse", "initials": "PM",
     "color": "#1E4E7A", "bio": "The gentle voice and steady hands your pet meets first — and the person who remembers their favourite treat."},
    {"name": "Joseph Wanjiru", "role": "Client Care Lead", "initials": "JW",
     "color": "#27B6C4", "bio": "Books your visits, remembers your pet's quirks, and greets every family with a genuine smile."},
]

TESTIMONIALS = [
    {"author": "Sarah M.", "pet": "Dog mum to Biscuit", "initials": "SM", "color": "#27B6C4",
     "rating": 5, "featured": True,
     "quote": "My old collie is terrified of vets, but the team here was so patient with him. First time he's ever come home relaxed. We won't go anywhere else."},
    {"author": "Tom N.", "pet": "Cat dad to Mochi", "initials": "TN", "color": "#159AA8",
     "rating": 5, "featured": False,
     "quote": "They caught my cat's kidney issue early during a routine check. Clear about the costs, kind about the hard bits. Genuinely grateful for this clinic."},
    {"author": "Lucy O.", "pet": "Puppy parent to Ziggy", "initials": "LO", "color": "#12304F",
     "rating": 5, "featured": False,
     "quote": "Called in a panic on a Sunday and they talked me through everything, then saw us within the hour. That kind of care is rare. Thank you, PELIVET."},
    {"author": "James K.", "pet": "Dog dad to Rex", "initials": "JK", "color": "#0E7A86",
     "rating": 5, "featured": False,
     "quote": "Rex needed surgery and I was terrified. Dr. Otieno explained every step and called me the next day to check in. Five stars isn't enough."},
    {"author": "Wanjiku N.", "pet": "Cat mum to Simba", "initials": "WN", "color": "#1E4E7A",
     "rating": 5, "featured": False,
     "quote": "Friendly front desk, spotless clinic, and they never rush you. Simba actually purrs on the exam table now, which tells you everything."},
    {"author": "Daniel A.", "pet": "Rabbit parent to Clover", "initials": "DA", "color": "#159AA8",
     "rating": 5, "featured": False,
     "quote": "Finding a vet who's great with rabbits is hard. These guys know their stuff and clearly love what they do. Highly recommend."},
]

FAQS = [
    {"q": "Do I need an appointment, or can I walk in?",
     "a": "We happily accept walk-ins and will always see emergencies, but booking ahead means shorter waits and a slot that suits you. You can book online in under a minute."},
    {"q": "What should I bring to my first visit?",
     "a": "Any previous medical records or vaccination certificates, a list of current medications, and — if possible — a recent stool sample. Most importantly, bring your questions."},
    {"q": "How do you keep anxious pets calm?",
     "a": "We practise fear-free, low-stress handling: unhurried visits, gentle restraint, treats, pheromone diffusers, and quiet rooms. We move at your pet's pace, never the clock's."},
    {"q": "Do you offer payment options?",
     "a": "We're transparent about costs upfront — no surprise bills. Talk to our front desk about available payment options and we'll find something that works for your family."},
    {"q": "What are your emergency hours?",
     "a": "Our emergency line is staffed 24 hours a day, 7 days a week. If something's wrong outside normal hours, call us and we'll triage immediately."},
]
