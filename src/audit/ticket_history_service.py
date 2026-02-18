from queries.query_audit import INSERT_HISTORY_SQL


class TicketHistoryService:

    def log_event(
        self,
        cursor,
        id_ticket,
        event_type,
        actor_type,
        actor_id,
        old_value=None,
        new_value=None,
        note=None,
    ):
        data_history = (
            id_ticket,
            event_type,
            old_value,
            new_value,
            actor_type,
            actor_id,
            note,
        )
        cursor.execute(INSERT_HISTORY_SQL, data_history)
