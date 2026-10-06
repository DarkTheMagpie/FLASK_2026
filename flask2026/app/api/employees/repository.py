from app.extensions import db
from app.models import Employee, VacationRequest


class EmployeeRepository:

    @staticmethod
    def get_by_id(employee_id: int) -> Employee | None:
        return Employee.query.get(employee_id)
