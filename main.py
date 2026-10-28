# ==========================================================
# SYNC - MAIN FASTAPI APPLICATION
# ==========================================================


# ==========================================================
# IMPORTS
# ==========================================================

import os

import httpx

from dotenv import load_dotenv
from groq import Groq

from fastapi import (
    FastAPI,
    Request,
    Query,
    HTTPException
)

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel, Field

from database import Base, engine
from models.user import User
from models.user_profile import UserProfile
from models.todo import TodoTask

from routers.auth import router as auth_router
from routers.todo import router as todo_router


# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# ==========================================================
# GROQ CLIENT
# ==========================================================

groq_client = None

if GROQ_API_KEY:

    groq_client = Groq(
        api_key=GROQ_API_KEY
    )

else:

    print(
        "WARNING: GROQ_API_KEY was not found in .env"
    )


# ==========================================================
# DATABASE
# ==========================================================
# DATABASE
# DATABASE
Base.metadata.create_all(bind=engine)


# ==========================================================
# FASTAPI APP
# ==========================================================

app = FastAPI(
    title="SYNC"
)


# ==========================================================
# STATIC FILES
# ==========================================================

app.mount(
    "/static",
    StaticFiles(
        directory="static"
    ),
    name="static"
)


# ==========================================================
# TEMPLATES
# ==========================================================

templates = Jinja2Templates(
    directory="templates"
)


# ==========================================================
# AUTH ROUTER
# ==========================================================

app.include_router(
    auth_router
)
app.include_router(
    todo_router
)


# ==========================================================
# HOME / LOGIN
# ==========================================================

@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


# ==========================================================
# LOGIN
# ==========================================================

