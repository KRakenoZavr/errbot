FROM python:3.9

ENV ERR_USER err
ENV DEBIAN_FRONTEND noninteractive
ENV PATH /app/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Set default locale for the environment
ENV LC_ALL C.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Add err user and group
RUN groupadd -r $ERR_USER \
    && useradd -r \
       -g $ERR_USER \
       -d /srv \
       -s /bin/bash \
       $ERR_USER
# Install packages and perform cleanup
RUN apt-get update \
  && apt-get -y install --no-install-recommends \
         git \
         qalc \
         locales \
         dnsutils \
         libssl-dev \
         build-essential \
         python3-dnspython \
         python3-dev \
         python3-openssl \
         python3-pip \
         python3-cffi \
         python3-pyasn1 \
         python3-geoip \
         python3-lxml \
         libpq-dev \
         gcc \
    && locale-gen C.UTF-8 \
    && /usr/sbin/update-locale LANG=C.UTF-8 \
    && echo 'en_US.UTF-8 UTF-8' >> /etc/locale.gen \
    && locale-gen \
    && pip3 install virtualenv \
    && pip3 install -U setuptools \
	&& rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apt/archives

RUN mkdir /app /srv/data /srv/plugins /srv/errbackends /srv/errstorages

COPY requirements.txt /app/requirements.txt

RUN virtualenv /app/venv
RUN . /app/venv/bin/activate; pip install --no-cache-dir -r /app/requirements.txt

COPY config.py /app/config.py
COPY run.sh /app/venv/bin/run.sh
COPY ./plugins /srv/plugins
COPY ./errbackends /srv/errbackends
COPY ./errstorages /srv/errstorages

RUN chown -R $ERR_USER. /srv /app && chmod +x /app/venv/bin/run.sh


EXPOSE 3141 3142
VOLUME ["/srv"]

ENTRYPOINT ["/app/venv/bin/run.sh"]
