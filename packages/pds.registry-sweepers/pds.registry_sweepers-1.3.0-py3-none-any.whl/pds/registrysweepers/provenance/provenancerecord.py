from __future__ import annotations

from typing import Dict
from typing import Optional

from pds.registrysweepers.provenance.constants import METADATA_SUCCESSOR_KEY
from pds.registrysweepers.provenance.versioning import SWEEPERS_PROVENANCE_VERSION
from pds.registrysweepers.provenance.versioning import SWEEPERS_PROVENANCE_VERSION_METADATA_KEY
from pds.registrysweepers.utils.productidentifiers.pdslidvid import PdsLidVid


class ProvenanceRecord:
    lidvid: PdsLidVid
    _successor: Optional[PdsLidVid]
    skip_write: bool

    def __init__(self, lidvid: PdsLidVid, successor: Optional[PdsLidVid], skip_write: bool = False):
        self.lidvid = lidvid
        self._successor = successor
        self.skip_write = skip_write

    @property
    def successor(self) -> Optional[PdsLidVid]:
        return self._successor

    def set_successor(self, successor: PdsLidVid):
        if successor != self._successor:
            self._successor = successor
            self.skip_write = False

    @staticmethod
    def from_source(_source: Dict) -> ProvenanceRecord:
        if METADATA_SUCCESSOR_KEY in _source and _source[METADATA_SUCCESSOR_KEY] is not None:
            successor = PdsLidVid.from_string(_source[METADATA_SUCCESSOR_KEY])
        else:
            successor = None
        skip_write = _source.get(SWEEPERS_PROVENANCE_VERSION_METADATA_KEY, 0) >= SWEEPERS_PROVENANCE_VERSION
        return ProvenanceRecord(
            lidvid=PdsLidVid.from_string(_source["lidvid"]), successor=successor, skip_write=skip_write
        )

    @staticmethod
    def from_doc(doc: Dict) -> ProvenanceRecord:
        return ProvenanceRecord.from_source(doc["_source"])
