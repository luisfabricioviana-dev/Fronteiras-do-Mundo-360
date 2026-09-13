from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class GeoAsset:
    asset_id: str
    canonical_name: str
    asset_type: str
    source: str
    verified: bool = False
    disputed: bool = False


class GeoAssetRegistry:
    def __init__(self) -> None:
        self._assets: Dict[str, GeoAsset] = {}

    def register(self, asset: GeoAsset) -> None:
        if asset.asset_id in self._assets:
            raise ValueError(f"Duplicate asset_id: {asset.asset_id}")
        if asset.disputed and not asset.verified:
            raise ValueError("Disputed assets must be verified before registration")
        self._assets[asset.asset_id] = asset

    def get(self, asset_id: str) -> Optional[GeoAsset]:
        return self._assets.get(asset_id)

    def require(self, asset_id: str) -> GeoAsset:
        asset = self.get(asset_id)
        if asset is None:
            raise KeyError(f"Unknown geo asset: {asset_id}")
        return asset
