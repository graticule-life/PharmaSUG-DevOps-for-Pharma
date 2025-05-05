FROM quay.io/jupyter/minimal-notebook:x86_64-2025-04-30

USER root

RUN apt-get update -y && \
  apt-get install -y --no-install-recommends \
  # r lib source build requirements
  cmake \
  libcurl4-openssl-dev \
  libfontconfig1-dev \
  libfreetype6-dev \
  libfribidi-dev \
  libharfbuzz-dev \
  libjpeg-dev \
  libpng-dev \
  libtiff5-dev \
  libssl-dev \
  libxml2-dev \
  unixodbc-dev \
  zlib1g-dev \
  gnupg2 \
  jq && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

RUN \
  echo "deb [arch=amd64] https://cloud.r-project.org/bin/linux/ubuntu noble-cran40/" >> /etc/apt/sources.list && \
  wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc && \
  # published fingerprint at https://cran.r-project.org/bin/linux/ubuntu/fullREADME.html
  gpg --show-keys /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc | grep E298A3A825C0D65DFD57CBB651716619E084DAB9 && \
  echo "deb [arch=amd64] https://r2u.stat.illinois.edu/ubuntu noble main" > /etc/apt/sources.list.d/cranapt.list && \
  wget -qO- https://eddelbuettel.github.io/r2u/assets/dirk_eddelbuettel_key.asc | tee -a /etc/apt/trusted.gpg.d/cranapt_key.asc && \
  gpg --show-keys /etc/apt/trusted.gpg.d/cranapt_key.asc | grep AE89DB0EE10E60C01100A8F2A1489FE2AB99A21A

ARG R_VERSION=4.4.2-1.2404.0
RUN apt-get update -y && \
  apt-get install -y --no-install-recommends \
  r-base-core=${R_VERSION} \
  r-base-dev=${R_VERSION} && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

# Install R packages using R's package manager
RUN R -e "install.packages(c('utf8', 'IRkernel'), repos='https://cloud.r-project.org/')"

USER ${NB_USER}

WORKDIR /home/${NB_USER}
