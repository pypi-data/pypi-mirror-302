import abc
import inspect
from io import StringIO

import rich.repr
import unify
from pydantic import BaseModel, create_model
from pydantic._internal._model_construction import ModelMetaclass
from rich.console import Console

RICH_CONSOLE = Console(file=StringIO())


class _Formatted(abc.ABC):

    @staticmethod
    def _indent_text(to_print):
        chunks = to_print.split("\n")
        num_chunks = len(chunks)
        detected = False
        prev_chunk = chunks[0]
        for i, chunk in enumerate(chunks[:-1]):
            if i in (0, num_chunks - 2) or chunk.startswith(" "):
                detected = False
                continue
            if not detected:
                prev_chunk = chunks[i - 1]
            detected = True
            leading_spaces = len(prev_chunk) - len(prev_chunk.lstrip())
            chunks[i] = " " * (leading_spaces + 11) + chunk
        return "\n".join(chunks)

    def _repr(self, to_print):
        # ToDO find more elegant way to do this
        global RICH_CONSOLE
        with RICH_CONSOLE.capture() as capture:
            RICH_CONSOLE.print(to_print)
        return self._indent_text(capture.get())

    def __repr__(self) -> str:
        return self._repr(self)

    def __str__(self) -> str:
        return self._repr(self)

    def _prune_dict(self, val, prune_policy):

        def keep(v, k=None, prune_pol=None):
            if v is None:
                return False
            if not prune_pol:
                return True
            if (
                isinstance(prune_pol, dict)
                and "keep" not in prune_pol
                and "skip" not in prune_pol
            ):
                return True
            if "keep" in prune_pol:
                if k not in prune_pol["keep"]:
                    return False
                prune_val = prune_pol["keep"][k]
                return prune_val is None or prune_val == v
            elif "skip" in prune_pol:
                if k not in prune_pol["skip"]:
                    return True
                prune_val = prune_pol["skip"][k]
                return prune_val is not None and prune_val != v
            else:
                raise Exception(
                    "expected prune_pol to contain either 'keep' or 'skip',"
                    "but neither were present: {}.".format(prune_pol),
                )

        if (
            not isinstance(val, dict)
            and not isinstance(val, list)
            and not isinstance(val, tuple)
        ):
            return val
        elif isinstance(val, dict):
            return {
                k: self._prune_dict(
                    v,
                    (
                        prune_policy[k]
                        if (isinstance(prune_policy, dict) and k in prune_policy)
                        else None
                    ),
                )
                for k, v in val.items()
                if keep(v, k, prune_policy)
            }
        elif isinstance(val, list):
            return [
                self._prune_dict(
                    v,
                    (
                        prune_policy[i]
                        if (isinstance(prune_policy, list) and i < len(prune_policy))
                        else None
                    ),
                )
                for i, v in enumerate(val)
                if keep(v, prune_pol=prune_policy)
            ]
        else:
            return (
                self._prune_dict(
                    v,
                    (
                        prune_policy[i]
                        if (isinstance(prune_policy, tuple) and i < len(prune_policy))
                        else None
                    ),
                )
                for i, v in enumerate(val)
                if keep(v, prune_pol=prune_policy)
            )

    def _prune_pydantic(self, val, dct):
        if isinstance(dct, BaseModel):
            dct = dct.model_dump()
        if not inspect.isclass(val) or not issubclass(val, BaseModel):
            return type(dct)
        fields = val.model_fields
        if isinstance(val.model_extra, dict):
            fields = {**fields, **val.model_extra}
        config = {
            k: (self._prune_pydantic(fields[k].annotation, v), None)
            for k, v in dct.items()
            if k in fields
        }
        if isinstance(val, ModelMetaclass):
            name = val.__qualname__
        else:
            name = val.__class__.__name__
        return create_model(name, **config)

    @staticmethod
    def _annotation(v):
        if hasattr(v, "annotation"):
            return v.annotation
        return type(v)

    @staticmethod
    def _default(v):
        if hasattr(v, "default"):
            return v.default
        return None

    def _create_pydantic_model(self, item, dct):
        if isinstance(dct, BaseModel):
            dct = dct.model_dump()
        fields = item.model_fields
        if item.model_extra is not None:
            fields = {**fields, **item.model_extra}
        config = {
            k: (self._prune_pydantic(self._annotation(fields[k]), v), None)
            for k, v in dct.items()
        }
        model = create_model(
            item.__class__.__name__,
            **config,
            __cls_kwargs__={"arbitrary_types_allowed": True},
        )
        return model(**dct)

    def _prune(self, item):
        prune_policy = unify.key_repr(item)
        dct = self._prune_dict(item.model_dump(), prune_policy)
        return self._create_pydantic_model(item, dct)


@rich.repr.auto
class _FormattedBaseModel(_Formatted, BaseModel):

    def __repr__(self) -> str:
        return self._repr(self._prune(self) if unify.repr_mode() == "concise" else self)

    def __str__(self) -> str:
        return self._repr(self._prune(self) if unify.repr_mode() == "concise" else self)

    def __rich_repr__(self):
        rep = self._prune(self) if unify.repr_mode() == "concise" else self
        for k in rep.model_fields:
            yield k, rep.__dict__[k]
        if rep.model_extra is None:
            return
        for k, v in rep.model_extra.items():
            yield k, v

    def full_repr(self):
        """
        Return the full un-pruned representation, regardless of the mode currently set.
        """
        with unify.ReprMode("verbose"):
            return self._repr(self)
