# rainbow

### some release

+ python: 3.8.5
+ django: 3.1.4
+ ubuntu: ubuntu:20.04
+ nginx: 1.19
+ postgres: 13
+ redis: 6.0
+ rabbitmq: 3.8.9


### requirment

+ docker
+ docker-compose

### unit test in local requirment

**for mac**
```shell script
brew install postgresql
createuser -d -a -P rainbow
createdb -O rainbow rainbow
pg_ctl -D /usr/local/var/postgres -l logfile start
```

```shell script
brew install redis
set `daemonize yes` in `/usr/local/etc/redis.conf`
redis-server /usr/local/etc/redis.conf
```

```shell script
brew install rabbitmq
brew services start rabbitmq
```
