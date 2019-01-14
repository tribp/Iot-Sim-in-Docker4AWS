# Iot-Sim-in-Docker4AWS

## Goal
Is to make a software Iot simulation device in Docker for AWS.
The device will send Iot messages to AWS-Iot hub for test purposes.

## Steps we will take:

1. Install Docker
2. Run Alpine container
3. Pimp this container
4. Create 'thing' in AWS
5. Prepare container with AWS-SDK + AWS certificates
6. Run (software) Iot device
7. Verify messages in AWS
8. Optional: prepare Pipeline + database
8. Visualize

## 1 Install Docker
### 1.1 Install Docker CE (Community Edition) on MAC / PC

https://docs.docker.com/install/overview/

### 1.2 Verify Docker
```
docker --version
Docker version 18.03.0-ce, build 0520e24
```
PS: see other Repo for additional Docker commands or info

## 2 Run Alpine container
Why 'Alpine' ?
Lets give it a try :-)

Alpine is the 'leanest' linux distribution, stripped from EVERYTHING, but the essential.
Pro -> this will give us a very small distribution (5MB) for the local PC, with an extra bonus of a minimal security attack surface and finally a better understanding of what components we need.

```
docker pull alpine                                          -> pulls latest image of alpine
docker container run -it --name mySmallLinux alpine sh      -> start container + shell
```
## 3 Pimp this container
We even need some basic stuff, remember the 5MB footprint, + ...

Essential thing we need:
- nano as text editor
- bash to execute our script
- git to get the repositories
- python

For this we will use 'apk' the Alpine package manager
see: https://wiki.alpinelinux.org/wiki/Alpine_Linux_package_management

### 3.1 Commands  

```
apk add nano
apk add bash
apk add git
apk add python

```
### 3.2 Saving your homework

In order not to lose our homework an to keep all the changes to this container we need to tell docker to do so.  
First we need to get the ID of the container and then execute a commit on this container.

Get the id of the container:
```
docker ps
```

Commit (save) the container
PS: additional info about version info etc :
https://docs.docker.com/engine/reference/commandline/commit/

```
docker ec8532ba15c1 commit
```

<img src="images/Docker_commit" width="800px" >

## 1.5 Execute docker image (or test)
```

```
## 1.6 Analyze containers
```


```
