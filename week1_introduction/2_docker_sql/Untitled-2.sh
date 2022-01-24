docker run -it \
    -e POSTGRES_USER=root \
    -e POSTGRES_PASSWORD=root \
    -e POSTGRES_DB=ny_taxi \
    -v /home/wtsang/projects/dataeng-zc/week1_introduction/2_docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/ny_taxi_postgres_data \
    -p 5432:5432 \
    postgres:13