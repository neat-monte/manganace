from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.setup import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


# noinspection PyMethodMayBeStatic
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """ CRUD object with default methods to Create, Read, Update, Delete (CRUD) """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id_: Any) -> Optional[ModelType]:
        """ Retrieves an object by id """
        return db.query(self.model).filter(self.model.id == id_).first()

    def get_all(self, db: Session) -> List[ModelType]:
        """ Retrieves all objects """
        return db.query(self.model).all()

    def get_multi(self, db: Session, skip: int, limit: int) -> List[ModelType]:
        """ Retrieves a limited range of objects """
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        """ Creates a new object with provided schema """
        obj_in_data = jsonable_encoder(obj_in, by_alias=False)
        db_obj = self.model(**obj_in_data)
        return self._add_save(db, db_obj)

    def update(self, db: Session, id_: int, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        """ Updates properties of the existing object by provided id """
        db_obj = self.get(db, id_)
        return self.update(db, db_obj, obj_in)

    def update_obj(self, db: Session, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        """ Updates properties of the existing provided object """
        self._update_properties(db_obj, obj_in)
        return self._add_save(db, db_obj)

    def remove(self, db: Session, id_: int) -> ModelType:
        """ Deletes an object by the provided id """
        db_obj = db.query(self.model).get(id_)
        return self._delete_save(db, db_obj)

    def _update_properties(self, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> None:
        """ Updates properties of the provided object with the properties from the provided schema """
        db_obj_data = jsonable_encoder(db_obj, by_alias=False)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in db_obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

    def _add_save(self, db: Session, db_obj: ModelType):
        """ Adds the provided object to the database and saves it """
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def _delete_save(self, db: Session, db_obj: ModelType):
        """ Deletes the provided object from the database and saves it """
        db.delete(db_obj)
        db.commit()
        return db_obj
