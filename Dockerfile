ARG FUNCTION_DIR="/function"

FROM python:3.12-slim

# Include global arg in this stage of the build
ARG FUNCTION_DIR

# Copy function code
RUN mkdir -p ${FUNCTION_DIR}
COPY ./testlambda.py ${FUNCTION_DIR}

# Install the function's dependencies
RUN pip install \
        awslambdaric

# Set runtime interface client as default command for the container runtime
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
# Pass the name of the function handler as an argument to the runtime
CMD [ "/function/testlambda.handler" ]