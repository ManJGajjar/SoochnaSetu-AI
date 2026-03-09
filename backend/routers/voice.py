"""Voice Router - Speech-to-text and text-to-speech endpoints."""
import os
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

USE_AWS_VOICE = os.getenv("USE_AWS_VOICE", "false").lower() == "true"


class TranscribeRequest(BaseModel):
    audioData: str  # base64 encoded
    language: Optional[str] = "en-IN"


class SynthesizeRequest(BaseModel):
    text: str
    language: str = "en-IN"


@router.post("/transcribe")
def transcribe(request: TranscribeRequest):
    """Transcribe audio to text using Transcribe or Web Speech API."""
    if USE_AWS_VOICE:
        try:
            return _aws_transcribe(request.audioData, request.language)
        except Exception:
            pass

    return {
        "transcript": "",
        "detectedLanguage": request.language,
        "confidence": 0.0,
        "message": "Voice transcription handled on client side via Web Speech API",
    }


@router.post("/synthesize")
def synthesize(request: SynthesizeRequest):
    """Convert text to speech using Polly or Web Speech API."""
    if USE_AWS_VOICE:
        try:
            return _aws_synthesize(request.text, request.language)
        except Exception:
            pass

    return {
        "audioUrl": None,
        "text": request.text,
        "message": "Text-to-speech handled on client side via Web Speech Synthesis API",
    }


def _aws_transcribe(audio_data: str, language: str):
    import boto3, base64, uuid, time
    s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION", "ap-south-1"))
    transcribe = boto3.client("transcribe", region_name=os.getenv("AWS_REGION", "ap-south-1"))
    bucket = "soochna-setu-audio-11b22"

    audio_bytes = base64.b64decode(audio_data)
    key = f"transcriptions/{uuid.uuid4()}.mp3"
    s3.put_object(Bucket=bucket, Key=key, Body=audio_bytes)

    job_name = f"soochna-setu-{uuid.uuid4().hex[:8]}"
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": f"s3://{bucket}/{key}"},
        MediaFormat="mp3",
        LanguageCode=language,
    )

    for _ in range(30):
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status["TranscriptionJob"]["TranscriptionJobStatus"] in ("COMPLETED", "FAILED"):
            break
        time.sleep(1)

    if status["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
        import urllib.request, json
        uri = status["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        result = json.loads(urllib.request.urlopen(uri).read())
        transcript = result["results"]["transcripts"][0]["transcript"]
        return {"transcript": transcript, "detectedLanguage": language, "confidence": 0.9}

    return {"transcript": "", "detectedLanguage": language, "confidence": 0.0}


def _aws_synthesize(text: str, language: str):
    import boto3
    import uuid
    import time

    polly = boto3.client("polly", region_name=os.getenv("AWS_REGION", "ap-south-1"))
    s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION", "ap-south-1"))
    bucket = "soochna-setu-audio-11b22"

    voice_map = {"en-IN": "Kajal", "hi-IN": "Aditi"}
    voice = voice_map.get(language, "Aditi")

    response = polly.synthesize_speech(
        Text=text, 
        OutputFormat="mp3", 
        VoiceId=voice,
        Engine="neural"
    )
    
    if "AudioStream" in response:
        audio_stream = response["AudioStream"].read()
        
        # Save to S3
        file_name = f"tts/{int(time.time())}_{uuid.uuid4().hex[:6]}.mp3"
        s3.put_object(
            Bucket=bucket,
            Key=file_name,
            Body=audio_stream,
            ContentType="audio/mpeg"
        )
        
        audio_url = f"https://{bucket}.s3.amazonaws.com/{file_name}"
        return {"audioUrl": audio_url, "text": text, "message": "Audio generated via AWS Polly"}
        
    return {"audioUrl": None, "text": text, "message": "Failed to generate audio"}
