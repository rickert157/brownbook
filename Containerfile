FROM ubuntu

RUN apt update && apt install git python3-venv -y

WORKDIR /root/brownbook

RUN git clone https://github.com/rickert157/brownbook /root/brownbook

RUN python3 -m venv venv && ./venv/bin/pip install -r requirements.txt

CMD ["./venv/bin/python", "-m", "modules.crowler"]
