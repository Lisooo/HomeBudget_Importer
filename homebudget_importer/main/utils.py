from homebudget_importer import db
from homebudget_importer.models import OperationHistorySrc
from homebudget_importer.operations import utils as oprtn
from homebudget_importer.logs import utils as logs
from homebudget_importer.files import utils as csv
from homebudget_importer.config import Config


def unificate_rows_length(v_value_list):
    v_value_len = len(v_value_list)

    while v_value_len < 13:  # UNIFICATE COLUMNS LENGTH TO 13
        v_value_list.append('')
        v_value_len += 1

    return v_value_list


def replace_polish_letters(v_value_list):
    eol = len(v_value_list)
    j = 0

    while j < eol:
        if v_value_list[j] == '':
            v_value_list[j] = ''
        else:
            value_nm = str(v_value_list[j])
            value_nm = value_nm.replace("'", "")
            value_nm = value_nm.replace("ą", "a").replace("Ą", 'A')
            value_nm = value_nm.replace("ę", "e").replace("Ę", 'E')
            value_nm = value_nm.replace("ó", "o").replace("Ó", 'O')
            value_nm = value_nm.replace("ł", "l").replace("Ł", 'L')
            value_nm = value_nm.replace("ń", "n").replace("Ń", 'N')
            value_nm = value_nm.replace("ż", "z").replace("Ż", 'Z')
            value_nm = value_nm.replace("ź", "z").replace("Ź", 'Z')
            value_nm = value_nm.replace("ć", "c").replace("Ć", 'C')
            value_nm = value_nm.replace("ś", "s").replace("Ś", 'S')
            v_value_list[j] = value_nm.upper().encode('utf-8').decode('ascii', 'ignore')    # ENCODING
        j += 1

    return v_value_list


def import_file(v_dir, v_file_nm):
    print("")
    print("IMPORTING FILE: " + v_file_nm)
    v_lines_list = csv.extract_csv_rows_into_list(v_dir, v_file_nm) # GETTING ROWS FROM CSV FIL
    i = 0
    eof = len(v_lines_list)
    v_rec_cnt = eof - 1

    while i < eof:
        if i == 0:  # IGNORE COLUMNS
            pass
        else:
            v_value_list = v_lines_list[i]
            v_value_list = unificate_rows_length(v_value_list)
            v_value_list = replace_polish_letters(v_value_list)
            if v_value_list is None:
                pass
            else:
                v_operation_id = oprtn.set_operation_id()
                #   PRZYPISYWANIE / WERYFIKACJA ZMIENNYCH
                v_operation_dt = v_value_list[0]  # data operacji
                v_currency_dt = v_value_list[1]  # data transakcji/waluty
                v_operation_tp = v_value_list[2]  # typ transakcji
                v_amount_val = v_value_list[3]  # kwota transakcji
                v_currency_nm = v_value_list[4]  # waluta
                v_account_bal = v_value_list[5]  # bilans po transakcji
                v_operation_desc = v_value_list[6]  # szczegoly transakcji
                v_tmp_1 = v_value_list[7]  # opis transakcji
                v_tmp_2 = v_value_list[8]  # dodatkowe wartości
                v_tmp_3 = v_value_list[9]  # dodatkowe wartosci 2
                v_tmp_4 = v_value_list[10]  # dodatkowe wartosci 3
                v_tmp_5 = v_value_list[11]  # dodatkowe wartosci 4
                v_tmp_6 = v_value_list[12]  # dodatkowe wartosci

                #   INSERT DO TABELI
                v_OperationHistorySrc = OperationHistorySrc(operation_id=v_operation_id,
                                                              operation_dt=v_operation_dt,
                                                              operation_tp = v_operation_tp,
                                                              currency_dt=v_currency_dt,
                                                              amount_val=v_amount_val,
                                                              currency_nm=v_currency_nm,
                                                              account_bal=v_account_bal,
                                                              operation_desc=v_operation_desc,
                                                              tmp_1=v_tmp_1,
                                                              tmp_2=v_tmp_2,
                                                              tmp_3=v_tmp_3,
                                                              tmp_4=v_tmp_4,
                                                              tmp_5=v_tmp_5,
                                                              tmp_6=v_tmp_6)
                db.session.add(v_OperationHistorySrc)
        i += 1
    # UPDATE REC_CNT IN IMPORT_LOG
    # logs.update_rec_cnt(v_file_nm, v_rec_cnt)


def import_file_stg():
    print("*****************************************************")
    print("***** Wczytuje pliki do Operation History Table *****")
    print("*****************************************************")
    print("")

    v_file_list = csv.get_file_list(Config.CSV_FILES_DIR)
    v_transf_file_list = logs.get_transferred_file_list()

    for v_file_nm in v_file_list:
        if v_file_nm in v_transf_file_list:
            print("> " + v_file_nm + " - exists in transaction history table")
            pass
        else:
            import_file(Config.CSV_FILES_DIR, v_file_nm)  # insert data from file and set operation_id
            logs.update_transferred(v_file_nm, 'T')  # update imported_flg to 'T'
            db.session.commit()
            print("FINAL STATUS: " + v_file_nm + " - successfully imported into transaction history table")

    print("")
    print("*****************************************************")
    print("****************** KONIEC IMPORTU *******************")
    print("*****************************************************")


def importer():
    import_file_stg()

