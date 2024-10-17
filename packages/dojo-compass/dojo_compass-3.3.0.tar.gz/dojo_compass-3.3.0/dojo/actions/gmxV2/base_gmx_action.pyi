from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from dojo.actions.base_action import BaseAction as BaseAction
from dojo.observations import GmxV2Observation as GmxV2Observation

@dataclass(kw_only=True)
class BaseGmxAction(DataClassJsonMixin, BaseAction[GmxV2Observation]):
    gas: int | None = ...
    gas_price: int | None = ...
    def __init__(self, *generated_args, agent, gas=..., gas_price=..., **generated_kwargs) -> None: ...
