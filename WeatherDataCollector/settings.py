import logging


# Debug mode
DEBUG = True

# Data Ingestion endpoint in the PX Cloud
DI_ENDPOINT = "wss://gateway-predix-data-services.run.aws-usw02-pr.ice.predix.io/v1/stream/messages"

ORIGIN = "http://www.pactera.com"

BEARER_TOKEN = "eyJhbGciOiJSUzI1NiJ9.eyJqdGkiOiJiY2UxYjBlNy1jMTkzLTQ2YzQtODViNC02YTM1OTlkMTU4MDkiLCJzdWIiOiJ0aW1lc2VyaWVzLWluZ2VzdGlvbiIsInNjb3BlIjpbInRpbWVzZXJpZXMuem9uZXMuNTY1MzQ4YmMtZWRhNi00YTdiLWI3MmQtZTI3MjM1MWUwNmExLnVzZXIiLCJ1YWEucmVzb3VyY2UiLCJvcGVuaWQiLCJ1YWEubm9uZSIsInRpbWVzZXJpZXMuem9uZXMuNTY1MzQ4YmMtZWRhNi00YTdiLWI3MmQtZTI3MjM1MWUwNmExLmluZ2VzdCJdLCJjbGllbnRfaWQiOiJ0aW1lc2VyaWVzLWluZ2VzdGlvbiIsImNpZCI6InRpbWVzZXJpZXMtaW5nZXN0aW9uIiwiYXpwIjoidGltZXNlcmllcy1pbmdlc3Rpb24iLCJncmFudF90eXBlIjoiY2xpZW50X2NyZWRlbnRpYWxzIiwicmV2X3NpZyI6IjdiNWRlMmY4IiwiaWF0IjoxNDU3MzQ3Mjk5LCJleHAiOjE0NTczOTA0OTksImlzcyI6Imh0dHBzOi8vODBlYzQ0MTUtYWQ4YS00NmNlLWIzMTAtZjZiNmMxODc5NjRkLnByZWRpeC11YWEucnVuLmF3cy11c3cwMi1wci5pY2UucHJlZGl4LmlvL29hdXRoL3Rva2VuIiwiemlkIjoiODBlYzQ0MTUtYWQ4YS00NmNlLWIzMTAtZjZiNmMxODc5NjRkIiwiYXVkIjpbInRpbWVzZXJpZXMtaW5nZXN0aW9uIiwidGltZXNlcmllcy56b25lcy41NjUzNDhiYy1lZGE2LTRhN2ItYjcyZC1lMjcyMzUxZTA2YTEiLCJ1YWEiLCJvcGVuaWQiXX0.ctrpJn8o5m4Rn0Gv9ekKABc8u-emWJ61VfDXU6XPWH8f0XaNbEQKD_pHXmwckp_TfR3LC3OPKlo0f1QshjmgJVM8ucZN2YcAVo-W0WoLz6KFLhDPASfrKEP_EV0jXhPn4jYRWK_qRdAJKAoGPO5tDyjDQS-R4pCwl5LzYCTFZ1KhAGrAOnp5AxsPIlBSXXRqXDN0i5zMrkE5x18Pknji46ARrD-1Kf0XExGnECzCQWXw_rl19SXYkLJxVufq70S870-lyQcuQlnzvnXDb3laCZ8mkcbNDqdgxjKyQu_TDpiAvT0SKfi5KyQseCYE1q6F2_MCnwIfdttkSx8AGROhIQ"

# Predix Zone ID
PREDIX_ZONE_ID = "565348bc-eda6-4a7b-b72d-e272351e06a1"

# Log settings
LOG_LEVEL = logging.DEBUG if DEBUG else logging.WARN
LOG_FORMAT = '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'

