# Kanban-Boards

Kanban-Boards

# Commands

- docker-compose -f local.yml down -v
- docker-compose -f local.yml build --no-cache
- docker-compose -f local.yml up
- docker-compose -f local.yml exec application flask black
- docker-compose -f local.yml exec application flask flake8
- docker-compose -f local.yml exec application flask test
- docker-compose -f local.yml exec application flask cov
- docker-compose -f local.yml exec application flask dbsetup reset --with-testdb
- docker-compose -f local.yml exec application flask db init (if no migrations folder is available)
- docker-compose -f local.yml exec --user "$(id -u):$(id -g)" application flask db migrate
- docker-compose -f local.yml exec application flask db upgrade
- docker-compose -f local.yml exec application flask add all
- docker-compose -f local.yml exec --user "$(id -u):$(id -g)" application flask babel extract
- docker-compose -f local.yml exec --user "$(id -u):$(id -g)" application flask babel init --language <lang_code> (create a language folder)
- docker-compose -f local.yml exec --user "$(id -u):$(id -g)" application flask babel update (update the language folders)
- docker-compose -f local.yml exec --user "$(id -u):$(id -g)" application flask babel compile (compile the translations)

