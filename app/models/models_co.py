from sqlalchemy import text
from sqlalchemy.dialects.mysql import VARCHAR, TINYINT, INTEGER, CHAR, TEXT
from sqlalchemy.sql.schema import Column, PrimaryKeyConstraint, ForeignKeyConstraint

from app.db import Base


class CoLanguages(Base):
    __tablename__ = "co_languages"
    id = Column(INTEGER(display_width=11), autoincrement=True, nullable=False)
    code = Column(VARCHAR(charset='utf8', collation='utf8_general_ci', length=5), nullable=False)
    language = Column(VARCHAR(charset='utf8', collation='utf8_general_ci', length=30), nullable=False)
    available = Column(TINYINT(display_width=1), server_default=text("1"), nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint("code"),
    )

class CoCountries(Base):
    __tablename__ = "co_countries"
    iso = Column(CHAR(length=2), nullable=False)
    name = Column(VARCHAR(length=80), nullable=False)
    iso3 = Column(CHAR(length=3), nullable=True)
    available = Column(TINYINT(display_width=1), server_default=text('0'), nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint("iso"),
    )

class CoAddresses(Base):
    __tablename__ = "co_addresses"
    id = Column(INTEGER(display_width=11), autoincrement=True, nullable=False)
    name = Column(VARCHAR(length=255), nullable=True)
    streetAndNumber = Column(VARCHAR(length=255), nullable=True)
    city = Column(VARCHAR(length=255), nullable=False)
    country = Column(VARCHAR(length=255), nullable=False)
    zip = Column(VARCHAR(length=255), nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(["country"], ["co_countries.iso"],
            name="co_addresses_country_fk",onupdate="CASCADE", ondelete="CASCADE"),
    )