notes bazar :

    - @ :    https://qa.luos.io/
             77.199.117.170

    - Volume :  docker run -v ~/scripts:/home/luos_adm/Luos_tests/Docker/
    - commandes :
        tcpdump -i lo -s 0 -A 'tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x47455420'

        #docker container rm qapi_web_1
        docker-compose up -d --build # Build la 1ère fois
        systemctl stop nginx
        docker container stop qapi_web_1
        docker container start qapi_web_1
        systemctl start nginx
        docker container ls
        docker-compose exec web pytest .

        clear; curl -X GET '127.0.0.1:8002/ping';echo
        clear; curl -X POST -H "Content-Type: application/json" -d '{"title":"Hello", "description":"basic test"}' '127.0.0.1:8002/regression';echo;echo
