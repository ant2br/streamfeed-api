from typing import List, Optional
from src.models.user import User
from src.dto.user import UserCreateDTO, UserUpdateDTO
from passlib.context import CryptContext

class UsersService:
    # Configuração do contexto de criptografia
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def hash_password(password: str) -> str:
        return UsersService.pwd_context.hash(password)

    async def listar_usuarios(self) -> List[User]:
        return await User.all()

    async def obter_usuario(self, id: int) -> Optional[User]:
        return await User.filter(id=id).first()
    
    
    async def alterar_senha(self, user_id: int, nova_senha: str) -> Optional[User]:

        user = await User.filter(id=user_id).first()
        if not user:
            return None
        
        # Criptografa a nova senha
        user.hashed_password = self.hash_password(nova_senha)
        
        # Salva o usuário com a nova senha no banco de dados
        await user.save()
        
        return user


    async def inserir_usuario(self, item: UserCreateDTO) -> User:
        hashed_password = self.hash_password(item.password)  # Criptografa a senha
        user = await User.create(
            username=item.username.lower(),
            email=item.email.lower(),
            full_name=item.full_name,
            hashed_password=hashed_password,  # Usa a senha criptografada
            is_active=True,
            is_superuser=False,
            tenant=1,
            permissionGroupId = item.permissionGroupId

        )
        return user

    async def atualizar_usuario(self, id: int, item: UserUpdateDTO) -> Optional[User]:
        user = await User.filter(id=id).first()
        if user:
            user.username = item.username.lower()
            user.email = item.email.lower()
            user.full_name = item.full_name
            user.is_active = item.is_active
            user.is_superuser = False
            user.permissionGroupId = item.permissionGroupId
            await user.save()
            return user
        return None

    async def deletar_usuario(self, id: int) -> bool:
        user = await User.filter(id=id).first()
        if user:
            await user.delete()
            return True
        return False
