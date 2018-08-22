FROM bamos/ubuntu-opencv-dlib-torch:ubuntu_14.04-opencv_2.4.11-dlib_19.0-torch_2016.07.12
MAINTAINER Brandon Amos <brandon.amos.cs@gmail.com>

# TODO: Should be added to opencv-dlib-torch image.
RUN ln -s /root/torch/install/bin/* /usr/local/bin

RUN apt-get update && apt-get install -y \
    curl \
    git \
    graphicsmagick \
    libssl-dev \
    libffi-dev \
    python-dev \
    python-pip \
    python-numpy \
    python-nose \
    python-scipy \
    python-pandas \
    python-protobuf \
    python-openssl \
    wget \
    zip \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


WORKDIR /code
COPY . /code

# TODO: add git pull openface repository into root folder, so we dont have to do it manually

ADD ./openface /root/openface
RUN python -m pip install --upgrade --force pip
RUN pip install -r requirements.txt --ignore-installed
RUN cd ~/openface && \
    ./models/get-models.sh && \
    python2 setup.py install


EXPOSE 8000 9000

ENV PYTHONUNBUFFERED 1

CMD /bin/bash -l -c '/root/openface/demos/web/start-servers.sh'
