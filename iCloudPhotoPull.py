from pyicloud import PyiCloudService
import getpass
import sys
import shutil

username = raw_input("Enter Apple ID: ")
pw = getpass.getpass(prompt='Enter Password: ')

api = PyiCloudService(username, pw)

if api.requires_2sa:
    import click
    print("Two-step authentication required. Your trusted devices are:")

    devices = api.trusted_devices
    for i, device in enumerate(devices):
        print("  %s: %s" % (i, device.get('deviceName',"SMS to %s" % device.get('phoneNumber'))))

    device = click.prompt('Which device would you like to use?', default=0)
    device = devices[device]
    if not api.send_verification_code(device):
        print("Failed to send verification code")
        sys.exit(1)

    code = click.prompt('Please enter validation code')
    if not api.validate_verification_code(device, code):
        print("Failed to verify verification code")
        sys.exit(1)

for photo in api.photos.all.photos:
    download = photo.download()
    with open(photo.filename, 'wb') as opened_file:
        shutil.copyfileobj(download.raw, opened_file)