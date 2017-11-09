#DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#docker run -v $DIR/collections:/etc/newman -t postman/newman_ubuntu1404:3.8.1 run CohortePlatform_Demo.postman_collection.json --disable-unicode --ignore-redirects


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


cd $DIR 

COLLECTION_FILE_NAME=$1
SERVER_HOST=$2

echo "DIR=$DIR"
echo "COLLECTION_FILE_NAME=$COLLECTION_FILE_NAME"
echo "SERVER_HOST=$SERVER_HOST"


sed  "s/{{host}}/$SERVER_HOST/g" collections/$COLLECTION_FILE_NAME > used_$COLLECTION_FILE_NAME
docker run -v $DIR:/etc/newman -t postman/newman_ubuntu1404:3.8.1 run used_$COLLECTION_FILE_NAME --disable-unicode --ignore-redirects

rm -f used_$COLLECTION_FILE_NAME

