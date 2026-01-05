from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from poster import create_poster, fetch_image_from_url   # <- yahi rahe
from PIL import Image
from io import BytesIO
import uvicorn


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in prod
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
    """
    Accepts form-data (multipart).
    - either provide logoURL (public url) OR upload logoFile.
    - returns generated PNG image bytes directly.
    """
    # Validate inputs (basic)
    if not salonName:
        raise HTTPException(status_code=400, detail="salonName required")

    logo_img = None
    # if file uploaded
    if logoFile:
        try:
            contents = await logoFile.read()
            logo_img = Image.open(BytesIO(contents)).convert("RGBA")
        except Exception as e:
            raise HTTPException(status_code=400, detail="invalid uploaded logo")
    elif logoURL:
        # fetch remote
        logo_img = fetch_image_from_url(logoURL)
        if logo_img is None:
            raise HTTPException(status_code=400, detail="unable to fetch logo from url")

    # create poster
    png_bytes = create_poster(
        salon_name=salonName,
        logo_image=logo_img,
        contact=contact,
        website=website,
        offer=offer or "50% off on any service",
        address=address,
    )

    return StreamingResponse(BytesIO(png_bytes), media_type="image/png")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
