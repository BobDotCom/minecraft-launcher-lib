microsoft_account
==========================
microsoft_account contains functions for login with a Microsft Account. Before using this module you need to `create a Azure application <https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app>`_. Many thanks to wiki.vg for it's `documentation of the login process <https://wiki.vg/Microsoft_Authentication_Scheme>`_.

.. code:: python

    get_login_url(client_id: str, redirect_uri: str) -> str

Returns the url to the website on which the user logs in.

.. code:: python

    url_contains_auth_code(url: str) -> bool

Checks if the given url contains a authorization code.

.. code:: python

    get_auth_code_from_url(url: str)

Get the authorization code from the url.

.. code:: python

    complete_login(client_id: str, client_secret: str, redirect_uri: str, auth_code: str) -> Dict[str, Union[List[Dict[str, str]]]]

Do the complete login process. It returns the following:

.. code:: json

    {
        "id" : "The uuid",
        "name" : "The username",
        "access_token": "The acces token",
        "refresh_token": "The refresh token",
        "skins" : [{
            "id" : "6a6e65e5-76dd-4c3c-a625-162924514568",
            "state" : "ACTIVE",
            "url" : "http://textures.minecraft.net/texture/1a4af718455d4aab528e7a61f86fa25e6a369d1768dcb13f7df319a713eb810b",
            "variant" : "CLASSIC",
            "alias" : "STEVE"
        } ],
        "capes" : []
    }

.. code:: python

    complete_refresh(client_id: str, client_secret: str, redirect_uri: str, refresh_token: str) -> Dict[str, Union[List[Dict[str, str]]]]

Do the complete login process with a refresh token. It returns the same as complete_login().

.. code:: python

    get_authorization_token(client_id: str, client_secret: str, redirect_uri: str, auth_code: str) -> Dict[str, str]

Get the authorization token.

.. code:: python

    refresh_authorization_token(client_id: str, client_secret: str, redirect_uri: str, refresh_token: str,) -> Dict[str, str]

Refresh the authorization token.

.. code:: python

    authenticate_with_xbl(access_token: str) -> Dict[str, Union[str, Dict[str, List[Dict[str, str]]]]]

Authenticate with Xbox Live.

.. code:: python

    authenticate_with_xsts(xbl_token: str) -> Dict[str, Union[str, Dict[str, Union[str, List[str]]]]]

Authenticate with XSTS.

.. code:: python

    authenticate_with_minecraft(userhash: str, xsts_token: str) -> Dict[str, Union[str, List, int]]

Authenticate with Minecraft.

.. code:: python

    get_store_information(token: str) -> Dict[str, Union[List[Dict[str, str]]]]

Get the store information.

.. code:: python

    get_profile(token: str) -> Dict[str, Union[List[Dict[str, str]]]]

Get the profile.
