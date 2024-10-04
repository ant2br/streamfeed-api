# from pydantic import BaseModel
# from typing import List, Optional

# # DTO para criar um novo grupo de permissões
# class PermissionGroupCreateDTO(BaseModel):
#     name: str
#     permissions: Optional[List[int]] = None  # Lista de IDs de permissões a serem associadas ao grupo
#     is_active: Optional[bool] = True  # Campo padrão para ativo

#     class Config:
#         from_attributes = True  # Permite compatibilidade com ORM

# # DTO para atualizar um grupo de permissões existente
# class PermissionGroupUpdateDTO(BaseModel):
#     name: Optional[str] = None
#     permissions: Optional[List[int]] = None  # Lista de IDs de permissões a serem associadas ao grupo
#     is_active: Optional[bool] = None  # Permite que seja omitido ao atualizar

#     class Config:
#         from_attributes = True  # Permite compatibilidade com ORM

# # DTO para resposta de grupo de permissões
# class PermissionGroupResponseDTO(BaseModel):
#     id: int  # ID do grupo de permissões
#     name: str  # Nome do grupo de permissões
#     permissions: List[int]  # Lista de IDs de permissões associadas ao grupo

#     class Config:
#         from_attributes = True  # Permite compatibilidade com ORM
