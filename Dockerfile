# Use an official Ubuntu as a parent image
FROM ubuntu:20.04

# Set environment variables
ENV ANDROID_HOME="/android-sdk"
ENV ANDROID_SDK_ROOT="/android-sdk"
ENV PATH="$PATH:/flutter-sdk/flutter/bin:/android-sdk/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools"
ENV DEBIAN_FRONTEND=noninteractive

# Install general dependencies
RUN apt-get update -y && apt-get upgrade -y

RUN apt-get install -y curl git unzip xz-utils zip libglu1-mesa

RUN apt-get install -y python3 python3-pip python3-venv

RUN apt-get install -y clang cmake ninja-build pkg-config libgtk-3-dev liblzma-dev libstdc++-9-dev

RUN dpkg --add-architecture i386 && apt-get update

RUN apt-get install -y libc6:i386 libncurses5:i386 libstdc++6:i386 lib32z1 libbz2-1.0:i386 openjdk-11-jdk

# Install Flutter
RUN mkdir /flutter-sdk && \
    cd /flutter-sdk && \
    curl -O https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_3.22.1-stable.tar.xz && \
    tar -xf flutter_linux_3.22.1-stable.tar.xz && \
    rm -rf flutter_linux_3.22.1-stable.tar.xz

# Configure Flutter
RUN git config --global --add safe.directory /flutter-sdk/flutter && \
    flutter doctor

# Install Flet
RUN pip3 install flet gradio

# Install Android SDK
RUN mkdir /android-sdk && \
    cd /android-sdk && \
    curl -O https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip && \
    unzip commandlinetools-linux-11076708_latest.zip -d /android-sdk && \
    rm -rf commandlinetools-linux-11076708_latest.zip && \
    yes | sdkmanager "platforms;android-34" "cmdline-tools;latest" "build-tools;34.0.0" "platform-tools" && \
    yes | sdkmanager --licenses && \
    yes | flutter doctor --android-licenses

# Run Flutter doctor to check the installation
RUN flutter doctor

# Set up the PATH environment variable
RUN echo 'export PATH="$PATH:/flutter-sdk/flutter/bin:/android-sdk/cmdline-tools/latest/bin:/android-sdk/platform-tools"' >> ~/.bashrc && \
    echo 'export ANDROID_HOME="/android-sdk"' >> ~/.bashrc && \
    echo 'export ANDROID_SDK_ROOT="/android-sdk"' >> ~/.bashrc

# Source the updated bash profile
RUN /bin/bash -c "source ~/.bashrc"

# Set the working directory
WORKDIR /workspace

COPY app.py /workspace/.

# Command to keep the container running
CMD ["python3", "/workspace/app.py"]
