from sqlalchemy import text
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATETIME, CHAR, TINYINT
from sqlalchemy.sql.schema import Column, PrimaryKeyConstraint, ForeignKeyConstraint

from app.db import Base


class AUsers(Base):
    __tablename__ = "a_users"
    id = Column(INTEGER(display_width=11), autoincrement=True, nullable=False)
    uuid = Column(CHAR(length=36), server_default=text("(UUID())"), unique=True, nullable=False)
    uniqueId = Column(VARCHAR(length=8), unique=True, nullable=False)
    fullName = Column(VARCHAR(length=255), nullable=True)
    email = Column(VARCHAR(length=255), nullable=True)
    password = Column(VARCHAR(length=60), nullable=True)
    addressId = Column(INTEGER(display_width=11), nullable=True)
    interfaceLanguageCode = Column(VARCHAR(charset='utf8', collation='utf8_general_ci', length=5), server_default=text("'fr'"), nullable=False)
    createdAt = Column(DATETIME, nullable=True)
    updatedAt = Column(DATETIME, nullable=True)
    deletedAt = Column(DATETIME, nullable=True)
    updatedPasswordAt = Column(DATETIME, nullable=True)
    phone = Column(VARCHAR(length=20), nullable=True)
    isActive = Column(TINYINT(display_width=1), server_default=text("1"), nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(["addressId"], ["co_addresses.id"],
            name="a_users_addressId_fk",onupdate="CASCADE", ondelete="CASCADE"),
        ForeignKeyConstraint(["interfaceLanguageCode"], ["co_languages.code"],
            name="a_users_interfaceLanguageCode_fk",onupdate="CASCADE", ondelete="CASCADE"),
    )


class AUsersRoles(Base):
    __tablename__ = "a_users_roles"
    id = Column(INTEGER(display_width=11), autoincrement=True, nullable=False)
    userId = Column(INTEGER(display_width=11), nullable=False)
    roleId = Column(INTEGER(display_width=11), nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(["userId"], ["a_users.id"],
            name="a_users_roles_userId_fk",onupdate="CASCADE", ondelete="CASCADE"),
        ForeignKeyConstraint(["roleId"], ["config_roles.id"],
            name="a_users_roles_roleId_fk",onupdate="CASCADE", ondelete="CASCADE"),
    )

class AUsersTags(Base):
    __tablename__ = "a_users_tags"
    id = Column(INTEGER(display_width=11), autoincrement=True, nullable=False)
    userId = Column(INTEGER(display_width=11), nullable=False)
    tagId = Column(INTEGER(display_width=11), nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(["userId"], ["a_users.id"],
            name="a_users_tags_userId_fk",onupdate="CASCADE", ondelete="CASCADE"),
        ForeignKeyConstraint(["tagId"], ["config_tags.id"],
            name="a_users_tags_tagId_fk",onupdate="CASCADE", ondelete="CASCADE"),
    )