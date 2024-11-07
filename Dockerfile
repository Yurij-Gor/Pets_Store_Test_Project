# Dockerfile
FROM ubuntu:latest

# Install Python, pip, wget, and python3-venv
RUN apt-get update && \
    apt-get install -y python3 python3-pip wget python3-venv && \
    apt-get clean

# Install Java for Allure CLI
RUN apt-get install -y openjdk-11-jdk && \
    apt-get clean;

# Set environment variables for Java
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Set the working directory
WORKDIR /tests_project/

# Copy requirements and install them in a virtual environment
COPY requirements.txt .
RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install --upgrade pip
RUN /opt/venv/bin/pip install -r requirements.txt

# Install Allure CLI for generating test reports
RUN wget https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.13.8/allure-commandline-2.13.8.tgz -O allure-commandline.tgz && \
    tar -zxvf allure-commandline.tgz -C /opt/ && \
    ln -s /opt/allure-2.13.8/bin/allure /usr/bin/allure && \
    rm -f allure-commandline.tgz

# Default command to run tests and generate Allure reports
CMD ["/opt/venv/bin/python", "-m", "pytest", "-s", "--alluredir=test_results/", "/tests_project/tests/"]
