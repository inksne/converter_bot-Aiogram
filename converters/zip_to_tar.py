from io import BytesIO

import zipfile
import tarfile


def convert_zip_to_tar_gz(zip_data: bytes) -> bytes:
    with zipfile.ZipFile(BytesIO(zip_data), 'r') as zip_ref:
        output = BytesIO()
        with tarfile.open(fileobj=output, mode='w:gz') as tar_ref:
            for file_name in zip_ref.namelist():
                file_data = zip_ref.read(file_name)
                tar_info = tarfile.TarInfo(name=file_name)
                tar_info.size = len(file_data)
                tar_ref.addfile(tar_info, fileobj=BytesIO(file_data))
        output.seek(0)
        return output.read()


def convert_tar_gz_to_zip(tar_gz_data: bytes) -> bytes:
    with tarfile.open(fileobj=BytesIO(tar_gz_data), mode='r:gz') as tar_ref:
        output = BytesIO()
        with zipfile.ZipFile(output, mode='w') as zip_ref:
            for file_info in tar_ref:
                if file_info.isfile():
                    file_data = tar_ref.extractfile(file_info).read()
                    zip_ref.writestr(file_info.name, file_data)
        output.seek(0)
        return output.read()