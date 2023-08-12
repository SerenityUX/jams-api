# JAMS API
A basic API for JAMS. This is a work in progress.

## Supported routes

| Route | Method | Supported? |
| --- | --- |  --- |
| `/openai/models` | GET | [x] |
| `/openai/models/:model` | GET | [x] |
| `/openai/chat/completions` | POST | [x] |
| `/openai/images/generations` | POST | [x] |
| `/openai/embeddings` | POST | [x] |

Rest of the routes are not supported yet.

## Usage
For OpenAI API, just replace the `https://api.openai.com/v1/` with `https://jamsapi.hackclub.dev/openai/` and you're good to go.
