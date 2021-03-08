```bash
brew install k6
k6 run crr.js
```

- `hammer`: dummy hammering the endpoint
- `crr`: using `constant-arrival-rate` executor to generate desired constant request rate. does 20rps
