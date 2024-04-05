## Docker 

### Go inside docker container
```bash
docker run -it --entrypoint /bin/sh ajinzrathod/jai-swaminarayan-flask:0.0.1.RELEASE
```

### Forcefully kill and delete a docker container
```bash
ps -ef | grep ac439
```

Example output:
root      180199      
ajinzra+  193852  181211  

```bash
sudo kill 180199
sudo kill 181211all

docker container rm ac439
```


### Run container in interactive shell
```bash
docker run -it --rm -p 5000:5000 -v $(pwd):/app <container-name> sh
```

The `--rm` flag tells Docker to remove the container once it stops running. This is useful for temporary containers that you don't need to keep around after you're done testing or developing.

If you don't use the `--rm` flag, the container will not be deleted when you exit, and you can start it again later if needed.


### Go inside container
docker exec -it <container-name> sh

The -it flag in the command docker exec -it <container-name> sh is a combination of two separate flags:

* -i or --interactive: This flag keeps the standard input (stdin) open for the container. It allows you to interact with the running container by providing input when necessary.

* -t or --tty: This flag allocates a pseudo-terminal (TTY) for the container. It provides a text-based interface that allows you to interact with the shell inside the container, making it feel like a normal terminal session.

### Running the Environment

```bash
docker-compose up --build
```
* The `--build` flag in the command docker-compose up --build tells Docker Compose to build or rebuild the images before starting the containers. 
* If you don't use `--build`, Docker Compose will not automatically rebuild the image. Instead, it will start the containers using the existing image.
