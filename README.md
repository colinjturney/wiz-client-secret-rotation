# Disclaimer - PLEASE READ

By using this software and associated documentation files (the “Software”) you hereby agree and understand that:

1. The use of the Software is free of charge and may only be used by Wiz customers for its internal purposes.
2. The Software should not be distributed to third parties.
3. The Software is not part of Wiz’s Services and is not subject to your company’s services agreement with Wiz.
4. THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL WIZ BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE USE OF THIS SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Description

This repository contains three files:

* rotate.py: A python script that will check if the given Wiz Client ID and Secret are close to expiry and, if they are, rotate them and update the expiry date.
* wiz_auth.sh: A file containing two initial values of the client id and secret that are to be bootstrapped
* wrapper.sh: A wrapper script that supplies the values of the client_id and secret to the python script.

# How to run

1. Create a service account with the required API scopes, with the following in API scopes required addition: read:service_accounts update:service_accounts. Store its initial values in wiz_auth.sh in the format shown.
2. Run the wrapper script. In real life, this could be scheduled on a daily basis through cron or similar.