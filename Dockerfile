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
  jq \
  libzmq3-dev && \
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

# Set up Python and R kernels
WORKDIR /opt/conda/share/jupyter/kernels
RUN jq '.display_name = "python3"' python3/kernel.json >> python3/tmp.json && mv python3/tmp.json python3/kernel.json

# Install R packages in dependency order
RUN Rscript -e "install.packages(c('cli', 'lifecycle'), repos='https://cloud.r-project.org/')" && \
    Rscript -e "install.packages(c('vctrs', 'pillar'), repos='https://cloud.r-project.org/')" && \
    Rscript -e "install.packages(c('utf8', 'jsonlite', 'repr', 'IRdisplay', 'uuid'), repos='https://cloud.r-project.org/')" && \
    Rscript -e "install.packages('IRkernel', repos='https://cloud.r-project.org/')" && \
    Rscript -e "if (!require('IRkernel')) stop('Failed to install IRkernel')"

RUN Rscript -e "if (!require('IRkernel')) stop('IRkernel not found')" && \
    Rscript -e 'IRkernel::installspec(name="ir", displayname="R 4.4.2")'

# Set up Jupyter config directory
RUN mkdir -p /home/${NB_USER}/.local/share/jupyter && \
    mkdir -p /home/${NB_USER}/.ipython && \
    chown -R ${NB_USER}:users /home/${NB_USER}/.local && \
    chown -R ${NB_USER}:users /home/${NB_USER}/.ipython

USER ${NB_USER}

WORKDIR /home/${NB_USER}

COPY --chown=${NB_USER} ./pyproject.toml ./
COPY --chown=${NB_USER} ./source ./source