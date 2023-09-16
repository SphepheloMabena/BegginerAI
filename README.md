# BeginnerAI

How to add the project:

-> Clone the repo.
-> Install **python**.
-> Install **docker**
-> In the root directory, run `source /venv/bin/activate`
-> Then run `pip3 install -r requirements.txt`
-> Create a `.env` file in the *beginneraichat* directory and get the keys from the WhatsApp Group
-> To build a docker image, run `docker build -t beginner-ai .`
-> To run the docker image, run `docker run -p 8000:8000 beginnerai`
-> To stop all running docker containers, run `docker stop $(docker ps -aq)`
Then you're sorted.
