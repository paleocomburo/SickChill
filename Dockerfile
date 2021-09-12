FROM python:3.7-slim

LABEL org.opencontainers.image.source="https://github.com/sickchill/sickchill"
LABEL maintainer="miigotu@gmail.com"
ENV PYTHONIOENCODING="UTF-8"

# docker run -dit --user 1000:1000 --name sickchill --restart=always \
# -v ShowPath:/ShowPath \
# -v DownloadPath:/DownloadPath \
# -v /docker/sickchill/data:/data \
# -v /docker/sickchill/cache/gui:/app/sickchill/sickchill/gui/slick/cache \
# -v /etc/localtime:/etc/localtime:ro
# -p 8080:8081 sickchill/sickchill

VOLUME /data /downloads /tv
RUN mkdir /app /var/run/sickchill
WORKDIR /app/sickchill
COPY pyproject.toml /app/sickchill
COPY poetry.lock /app/sickchill

RUN sed -i -e's/ main/ main contrib non-free/gm' /etc/apt/sources.list
RUN apt-get update -qq && apt-get install -yq git libxml2 libxml2-dev libxslt1.1 \
libxslt1-dev libffi-dev libssl1.1 libssl-dev python3-dev \
libmediainfo0v5 libmediainfo-dev mediainfo unrar-free curl build-essential && \
apt-get clean -yqq && rm -rf /var/lib/apt/lists/*

# unrar non-free is not available for ARM HF, use the free version.
RUN curl -OLsS http://http.us.debian.org/debian/pool/main/libf/libffi/libffi6_3.2.1-9_armhf.deb && \
dpkg -i libffi6_3.2.1-9_armhf.deb && \
rm -f libffi6_3.2.1-9_armhf.deb

# Break layer cache, always install poetry and depends.
ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
export PATH="$HOME/.cargo/bin:/root/.local/bin:$PATH" && \
ln -s /usr/bin/python3 /usr/bin/python

RUN pip install --pre --upgrade --prefer-binary \
poetry pip wheel setuptools virtualenv setuptools_rust

RUN poetry export --format requirements.txt > requirements.txt && \
python -m virtualenv -p python3.7 .venv && \
.venv/bin/python3 -m pip install --pre --upgrade --prefer-binary \
-r requirements.txt && rm requirements.txt

COPY . /app/sickchill
RUN chmod -R 777 /app/sickchill

CMD .venv/bin/python3 SickChill.py -q --nolaunch --datadir=/data --port 8081

EXPOSE 8081

HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost:8081/ || curl -f https://localhost:8081/ || exit 1
