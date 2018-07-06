import click
import yaml
from OpenSSL import crypto
import os
import sys
import datetime

key = crypto.PKey()
    
# Generate a private key and write it to current directory. 
def generateKey(cn, keypath):
    TYPE_RSA = crypto.TYPE_RSA
    if os.path.exists(keypath):
        click.echo("Private key file already exists at {0}. Exiting".format(keypath))
        return 1
    else:
        print("Generating key...")
        key.generate_key(TYPE_RSA, 4096)
        f = open(keypath, "wb")
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
        f.close()
        click.echo("Private key file written to {0}".format(keypath))
    return 0

# Generate a CSR and write it to current directory.
def generateCSR(csr_info, csrpath):
    req = crypto.X509Req()
    req.get_subject().CN = csr_info['common-name']
    req.get_subject().C = csr_info['country-code']
    req.get_subject().ST = csr_info['state-province']
    req.get_subject().L = csr_info['city-town-locality']
    req.get_subject().O = csr_info['organization']
    req.get_subject().OU = csr_info['organizational-unit']
    req.get_subject().emailAddress = csr_info['email']
    req.set_pubkey(key)
    req.sign(key, "sha256")

    if os.path.exists(csrpath):
        click.echo("CSR file already exists at {0}. Exiting".format(csrpath))
        return 1
    else:
        f = open(csrpath, "wb")
        f.write(crypto.dump_certificate_request(crypto.FILETYPE_PEM, req))
        f.close()
        click.echo("CSR file written to {0}. Exiting".format(csrpath))
        return 0
    

@click.command()
@click.option('--generate-template', is_flag=True, help='Create a YAML template with CSR fields')
@click.option('--from-template', type=str, help='Load all fields from specified YAML template')
@click.option('--country-code', '-c', type=str, help='2 Letter Country code')
@click.option('--state', '-s', type=str, help='Full state name')
@click.option('--locality', '-l', type=str, help="City/Location")
@click.option('--org', '-o', type=str, help="Organization name")
@click.option('--org-unit', '-u', type=str, help="Organization Unit name.")
@click.option('--email', '-e', type=str, help="Webmaster email address")
@click.option('--key-file', type=str, help='Private key file output path, defaults to working directory')
@click.option('--csr-file', type=str, help='CSR file output path, defaults to current directory')
@click.argument('domain', required=False)
def main(domain, generate_template,  from_template, country_code, state, locality, org, org_unit, email, key_file, csr_file):
    """CLI tool to generate CSRs for a domain with specifications from a YAML file or arguments."""
    
    if generate_template:
        template = {
                'country-code': 'US',
                'city-town-locality': 'New York',
                'state-province': 'NY',
                'organization': 'Daily Bugle',
                'organizational-unit': 'Web Services',
                'email': 'haveyouseenspiderman@dailybugle.com'
            }
        try:
            with open('csrgen-template.yaml', 'w') as yaml_file:
                yaml.dump(template, yaml_file, default_flow_style=False)
            click.echo('Tempalte written to ./csrgen-template.yaml. Exiting')
            return 0
        except:
            click.echo('Failed to write to current directory. Exiting')
            return 1

    if not domain:
        click.echo('Please provide a domain or seek --help. Exiting')
        return 1
    
    d = datetime.datetime.now().date()
    if key_file:
        key_path = key_file
    else:
        key_path = "./" + domain + '-' + str(d) + '.key'
        
    if csr_file:
        csr_path = csr_file
    else:
        csr_path =  "./" + domain + '-' + str(d) + '.csr'
    
    click.echo('Generating CSR for {0}'.format(domain))    
    if from_template:
        if not country_code and not state and not locality and not org and not org_unit:
            click.echo('Using {0} for field values'.format(from_template))
            try:
                with open(from_template, 'r') as stream:
                    csr_info = yaml.load(stream)
            except:
                click.echo('Unable to parse YAML template, please check syntax or template path. Exiting')
                return 1
        else:
            click.echo('You must provide CSR fields as a YAML template or arguments, not both. Exiting')
            return 1
        
    else:
        if country_code and state and locality and org and org_unit and email:
            csr_info = {
                'country-code': country_code,
                'city-town-locality': locality,
                'state-province': state,
                'organization': org,
                'organizational-unit': org_unit,
                'email': email
            }
        else:
            click.echo('Not all field values were provided. Check your arguments or use --help. Exiting')
            return 1
        
    csr_info['common-name'] = domain
    click.echo("Country Code: {0}".format(csr_info['country-code']))
    click.echo("State/Province: {0}".format(csr_info['state-province']))
    click.echo("City/Town/Locality: {0}".format(csr_info['city-town-locality']))
    click.echo("Organization: {0}".format(csr_info['organization']))
    click.echo("Organizational Unit: {0}".format(csr_info['organizational-unit']))
    click.echo("Email: {0}".format(csr_info['email']))
    
    # Exit if generateKey fails
    if generateKey(csr_info['common-name'], key_path):
        return 1
    generateCSR(csr_info, csr_path)
    return 0
