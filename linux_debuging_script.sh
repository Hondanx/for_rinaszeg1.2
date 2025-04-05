#!/bin/bash

# Create a custom OpenSSL configuration file to enable legacy algorithms
echo "Creating OpenSSL configuration to enable MD4..."

cat > /tmp/openssl.cnf << 'EOL'
openssl_conf = openssl_init

[openssl_init]
providers = provider_sect

[provider_sect]
default = default_sect
legacy = legacy_sect

[default_sect]
activate = 1

[legacy_sect]
activate = 1
EOL

# Add to environment variables before running the script
echo "To use this configuration, run:"
echo "export OPENSSL_CONF=/tmp/openssl.cnf"
echo "python3 nato-translator.py"