# Copy these files into the following directory:
/etc/systemd/system

# Start the service:                
sudo systemctl start freqtrade.service

# Check the service status:        
sudo systemctl status freqtrade.service

# Stop the service:                
sudo systemctl stop freqtrade.service

# Enable the service at system startup (start at boot):
sudo systemctl enable freqtrade.service

# Disable the service at system startup (no start at boot):
sudo systemctl disable freqtrade.service

# After each service config change
sudo systemctl daemon-reload

# Show activity 
sudo tail -f /var/log/syslog


