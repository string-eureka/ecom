from storages.backends.azure_storage import AzureStorage
import environ
env = environ.Env()
environ.Env.read_env()

class AzureMediaStorage(AzureStorage):
    account_name = env('AZURE_ACCOUNT_NAME')
    account_key = "0DKGUiRJYN0yrfRH2qsb8uroDn/Za3mJrvwiGd9GEzuMHHaYy4R/DGhZllFOY1DIAVJBRSdWc9pf+ASt0c72XA=="
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = env('AZURE_ACCOUNT_NAME')
    account_key = "i8tvNBJv0hI/D+CGOoiluihTAkVXIwKnFchtxh3ne3SmmmNKU1zFEUEBfptMoE2E9tcBGzHjceba+AStQNqMHQ=="
    azure_container = 'static'
    expiration_secs = None