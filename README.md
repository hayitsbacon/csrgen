# CSR Generation CLI Tool

CLI tool to generate CSRs for a domain with specifications from a YAML file or arguments.


# Installation
```
git clone github.com/hayitsbacon/csrgen && \
cd csrgen && \
pip install .
```

# Usage

To use it:
```
    $ csrgen-cli --help
    Usage: csrgen [OPTIONS] [DOMAIN]

  CLI tool to generate CSRs for a domain with specifications from a YAML
  file or arguments.

Options:
  --generate-template      Create a YAML template with CSR fields
  --from-template TEXT     Load all fields from specified YAML template
  -c, --country-code TEXT  2 Letter Country code
  -s, --state TEXT         Full state name
  -l, --locality TEXT      City/Location
  -o, --org TEXT           Organization name
  -u, --org-unit TEXT      Organization Unit name.
  -e, --email TEXT         Webmaster email address
  --key-file TEXT          Private key file output path, defaults to working
                           directory
  --csr-file TEXT          CSR file output path, defaults to current directory
  --help                   Show this message and exit.
```
