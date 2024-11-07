FROM ubuntu:latest

# Install Python, pip, wget, venv, and Java (Java is required for Allure CLI)
RUN apt-get update && \
    apt-get install -y python3 python3-pip wget python3-venv openjdk-11-jdk && \
    apt-get clean;

# Set environment variables for Java
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Set the working directory within the container
WORKDIR /tests_project/

# Copy requirements.txt and install dependencies in a Python virtual environment
COPY requirements.txt .
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt

# Copy all project files into the container’s working directory
COPY . .

# Install Allure CLI for generating test reports
RUN wget https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.13.8/allure-commandline-2.13.8.tgz -O allure-commandline.tgz && \
    tar -zxvf allure-commandline.tgz -C /opt/ && \
    ln -s /opt/allure-2.13.8/bin/allure /usr/bin/allure && \
    rm -f allure-commandline.tgz

# Default command to run tests and generate Allure reports
CMD ["/opt/venv/bin/python", "-m", "pytest", "-s", "--alluredir=test_results/", "/tests_project/tests/"]
