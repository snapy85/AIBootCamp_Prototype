# src/Helpers/filters.py

RELEVANT_KEYWORDS = [
    # Core MDW-related
    "mdw", "maid", "helper", "domestic worker", "migrant",
    "employment agency", "accredited agency", "agency license",
    "work permit", "pass", "ipa", "in-principle approval",
    "employer", "employment contract", "contract terms",
    "rest day", "day off", "levy", "monthly levy",
    "placement fee", "transfer helper", "new helper",
    "replacement", "termination", "notice period",
    "insurance", "medical insurance", "personal accident insurance",
    "medical checkup", "six-monthly medical", "pregnancy test",
    "security bond", "orientation programme", "settling-in programme",
    "onboarding", "medical examination", "form submission",
    "mdw portal", "mom portal", "employment history",
    "employer eligibility", "hiring eligibility",
    "living conditions", "housing", "accommodation",
    "employer responsibilities", "employer obligations",
    "salary", "wages", "remittance", "bank account",
    "agency dispute", "complaint", "termination process",

    # Nanny/childcare-specific
    "nanny", "childcare", "babysitter", "infant care", "toddler care",
    "child safety", "child supervision", "child development",
    "feeding schedule", "nap schedule", "toilet training",
    "home-based childcare", "nanny duties", "childcare expectations",
    "early childhood", "pediatric first aid", "CPR training",
    "diaper changing", "milk preparation", "infant hygiene",
    "learning activities", "playtime supervision", "storytelling",
    "sleep routine", "discipline policy", "child emotional support",
    "bonding with child", "parental instructions", "nanny checklist", "nannies", "confinement"
]

INAPPROPRIATE_KEYWORDS = [
    "sex", "sexual", "nude", "naked", "intimacy", "intimate",
    "harass", "harassment", "molest", "rape", "assault", "abuse",
    "expose", "porn", "touch", "inappropriate", "kiss", "bed"
]

def is_question_relevant(question: str) -> bool:
    question = question.lower()
    return any(keyword in question for keyword in RELEVANT_KEYWORDS)

def is_question_safe(question: str) -> bool:
    question = question.lower()
    return not any(keyword in question for keyword in INAPPROPRIATE_KEYWORDS)
