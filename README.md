# text similarity api

simple implementation of spacy's intelligent text similarty api,
wrapped with fastapi for easy url-url comparison.

## installation

installation is as simple as installing app dependencies,
including several python packages, and spacy's large english
language model, and setting an environment variable.

in a fresh virtual env, install deps via

```shell
$ make install
```

then, point the app to your instance of the postlight mercury api:

```shell
export MERCURY_API_URL=https://...
```

## usage

after installing dependencies, run the dev server:

```shell
$ make run
```

this will start `uvicorn`, and make the api available
at `http://localhost:8000`.

this api provides a single endpoint, `compare`,
that expects two urls to mine and compare.

send a `post` request of the following shape to
`http://localhost:8000/compare`:

```json
{
  "url_a": "https://apnews.com/16cd6173232a01ec04780db3eea4de79",
  "url_b": "https://www.nytimes.com/aponline/2020/03/07/world/europe/ap-eu-virus-outbreak-pandemic.html"
}
```

behind the scenes, this hits a lambda-hosted version of postlight's
mercury content extraction app, cleans the extracted html,
and then compares the text.

if you would like to have the extracted text for each url,
use the `include_text` query string argument:

```
$ curl -X POST -d '{ ... }' http://localhost:8000/compare?include_text=1
```

if everything goes according to plan, you should see a response similar to:

```json
{
  "similarity": 0.9999228888622196
}
```

or, if you asked for the source text,

```json
{
  "similarity": 0.9999228888622196,
  "text": {
    "a": {
      "url": "https://...",
      "text": "LONDON (AP) — As cases of the coronavirus"
    },
    "b": {
      "url": "https://...",
      "text": "Continue reading the main storyLONDON — As cases of the"
    }
  }
}
```

## relevant links

- [mercury parser](https://github.com/postlight/mercury-parser), the core parser
- [mercury parser api](https://github.com/postlight/mercury-parser-api), easily deployable as an aws lambda function

## notes

- hosting the mercury api parser as a lambda function is a quick, cheap, and simple way to
  extract text content and metadata from urls.
- your first request on boot will be slow, as the spacy model needs to load. subsequent requests will be faster.
