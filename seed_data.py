import uuid
from database import engine, Base, SessionLocal
from models import Suspect, CaseTemplate

def reset_database():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)

def seed_suspects(db):
    suspects = [
        Suspect(key="chef", name="Vidhur", occupation="Head chef", personality="Warm but easily flustered under pressure. Talks with his hands, over-shares about the kitchen.", background="Head chef at the manor for 12 years. Fiercely protective of his kitchen staff."),
        Suspect(key="librarian", name="Elena", occupation="Librarian", personality="Precise, a little cold, chooses her words carefully. Dislikes being interrupted.", background="Has curated the manor's private library for 8 years. Knows most of the house's old secrets."),
        Suspect(key="caretaker", name="Owen", occupation="Caretaker", personality="Gruff, plainspoken, seems bored by questions but notices everything.", background="Maintains the grounds and cellar. Been with the family since before the current owner."),
        Suspect(key="teacher", name="Priya", occupation="Tutor", personality="Composed, articulate, slightly performative - used to being listened to.", background="Tutors the family's children three days a week. A recent addition to the household."),
        Suspect(key="mailman", name="Frank", occupation="Mailman", personality="Chatty, eager to be helpful, sometimes to the point of rambling off-topic.", background="Delivers to the manor daily and knows the comings and goings of the whole estate.")
    ]
    for s in suspects:
        db.add(s)
    db.commit()

