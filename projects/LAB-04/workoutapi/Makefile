run:
	@uvicorn workout_api.main:app --reload

create-migrations:
	@${PYTHONPATH}$(pwd) alembic revision --autogenerate -m $(d)

run-migrations:
	@${PYTHONPATH}$(pwd) alembic upgrade head
