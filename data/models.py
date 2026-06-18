from sqlalchemy import Integer, String, Float, Text, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from data.database import Base

class Medication(Base):
    __tablename__ = "medication"

    #id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom: Mapped[str] = mapped_column(String(255), primary_key=True)          # name_fr dans le JSON
    dci1: Mapped[str] = mapped_column(String(255))         # active_ingredient
    dosage: Mapped[str] = mapped_column(String(100))
    unite_dosage: Mapped[str] = mapped_column(String(50))
    forme: Mapped[str | None] = mapped_column(String(100), nullable=True)
    presentation: Mapped[str | None] = mapped_column(Text, nullable=True)
    ppv: Mapped[float | None] = mapped_column(Numeric, nullable=True)
    ph: Mapped[float | None] = mapped_column(Numeric, nullable=True)
    prix_br: Mapped[float | None] = mapped_column(Numeric, nullable=True)
    princeps_generique: Mapped[str | None] = mapped_column(String(10), nullable=True)
    taux_remboursement: Mapped[str | None] = mapped_column(String(50), nullable=True)
    nom_ar: Mapped[str | None] = mapped_column(String(255), nullable=True)
    search_name: Mapped[str | None] = mapped_column(String(255), nullable=True)