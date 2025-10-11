# Email Configuration Template
# Copy this file to email_config.py and fill in your details

# Gmail Configuration (recommended)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Your email credentials
EMAIL_ADDRESS = "your-email@gmail.com"
EMAIL_PASSWORD = "your-app-password"  # Use App Password, not regular password

# For Gmail, you need to:
# 1. Enable 2-factor authentication
# 2. Generate an App Password: https://myaccount.google.com/apppasswords
# 3. Use the App Password instead of your regular password

# Alternative: Outlook/Hotmail
# SMTP_SERVER = "smtp-mail.outlook.com"
# SMTP_PORT = 587

# Alternative: Yahoo
# SMTP_SERVER = "smtp.mail.yahoo.com"
# SMTP_PORT = 587

# Environment Variables (recommended for security)
# Set these in your system environment or .env file:
# EMAIL_ADDRESS=your-email@gmail.com
# EMAIL_PASSWORD=your-app-password
