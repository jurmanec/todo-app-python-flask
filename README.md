# Get tasks
## Browser
```text
http://127.0.0.1:5000/tasks
```

## Terminal
```shell
curl -X GET 'http://127.0.0.1:5000/tasks'
```

# Create a task
```shell
curl -d '{"description":"first task"}' -H 'Content-Type: application/json' http://127.0.0.1:5000/tasks
```

# Update a task
```shell
curl -d  '{"description":"first task","status":"started"}' -X PUT -H 'Content-Type: application/json' 'http://127.0.0.1:5000/tasks/1'
```

# Delete a task
## Create
```shell
curl -d '{"description":"first task"}' -H 'Content-Type: application/json' http://127.0.0.1:5000/tasks
```
## Delete
```shell
curl -X DELETE -H 'Content-Type: application/json' 'http://127.0.0.1:5000/tasks/2'
```