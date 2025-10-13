# service-proxy

Run:
`npm start`

Run with Docker:
`docker-compose up`

Asset call:
`GET http://localhost:3000/asset?path=<path-to-asset>`
Example:
`http://localhost:3000/asset?path=api/portraits/thumb/women/65.jpg`

API call:
`GET http://localhost:3000/api?path=<path-to-asset>`
`POST http://localhost:3000/api?path=<path-to-asset> { payload }`