# models/models.py
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("full_name", String),
    Column("phone", String),
    Column("job", String),
    Column("created_at", DateTime)
)
