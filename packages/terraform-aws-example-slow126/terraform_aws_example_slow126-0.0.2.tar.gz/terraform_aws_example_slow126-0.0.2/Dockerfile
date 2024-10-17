FROM python:3.9-slim-buster

WORKDIR /app

COPY ./src/terraform_aws_example_slow126/docker_test.py .

RUN apt-get update && \
    apt-get install -y curl && \
    pip install awscli && \
    apt-get -y install git && \
    apt-get -y install unzip && \
    apt-get -y install wget && \
    wget https://releases.hashicorp.com/terraform/1.9.8/terraform_1.9.8_darwin_arm64.zip && \
    unzip terraform_1.9.8_darwin_arm64.zip && \
    mv terraform /usr/local/bin/ && \
    ls -la /usr/local/bin


CMD ["python", "docker_test.py"]