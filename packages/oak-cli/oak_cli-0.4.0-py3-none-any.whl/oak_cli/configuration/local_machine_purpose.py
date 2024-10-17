import json
from typing import List, Optional

import typer

from oak_cli.configuration.common import (
    check_and_handle_config_file,
    get_config_value,
    update_config_value,
)
from oak_cli.configuration.keys.enums import ConfigurableConfigKey
from oak_cli.utils.typer_augmentations import AliasGroup
from oak_cli.utils.types import CustomEnum

app = typer.Typer(cls=AliasGroup)


class LocalMachinePurpose(CustomEnum):
    """A machine can have one, multiple, or all of these purposes."""

    EVERYTHING = "everything"

    ROOT_ORCHESTRATOR = "root_orchestrator"
    CLUSTER_ORCHESTRATOR = "cluster_orchestrator"
    WORKER_NODE = "worker_node"

    ADDON_SUPPORT = "addon_support"

    DEVELOPMENT = "development"


def get_local_machine_purposes_from_config(
    terminate_if_key_is_missing_from_conf: bool = True,
) -> Optional[List[LocalMachinePurpose]]:
    check_and_handle_config_file()
    config_json_string = get_config_value(
        ConfigurableConfigKey.LOCAL_MACHINE_PURPOSE,
        terminate_if_key_is_missing_from_conf,
    )
    if not config_json_string:
        return None
    config_list = json.loads(config_json_string)
    return [LocalMachinePurpose(purpose_name) for purpose_name in config_list]


def check_if_local_machine_has_required_purposes(
    required_purposes: List[LocalMachinePurpose],
) -> bool:
    local_machine_purposes = get_local_machine_purposes_from_config(
        terminate_if_key_is_missing_from_conf=False
    )
    if not local_machine_purposes:
        return False
    if LocalMachinePurpose.EVERYTHING in local_machine_purposes:
        return True
    return set(required_purposes).issubset(set(local_machine_purposes))


@app.command(
    "configure",
    help="\n".join(
        (
            "Configure the purpose of the local machine w.r.t. Oakestra.",
            "You can specify one or multiple purposes at once.",
        )
    ),
)
def configure_local_machine_purpose(
    # NOTE: Sets are not yet supported by the frameworks.
    local_machine_purposes: List[LocalMachinePurpose],
) -> None:
    local_machine_purposes_set = set(local_machine_purposes)
    if LocalMachinePurpose.EVERYTHING in local_machine_purposes_set:
        local_machine_purposes_set = {LocalMachinePurpose.EVERYTHING}
    check_and_handle_config_file()
    update_config_value(
        key=ConfigurableConfigKey.LOCAL_MACHINE_PURPOSE,
        # NOTE: The config only supports strings.
        value=json.dumps([purpose.value for purpose in local_machine_purposes_set]),
    )
