# pylint: disable=E1101
import os
from typing import Dict

import httpx
from pydantic import BaseModel, Field, SecretStr


class APICredentials(BaseModel):
    api_societe_token: SecretStr = Field(...)
    api_sirene_client: SecretStr = Field(...)
    api_sirene_secret: SecretStr = Field(...)


class Companies:
    def __init__(self):
        self.__credentials: APICredentials = APICredentials(
            api_societe_token=SecretStr(
                os.environ.get("EAZYRENT_API__SOCIETE__API_KEY", "")
            ),
            api_sirene_client=SecretStr(
                os.environ.get("EAZYRENT_API__SIRENE__CLIENT_ID", "")
            ),
            api_sirene_secret=SecretStr(
                os.environ.get("EAZYRENT_API__SIRENE__CLIENT_SECRET", "")
            ),
        )

    def __get_societe_api_headers(self) -> Dict[str, str]:
        key_name = os.environ.get("EAZYRENT_API__SOCIETE__KEY_NAME", "Token")
        token = (
            self.__credentials.api_societe_token.get_secret_value()
        )  # pylint: disable=no-member
        auth_header = f"{key_name} {token}"
        return {"X-Authorization": auth_header}

    def get_company_from_api_societe(self, crn: str):
        """Get company information from API.

        args:
            - crn (str): The company registration number (SIREN)
        """
        url = os.environ.get("EAZYRENT_API_SOCIETE__ENDPOINT", "").format(siren=crn)
        response = httpx.get(url, headers=self.__get_societe_api_headers(), timeout=5)
        response.raise_for_status()
        return response.json()

    def get_company_from_api_sirene(self, crn: str):
        """Get company information from API.

        args:
            - crn (str): The company registration number (SIRET)
        """
        pass
