import os
import codecs
import pandas as pd
import numpy as np

from decimal import Decimal


def generate_txt_file(filename, user_session, basedir):
    # Seto mensagem de retorno False caso algum erro aconteça
    msg = None

    # Recebo o base dir para não incluir na base o diretório utils
    UPLOAD_FOLDER = os.path.join(basedir, "upload")

    try:
        file_xls = pd.ExcelFile(os.path.join(UPLOAD_FOLDER, filename))

        # Utilizo o numpy para trocar arquivos nan para '' string vazia
        sheet_0200 = file_xls.parse(0).replace(np.nan, "", regex=True)  # seta página 0200
        sheet_h005 = file_xls.parse(1).replace(np.nan, "", regex=True)  # seta página H005
        sheet_h010 = file_xls.parse(2).replace(np.nan, "", regex=True)  # seta página H010
        sheet_k100 = file_xls.parse(3).replace(np.nan, "", regex=True)  # seta página K100
        sheet_k200 = file_xls.parse(4).replace(np.nan, "", regex=True)  # seta página K200

        # Seto quantidade de linhas que irei percorrer
        count_0200 = len(sheet_0200["COD_ITEM"])
        count_H010 = len(sheet_h010["COD_ITEM"])
        count_K200 = len(sheet_k200["COD_ITEM"])

        # Crio arquivo txt no formato UTF-8 para o bloco H
        with codecs.open(os.path.join(UPLOAD_FOLDER, user_session + "-blocos_h_0200_k.txt"), 
            "w+", "utf-8") as file_blocos:
            file_blocos.write("*** REGISTRO - 0200 ***" + os.linesep + os.linesep)

            if count_0200 > 0:
                # 0200 - |REG|COD_ITEM|DESCR_ITEM|COD_BARRA|COD_ANT_ITEM|UNID_INV|TIPO_ITEM|COD_NCM|EX_IPI|COD_GEN|COD_LST|ALIQ_ICMS|CEST|
                for i in range(count_0200):
                    file_blocos.write(
                        "|0200|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|".format(
                            sheet_0200["COD_ITEM"][i] + "_n",
                            sheet_0200["DESCR_ITEM"][i],
                            sheet_0200["COD_BARRA"][i],
                            sheet_0200["COD_ANT_ITEM"][i],
                            sheet_0200["UNID_INV"][i],
                            "{:02d}".format(sheet_0200["TIPO_ITEM"][i]),
                            sheet_0200["COD_NCM"][i],
                            sheet_0200["EX_IPI"][i],
                            "{:02d}".format(sheet_0200["COD_GEN"][i]),
                            sheet_0200["COD_LST"][i],
                            sheet_0200["ALIQ_ICMS"][i],
                            sheet_0200["CEST"][i] != ""
                            and "{:07d}".format(int(sheet_0200["CEST"][i]))
                            or "",
                        )
                        + os.linesep
                    )

                # 0990 - Totalizador
                file_blocos.write("|0990|{}| - Somar este valor no arquivo original".format(count_0200) + os.linesep)

            file_blocos.write(os.linesep + "*** REGISTRO - H ***" + os.linesep + os.linesep)

            if count_H010 > 0:
                # H001/H005 - |REG|DT_INV|VL_INV|MOT_INV|
                file_blocos.write("|H001|0|" + os.linesep)
                file_blocos.write(
                    "|H005|{}|{}|{}|".format(
                        "{:08d}".format(int(sheet_h005["DT_INV"][0])),
                        "{:.2f}".format(sheet_h005["VL_INV"][0]).replace(".", ","),
                        "01",
                    )
                    + os.linesep
                )

                # H010 - |REG|COD_ITEM|UNID|QTD|VL_UNIT|VL_ITEM|IND_PROP|COD_PART|TXT_COMPL|COD_CTA|VL_ITEM_IR|
                for i in range(count_H010):
                    file_blocos.write(
                        "|H010|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|".format(
                            sheet_h010["COD_ITEM"][i] + "_n",
                            sheet_h010["UNID"][i],
                            "{:.3f}".format(sheet_h010["QTD"][i]).replace(".", ","),
                            "{:.6f}".format(sheet_h010["VL_UNIT"][i]).replace(".", ","),
                            "{:.2f}".format(sheet_h010["VL_ITEM"][i]).replace(".", ","),
                            sheet_h010["IND_PROP"][i],
                            sheet_h010["COD_PART"][i],
                            sheet_h010["TXT_COMPL"][i],
                            sheet_h010["COD_CTA"][i],
                            "{:.2f}".format(sheet_h010["VL_ITEM_IR"][i]).replace(".", ","),
                        )
                        + os.linesep
                    )

                # Totalizador bloco H
                file_blocos.write("|H990|{}|".format(count_H010 + 3) + os.linesep)
            else:
                # Texto referente ao bloco vazio
                file_blocos.write("|H001|1|" + os.linesep)
                file_blocos.write("|H990|2|" + os.linesep)

            file_blocos.write(os.linesep + "*** REGISTRO - K ***" + os.linesep + os.linesep)

            if count_K200 > 0:
                # K001/K100 - |REG|DT_INI|DT_FIN|
                file_blocos.write("|K001|0|" + os.linesep)
                file_blocos.write(
                    "|K100|{}|{}|".format(
                        "{:08d}".format(int(sheet_k100["DT_INI"][0])),
                        "{:08d}".format(int(sheet_k100["DT_FIN"][0])),
                    )
                    + os.linesep
                )

                # K200 - |REG|DT_EST|COD_ITEM|QTD|IND_EST|COD_PART|
                for i in range(count_K200):
                    file_blocos.write(
                        "|K200|{}|{}|{}|{}|{}|".format(
                            "{:08d}".format(int(sheet_k200["DT_EST"][i])),
                            sheet_k200["COD_ITEM"][i] + "_n",
                            "{:.3f}".format(sheet_k200["QTD"][i]).replace(".", ","),
                            sheet_k200["IND_EST"][i],
                            sheet_k200["COD_PART"][i],
                        )
                        + os.linesep
                    )

                # Totalizador bloco k
                file_blocos.write("|K990|{}|".format(count_K200 + 3) + os.linesep)
            else:
                # Texto referente ao bloco vazio
                file_blocos.write("|K001|1|" + os.linesep)
                file_blocos.write("|K990|2|" + os.linesep)

            # Totalizadores
            file_blocos.write(os.linesep + "*** TOTALIZADORES ***" + os.linesep + os.linesep)
            file_blocos.write("|9900|0200|{}| - Somar este valor no arquivo original".format(count_0200) + os.linesep)
            file_blocos.write("|9900|H001|1|" + os.linesep)

            if count_H010 > 0:
                file_blocos.write("|9900|H005|1|" + os.linesep)
                file_blocos.write("|9900|H010|{}|".format(count_H010) + os.linesep)

            file_blocos.write("|9900|H990|1|" + os.linesep)
            file_blocos.write("|9900|K001|1|" + os.linesep)

            if count_K200 > 0:
                file_blocos.write("|9900|K100|1|" + os.linesep)
                file_blocos.write("|9900|K200|{}|".format(count_K200) + os.linesep)

            file_blocos.write("|9900|K990|1|" + os.linesep)
            file_blocos.write("|9999|0| - verifique em que linha se encontra este registro e substitua" + os.linesep)
        msg = True
    except Exception as e:
        msg = False

    # Removo arquivo xls para não consumir meu HD no heroku
    os.remove(os.path.join(UPLOAD_FOLDER, filename))

    return msg
