FROM redhat/ubi9-minimal

ENV UV_VERSION="0.10.9"
ENV PYTHON_VERSION="3.13.12"
ENV APP_PREFIX="simon_aksw_org"
ENV VIRTUAL_ENV="/app"
ENV PATH="/app/bin:$PATH"

# copy files
COPY requirements.txt /tmp/
COPY $APP_PREFIX*.tar.gz /tmp/
COPY scripts/*.sh /usr/local/bin/

# do provisioning
WORKDIR /data
RUN /usr/local/bin/provisioning.sh

# configure image
EXPOSE 5050
ENTRYPOINT ["entrypoint.sh"]

