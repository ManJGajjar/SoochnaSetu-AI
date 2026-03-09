import os
import boto3
import time
from botocore.exceptions import ClientError

def test_aws_voice_services():
    print("Testing AWS Voice Services Integration...")
    region = os.getenv("AWS_REGION", "ap-south-1")
    s3_bucket = "soochna-setu-audio-11b22"
    
    # 1. Test Polly
    print("\n1. Testing Amazon Polly (Text-to-Speech)...")
    try:
        polly = boto3.client('polly', region_name=region)
        response = polly.synthesize_speech(
            Text="Hello, this is a test of the Soochna Setu voice system.",
            OutputFormat='mp3',
            VoiceId='Kajal',
            LanguageCode='hi-IN',
            Engine='neural'
        )
        if "AudioStream" in response:
            print("✅ Polly test successful! Received audio stream.")
        else:
            print("❌ Polly test failed: No AudioStream in response.")
    except ClientError as e:
        print(f"❌ Polly test failed: {e}")
        return

    # 2. Test S3 (required for Transcribe)
    print(f"\n2. Testing Amazon S3 bucket ({s3_bucket}) access...")
    try:
        s3 = boto3.client('s3', region_name=region)
        # Just check if bucket exists and we have access
        s3.head_bucket(Bucket=s3_bucket)
        print(f"✅ S3 bucket '{s3_bucket}' is accessible.")
        
        # Upload a dummy file just to be sure
        test_key = "test_write.txt"
        s3.put_object(Bucket=s3_bucket, Key=test_key, Body=b"test")
        s3.delete_object(Bucket=s3_bucket, Key=test_key)
        print("✅ S3 write/delete successful.")

    except ClientError as e:
        print(f"❌ S3 bucket test failed: {e}")
        print("Note: Transcribe requires S3 to store temporary audio.")
        return

    # 3. Test Transcribe
    print("\n3. Testing Amazon Transcribe (Speech-to-Text) Initialization...")
    try:
        transcribe = boto3.client('transcribe', region_name=region)
        # We'll just list transcription jobs to verify permissions, launching a real
        # transcription job takes several minutes to complete.
        response = transcribe.list_transcription_jobs(MaxResults=1)
        print("✅ Transcribe permissions verified! Successfully called list_transcription_jobs.")
    except ClientError as e:
        print(f"❌ Transcribe test failed: {e}")

if __name__ == "__main__":
    test_aws_voice_services()
