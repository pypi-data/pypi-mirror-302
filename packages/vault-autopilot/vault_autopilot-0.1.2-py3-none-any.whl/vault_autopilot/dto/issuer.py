from typing import Literal, NotRequired

from typing_extensions import TypedDict

from .._pkg.asyva.dto import issuer
from .abstract import AbstractDTO


class Certificate(
    issuer.CommonFields,
    issuer.KeyGenerationFields,
    issuer.ManagedKeyFields,
): ...


class Options(issuer.IssuerMutableFields): ...


class Chaining(TypedDict):
    upstream_issuer_ref: str
    signature_bits: NotRequired[int]
    skid: NotRequired[str]
    use_pss: NotRequired[bool]
    add_basic_constraints: NotRequired[bool]


class IssuerApplyDTO(AbstractDTO):
    class Spec(TypedDict):
        name: str
        secrets_engine_ref: str
        certificate: Certificate
        options: NotRequired[Options]
        chaining: NotRequired[Chaining]
        # TODO: extra_params: NotRequired[issuer.IssuerMutableFields]

    kind: Literal["Issuer"] = "Issuer"
    spec: Spec

    def absolute_path(self) -> str:
        return "/".join((self.spec["secrets_engine_ref"], self.spec["name"]))

    def upstream_issuer_absolute_path(self) -> str:
        assert "chaining" in self.spec, "Chaining field is required"
        return self.spec["chaining"]["upstream_issuer_ref"]


class IssuerGetDTO(issuer.IssuerReadDTO): ...
