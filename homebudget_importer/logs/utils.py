from homebudget_importer.models import ImportLog


def get_transferred_file_list():
    file_list = []
    rslt = ImportLog.query.filter_by(import_flg='T').all()
    for row in rslt:
        file_list.append(row.file_nm)

    file_list = str(file_list)
    file_list = file_list.replace('[', '').replace(']', '').replace(',)', '').replace('(', '')

    return file_list


def update_transferred(v_file_nm, v_status):
    log = ImportLog.query.filter_by(file_nm=v_file_nm).first()
    log.import_flg = v_status
    return True
