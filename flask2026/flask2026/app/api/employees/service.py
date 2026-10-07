from app.api.employees.repository import EmployeeRepository


class EmployeeService:

    @staticmethod
    def get_employee(employee_id: int):
        employee = EmployeeRepository.get_by_id(employee_id)

        if employee is None:
            return None

        return {
            "id": employee.id,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "full_name": employee.full_name,
            "email": employee.email,
            "position": employee.position,
            "salary": float(employee.salary) if employee.salary else None,
            "hire_date": employee.hire_date.isoformat(),
            "vacation_days": employee.vacation_days,
            "department": {
                "id": employee.department.id,
                "name": employee.department.name,
            },
        }
