from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import qrcode
import boto3
import os
from io import BytesIO
from dotenv import load_dotenv
import re

# Load environment variables (AWS Access Key and Secret Key)
load_dotenv()

app = FastAPI()

# Allowing CORS for local testing
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AWS S3 Configuration
# s3 = boto3.client(
#     's3',
#     aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
#     aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
    # Optionally add region_name='your-region' if not using default region
# )

# for three tier arch

s3 = boto3.client('s3')


bucket_name = os.getenv("S3_BUCKET_NAME")  # Change to your bucket name

def sanitize_filename(url: str) -> str:
    """Sanitize URL to create a safe S3 filename."""
    # Remove protocol and replace non-alphanumeric chars with '_'
    filename = re.sub(r'\W+', '_', url)
    return f"qr_codes/{filename}.png"

@app.post("/generate-qr/")
async def generate_qr(url: str = Query(...)):
    # Generate QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR Code to BytesIO object
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    # Generate sanitized file name for S3
    file_name = sanitize_filename(url)

    try:
        # Upload to S3 (FIXED)
        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=img_byte_arr.getvalue(),  # Convert BytesIO to bytes
            ContentType='image/png',
            
        )
        # Generate a pre-signed URL that expires in 1 hour
        s3_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': file_name},
            ExpiresIn=3600
        )
        return {"qr_code_url": s3_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"S3 upload failed: {str(e)}")

# Optional: Health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}
