from urllib.parse import urlparse
import typing
from safe_imagefield import default_settings
import clamd

from django import conf
from django.utils import functional



def get_scanner(socket: str, timeout: int=None) -> typing.Union[clamd.ClamdUnixSocket, clamd.ClamdNetworkSocket]:
    if socket.startswith('unix://'):
        return clamd.ClamdUnixSocket(socket[7:], timeout)
    elif socket.startswith('tcp://'):
        uri = urlparse(socket)

        return clamd.ClamdNetworkSocket(
            uri.hostname, uri.port or 3310, timeout
        )
    else:
        raise NotImplementedError(
            'Missed or unsupported ClamAV connection string schema. '
            'Only tcp:// or unix:// is allowed.'
        )


def _get_default_scanner() -> typing.Union[clamd.ClamdUnixSocket, clamd.ClamdNetworkSocket]:
    return get_scanner(
        getattr(conf.settings, 'CLAMAV_SOCKET', default_settings.CLAMAV_SOCKET),
        getattr(conf.settings, 'CLAMAV_TIMEOUT', default_settings.CLAMAV_TIMEOUT),
    )


scanner = functional.SimpleLazyObject(_get_default_scanner)

#virus_desc = tuple
def scan_file(f) -> dict[str, tuple[str, str]]:
    _pos = f.tell()
    f.seek(0)
    status, virus_name = scanner.instream(f)['stream']
    f.seek(_pos)

    return status, virus_name
