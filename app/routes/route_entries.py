from . import (
    auth_route,
    super_admin_route,
    dramatiq_routes
    )

"""
add your protected route here
"""
PROTECTED_ROUTES = [
    super_admin_route.router
]


"""
add your public route here
"""
PUBLIC_ROUTES = [
    auth_route.router,
    dramatiq_routes.router
]
