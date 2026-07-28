"""MCP server, skill, and hosted-connector identities."""

from .identity_common import required


def mcp_identity(server_name: str, version: str = "") -> str:
    identity = f"mcp:{required(server_name, 'MCP server name')}"
    if version.strip():
        identity += f"@{version.strip()}"
    return identity


def skill_identity(
    provider: str,
    source: str,
    skill_name: str,
    version: str = "",
) -> str:
    identity = (
        f"skill:{required(provider, 'skill provider').lower()}/"
        f"{required(source, 'skill source').strip('/')}/"
        f"{required(skill_name, 'skill name')}"
    )
    if version.strip():
        identity += f"@{version.strip()}"
    return identity


def connector_identity(provider: str, connector_id: str) -> str:
    return (
        f"connector:{required(provider, 'connector provider').lower()}/"
        f"{required(connector_id, 'connector ID')}"
    )
