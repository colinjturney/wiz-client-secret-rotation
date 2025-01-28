# Wiz Client Secret Rotation

# Disclaimer - PLEASE READ

By using this software and associated documentation files (the “Software”) you hereby agree and understand that:

1. The use of the Software is free of charge and may only be used by Wiz customers for its internal purposes.
2. The Software should not be distributed to third parties.
3. The Software is not part of Wiz’s Services and is not subject to your company’s services agreement with Wiz.
4. THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL WIZ BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE USE OF THIS SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Description

The purpose of this container image is to automatically manage the rotation of a Wiz Client Secret. This is intended to offer the following benefits:

1. Adhering to good secrets management practice by rotating secrets, reducing the chance that leaked credentials will be compromised.
2. Removing attack vector of hardcoded credentials in configuration files, since the tool will keep them rotated.
3. Ensuring that once a credential reaches its expiry date, it is rotated and it's expiry date is extended.

For POC purposes, this is currently managed as CLIENT_ID and CLIENT_SECRET stored within the same container image.

This repository contains a directory named `docker` which itself contains a `Dockerfile` and `scripts` directory:

The `scripts` directory contains three files:

* rotate.py: A python script that will check if the given Wiz Client ID and Secret are close to expiry and, if they are, rotate them and update the expiry date.
* wiz_auth.sh: A file containing two initial values of the client id and secret that are to be bootstrapped
* wiz-sa-rotate.sh: A wrapper script that supplies the values of the client_id and secret to the python script.
* wiz-sa-entrypoint.sh: An entrypoint script for the container once it first starts.

# How to run

1. Create a service account with the required API scopes, with the following in API scopes required addition: read:service_accounts update:service_accounts. Store its initial values in wiz_auth.sh in the format shown.
2. Run the wrapper script. In real life, this could be scheduled on a daily basis through cron or similar.

# Future Extensions

## Kubernetes Integration

Manage WIZ_CLIENT_ID and WIZ_CLIENT_SECRET as a Kubernetes Secret, for easy consumption by other Wiz-related Kubernetes tooling such as the Kubernetes Connector, Admissions Controller and Runtime sensor.