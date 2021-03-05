- `pk.json` not checked in, can be e.g. baked-in service account private key
- firestore and pubsub async connectors
- jwt auth
- `swagger` and `redoc` out of the box, depend on truthy `is_staging`
- apm with sentry (middleware) and gcp error reporting (custom handler)
- default uvicorn workers, alter accordingly to underlying compute resource
- pylance language server, typeshed in the path, e.g. `sample.code-workspace` could be:
```json
{
    "folders": [
        {
            "path": "/this/repo"
        }
    ],
    "settings": {
        "python.pythonPath": "/usr/local/bin/python3.9",
        "python.analysis.extraPaths": [
            "/this/repo",
            "path/to/typeshed"
        ]
    }
}
```