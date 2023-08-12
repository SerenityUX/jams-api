# JAMS API
A basic API for JAMS. This is a work in progress.

## Supported routes

| Route | Method | Supported? |
| --- | --- |  --- |
| `/openai/models` | GET | :check_mark: |
| `/openai/models/:model` | GET | :check_mark: |
| `/openai/chat/completions` | POST | :check_mark: |
| `images/generations` | POST | :check_mark: |
| `/embeddings` | POST | :check_mark: |

Rest of the routes are not supported yet.

## Usage
For OpenAI API, just replace the `https://api.openai.com/v1/` with `https://jamsapi.herokuapp.com/openai/` and you're good to go.
