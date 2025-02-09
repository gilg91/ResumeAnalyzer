import boto3
import os
from dotenv import load_dotenv
from fastapi import APIRouter, File, UploadFile, HTTPException
from botocore.exceptions import NoCredentialsError

router = APIRouter()

# Load environment variables from .env file
load_dotenv()

# AWS Configuration (now using env variables)
S3_BUCKET = "resume-analyzer-bucket"
S3_REGION = os.getenv("AWS_REGION")
S3_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
S3_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Initialize S3 Client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
    region_name=S3_REGION
)

@router.post("/resume/upload/")
async def upload_resume(file: UploadFile = File(...)):
    try:
        # Upload file to S3
        s3_client.upload_fileobj(file.file, S3_BUCKET, file.filename)

        # Generate a Signed URL (valid for 1 hour)
        signed_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": S3_BUCKET, "Key": file.filename},
            ExpiresIn=3600  # Link expires in 1 hour
        )

        return {"message": "File uploaded successfully!", "signed_url": signed_url}

    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
