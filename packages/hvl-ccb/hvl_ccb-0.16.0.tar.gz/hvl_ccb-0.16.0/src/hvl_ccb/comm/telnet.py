#  Copyright (c) ETH Zurich, SIS ID and HVL D-ITET
#
"""
Communication protocol for telnet. Makes use of the `telnetlib
<https://docs.python.org/3/library/telnetlib.html>`_ library.
"""

import logging
import telnetlib
from ipaddress import IPv4Address, IPv6Address
from typing import Optional, Union, cast

from hvl_ccb.comm import (
    AsyncCommunicationProtocol,
    AsyncCommunicationProtocolConfig,
    CommunicationError,
)
from hvl_ccb.configuration import configdataclass
from hvl_ccb.utils.typing import Number
from hvl_ccb.utils.validation import validate_and_resolve_host, validate_tcp_port

logger = logging.getLogger(__name__)


class TelnetError(IOError, CommunicationError):
    """Telnet communication related errors."""


@configdataclass
class TelnetCommunicationConfig(AsyncCommunicationProtocolConfig):
    """
    Configuration dataclass for :class:`TelnetCommunication`.
    """

    #: Host to connect to
    #: can be ``localhost`` or
    host: Optional[Union[str, IPv4Address, IPv6Address]] = None

    #: Port at which the host is listening
    port: int = 0

    #: Timeout for reading a line
    timeout: Number = 0.2

    def clean_values(self) -> None:
        super().clean_values()
        if self.timeout < 0:
            msg = "Timeout has to be >= 0."
            raise ValueError(msg)
        self.force_value(  # type: ignore[attr-defined]
            "host",
            validate_and_resolve_host(self.host, logger),  # type: ignore[arg-type]
        )
        validate_tcp_port(self.port, logger)

    def create_telnet(self) -> Optional[telnetlib.Telnet]:
        """
        Create a telnet client
        :return: Opened Telnet object or None if connection is not possible
        """
        if self.host is None:
            return None

        try:
            tn = telnetlib.Telnet(host=cast(str, self.host), port=self.port)  # noqa: S312 telnet will be removed in a future version
        except (ConnectionRefusedError, TimeoutError, OSError) as exc:
            raise TelnetError from exc
        else:
            return tn


class TelnetCommunication(AsyncCommunicationProtocol):
    """
    Implements the Communication Protocol for telnet.
    """

    def __init__(self, configuration) -> None:
        """
        Constructor for TelnetCommunication.
        """

        super().__init__(configuration)

        self._tn: Optional[telnetlib.Telnet] = self.config.create_telnet()

    @property
    def is_open(self) -> bool:
        """
        Is the connection open?

        :return: True for an open connection
        """
        return self._tn is not None and self._tn.sock is not None  # type: ignore[attr-defined]

    def open(self) -> None:
        """
        Open the telnet connection unless it is not yet opened.
        """
        if self.is_open:
            return

        with self.access_lock:
            try:
                self._tn.open(self._tn.host, self._tn.port)  # type: ignore[union-attr,arg-type]
            except (ConnectionRefusedError, TimeoutError, OSError) as exc:
                raise TelnetError from exc

    def close(self) -> None:
        """
        Close the telnet connection unless it is not closed.
        """
        if not self.is_open:
            return

        with self.access_lock:
            self._tn.close()  # type: ignore[union-attr]

    @staticmethod
    def config_cls():
        return TelnetCommunicationConfig

    def write_bytes(self, data: bytes) -> int:
        """
        Write the data as `bytes` to the telnet connection.

        :param data: Data to be sent.
        :raises TelnetError: when connection is not open, raises an Error during the
            communication
        """

        if not self.is_open:
            msg = "The Telnet connection is not open."
            raise TelnetError(msg)

        with self.access_lock:
            cast(telnetlib.Telnet, self._tn).write(data)

        return 0

    def read_bytes(self) -> bytes:
        """
        Read data as `bytes` from the telnet connection.

        :return: data from telnet connection
        :raises TelnetError: when connection is not open, raises an Error during the
            communication
        """

        if not self.is_open:
            msg = "The Telnet connection is not open."
            raise TelnetError(msg)

        try:
            return (
                cast(telnetlib.Telnet, self._tn)
                .read_until(match=self.config.terminator, timeout=self.config.timeout)
                .strip()
            )
        except EOFError:
            return b""
