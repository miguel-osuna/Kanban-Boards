# Kanban-Boards

Kanban-Boards

# Commands

- docker-compose down -v
- docker-compose build --no-cache
- docker-compose up
- docker-compose exec app flask black
- docker-compose exec app flask flake8
- docker-compose exec app flask test
- docker-compose exec app flask cov
- docker-compose exec app flask dbsetup reset --with-testdb
- docker-compose exec app flask db init (if no migrations folder is available)
- docker-compose exec --user "$(id -u):$(id -g)" app flask db migrate
- docker-compose exec app flask db upgrade
- docker-compose exec app flask add all
- docker-compose exec --user "$(id -u):$(id -g)" app flask babel extract
- docker-compose exec --user "$(id -u):$(id -g)" app flask babel init --language <lang_code> (create a language folder)
- docker-compose exec --user "$(id -u):$(id -g)" app flask babel update (update the language folders)
- docker-compose exec --user "$(id -u):$(id -g)" app flask babel compile (compile the translations)
