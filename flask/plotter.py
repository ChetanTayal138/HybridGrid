import matplotlib.pyplot as plt 
import numpy as np 
from database_ops import *
import io 





def obtain_all_documents(db):
    UPRVUNL_docs = get_documents(db, "UPRVUNL")
    UPJVNL_docs = get_documents(db, "UPJVNL")
    IPP_docs = get_documents(db, "IPP")
    final_docs = UPRVUNL_docs + UPJVNL_docs + IPP_docs 
    return final_docs




def obtain_plots(generator):

    db = get_database("Uttar-Pradesh")
    alld = obtain_all_documents(db)
    for i in alld:
        if(i['gen_name'] == generator):
            dc = np.array(i['DC'])
            sched = np.array(i['Schedule'])
            actual = np.array(i['Actual'])
            oi_ui = np.array(i['OI_UI'])


            fig = plt.figure(figsize=(7,7))

            plt.subplot(221)
            plt.ylabel("MW")
            plt.title("DC")
            plt.plot(dc)
            plt.subplot(222)
            plt.title("SCHEDULE")
            plt.plot(sched)
            plt.subplot(223)
            plt.ylabel("MW")
            plt.title("ACTUAL")
            plt.plot(actual)
            plt.subplot(224)
            plt.title("(+)OI_UI(-)")
            plt.plot(oi_ui)
            plt.show()
            bytes_image = io.BytesIO()
            plt.savefig(bytes_image, format = "png")
            bytes_image.seek(0)
            plt.close()
            return bytes_image










if __name__ == "__main__":
    obtain_plots("VPRG")
