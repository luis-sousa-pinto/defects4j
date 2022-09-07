FROM ubuntu:20.04

MAINTAINER Luís Pinto <luis.pinto@outlook.com>

#############################################################################
# Requirements
#############################################################################

#ENV JAVA_VER 8
#ENV JAVA_HOME /usr/lib/jvm/java-8-oracle

# Install git, wget, Oracle Java8
# RUN \
#   apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C2518248EEA14886 && \
#   apt-get update && \
#   apt-get install software-properties-common -y && \
#   apt-get install -y && \
#   wget \
#   git \
#   build-essential \
#   subversion \
#   perl \
#   curl \
#   unzip \
#   cpanminus \
#   make \
#   && \    
#   echo oracle-java${JAVA_VER}-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections && \
#   apt-get install -y --force-yes --no-install-recommends oracle-java${JAVA_VER}-installer oracle-java${JAVA_VER}-set-default && \
#   apt-get clean && \
#   rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
#   rm -rf /var/cache/oracle-jdk${JAVA_VER}-installer


RUN \
  apt-get update -y && \
  apt-get install software-properties-common -y && \
  apt-get update -y && \
  apt-get install -y openjdk-8-jdk \
  wget \
  git \
  build-essential \
  subversion \
  perl \
  curl \
  unzip \
  cpanminus \
  make \
  && \
  rm -rf /var/lib/apt/lists/*

RUN apt-get update && add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y python3.6 python3-distutils python3-pip python3-apt

# Java version
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

# Timezone
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


# Maven
RUN wget --no-verbose -O /tmp/apache-maven-3.3.9-bin.tar.gz http://www-eu.apache.org/dist/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz && \
  tar xzf /tmp/apache-maven-3.3.9-bin.tar.gz -C /opt/ && \
  ln -s /opt/apache-maven-3.3.9 /opt/maven && \
  ln -s /opt/maven/bin/mvn /usr/local/bin  && \
  rm -f /tmp/apache-maven-3.3.9-bin.tar.gz

ENV MAVEN_HOME /opt/maven

#############################################################################
# Setup Defects4J
#############################################################################

# ----------- Step 1. Clone defects4j from github --------------
WORKDIR /
RUN git clone https://github.com/Crissal1995/defects4j.git defects4j
#https://github.com/rjust/defects4j.git defects4j

# ----------- Step 2. Initialize Defects4J ---------------------
WORKDIR /defects4j
RUN cpanm --installdeps .
RUN ./init.sh

# ----------- Step 3. Add Defects4J's executables to PATH: ------
ENV PATH="/defects4j/framework/bin:${PATH}"  
#--------------
