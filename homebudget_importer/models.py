from homebudget_importer import db
import datetime


class OperationHistorySrc(db.Model):
    __tablename__ = 'OPERATION_HISTORY_SRC'

    operation_id = db.Column(db.Integer, primary_key=True)
    operation_dt = db.Column(db.String(200), nullable=False)
    operation_tp = db.Column(db.String(200), nullable=False)
    currency_dt = db.Column(db.String(200), nullable=False)
    amount_val = db.Column(db.String(200), nullable=False)
    currency_nm = db.Column(db.String(200), nullable=False)
    account_bal = db.Column(db.String(200), nullable=False)
    operation_desc = db.Column(db.String(300), nullable=False)
    tmp_1 = db.Column(db.String(200), nullable=True)
    tmp_2 = db.Column(db.String(200), nullable=True)
    tmp_3 = db.Column(db.String(200), nullable=True)
    tmp_4 = db.Column(db.String(200), nullable=True)
    tmp_5 = db.Column(db.String(200), nullable=True)
    tmp_6 = db.Column(db.String(200), nullable=True)


class ImportLog(db.Model):
    __tablename__ = 'IMPORT_LOG'

    file_id = db.Column(db.Integer, primary_key=True)
    file_nm = db.Column(db.String(40), nullable=True, unique=True)
    operation_dt = db.Column(db.Date, nullable=False)
    download_dtm = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow)
    download_msg = db.Column(db.String(100), nullable=True)
    import_flg = db.Column(db.String(1), nullable=True, default=None)
    etl_flg = db.Column(db.String(1), nullable=True, default=None)

    def __repr__(self):
        return f"ImportLog('{self.file_nm}', '{self.operation_dt}', '{self.download_dtm}', '{self.download_msg}', '{self.import_flg}', '{self.etl_flg}')"
