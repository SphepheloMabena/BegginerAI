# BeginnerAI

### How to setup the project:

1. Clone the repo.
2. Install **python**.
3. Install **docker**
4. In the root directory, run `source /venv/bin/activate`
5. Then run `pip3 install -r requirements.txt`
6. Create a `.env` file in the **beginneraichat** directory and get the keys from the WhatsApp Group

### Docker stuff

- To build a docker image, run `docker build -t beginner-ai .`
- To run the docker image, run `docker run -p 8000:8000 beginner-ai`
- To stop all running docker containers, run `docker stop $(docker ps -aq)`


### How to ssh into the Alibaba VM instance
Run the following command: `ssh root@47.88.4.32`
  
Then you're all sorted :):+1:
