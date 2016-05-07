# apache-proxy-generator
Python script for generating Apache 2.4 proxy virtual hosts for Odoo

# Install

```
cd /opt
git clone https://github.com/antespi/apache-proxy-generator
```

# Configuration

There is a sample configuration in folder ```config_dist```. To create your own configuration copy it to another folder:

```
cd /opt/apache-proxy-generator
cp -a config_dist config
```

Now you can define your common options:

```
nano config/common.yaml
```

There is a folder for each machine who this Apache instance does reverse proxy. Inside it there is a YAML config file for each service.

For example, for ```localhost``` machine, we can define custom params for service one and service two:

```
nano config/localhost/service-one.yaml
nano config/localhost/service-two.yaml
```

# Usage

For adding or replace a service (virtual host) you can execute ```add.py```

```
cd /opt/apache-proxy-generator
./add.py -c config/localhost/service-one.yaml
```

If you want to add or replace all service for a machine, then execute ```add_all.sh```

```
cd /opt/apache-proxy-generator
./add_all.sh localhost
```