def seed_cases(db):
    cases = [
        CaseTemplate(
            id=str(uuid.uuid4()),
            victim="Mr. Blackwood",
            location="The Wine Cellar",
            method="Poisoned vintage wine",
            window="9:00 PM - 10:00 PM",
            motive="Blackwood was going to sell the estate and fire the entire staff without severance.",
            murderer_key="chef",
            suspect_facts={
                "chef": {
                    "alibi": {"truth": "I was supposedly in the kitchen, but I actually slipped down to the cellar at 9:15 to deliver the wine.", "evasive": True, "reason": "I am the murderer and don't want anyone to know I was in the cellar."},
                    "relationship": {"truth": "I hated him. He disrespected my craft and threatened my livelihood.", "evasive": True, "reason": "My hatred gives me an obvious motive."},
                    "saw": {"truth": "I saw Elena pacing near the library upstairs.", "evasive": False, "reason": ""},
                    "rumor": {"truth": "People say Owen has been stealing from the cellar, but I know it's a lie.", "evasive": False, "reason": ""}
                },
                "librarian": {
                    "alibi": {"truth": "I was organizing the archives from 8:00 PM to 11:00 PM.", "evasive": False, "reason": ""},
                    "relationship": {"truth": "He was a brute who didn't appreciate literature. We rarely spoke.", "evasive": False, "reason": ""},
                    "saw": {"truth": "I heard heavy footsteps on the stairs around 9:30 PM, but I didn't see who it was.", "evasive": True, "reason": "I am secretly losing my hearing and don't want anyone to know, so I'm vague about sounds."},
                    "rumor": {"truth": "I heard Vidhur arguing with Blackwood earlier this afternoon.", "evasive": False, "reason": ""}
                },
                "caretaker": {
                    "alibi": {"truth": "I was checking the perimeter near the greenhouse. Didn't go near the cellar.", "evasive": False, "reason": ""},
                    "relationship": {"truth": "I'm paid to work, not to like him.", "evasive": False, "reason": ""},
                    "saw": {"truth": "I saw Vidhur coming up from the cellar stairs looking flushed.", "evasive": False, "reason": ""},
                    "rumor": {"truth": "Priya looked very nervous today, kept looking over her shoulder.", "evasive": False, "reason": ""}
                },
                "teacher": {
                    "alibi": {"truth": "I was in my room grading papers. I had a headache and locked the door.", "evasive": True, "reason": "I was actually meeting someone secretly outside, but it has nothing to do with the murder."},
                    "relationship": {"truth": "He employed me. That's all.", "evasive": False, "reason": ""},
                    "saw": {"truth": "I didn't see anything. I was alone in my room.", "evasive": True, "reason": "I'm sticking to my fake alibi."},
                    "rumor": {"truth": "Frank usually delivers packages around 8 PM, but he was late tonight.", "evasive": False, "reason": ""}
                },
                "mailman": {
                    "alibi": {"truth": "I was finishing my route, got caught in the rain.", "evasive": False, "reason": ""},
                    "relationship": {"truth": "Just a customer. He tipped poorly.", "evasive": False, "reason": ""},
                    "saw": {"truth": "I saw Priya sneaking back in through the side door at 9:45 PM.", "evasive": False, "reason": ""},
                    "rumor": {"truth": "Everyone knows the chef hated him.", "evasive": False, "reason": ""}
                }
            }
        ),
        CaseTemplate(
            id=str(uuid.uuid4()),
            victim="Lady Eleanor",
            location="The Greenhouse",
            method="Strangulation with a gardening hose",
            window="10:00 PM - 11:00 PM",
            motive="She discovered a dark secret from the past and was going to report it to the authorities.",
            murderer_key="caretaker",
            suspect_facts={
                "chef": {
                    "alibi": {"truth": "I was cleaning the kitchen after the dinner service.", "evasive": False, "reason": ""},
                    "relationship": {"truth": "She was demanding, but she appreciated my cooking.", "evasive": False, "reason": ""},
                    "saw": {"truth": "I saw Owen taking a long piece of hose from the shed.", "evasive": False, "reason": ""},
                    "rumor": {"truth": "Frank was asking a lot of questions about Lady Eleanor's schedule.", "evasive": False, "reason": ""}
                },
                "librarian": {
                    "alibi": {"truth": "I fell asleep in the reading room.", "evasive": True, "reason": "I was actually reading a forbidden book from her private collection."},
                    "relationship": {"truth": "We shared a love for rare books. I respected her.", "evasive": False, "reason": ""},
                    "saw": {"truth": "I didn't see anything, I was 'asleep'.", "evasive": True, "reason": "Trying to maintain my alibi."},
                    "rumor": {"truth": "I know Owen hated how she treated him like a peasant.", "evasive": False, "reason": ""}
                },
                "caretaker": {
                    "alibi": {"truth": "I was in the greenhouse, but I left at 9:30 PM.", "evasive": True, "reason": "I am the murderer and was there during the window."},
                    "relationship": {"truth": "She was a tyrant who threatened to have me arrested for a past mistake.", "evasive": True, "reason": "This is my motive for the murder."},
                    "saw": {"truth": "I saw no one. It was dark.", "evasive": False, "reason": ""},
                    "rumor": {"truth": "I think the chef has been stealing food.", "evasive": False, "reason": ""}
                },
                "teacher": {
                    "alibi": {"truth": "I was in the parlor playing the piano.", "evasive": False, "reason": ""},
                    "relationship": {"truth": "She was very kind to me, actually.", "evasive": False, "reason": ""},
                    "saw": {"truth": "I saw a shadow moving near the greenhouse around 10:15 PM.", "evasive": False, "reason": ""},
                    "rumor": {"truth": "The librarian seemed very secretive about some new books.", "evasive": False, "reason": ""}
                },
                "mailman": {
                    "alibi": {"truth": "I was off duty, having a drink at the local pub.", "evasive": False, "reason": ""},
                    "relationship": {"truth": "Rarely spoke to her directly.", "evasive": False, "reason": ""},
                    "saw": {"truth": "I wasn't near the manor.", "evasive": False, "reason": ""},
                    "rumor": {"truth": "People at the pub said Owen was furious today.", "evasive": False, "reason": ""}
                }
            }
        ),
        CaseTemplate(
            id=str(uuid.uuid4()),
            victim="Professor Sterling",
            location="The Boathouse",
            method="Blunt force trauma from an oar",
            window="Midnight - 1:00 AM",
            motive="He was about to expose academic fraud.",
            murderer_key="teacher",
            suspect_facts={
                "chef": {
                    "alibi": {"truth": "I was fast asleep in my quarters.", "evasive": False, "reason": ""},
                    "relationship": {"truth": "He was a guest. I just cooked for him.", "evasive": False, "reason": ""},
                    "saw": {"truth": "Nothing, I sleep soundly.", "evasive": False, "reason": ""},
                    "rumor": {"truth": "I heard Priya pacing in her room right above mine.", "evasive": False, "reason": ""}
                },
                "librarian": {
                    "alibi": {"truth": "I was cataloging some new donations.", "evasive": False, "reason": ""},
                    "relationship": {"truth": "He was brilliant but arrogant.", "evasive": False, "reason": ""},
                    "saw": {"truth": "I saw Priya heading towards the lake around midnight.", "evasive": False, "reason": ""},
                    "rumor": {"truth": "Sterling and Priya had a loud argument yesterday.", "evasive": False, "reason": ""}
                },
                "caretaker": {
                    "alibi": {"truth": "I was repairing a leak in the roof.", "evasive": True, "reason": "I was actually slacking off and drinking in the shed."},
                    "relationship": {"truth": "Didn't know him.", "evasive": False, "reason": ""},
                    "saw": {"truth": "I heard a loud splash, but didn't look.", "evasive": True, "reason": "I don't want anyone to know I was drinking in the shed."},
                    "rumor": {"truth": "Priya seemed very angry at dinner.", "evasive": False, "reason": ""}
                },
                "teacher": {
                    "alibi": {"truth": "I was taking a midnight stroll by the lake, but not near the boathouse.", "evasive": True, "reason": "I am the murderer and was exactly at the boathouse."},
                    "relationship": {"truth": "He was my mentor, but he stole my research and was going to take credit for it.", "evasive": True, "reason": "This is my motive for the murder."},
                    "saw": {"truth": "I thought I saw someone else near the water, maybe Owen?", "evasive": True, "reason": "I am trying to shift the blame."},
                    "rumor": {"truth": "Sterling made a lot of enemies.", "evasive": False, "reason": ""}
                },
                "mailman": {
                    "alibi": {"truth": "I was doing a late-night special delivery.", "evasive": True, "reason": "I was delivering contraband, unrelated to the murder."},
                    "relationship": {"truth": "Never met him.", "evasive": False, "reason": ""},
                    "saw": {"truth": "I saw a woman's silhouette by the boathouse.", "evasive": True, "reason": "I don't want to admit I was there delivering contraband, but I did see this."},
                    "rumor": {"truth": "I heard the professor was a fraud.", "evasive": False, "reason": ""}
                }
            }
        )
    ]
    for c in cases:
        db.add(c)
    db.commit()

if __name__ == "__main__":
    reset_database()
    db = SessionLocal()
    try:
        seed_suspects(db)
        seed_cases(db)
        print("Database seeded successfully with 5 suspects and 3 hand-written cases.")
    finally:
        db.close()
