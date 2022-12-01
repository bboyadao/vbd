---
Pre-requires
- Docker
- Docker compose
- Make
---
### Up.
#### Clone the code and run commands:

`make up`,
`make mi`,
`make mock`,
`make test`,


This will `up` containers, `migrate` schema, run the `test`. 

+ Navigate to [http://localhost:8000/doc](http://localhost:8000/doc) to check friendly `API` documents.
---
### Manual tests.
- I've prepared a list of user's prefix `test_user_[1-49]`. So we can use this pattern to check (eg: http://localhost:8000/mobile/test_user_5/billing/).
---
### Down.
```bash
make down
```
- To `stop` and `down` all the containers in this compose
---