docker stop cohorte_demo 2>/dev/null;
docker rm cohorte_demo 2>/dev/null;
docker pull cohorte/demo:latest;
docker run -d --name cohorte_demo --privileged --cap-add SYS_ADMIN --restart always -v "/sys/fs/cgroup:/sys/fs/cgroup" -p 18090:8090 -p 18091:8091 -p 18092:8092 -p 18093:8093 -p 19000:9000 cohorte/demo:latest