@app.get(
    "/login",
    response_class=HTMLResponse
)
async def login(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


# ==========================================================
# REGISTER
# ==========================================================

@app.get(
    "/register",
    response_class=HTMLResponse
)
async def register(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="register.html"
    )


# ==========================================================
# DASHBOARD
# ==========================================================

@app.get(
    "/dashboard",
    response_class=HTMLResponse
)
async def dashboard(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html"
    )


# ==========================================================
# CALENDAR
# ==========================================================

@app.get(
    "/calendar",
    response_class=HTMLResponse
)
async def calendar(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="calendar.html"
    )


# ==========================================================
# HEALTH
# ==========================================================

@app.get(
    "/health",
    response_class=HTMLResponse
)
async def health(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="health.html"
    )


# ==========================================================
# HISTORY
# ==========================================================

@app.get(
    "/history",
    response_class=HTMLResponse
)
async def history(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="history.html"
    )


# ==========================================================
# SETTINGS
# ==========================================================

@app.get(
    "/settings",
    response_class=HTMLResponse
)
async def settings(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="settings.html"
    )

# ==========================================================
# ONBOARDING
# ==========================================================

@app.get(
    "/onboarding",
    response_class=HTMLResponse
)
async def onboarding(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="onboarding.html"
    )
# ==========================================================
# AI SETUP
# ==========================================================

@app.get("/Aisetup")
async def ai_setup():
    return RedirectResponse(
        url="/onboarding",
        status_code=303
    )



# AI COMPANION
# ==========================================================

@app.get(
    "/ai-companion",
    response_class=HTMLResponse
)
async def ai_companion(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html"
    )


# ==========================================================
# API HEALTH CHECK
# ==========================================================

@app.get(
    "/api/health"
)
async def api_health():

    return {
        "success": True,
        "message": "SYNC API is running",
        "ai_configured": bool(GROQ_API_KEY)
    }


# ==========================================================
# AI CHAT REQUEST MODELS
# ==========================================================

class ChatHistoryItem(BaseModel):

    sender: str
    message: str


class ChatRequest(BaseModel):

    message: str = Field(
        min_length=1,
        max_length=3000
    )

    companion_name: str = Field(
        default="Bloom",
        max_length=30
    )

    history: list[ChatHistoryItem] = Field(
        default_factory=list
    )


# ==========================================================
# AI COMPANION SYSTEM INSTRUCTIONS
# ==========================================================

SYNC_AI_PROMPT = """
You are the wellness companion inside an application called SYNC.

SYNC is a menstrual-cycle and women's wellness application.

Your purpose is to provide supportive, clear, non-judgmental,
evidence-informed general health information.

The user may ask questions that feel private, embarrassing,
sensitive, sexual, reproductive, or uncomfortable.

Treat these questions normally and respectfully.

You may discuss topics including:

- menstrual cycles
- late or missed periods
- irregular periods
- period cramps
- PMS
- menstrual flow
- spotting
- ovulation
- fertility basics
- pregnancy possibility
- pregnancy symptoms
- pregnancy testing
- PCOS
- PCOD
- hormonal symptoms
- vaginal discharge
- vaginal odor
- vaginal itching
- vaginal irritation
- vaginal dryness
- vulvar health
- sexual health
- contraception
- bleeding after sex
- breast tenderness
- acne
- bloating
- headaches
- nausea
- fatigue
- dizziness
- constipation
- diarrhea
- sleep
- mood changes
- stress
- general reproductive wellness


STYLE:

Be warm, calm, straightforward and respectful.

Never shame the user.

Do not act shocked by sexual or intimate questions.

Do not use childish language.

Avoid unnecessarily long answers.

Answer the user's actual question first.

When useful, ask ONE relevant follow-up question.

Do not interrogate the user with many questions at once.

Use simple language unless the user asks for technical detail.

You are a wellness companion, not a doctor.


MEDICAL SAFETY:

Never claim to diagnose the user.

Do not say:
"You have PCOS"
"You have an infection"
"You are pregnant"
"You are not pregnant"

Instead explain possible causes and appropriate next steps.

Do not claim that symptoms alone can confirm pregnancy.

For pregnancy questions, explain that pregnancy tests and
medical evaluation are more reliable than symptoms alone.

Do not claim PCOS or PCOD can be diagnosed from symptoms alone.

Explain that diagnosis normally requires assessment by a
qualified healthcare professional.

Do not recommend prescription medication or tell users to
start, stop or change prescription medication.

Do not provide unsafe home remedies.

Do not recommend inserting household products, chemicals,
herbs, oils, soaps or other substances into the vagina.

For vaginal health, explain that the vagina generally
cleans itself and unnecessary internal cleansing or
douching can cause irritation.

When discussing intimate health, distinguish the vagina
from the vulva when relevant.


URGENT SYMPTOMS:

If the user describes symptoms that may require urgent
medical attention, clearly tell them to seek urgent
medical care.

Examples include:

- fainting
- severe difficulty breathing
- severe or rapidly worsening pelvic or abdominal pain
- severe one-sided pelvic pain
- very heavy bleeding
- pregnancy possibility combined with severe one-sided
  abdominal/pelvic pain, fainting, shoulder pain or
  significant bleeding
- severe allergic reaction
- confusion
- severe weakness
- other obviously dangerous symptoms

Do not bury urgent guidance underneath a long explanation.


LATE OR MISSED PERIODS:

Explain that late periods can have many causes including
pregnancy, stress, illness, travel, sleep changes,
weight changes, exercise changes and hormonal conditions.

If pregnancy is possible, explain when pregnancy testing
may be useful.

Do not assume pregnancy.


PCOS / PCOD:

Explain common symptoms when asked.

Make clear that symptoms overlap with many other
conditions and cannot confirm PCOS.

Encourage professional assessment when symptoms are
persistent or concerning.


VAGINAL DISCHARGE:

Explain that discharge can normally change throughout
the menstrual cycle.

When relevant, mention concerning features such as:

- strong or unusual odor
- significant itching
- burning
- pelvic pain
- sores
- unusual bleeding
- fever

Do not automatically label discharge as an infection.


PRIVACY:

Do not ask for the user's full name, exact address,
phone number or other unnecessary identifying information.

Only ask health-related follow-up questions when they
actually help answer the user's question.


NEARBY GYNECOLOGISTS:

SYNC has a separate Nearby Gynecologist feature.

If the user wants to find a gynecologist near them,
tell them to use the Nearby Gynecologist option in
the companion.

Do not invent doctor names or locations.


RESPONSE FORMAT:

Prefer short paragraphs and small bullet lists.

Usually keep the response below about 250 words.

For simple questions, be much shorter.

Do not repeatedly add generic disclaimers to every answer.

Give safety guidance when it is actually relevant.
"""


# ==========================================================
# AI CHAT API
# ==========================================================

@app.post(
    "/api/chat"
)
async def ai_chat(
    chat_request: ChatRequest
):

    # ======================================================
    # CHECK API KEY
    # ======================================================

    if not GROQ_API_KEY or groq_client is None:

        raise HTTPException(
            status_code=503,
            detail=(
                "AI Companion is not configured. "
                "Add GROQ_API_KEY to your .env file "
                "and restart the server."
            )
        )


    user_message = (
        chat_request.message.strip()
    )


    if not user_message:

        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )


    # ======================================================
    # BUILD CONVERSATION
    # ======================================================

    messages = [
        {
            "role": "system",
            "content": SYNC_AI_PROMPT
        }
    ]


    # ------------------------------------------------------
    # Companion identity
    # ------------------------------------------------------

    companion_name = (
        chat_request.companion_name.strip()
        or
        "Bloom"
    )


    messages.append(
        {
            "role": "system",
            "content": (
                f"The user has named you "
                f"'{companion_name}'. "
                f"When referring to yourself, you may use "
                f"the name {companion_name}."
            )
        }
    )


    # ======================================================
    # ADD RECENT CHAT HISTORY
    # ======================================================

    # Only send the most recent messages.
    # This keeps requests smaller and avoids sending
    # unnecessary old conversation data.

    recent_history = (
        chat_request.history[-12:]
    )


    for item in recent_history:

        sender = (
            item.sender
            .strip()
            .lower()
        )


        content = (
            item.message
            .strip()
        )


        if not content:

            continue


        if sender == "user":

            messages.append(
                {
                    "role": "user",
                    "content": content
                }
            )


        elif sender in (
            "bot",
            "assistant"
        ):

            messages.append(
                {
                    "role": "assistant",
                    "content": content
                }
            )


    # ======================================================
    # ADD CURRENT MESSAGE
    # ======================================================

    messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )


    # ======================================================
    # ASK GROQ
    # ======================================================

    try:

        completion = (
            groq_client
            .chat
            .completions
            .create(
                model="llama-3.1-8b-instant",

                messages=messages,

                temperature=0.4,

                max_tokens=600
            )
        )


        reply = (
            completion
            .choices[0]
            .message
            .content
        )


        if not reply:

            raise ValueError(
                "Groq returned an empty response."
            )


        return {
            "success": True,
            "reply": reply.strip(),
            "companion_name": companion_name
        }


    # ======================================================
    # GROQ / GENERAL ERROR
    # ======================================================

    except Exception as error:

        print(
            "AI Companion error:",
            repr(error)
        )


        raise HTTPException(
            status_code=503,
            detail=(
                "The AI Companion is temporarily "
                "unavailable. Please try again."
            )
        )


