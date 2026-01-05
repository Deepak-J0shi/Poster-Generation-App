from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from poster import create_poster, fetch_image_from_url
from PIL import Image
from io import BytesIO

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generate")
async def generate_poster(
    salonName: str = Form(...),
    contact: str = Form(""),
    website: str = Form(""),
    offer: str = Form(""),
    address: str = Form(""),
    logoURL: str = Form(None),
    logoFile: UploadFile = File(None),
):
    if not salonName:
        raise HTTPException(status_code=400, detail="salonName required")

    logo_img = None

    if logoFile:
        try:
            contents = await logoFile.read()
            logo_img = Image.open(BytesIO(contents)).convert("RGBA")
        except Exception:
            raise HTTPException(status_code=400, detail="invalid uploaded logo")

    elif logoURL:
        logo_img = fetch_image_from_url(logoURL)
        if logo_img is None:
            raise HTTPException(status_code=400, detail="unable to fetch logo from url")

    png_bytes = create_poster(
        salon_name=salonName,
        logo_image=logo_img,
        contact=contact,
        website=website,
        offer=offer or "50% off on any service",
        address=address,
    )

    return StreamingResponse(BytesIO(png_bytes), media_type="image/png")
