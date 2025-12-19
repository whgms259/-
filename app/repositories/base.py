from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")

class BaseRepository(ABC, Generic[ModelType, CreateSchemaType]):
    @abstractmethod
    def get(self, obj_id: int) -> Optional[ModelType]:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[ModelType]:
        raise NotImplementedError

    @abstractmethod
    def create(self, obj_in: CreateSchemaType) -> ModelType:
        raise NotImplementedError
