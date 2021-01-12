# Kanban-Boards

Kanban-Boards

# Commands

docker-compose -f local.yml down -v
docker-compose -f local.yml build --no-cache
docker-compose -f local.yml up
docker-compose -f local.yml exec application flask dbsetup reset --with-testdb
docker-compose -f local.yml exec application flask add all
docker-compose -f local.yml exec application flask black
docker-compose -f local.yml exec application flask flake8
docker-compose -f local.yml exec application flask test
docker-compose -f local.yml exec application flask cov
docker-compose -f local.yml exec --user "$(id -u):$(id -g)" application flask db migrate
docker-compose -f local.yml exec application flask db upgrade
