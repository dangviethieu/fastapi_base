from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, FLOAT
from sqlalchemy.sql.schema import Column, PrimaryKeyConstraint, ForeignKeyConstraint

from app.db import Base


class ConfigRoles(Base):
    __tablename__ = "config_roles"
    id = Column(INTEGER(display_width=11), nullable=False)
    label = Column(VARCHAR(length=50), nullable=True)
    description = Column(VARCHAR(length=255), nullable=True)
    __table_args__ = (
        PrimaryKeyConstraint("id"),
    )

class ConfigPermission(Base):
    __tablename__ = "config_permissions"
    id = Column(INTEGER(display_width=11), nullable=False)
    label = Column(VARCHAR(length=50), nullable=True)
    __table_args__ = (
        PrimaryKeyConstraint("id"),
    )

class ConfigRoleHasPermissions(Base):
    __tablename__ = "config_role_has_permissions"
    id = Column(INTEGER(display_width=11), autoincrement=True, nullable=False)
    roleId = Column(INTEGER(display_width=11), nullable=False)
    permissionId = Column(INTEGER(display_width=11), nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(["roleId"], ["config_roles.id"],
            name="config_role_has_permissions_roleId_fk",onupdate="CASCADE", ondelete="CASCADE"),
        ForeignKeyConstraint(["permissionId"], ["config_permissions.id"],
            name="config_role_has_permissions_permissionId_fk",onupdate="CASCADE", ondelete="CASCADE"),
    )

class ConfigTagTypes(Base):
    __tablename__ = "config_tag_types"
    id = Column(INTEGER(display_width=11), nullable=False)
    label = Column(VARCHAR(length=50), nullable=True)
    __table_args__ = (
        PrimaryKeyConstraint("id"),
    )

class ConfigTags(Base):
    __tablename__ = "config_tags"
    id = Column(INTEGER(display_width=11), autoincrement=True, nullable=False)
    label = Column(VARCHAR(length=50), nullable=True)
    tagTypeId = Column(INTEGER(display_width=11), nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(["tagTypeId"], ["config_tag_types.id"],
            name="config_tags_tagTypeId_fk",onupdate="CASCADE", ondelete="CASCADE"),
    )