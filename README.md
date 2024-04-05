How to test if API works:
```
curl http://localhost:5000/status
```

How to use an endpoint for generating code and docs:
```
curl -X POST http://localhost:5000/generate-code -H 'Content-Type: application/json' -d '{"prompt":"write a class in python"}'
```
Write your prompt in json body of POST request like in example.