# FROM nvidia/cuda:11.3.0-devel-ubuntu18.04



# # RUN add-apt-repository ppa:graphics-drivers/ppa

# ENV BLENDER_MAJOR 2.92
# ENV BLENDER_VERSION 2.92.0
# ENV BLENDER_TAR_URL https://download.blender.org/release/Blender${BLENDER_MAJOR}/blender-${BLENDER_VERSION}-linux64.tar.xz

# RUN apt update

# RUN apt-get install -y \
# 		curl wget nano \
# 		bzip2 libfreetype6 libgl1-mesa-dev \
# 		libglu1-mesa \
# 		libxi6 libxrender1 && \
# 	apt-get -y autoremove

# # Install blender

# RUN mkdir /usr/local/blender && \
# 	wget --quiet ${BLENDER_TAR_URL} -O blender.tar.xz && \
# 	tar -xvf blender.tar.xz -C /usr/local/blender --strip-components=1 && \
# 	rm blender.tar.xz


# # RUN apt install -y software-properties-common
# RUN add-apt-repository ppa:deadsnakes/ppa
# RUN apt install -y python3.7

# ENV APP_HOME /app
# WORKDIR $APP_HOME
# COPY . ./

# RUN pip install --upgrade pip wheel future-fstrings
# RUN pip install -r requirements.txt
# # RUN pip install bpy==2.91a0
# # VOLUME /media

# # WORKDIR $APP_HOME
# ##RUN pip install bpy
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app.main:app





# Below one is stable but does not detect GPUs at all. So defaults to CPU

FROM nytimes/blender:2.92-gpu-ubuntu18.04
RUN apt update
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3.7
# RUN apt install -y nvidia-docker2
RUN add-apt-repository ppa:graphics-drivers/ppa
RUN apt install -y nvidia-driver-465
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
RUN pip install --upgrade pip wheel future-fstrings
RUN pip install -r requirements.txt
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app.main:app


# FROM python:3.7
# WORKDIR /app
# COPY . ./
# # VOLUME /media
# RUN pip install --upgrade pip wheel future-fstrings
# RUN pip install -r requirements.txt
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app.main:app