docker run -d --name demo \
           --privileged --cap-add SYS_ADMIN --restart always \
           -v "/sys/fs/cgroup:/sys/fs/cgroup" \
           -p 8090:8090 -p 8091:8091 -p 8092:8092 -p 8093:8093 -p 9000:9000 \
           cohorte/demo:latest