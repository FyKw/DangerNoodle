# Use an official Jenkins image as a parent image
FROM jenkins/jenkins:lts

RUN apt-get install docker -y
