from typing import Optional, Literal
from pydantic import BaseModel, conint, PositiveInt

N_SEMAINES = 52
MAX_ASTREINTES = 13


# todo test sum(site.n_rotation) >= min_aga + min_respi


class Parametres(BaseModel):
    max_astreintes: conint(ge=0, le=N_SEMAINES) = MAX_ASTREINTES
    repartition: Literal['site', 'effectifs'] = 'site'
    seed: Optional[int] = None
    min_aga: Optional[PositiveInt] = 1
    min_respi: Optional[PositiveInt] = 1


class Site(BaseModel):
    nom: str
    n_rotation: PositiveInt
    effectifs_aga: PositiveInt
    effectifs_respi: PositiveInt


class Technicien(BaseModel):
    nom: str
    specialite: Literal['aga', 'respi']
    site: str


class Rotation(BaseModel):
    semaine: conint(ge=0, le=N_SEMAINES - 1)
    technicien: Technicien
