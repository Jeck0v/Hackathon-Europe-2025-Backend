from db.session import get_db

data_user = [
    {
    }
]

data_feed = [
        {
            "id_subject": "1",
            "title": "EU Defense Spending Increase",
            "short_description": "The European Union plans a historic rise in defense spending to bolster its defense capabilities.",
            "image": "https://example.com/eu_defense_spending.jpg",
            "context": "In response to escalating geopolitical tensions and security concerns, EU leaders have agreed to significantly increase defense expenditures. This move aims to enhance the EU's autonomous defense capabilities and reduce reliance on external powers.",
            "impact": [
                "Strengthened EU defense infrastructure",
                "Increased investment in defense technologies",
                "Enhanced security for EU member states"
            ],
            "source": "The Guardian",
            "votes": {"0": 0, "1": 0, "2": 0}
        },
        {
            "id_subject": "2",
            "title": "EU's Support for Ukraine Amid Ongoing Conflict",
            "short_description": "EU leaders to discuss continued support for Ukraine in light of ongoing conflicts.",
            "image": "https://example.com/eu_ukraine_support.jpg",
            "context": "The European Council is set to address the latest developments in Russia's aggression against Ukraine and reaffirm the EU's commitment to supporting Ukraine through financial aid, military assistance, and humanitarian support.",
            "impact": [
                "Continued financial and military aid to Ukraine",
                "Strengthening of EU's geopolitical stance",
                "Potential economic implications for EU member states"
            ],
            "source": "European Movement",
            "votes": {"0": 0, "1": 0, "2": 0}
        },
        {
            "id_subject": "3",
            "title": "EU Migration Policy Reforms",
            "short_description": "The European Council to discuss strategic approaches to migration management.",
            "image": "https://example.com/eu_migration_policy.jpg",
            "context": "In light of recent migration challenges, EU leaders will engage in a strategic debate on migration, focusing on enhancing border security, improving asylum procedures, and fostering cooperation with third countries.",
            "impact": [
                "Strengthened EU border management",
                "Reformed asylum and migration policies",
                "Improved cooperation with non-EU countries"
            ],
            "source": "European Movement",
            "votes": {"0": 0, "1": 0, "2": 0}
        },
        {
            "id_subject": "4",
            "title": "EU's Climate Target for 2040",
            "short_description": "Environment ministers to discuss the EU's climate objectives for 2040.",
            "image": "https://example.com/eu_climate_target.jpg",
            "context": "EU environment ministers will convene to deliberate on the proposed climate targets for 2040, aiming to reinforce the EU's commitment to combating climate change and transitioning to a sustainable economy.",
            "impact": [
                "Setting ambitious emission reduction goals",
                "Promotion of renewable energy sources",
                "Influence on global climate policies"
            ],
            "source": "Industry Intelligence Inc.",
            "votes": {"0": 0, "1": 0, "2": 0}
        },
        {
            "id_subject": "5",
            "title": "EU Enlargement and Relations with Western Balkans",
            "short_description": "EU to discuss the accession process and cooperation with Western Balkan countries.",
            "image": "https://example.com/eu_western_balkans.jpg",
            "context": "The European Council will assess the progress of Western Balkan countries in their EU accession processes and explore ways to enhance regional cooperation and integration into the EU single market.",
            "impact": [
                "Potential expansion of the EU",
                "Strengthened political and economic ties",
                "Promotion of stability in the Western Balkans"
            ],
            "source": "European Movement",
            "votes": {"0": 0, "1": 0, "2": 0}
        },
        {
          "id_subject": "6",
          "title": "EU Artificial Intelligence Act Implementation",
          "short_description": "The European Union is set to implement the world's first comprehensive AI legislation, the Artificial Intelligence Act, aiming to regulate AI technologies based on their associated risks.",
          "image": "ttps://example.com/eu_western_balkans.jp]",
          "context": "The European Union has introduced the Artificial Intelligence Act to oversee the development and application of AI technologies. The legislation categorizes AI systems into four risk levels—minimal, limited, high, and unacceptable—with corresponding regulatory requirements. Officially published on July 12, 2024, the Act will enter into force on August 1, 2024, with full application by August 2, 2026. Some provisions, such as those banning certain AI practices, will apply earlier, starting February 2, 2025.",
          "impact": [
            "Regulatory sandboxes to support AI innovation",
            "Strict penalties for non-compliance, up to €35 million or 7% of global turnover"
          ],
          "source": "CECE - Committee for European Construction Equipment",
          "votes": {"0": 0, "1": 0, "2": 0}
        },
]

data_compromise = [
    {
        "id_subject": "1",
        "id_user": "1",
        "text": "Je test l'application"
    }
]
DEMO_compromise = [
    {
        "id_subject": "1",
        "text": "Je ne veux pas que mon argent parte n'importe où"
    }
]

def initialize_database():
    db = get_db()
    required_collections = ['users', 'feed', 'compromise', 'demo']
    existing_collections = db.list_collection_names()
    for collection in required_collections:
        if collection not in existing_collections:
            db.create_collection(collection)
            print(f"Collection '{collection}' créée.")

            # Make it better (just did it to be quick)
            try:
                match collection:
                    case 'users':
                        db[collection].insert_many(data_user)
                    case 'feed':
                        db[collection].insert_many(data_feed)
                    case 'compromise':
                        db[collection].insert_many(data_compromise)
                    case 'demo':
                        db[collection].insert_many(DEMO_compromise)
            except Exception as e:
                print(f"Error inserting data into {collection}: {e}")


initialize_database()