# ==========================================================
# NEARBY GYNECOLOGISTS API
# ==========================================================

@app.get(
    "/api/nearby-gynecologists"
)
async def nearby_gynecologists(

    lat: float = Query(
        ...,
        ge=-90,
        le=90,
        description="User latitude"
    ),

    lon: float = Query(
        ...,
        ge=-180,
        le=180,
        description="User longitude"
    )

):

    """
    Find gynecology-related healthcare locations
    within a 10 km radius of the user.

    Data source:
    OpenStreetMap through Overpass API.
    """


    # ======================================================
    # SEARCH SETTINGS
    # ======================================================

    radius = 10000


    # Multiple public endpoints give us a fallback if
    # one Overpass server is temporarily unavailable.

    overpass_urls = [

        "https://overpass-api.de/api/interpreter",

        "https://overpass.kumi.systems/api/interpreter"

    ]


    # ======================================================
    # OVERPASS QUERY
    # ======================================================

    overpass_query = f"""
[out:json][timeout:25];

(
    node
    ["healthcare"="doctor"]
    ["healthcare:speciality"~"gynaecology|gynecology",i]
    (around:{radius},{lat},{lon});

    way
    ["healthcare"="doctor"]
    ["healthcare:speciality"~"gynaecology|gynecology",i]
    (around:{radius},{lat},{lon});

    relation
    ["healthcare"="doctor"]
    ["healthcare:speciality"~"gynaecology|gynecology",i]
    (around:{radius},{lat},{lon});


    node
    ["healthcare:speciality"~"gynaecology|gynecology",i]
    (around:{radius},{lat},{lon});

    way
    ["healthcare:speciality"~"gynaecology|gynecology",i]
    (around:{radius},{lat},{lon});

    relation
    ["healthcare:speciality"~"gynaecology|gynecology",i]
    (around:{radius},{lat},{lon});


    node
    ["amenity"="doctors"]
    ["healthcare:speciality"~"gynaecology|gynecology",i]
    (around:{radius},{lat},{lon});

    way
    ["amenity"="doctors"]
    ["healthcare:speciality"~"gynaecology|gynecology",i]
    (around:{radius},{lat},{lon});

    relation
    ["amenity"="doctors"]
    ["healthcare:speciality"~"gynaecology|gynecology",i]
    (around:{radius},{lat},{lon});
);

out center tags;
"""


    # ======================================================
    # REQUEST OPENSTREETMAP / OVERPASS
    # ======================================================

    data = None

    last_error = None


    for overpass_url in overpass_urls:

        try:

            async with httpx.AsyncClient(
                timeout=30.0,
                headers={
                    "User-Agent":
                        "SYNC-Wellness-App/1.0",

                    "Accept":
                        "application/json"
                }
            ) as client:


                # IMPORTANT:
                # Overpass expects the query in a
                # form field named "data".

                response = await client.post(
                    overpass_url,
                    data={
                        "data":
                            overpass_query
                    }
                )


                print(
                    "Overpass endpoint:",
                    overpass_url
                )


                print(
                    "Overpass response status:",
                    response.status_code
                )


                response.raise_for_status()


                data = response.json()


                # Success — stop trying endpoints

                break


        # ==================================================
        # TIMEOUT
        # ==================================================

        except httpx.TimeoutException as error:

            last_error = error

            print(
                "Overpass timeout:",
                overpass_url,
                error
            )


        # ==================================================
        # HTTP STATUS ERROR
        # ==================================================

        except httpx.HTTPStatusError as error:

            last_error = error

            print(
                "Overpass status error:",
                overpass_url,
                error
            )


        # ==================================================
        # CONNECTION ERROR
        # ==================================================

        except httpx.RequestError as error:

            last_error = error

            print(
                "Overpass connection error:",
                overpass_url,
                error
            )


        # ==================================================
        # OTHER ERROR
        # ==================================================

        except Exception as error:

            last_error = error

            print(
                "Nearby gynecologist error:",
                overpass_url,
                repr(error)
            )


    # ======================================================
    # ALL OVERPASS SERVERS FAILED
    # ======================================================

    if data is None:

        print(
            "All Overpass endpoints failed:",
            repr(last_error)
        )


        raise HTTPException(
            status_code=503,
            detail=(
                "The nearby healthcare search "
                "service is temporarily unavailable. "
                "Please try again."
            )
        )


    # ======================================================
    # PROCESS RESULTS
    # ======================================================

    doctors = []


    for place in data.get(
        "elements",
        []
    ):

        tags = place.get(
            "tags",
            {}
        )


        # ==================================================
        # GET COORDINATES
        # ==================================================

        place_lat = place.get(
            "lat"
        )

        place_lon = place.get(
            "lon"
        )


        # Ways and relations usually use center coordinates

        if (
            place_lat is None
            or
            place_lon is None
        ):

            center = place.get(
                "center",
                {}
            )

            place_lat = center.get(
                "lat"
            )

            place_lon = center.get(
                "lon"
            )


        # Skip places without usable coordinates

        if (
            place_lat is None
            or
            place_lon is None
        ):

            continue


        try:

            place_lat = float(
                place_lat
            )

            place_lon = float(
                place_lon
            )

        except (
            TypeError,
            ValueError
        ):

            continue


        # ==================================================
        # NAME
        # ==================================================

        name = (
            tags.get("name")
            or
            "Gynecology Clinic"
        )


        # ==================================================
        # ADDRESS
        # ==================================================

        address_parts = [

            tags.get(
                "addr:housenumber"
            ),

            tags.get(
                "addr:street"
            ),

            tags.get(
                "addr:suburb"
            ),

            tags.get(
                "addr:city"
            ),

            tags.get(
                "addr:postcode"
            )

        ]


        address = ", ".join(

            str(part)

            for part in address_parts

            if part

        )


        if not address:

            address = (
                tags.get("addr:full")
                or
                "Address not available"
            )


        # ==================================================
        # PHONE
        # ==================================================

        phone = (

            tags.get("phone")

            or

            tags.get(
                "contact:phone"
            )

        )


        # ==================================================
        # WEBSITE
        # ==================================================

        website = (

            tags.get("website")

            or

            tags.get(
                "contact:website"
            )

        )


        # ==================================================
        # SPECIALITY
        # ==================================================

        speciality = (

            tags.get(
                "healthcare:speciality"
            )

            or

            "Gynecology"
        )


        # ==================================================
        # CREATE RESULT
        # ==================================================

        doctor = {

            "name":
                name,

            "address":
                address,

            "latitude":
                place_lat,

            "longitude":
                place_lon,

            "phone":
                phone,

            "website":
                website,

            "speciality":
                speciality

        }


        doctors.append(
            doctor
        )


    # ======================================================
    # REMOVE DUPLICATES
    # ======================================================

    unique_doctors = []

    seen = set()


    for doctor in doctors:

        key = (

            doctor[
                "name"
            ]
            .strip()
            .lower(),

            round(
                doctor["latitude"],
                5
            ),

            round(
                doctor["longitude"],
                5
            )

        )


        if key in seen:

            continue


        seen.add(
            key
        )


        unique_doctors.append(
            doctor
        )


    # ======================================================
    # FINAL RESPONSE
    # ======================================================

    return {

        "success":
            True,

        "radius_km":
            10,

        "user_location": {

            "latitude":
                lat,

            "longitude":
                lon

        },

        "count":
            len(
                unique_doctors
            ),

        "doctors":
            unique_doctors

    }