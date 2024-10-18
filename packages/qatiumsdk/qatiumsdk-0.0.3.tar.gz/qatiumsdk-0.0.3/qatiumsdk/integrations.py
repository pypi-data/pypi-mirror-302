from pyodide import ffi

class Integrations:
  def __init__(self, sdk):
    self.sdk = sdk

  async def fetch(self, options):
    """
    Performs a HTTP fetch proxied through Qatium's API integration gateway.
    Behaves in the same way as the built in fetch() method. Check the fetch
    method (https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) documentation
    to know more.

    #### Using secrets
    The fetch API works in combination with the Secrets API, to provide a secure way of integrating with third party APIs.
    You can use the stored secrets in the API requests using the format `$(secret:SECRET_KEY)` being `SECRET_KEY` the name of
    the secret stored.

    You can find an example of how to combine secrets in API integrations in
    this example (https://developer.qatium.app/plugins/getting-started/example-plugins/#6-integrate-external-service-using-api-secrets).

    Resolves to no-op when running in developer mode unless your developer account is
    approved by Qatium to do 3rd party API integrations. Find the details at the
    SDK documentation (https://developer.qatium.app/api/sdk/integrations/).
    
    This method is part of the {@link https://developer.qatium.app/api/sdk/integrations/ | Integrations API}.

    Args:
      input - URL as string, URL Object or Request object
      init - _(Optional)_ HTTP request options
    
    Returns:
    Promise resolving with the HTTP response

    Example:
      Perform a request to a 3rd party API
      ```
      async def init():
        reponse = await sdk.integrations.fetch('https://example.com')
        result = await response.text()
      ```
    """
    return self.sdk.integrations.fetch(ffi.to_js(options))
