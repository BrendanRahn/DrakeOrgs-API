ARG FUNCTION_DIR="/lambda"
ARG rie_DIR="/lambda_rie"

FROM python:3.12-slim

# Include global arg in this stage of the build
ARG FUNCTION_DIR
ARG rie_DIR

# Copy function code
RUN mkdir -p ${FUNCTION_DIR}
# COPY ./lambda ${FUNCTION_DIR}
COPY ./lambda_rie ${rie_DIR}

# Install the function's dependencies
COPY ./requirements.txt .


RUN pip install -r requirements.txt


ENTRYPOINT [ "/lambda_rie/aws-lambda-rie" ]

CMD [ "/usr/local/bin/python", "-m", "awslambdaric", "lambda/lambda_function.lambda_handler"]
