DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "deploy on api-dev"
ssh -o StrictHostKeyChecking=no -i $1 root@api-dev.cohorte.tech $(cat $DIR/../docker/demo/start_instance.sh)

echo "deploy on api-dev-arm"
ssh -o StrictHostKeyChecking=no -i $1 root@api-dev-arm.cohorte.tech $(cat $DIR/../docker/demo-arm64v8/start_instance.sh)