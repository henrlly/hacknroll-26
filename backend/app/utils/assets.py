from app.core.models import Asset


def format_assets(assets: list[Asset]) -> str:
    """Format list of Asset objects into a string for prompting."""
    formatted_assets = []
    for i, asset in enumerate(assets):
        formatted_assets.append(
            f"{i + 1}. Asset ID: {asset.asset_id}\n"
            f"  Type: {asset.asset_type}\n"
            f"  Short Description: {asset.asset_short_desc}\n"
            f"  Long Description: {asset.asset_long_desc}\n"
        )
    return "\n".join(formatted_assets)
