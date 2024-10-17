"""
Papai-specific functions and data schema.
"""

import io
import os
from typing import TypedDict

import pandas as pd
from google.oauth2 import service_account

from papai_unified_storage.storage import Storage, filesystem
from papai_unified_storage.utils import generate_temporary_filename, joinpath


class Parquet(TypedDict):
    bucket_name: str
    """
    workspace bucket name.
    """
    step_name: str
    """
    friendly folder name that we consider being the bucket.
    """
    object_name: str
    """
    path to the parquet file.
    """


class Bucket(TypedDict):
    bucket_name: str
    """
    workspace bucket name.
    """
    step_name: str
    """
    friendly folder name that we consider being the bucket.
    """
    settings: dict
    """
    store connection settings to external buckets.
    """


class Registry(TypedDict):
    bucket_name: str
    """
    workspace bucket name.
    """
    artefacts_path: str
    """
    path to the artefact folder.
    """
    registry_name: str


def _get_io_config(key: str, match_value: str, list_io: list, io_name: str) -> dict:
    for io_ in list_io:
        if io_[key] == match_value:
            return io_
    raise ValueError(f"Could not find {io_name} with name {match_value}")


def _get_bucket_fs(
    bucket_name: str, papai_fs: Storage, list_buckets: list[Bucket]
) -> tuple[Storage, str]:
    """Get a filesystem to interact with a specific bucket.

    Parameters
    ----------
    bucket_name : str
        Name of the bucket to interact with.
    papai_fs : Storage
        Default filesystem to interact with the bucket.
    list_buckets : list[Bucket]
        List of all bucket configurations.

    Returns
    -------
    filesystem, path_prefix : tuple[Storage, str]
        Filesystem that allows interaction with the bucket.
        Path prefix to be used in papai internal bucket. If you are using an
        external bucket, this will be an empty string.
    """
    bucket = _get_io_config("step_name", bucket_name, list_buckets, "dataset")
    settings = bucket["settings"]

    if "virtual_bucket_path" in settings:
        return papai_fs, settings["virtual_bucket_path"]

    available_protocols = {
        "AZURE_OBJECT_STORAGE_SETTINGS": _get_abfs,
        "S3_OBJECT_STORAGE_SETTINGS": _get_s3fs,
        "GC_OBJECT_STORAGE_SETTINGS": _get_gcsfs,
    }
    protocol = available_protocols[settings["kind"]]

    return filesystem(protocol, settings["storage_options"]), ""


def _get_abfs(settings: dict) -> Storage:
    account_name = settings["account_name"]
    account_key = settings["account_key"]
    return filesystem("abfs", account_name=account_name, account_key=account_key)


def _get_gcsfs(settings: dict) -> Storage:
    credentials_dict = {
        "type": "service_account",
        "private_key_id": settings["private_key_id"],
        "private_key": settings["private_key"],
        "client_email": settings["client_email"],
        "token_uri": "https://oauth2.googleapis.com/token",
    }
    credentials = service_account.Credentials.from_service_account_info(
        credentials_dict
    )
    return filesystem("gcsfs", token=credentials)


def _get_s3fs(settings: dict) -> Storage:
    endpoint = settings["endpoint"]
    access_key = settings["access_key"]
    secret_key = settings["secret_key"]
    return filesystem("s3fs", key=access_key, secret=secret_key, endpoint=endpoint)


def list_bucket_objects(
    bucket_name: str,
    papai_fs: Storage,
    list_buckets: list[Bucket],
    prefix: str = "",
    recursive: bool = True,
):
    """List bucket objects with name starting with `prefix`.

    Parameters
    ----------
    bucket_name : str
        Name of the bucket to list in.
    papai_fs : Storage
        Default filesystem to interact with the bucket.
    list_buckets : list[Bucket]
        List of all bucket configurations.
    prefix : str, optional
        List all objects that starts with `prefix`, by default "".
    recursive : bool, optional
        Whether to list objects that are deeper than `prefix`, by default True.
    """
    fs, path_prefix = _get_bucket_fs(bucket_name, papai_fs, list_buckets)
    if path_prefix != "":
        prefix = joinpath(path_prefix, prefix)
    fs.list_files(bucket_name, prefix, recursive)


def read_from_bucket_to_file(
    bucket_name: str, object_name: str, papai_fs: Storage, list_buckets: list[Bucket]
):
    """Download a file from a bucket to the local file system.

    Parameters
    ----------
    bucket_name : str
        Name of the bucket to download from.
    object_name : str
        Path to the object to download.
    papai_fs : Storage
        Default filesystem to interact with the bucket.
    list_buckets : list[Bucket]
        List of all bucket configurations.
    """
    fs, path_prefix = _get_bucket_fs(bucket_name, papai_fs, list_buckets)
    if path_prefix != "":
        bucket_name = joinpath(bucket_name, path_prefix)
    path = joinpath(bucket_name, object_name)
    fs.get_file(path)


