from automapper import mapper
from fastapi import (
    APIRouter, 
    Depends,
    status
)
from app.models.base_response_model import ApiResponse
from app.models.organization_models import (
    OrganizationRequest, 
    OrganizationResponse
)
from app.models.user_models import (
    UserCreationRequest, 
    UserCreationResponse
)
from app.services.company_creation_service import CompanyCreationService
from app.services.user_service import UserService

router = APIRouter(prefix="/admin", tags=["ORGANIZATION MANAGEMENT SERVICE"])


@router.post(
    "/org/create",
    response_model=ApiResponse[OrganizationResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_organization(
    request: OrganizationRequest, 
    service: CompanyCreationService = Depends(CompanyCreationService)
) -> ApiResponse[OrganizationResponse]:
    return ApiResponse(data=service.create_company(request.name))


@router.get(
    "/org/{id}", 
    response_model=ApiResponse[OrganizationResponse], 
    status_code=status.HTTP_200_OK
)
async def get_organization(
    id: int, 
    service:CompanyCreationService = Depends(CompanyCreationService)
) -> ApiResponse[OrganizationResponse]:
    return ApiResponse(data=service.get_company(id))


@router.post(
    "/user", 
    response_model=UserCreationResponse, 
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    request: UserCreationRequest, 
    service: UserService = Depends(UserService)
) -> UserCreationResponse:
    user = service.create_user(
        request.name,
        request.username,
        request.password,
        request.role,
        request.contact,
    )
    return mapper.to(UserCreationResponse).map(user)
