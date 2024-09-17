# Multi-Tenant Application with Separate Databases for Each Tenant

This repository provides a starter template for implementing a multi-tenant application with separate databases for each tenant.

## Getting Started

To set up the project, follow these steps:

1. **Configure Environment Variables**
   - Copy the `.env.sample` file to `.env`:
     ```sh
     cp .env.sample .env
     ```
   - Update the variables in the `.env` file according to your project requirements.

2. **Update Docker Configuration for Production**
   - Modify `docker-compose.prod.yml` for production release.
   - Add required volumes if necessary.

3. **Run Docker for Production**
   - Run the production Docker Compose file to check if the project is ready for production:
     ```sh
     docker-compose -f docker-compose.prod.yml up
     ```

4. **Run Docker for Development**
   - During development, use `docker-compose.yml` which runs PostgreSQL and RabbitMQ only:
     ```sh
     docker-compose up
     ```

5. **Add New Entity**
   - Create a new entity in the `app/entity` folder.
   - Import the new entity in `__init__.py`.
   - Generate the create or update table script automatically:
     ```sh
     alembic revision --autogenerate -m "Added account table"
     ```

6. **Verify and Modify Generated Scripts**
   - Check and verify the auto-generated table scripts in the `migration` folder.
   - Modify the generated script if required.

7. **Generate Required Tables**
   - Run the following command to generate the required tables before starting the application in development:
     ```sh
     alembic upgrade head
     ```

8. **Use VSCode Debugger**
   - You can use the VSCode debugger to run and debug the project during development.

9. **Add Background Tasks**
   - Add your background task to the `app/background_tasks` folder.
   - Import the background task in the last line of `app/dramatiq.py`.

10. **Send Background Task Method**
    - Use the background task method in the example background URL from the routes.

11. **Add New Routes**
    - Add any new route to the `routes` folder.
    - Import the new route in the route entries section.

