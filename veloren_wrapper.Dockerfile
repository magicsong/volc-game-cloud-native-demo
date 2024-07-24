FROM ai-test-cn-shanghai.cr.volces.com/agones-images/veloren/server-cli:weekly
RUN apt-get update && apt-get install -y curl netcat-openbsd python3 python3-pip
RUN apt-get install -y tcpdump vim
RUN pip3 install requests --break-system-packages
COPY start.sh /opt/start.sh
COPY server/health_check.py /opt/health_check.py

ENTRYPOINT [ "sh","/opt/start.sh" ]

