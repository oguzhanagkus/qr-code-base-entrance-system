import logging
import uuid
import requests
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.backends import default_backend as crypto_default_backend

from django.conf import settings
from django.core.mail import EmailMessage


class SSHKey:
    def __init__(self) -> None:
        self.key = rsa.generate_private_key(
            backend=crypto_default_backend(), public_exponent=65537, key_size=2048
        )

    def get_public_key(self) -> str:
        return (
            self.key.public_key()
                .public_bytes(
                crypto_serialization.Encoding.OpenSSH,
                crypto_serialization.PublicFormat.OpenSSH,
            ).decode()
        )

    def get_private_key(self) -> str:
        return self.key.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.TraditionalOpenSSL,
            crypto_serialization.NoEncryption(),
        ).decode()

    def save(self, name: str) -> None:
        with open("{}/{}_id_rsa".format(settings.KEY_URL, name), "w") as f:
            f.write(self.get_private_key())
        with open("{}/{}_id_rsa.pub".format(settings.KEY_URL, name), "w") as f:
            f.write(self.get_public_key())


class DigitalOcean:
    def __init__(self):
        self.base_url = settings.DIGITAL_OCEAN_URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(settings.DIGITAL_OCEAN_TOKEN),
        }

    def get_ssh_keys(self):
        url = "{}/account/keys".format(self.base_url)
        response = requests.get(url, headers=self.headers)
        return response.json()

    def create_ssh_key(self, name: str):
        ssh_key = SSHKey()
        ssh_key.save(name.lower())
        data = {
            "public_key": ssh_key.get_public_key(),
            "name": name,
        }
        url = "{}/account/keys".format(self.base_url)
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def get_droplets(self):
        url = "{}/droplets".format(self.base_url)
        response = requests.get(url, headers=self.headers)
        return response.json()

    def create_droplet(self, name: str, ssh_key_id: int, ssh_key_fingerprint: str):

        data = {
            "name": "mes-{}".format(name.lower()),
            "region": "fra1",
            "size": "s-1vcpu-1gb",
            "image": "ubuntu-20-04-x64",
            "ssh_keys": [ssh_key_id, ssh_key_fingerprint],
            "user_data": open("provision.sh", "r").read().replace("{{company_name_placeholder}}", name),
            "monitoring": True,
        }
        url = "{}/droplets".format(self.base_url)
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()


def generate_uuid() -> str:
    return str(uuid.uuid4())


def init_instance(company_name: str):
    initializer = DigitalOcean()
    ssh_key = initializer.create_ssh_key(company_name)
    ssh_key_id = ssh_key["ssh_key"]["id"]
    ssh_key_fingerprint = ssh_key["ssh_key"]["fingerprint"]
    instance = initializer.create_droplet(company_name, ssh_key_id, ssh_key_fingerprint)
    droplet_id = instance["droplet"]["id"]
    logging.info("Droplet created with ID: {}".format(droplet_id))
    return droplet_id


def notify_customer(company_name, email, ip_address):
    try:
        mail = EmailMessage(
            "Müsaade Entrance System Access Information",
            "Your system is ready! You can start to use by following link. https://{}".format(ip_address),
            "Müsaade Management System <{}>".format(settings.EMAIL_HOST_USER),
            [email]
        )
        mail.send()
        logging.info("Notification sent to: {} ".format(company_name))
    except Exception as exception:
        logging.exception("Exception occurred while sending notification email: {}".format(str(exception)))
        raise exception
