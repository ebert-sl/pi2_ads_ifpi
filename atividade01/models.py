from sqlmodel import Field, SQLModel
from typing import Optional

class Montadora(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    pais: str
    ano_fundacao: int

class ModeloVeiculo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    montadora_id: int = Field(foreign_key="montadora.id")
    valor_referencia: float
    motorizacao: float
    turbo: bool
    automatico: bool

class Veiculo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    modelo_id: int = Field(foreign_key="modeloveiculo.id")
    cor: str
    ano_fabricacao: int
    ano_modelo: int
    valor: float
    placa: str
    vendido: bool
