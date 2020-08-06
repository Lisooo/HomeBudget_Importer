from homebudget_importer.models import OperationHistorySrc
from homebudget_importer import db


def set_operation_id():
    if db.session.query(db.func.max(OperationHistorySrc.operation_id)).scalar() is None:
        v_operation_id = 1
    else:
        v_operation_id = db.session.query(
            db.func.max(OperationHistorySrc.operation_id)).scalar() + 1
    return v_operation_id
