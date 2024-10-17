import json
from typing import Any, Dict

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from storage.base_storage import BaseStorage
from storage.models import AssistantModel, Base, ThreadModel


class MySQLStorage(BaseStorage):
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)
        self._create_tables()

    def _execute_query(self, query, params=None):
        cursor = self.conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            self.conn.commit()
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: '{e}' occurred")
        finally:
            cursor.close()

    def _create_tables(self):
        """Create tables if they don't exist."""
        Base.metadata.create_all(self.engine)

    def save_assistant(self, assistant_id: str, data: Dict[str, Any]) -> None:
        session = self.Session()
        assistant = AssistantModel(
            id=assistant_id,
            name=data["name"],
            model=data["model"],
            data=json.dumps(data),
        )
        session.merge(assistant)  # Use merge to update or insert
        session.commit()
        session.close()

    def load_assistant(self, assistant_id: str) -> Dict[str, Any]:
        session = self.Session()
        assistant = session.query(AssistantModel).filter_by(id=assistant_id).first()
        session.close()
        if assistant:
            return json.loads(assistant.data)
        return {}

    def save_thread(self, thread_id: str, data: Dict[str, Any]) -> None:
        session = self.Session()
        thread = ThreadModel(
            id=thread_id, assistant_id=data["assistant_id"], data=json.dumps(data)
        )
        session.merge(thread)  # Use merge to update or insert
        session.commit()
        session.close()

    def load_thread(self, thread_id: str) -> Dict[str, Any]:
        session = self.Session()
        thread = session.query(ThreadModel).filter_by(id=thread_id).first()
        session.close()
        if thread:
            return json.loads(thread.data)
        return {}
