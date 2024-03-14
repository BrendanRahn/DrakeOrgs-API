ARG FUNCTION_DIR="/function"
ARG rie_DIR="/lambda_rie"

FROM python:3.12-slim

# Include global arg in this stage of the build
ARG FUNCTION_DIR
ARG rie_DIR

# Copy function code
RUN mkdir -p ${FUNCTION_DIR}
COPY ./lambda ${FUNCTION_DIR}
COPY ./lambda_rie ${rie_DIR}

# Install the function's dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Set runtime interface client as default command for the container runtime
ENTRYPOINT [ "/lambda_rie/aws-lambda-rie" ]
# Pass the name of the function handler as an argument to the runtime
CMD [ "/usr/local/bin/python", "-m", "awslambdaric", "function/lambda_function.lambda_handler"]
# CMD [ "function/lambda_function.lambda_handler"]