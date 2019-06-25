Kong 502 Logging Error
===

There seems to be a bug in kong logging that logs every 502 response as a GET request,
even if another method is used (eg. POST).

We have observed this issue with kong 1.1.1 up to 1.2.0 (latest, right now),
with both the tcp- and udp-log plugins, with and without database.

Getting started
---

You need both docker and docker-compose for this. Three shells will be needed for this demo.

In shell #1
```
$ dc build
$ dc up
```

In shell #2
```
$ curl -v -XPOST localhost:8000/nothing
An invalid response was received from the upstream server
```

If all went well, you'll get the following log in shell #1.

```
Starting kong502_udp-log_1       ... done
Starting kong502_buggy-service_1 ... done
Starting kong502_kong_1          ... done
Attaching to kong502_udp-log_1, kong502_buggy-service_1, kong502_kong_1
buggy-service_1  | Starting buggy service
udp-log_1        | Ready to receive UDP packets
buggy-service_1  | Everything started.
buggy-service_1  | Nothing
buggy-service_1  | POST / HTTP/1.1
buggy-service_1  | Host: buggy-service:8000
buggy-service_1  | Connection: keep-alive
buggy-service_1  | X-Forwarded-For: 172.19.0.1
buggy-service_1  | X-Forwarded-Proto: http
buggy-service_1  | X-Forwarded-Host: localhost
buggy-service_1  | X-Forwarded-Port: 8000
buggy-service_1  | X-Real-IP: 172.19.0.1
buggy-service_1  | User-Agent: curl/7.54.0
buggy-service_1  | Accept: */*
buggy-service_1  |
buggy-service_1  |
udp-log_1        | {"latencies":{"request":10,"kong":10,"proxy":0},"service":{"host":"buggy-service","created_at":1561468025,"connect_timeout":60000,"id":"18150dd9-9bf9-4dca-8900-07d895abc912","protocol":"http","name":"buggy-service","read_timeout":60000,"port":8000,"path":"\/","updated_at":1561468025,"retries":5,"write_timeout":60000},"request":{"querystring":{},"size":"86","uri":"\/nothing","url":"http:\/\/localhost:8000\/nothing","headers":{"host":"localhost:8000","accept":"*\/*","user-agent":"curl\/7.54.0"},"method":"GET"},"client_ip":"172.19.0.1","tries":[{"balancer_latency":0,"port":8000,"balancer_start":1561468027953,"ip":"172.19.0.2"}],"upstream_uri":"\/","response":{"headers":{"content-type":"text\/plain; charset=UTF-8","via":"kong\/1.1.1","server":"kong\/1.1.1","connection":"close","x-kong-proxy-latency":"10","x-kong-upstream-latency":"0","transfer-encoding":"chunked"},"status":502,"size":"318"},"route":{"created_at":1561468025,"id":"c4e5a80d-d498-47f6-9807-d48d87ccf4d6","service":{"id":"18150dd9-9bf9-4dca-8900-07d895abc912"},"name":"no-answer","preserve_host":false,"regex_priority":0,"paths":["\/nothing"],"updated_at":1561468025,"protocols":["http","https"],"strip_path":true},"started_at":1561468027943}
```

For your convenience, here's the formatted json. Notice the `"method": "GET"`, where it should really be `POST`.

```json
{
    "latencies": {
        "request": 10,
        "kong": 10,
        "proxy": 0
    },
    "service": {
        "host": "buggy-service",
        "created_at": 1561468025,
        "connect_timeout": 60000,
        "id": "18150dd9-9bf9-4dca-8900-07d895abc912",
        "protocol": "http",
        "name": "buggy-service",
        "read_timeout": 60000,
        "port": 8000,
        "path": "\/",
        "updated_at": 1561468025,
        "retries": 5,
        "write_timeout": 60000
    },
    "request": {
        "querystring": {},
        "size": "86",
        "uri": "\/nothing",
        "url": "http:\/\/localhost:8000\/nothing",
        "headers": {
            "host": "localhost:8000",
            "accept": "*\/*",
            "user-agent": "curl\/7.54.0"
        },
        "method": "GET"
    },
    "client_ip": "172.19.0.1",
    "tries": [
        {
            "balancer_latency": 0,
            "port": 8000,
            "balancer_start": 1561468027953,
            "ip": "172.19.0.2"
        }
    ],
    "upstream_uri": "\/",
    "response": {
        "headers": {
            "content-type": "text\/plain; charset=UTF-8",
            "via": "kong\/1.1.1",
            "server": "kong\/1.1.1",
            "connection": "close",
            "x-kong-proxy-latency": "10",
            "x-kong-upstream-latency": "0",
            "transfer-encoding": "chunked"
        },
        "status": 502,
        "size": "318"
    },
    "route": {
        "created_at": 1561468025,
        "id": "c4e5a80d-d498-47f6-9807-d48d87ccf4d6",
        "service": {
            "id": "18150dd9-9bf9-4dca-8900-07d895abc912"
        },
        "name": "no-answer",
        "preserve_host": false,
        "regex_priority": 0,
        "paths": [
            "\/nothing"
        ],
        "updated_at": 1561468025,
        "protocols": [
            "http",
            "https"
        ],
        "strip_path": true
    },
    "started_at": 1561468027943
}
```

Capturing with tcpdump
---

Optionally, you can capture the traffic to and from the kong container with tcpdump.
Provided your clone directory is named `kong502`, the following should work:

```
$ docker build tcpdump -t tcpdump:latest
$ docker run -it --net=container:kong502_kong_1 tcpdump
```