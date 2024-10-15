import pathlib
import typing

import numpy

from . import file_decoder
from . import events_stream
from . import file_type as file_type_module
from . import timestamp
from . import udp_decoder


def events_stream_from_array(
    events: numpy.ndarray,
    dimensions: tuple[int, int],
) -> events_stream.FiniteEventsStream:
    return events_stream.Array(events=events, dimensions=dimensions)


def events_stream_from_file(
    path: typing.Union[str, pathlib.Path],
    track_id: typing.Optional[int] = None,
    dimensions_fallback: tuple[int, int] = (1280, 720),
    version_fallback: typing.Optional[
        typing.Literal["dat1", "dat2", "evt2", "evt2.1", "evt3"]
    ] = None,
    t0: timestamp.Time = 0,
    file_type: typing.Optional[file_type_module.FileType] = None,
    csv_properties: file_decoder.CsvProperties = file_decoder.CsvProperties.default(),
) -> events_stream.FiniteEventsStream:
    """An event file decoder (supports .aedat4, .es, .raw, and .dat).

    track_id is only used if the type is aedat. It selects a specific stream in the container.
    If left unspecified (None), the first event stream is selected.

    dimensions_fallback is only used if the file type is EVT (.raw) or DAT and if the file's header
    does not specify the size.

    version_fallback is only used if the file type is EVT (.raw) or DAT and if the file's header
    does not specify the version.

    t0 is only used if the file type is ES.

    Args:
        path: Path of the input event file.
        track_id: Stream ID, only used with aedat files. Defaults to None.
        dimensions_fallback: Size fallback for EVT (.raw) and DAT files. Defaults to (1280, 720).
        version_fallback: Version fallback for EVT (.raw) and DAT files. Defaults to "dat2" for DAT and "evt3" for EVT.
        t0: Initial time for ES files, in seconds. Defaults to None.
        file_type: Override the type determination algorithm. Defaults to None.
    """
    return file_decoder.Decoder(
        path=pathlib.Path(path),
        track_id=track_id,
        dimensions_fallback=dimensions_fallback,
        version_fallback=version_fallback,
        t0=t0,
        csv_properties=csv_properties,
        file_type=file_type,
    )


def events_stream_from_stdin(
    dimensions: tuple[int, int],
    t0: timestamp.Time = 0,
    csv_properties: file_decoder.CsvProperties = file_decoder.CsvProperties.default(),
):
    return file_decoder.Decoder(
        path=None,
        track_id=None,
        dimensions_fallback=dimensions,
        version_fallback=None,
        t0=t0,
        csv_properties=csv_properties,
        file_type=file_type_module.FileType.CSV,
    )


def events_stream_from_udp(
    dimensions: tuple[int, int],
    address: typing.Union[
        tuple[str, int], tuple[str, int, typing.Optional[int], typing.Optional[str]]
    ],
    format: typing.Literal["t64_x16_y16_on8", "t32_x16_y15_on1"] = "t64_x16_y16_on8",
):
    return udp_decoder.Decoder(dimensions=dimensions, address=address, format=format)
