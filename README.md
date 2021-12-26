# FreqtradeMultibot
Repository belonging to the Freqtrade multibot Youtube video

## Create two service files in /etc/systemd/system for bot A and B

These configurations assume that freqtrade is installed in ``/opt/freqtrade``

### Bot A

```
nano freq_bot_a.service
```

Add the following lines


```
[Unit]
Description=Freqtrade bot A

[Service]
WorkingDirectory=/opt/freqtrade
ExecStart=/opt/freqtrade/.env/bin/freqtrade trade --config /opt/freqtrade/user_data/config_a.json
Restart=always
RestartSec=10
Type=notify
NotifyAccess=all
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=freqtrade_a
User=root
Group=root
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

### Bot B

Copy this file to a second file named freq_bot_b.service:

```
cp freq_bot_a.service freq_bot_b.service
```

Change all the 'a' options in this file to 'b'.

## Create two config files in your Freqtrade user_data directory for bot A and B

### Bot A

```
freqtrade new-config -c /opt/freqtrade/user_data/config_a.json
```

Change this file to your preferences, but change/add the following lines below:

```
    "api_server": {
        "enabled": true,
        "listen_ip_address": "127.0.0.1",
        "listen_port": 8080,
        "verbosity": "error",
        "enable_openapi": false,
        "jwt_secret_key": "SomeSecretKey",
        "CORS_origins": ["http://localhost:8080"],
        "username": "dcd",
        "password": "dcd"
    },
    "bot_name": "Freqtrade bot A",
    "user_data_dir": "/opt/freqtrade/user_data/",
    "strategy_path": "/opt/freqtrade/user_data/",
    "strategy": "SampleStrategy",
    "db_url": "sqlite:////opt/freqtrade/user_data/tradesv3_a.sqlite",
    "logfile": "syslog:/dev/log",
    "initial_state": "running",
    "forcebuy_enable": false,
    "internals": {
            "process_throttle_secs": 5,
            "heartbeat_interval": 60,
            "sd_notify": true
    }
}

```

Make sure you specify the correct strategy for bot a and the tradesv3 database name!

Other config options like trading pairs,  Volume/Static PairsList, buy/sell settings are configured to your own preferences.

### Bot B

Copy this config file to file b:

```
cp config_a.json config_b.json
```

Change/add the following lines:

```
    "api_server": {
        "enabled": true,
        "listen_ip_address": "127.0.0.1",
        "listen_port": 8081,
        "verbosity": "error",
        "enable_openapi": false,
        "jwt_secret_key": "SomeSecretKey",
        "CORS_origins": ["http://localhost:8080"],
        "username": "dcd",
        "password": "dcd"
    },
    "bot_name": "Freqtrade bot B",
    "user_data_dir": "/opt/freqtrade/user_data/",
    "strategy_path": "/opt/freqtrade/user_data/",
    "strategy": "SmaRsiStrategy",
    "db_url": "sqlite:////opt/freqtrade/user_data/tradesv3_b.sqlite",
    "logfile": "syslog:/dev/log",
    "initial_state": "running",
    "forcebuy_enable": false,
    "internals": {
            "process_throttle_secs": 5,
            "heartbeat_interval": 60,
            "sd_notify": true
    }

```

## Start the bots as a service

# Copy these files into the following directory:
/etc/systemd/system

# Start the service:
sudo systemctl start freq_bot_a.service
sudo systemctl start freq_bot_b.service

# Check the service status:        

# Stop the service:
sudo systemctl stop freq_bot_a.service
sudo systemctl stop freq_bot_b.service

# Enable the service at system startup (start at boot):
sudo systemctl enable freq_bot_a.service
sudo systemctl enable freq_bot_b.service

# Disable the service at system startup (no start at boot):
sudo systemctl disable freq_bot_a.service
sudo systemctl disable freq_bot_b.service

# After each service config change
sudo systemctl daemon-reload

# Show activity 
sudo tail -f /var/log/syslog

## See the bots in action with FreqUI

Open a browser and go to: http://localhost:8080

If your bot is on your local host. Otherwise enter the IP address of the server into the url.
