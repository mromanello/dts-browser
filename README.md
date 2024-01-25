# DTS demo browser

The [original code](https://github.com/chartes/dts-demo/) for this application was developed by [Julien Pilla](https://github.com/mrgecko) (École Nationale des Chartes), and further adapted by [Matteo Romanello](https://github.com/mromanello) (UniL) to work as a generic DTS browser.

## Run the browser on a container (Docker/Podman)

Navigate to the dts-broser root folder, then run :

```bash
docker build -t dts-browser-image .
```

start container with :

```bash
docker run --rm --name dts-browser -itd -p 5051:5051 -e "AGGREGATOR_URL=http://my-aggregator.com:8443" dts-browser-image
```

Parameter -e AGGREGATOR_URL should contain the url of your aggregator.