def write_file_in_bucket(
    bucket_name: str,
    file_name: str,
    *,
    data: io.BytesIO | str | None = None,
    file_path: str | bytes | os.PathLike | None = None,
    list_buckets: list[Bucket],
    papai_fs: Storage,
):
    """Upload a file to a bucket / Write data in a bucket.

    Parameters
    ----------
    bucket_name : str
        Name of the bucket to write in.
    file_name : str
        Path to which the data will be written / the file will be uploaded.
    list_buckets : list[Bucket]
        List of all bucket configurations.
    papai_fs : Storage
        Default filesystem to interact with the bucket.
    data : io.BytesIO | str | None, optional
        Data to write to the file, by default None.
    file_path : str | bytes | os.PathLike | None, optional
        File to upload to the bucket, by default None.
    """
    fs, path_prefix = _get_bucket_fs(bucket_name, papai_fs, list_buckets)
    if path_prefix != "":
        bucket_name = joinpath(bucket_name, path_prefix)
    path = joinpath(bucket_name, file_name)

    if data is not None:
        fs.write_to_file(path, content=data)
    elif file_path is not None:
        fs.put(file_path, path)

    raise ValueError("You must provide either data or a file_path")


def import_dataset(
    dataset_name: str, list_parquets: list[Parquet], papai_fs: Storage
) -> pd.DataFrame:
    """Load a pandas DataFrame from a parquet file in the papai bucket.

    Parameters
    ----------
    dataset_name : str
        Name of the dataset to load.
    list_parquets : list[Parquet]
        List of all parquet configurations.
    papai_fs : Storage
        Papai filesystem in which to find the dataset.

    Returns
    -------
    pd.DataFrame
    """
    parquet = _get_io_config("step_name", dataset_name, list_parquets, "dataset")
    parquet_path = joinpath(parquet["bucket_name"], parquet["object_name"])
    return papai_fs.read_dataset_from_parquet(parquet_path)


def export_dataset(
    dataset: pd.DataFrame,
    dataset_name: str,
    list_parquets: list[Parquet],
    papai_fs: Storage,
):
    """Write a pandas DataFrame to a parquet file in the papai bucket.

    Parameters
    ----------
    dataset : pd.DataFrame
        Pandas DataFrame to write to the bucket.
    dataset_name : str
        Name of the dataset to load.
    list_parquets : list[Parquet]
        List of all parquet configurations.
    papai_fs : Storage
        Papai filesystem in which to find the dataset.
    """
    parquet = _get_io_config("step_name", dataset_name, list_parquets, "dataset")
    parquet_path = joinpath(parquet["bucket_name"], parquet["object_name"])
    papai_fs.write_dataframe_to_parquet(parquet_path, dataset)


def _get_artefacts_folder_path(
    registry_name: str,
    list_registries: list[Registry],
    run_uuid: str | None = None,
) -> str:
    """
    Get the path to the artefacts folder in the papai filesystem.
    """
    registry = _get_io_config(
        "registry_name", registry_name, list_registries, "registry"
    )
    artefacts_folder_path = joinpath(
        registry["bucket_name"], registry["artefacts_path"]
    )

    if run_uuid is not None:
        artefacts_folder_path = artefacts_folder_path.rsplit("/", 1)[0] + "/" + run_uuid

    return artefacts_folder_path


def get_model_artefacts(
    registry_name: str,
    artefact_path: str,
    run_uuid: str,
    registry_inputs: list[Registry],
    papai_fs: Storage,
) -> str:
    """Download a model artefact from the papai filesystem.

    Parameters
    ----------
    registry_name : str
        Name of the registry to get the artefact from.
    artefact_path : str
        Path to the artefact.
    registry_inputs : list[Registry]
        List of all registry configurations.
    papai_fs : Storage
        PapAI filesystem to interact with the bucket.
    run_uuid : str
        The UUID of the run you want to get artefacts from.

    Returns
    -------
    str
        Local path to the downloaded artefact.
    """
    artefacts_folder_path = _get_artefacts_folder_path(
        registry_name, registry_inputs, run_uuid
    )
    artefact_full_path = joinpath(artefacts_folder_path, artefact_path)

    tmp_file = generate_temporary_filename()
    papai_fs.get_file(artefact_full_path, tmp_file)

    return tmp_file


def save_model_artefact(
    data,
    registry_name: str,
    artefact_path: str,
    registry_inputs: list[Registry],
    papai_fs: Storage,
    run_uuid: str = None,
):
    """Upload an artefact to the papai filesystem.

    Parameters
    ----------
    data: str | bytes
        Data to write to the file.
    registry_name : str
        Name of the registry to get the artefact from.
    artefact_path : str
        Path to the artefact.
    registry_inputs : list[Registry]
        List of all registry configurations.
    papai_fs : Storage
        PapAI filesystem to interact with the bucket.
    run_uuid : str
        The UUID of the run you want to get artefacts from.

    Returns
    -------
    str
        Local path to the downloaded artefact.
    """
    artefacts_folder_path = _get_artefacts_folder_path(
        registry_name, registry_inputs, run_uuid
    )
    artefact_full_path = joinpath(artefacts_folder_path, artefact_path)

    papai_fs.write_to_file(artefact_full_path, data)
