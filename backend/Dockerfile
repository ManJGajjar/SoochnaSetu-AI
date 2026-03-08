FROM public.ecr.aws/lambda/python:3.11

# Copy requirements first for Docker layer caching
COPY requirements.txt ${LAMBDA_TASK_ROOT}/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . ${LAMBDA_TASK_ROOT}/

# Set Lambda handler
CMD ["lambda_handler.handler"]
