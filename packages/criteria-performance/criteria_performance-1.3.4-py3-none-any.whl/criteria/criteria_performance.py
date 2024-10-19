import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors

class PerformanceCriteria:
    def __init__(self, data:None, val=100):
        self.__val = val
        self.__data = pd.read_csv(data) if type(data).__name__=="str" else data
        self.__classe, self.__score = self.__data[self.__data.columns[0]], self.__data[self.__data.columns[1]]
        self.__ppv, self.__pnv = self.ppv_pnv()
        self.__seuil = self.generate_seuil()
        self.__fp, self.__tp = self.fp_tp()
        self.__Tfp, self.__Ttp = self.Tfp_Ttp()
        self.__fn = self.calculate_fn()
        self.__fnr, self.__fpr = self.fnr_fpr()
        self.__rappel, self.__precision = self.coordonne()
        

    def ppv_pnv(self):
        ppv = np.array([v for k,v in zip(self.__classe,self.__score) if k==1])
        pnv = np.array([v for k,v in zip(self.__classe,self.__score) if k==-1])
        return ppv,pnv

    def get_ppv(self):
        return self.__ppv

    def get_pnv(self):
        return self.__pnv

    def generate_seuil(self):
        return np.linspace(self.__score.min() - 0.01, self.__score.max() + 0.01, self.__val)

    def get_seuil(self):
        return self.__seuil

    def fp_tp(self):
        fp = [(i, len(self.__pnv[self.__pnv > i])) for i in self.__seuil]
        tp = [(i, len(self.__ppv[self.__ppv > i])) for i in self.__seuil]
        return fp, tp

    def get_fp(self):
        return self.__fp

    def get_tp(self):
        return self.__tp

    def Tfp_Ttp(self):
        tfp = [k[1] / len(self.__pnv) for k in self.__fp]
        ttp = [k[1] / len(self.__ppv) for k in self.__tp]
        return tfp, ttp

    def get_tfp(self):
        return self.__Tfp

    def get_ttp(self):
        return self.__Ttp

    def calculate_fn(self):
        return [(k[0], len(self.__ppv) - k[1]) for k in self.__tp]

    def get_fn(self):
        return self.__fn

    def coordonne(self):
        rp = [(k[0], k[1] / (k[1] + m[1])) for k, m in zip(self.__tp, self.__fn)]
        pp = [(k[0], k[1] / (k[1] + m[1])) for k, m in zip(self.__tp, self.__fp) if (k[1] + m[1]) > 0]
        coordonne = [(k[1], m[1]) for k, m in zip(pp, rp)]
        return [i[0] for i in coordonne], [i[1] for i in coordonne]

    def get_rappel(self):
        return self.__rappel

    def get_precision(self):
        return self.__precision

    def fnr_fpr(self):
        return [k[1] / len(self.__ppv) for k in self.__fn], [k[1] / len(self.__pnv) for k in self.__fp]

    def get_fnr(self):
        return self.__fnr

    def get_fpr(self):
        return self.__fpr

    def dispOldDET(self, title="", xl="Seuil", point=False, c1="b", c2="orange", cp="red", grid=False,save=False,name="courbe_hold-DET"):
        plt.plot(self.__seuil, self.__fnr, label="FNR", c=c1)
        plt.plot(self.__seuil, self.__fpr, label="FPR", c=c2)
        if point:
            x_intersect, y_intersect = self.getEER()
            plt.scatter(x_intersect, y_intersect, color=cp, zorder=5, label=f"EER({x_intersect:.2f}, {y_intersect:.2f})")
        plt.xlabel(xl)
        plt.title(title)
        plt.legend()
        if grid:
            plt.grid()
        if save:
            plt.savefig(name + ".png")

    def dispDET(self, label="DET", xl="FNR", yl="FPR", c="orange", title="Courbe DET", grid=False,save=False,name="courbe_DET"):
        plt.plot(self.__fnr, self.__fpr, label=label, c=c)
        plt.xlabel(xl)
        plt.ylabel(yl)
        plt.title(title)
        plt.legend()
        if grid:
            plt.grid()
        if save:
            plt.savefig(name + ".png")

    def dispPR(self, label="P-R", xl="Rappel", yl="Précision", c="brown", title="Courbe Rappel-Précision", grid=False,save=False,name="courbe_P-R"):
        plt.plot(self.__rappel, self.__precision, label=label, c=c)
        plt.xlabel(xl)
        plt.ylabel(yl)
        plt.title(title)
        plt.legend()
        if grid:
            plt.grid()
        if save:
            plt.savefig(name + ".png")

    def dispROC(self, label="ROC", xl="TFP", yl="TTP", c="b", title="Courbe ROC", grid=False, save=False,name="courbe_ROC"):
        plt.plot(self.__Tfp, self.__Ttp, label=label, c=c)
        plt.title(title)
        plt.xlabel(xl)
        plt.ylabel(yl)
        plt.legend()
        if grid:
            plt.grid()
        if save:
            plt.savefig(name + ".png")
    
    def descriptionEER(self):
        x_intersect, y_intersect = self.getEER()
        
        if y_intersect is None or x_intersect is None:
            description = "Erreur:Veuillez fournir des valeurs valides pour le seuil et l'EER."
        else:
            eer_value = y_intersect * 100  # Convertir l'EER en pourcentage
            threshold_value = x_intersect  # Seuil

            description = (
                f"Résumé des Performances\n\n"
                f"Seuil:{threshold_value:.2f}\n"
                f"EER:{eer_value:.2f}%\n\n"
            )
            description+="Interprétation selon le Contexte d'Application:\n\n"
            # Biométrie
            description += "-Biométrie: "
            if eer_value < 2:
                description += "EER très bas, excellente performance.\n\n"
            elif 2 <= eer_value <= 5:
                description += "EER modéré, acceptable, mais améliorable.\n\n"
            else:
                description += "EER élevé, performances insuffisantes.\n\n"

            # Reconnaissance Vocale
            description += "-Reconnaissance Vocale : "
            if eer_value < 5:
                description += "EER bas, bon équilibre entre précision et convivialité.\n\n"
            elif 5 <= eer_value <= 10:
                description += "EER modéré, pourrait être amélioré.\n\n"
            else:
                description += "EER élevé, performances insuffisantes.\n\n"

            # Détection de Fraude
            description += "-Détection de Fraude: "
            if eer_value < 3:
                description += "EER bas, très bonne gestion des erreurs.\n\n"
            elif 3 <= eer_value <= 7:
                description += "EER modéré, risques modérés mais à surveiller.\n\n"
            else:
                description += "EER élevé, risque élevé d'erreurs, performances insuffisantes.\n\n"
            savoir="Le point de coordonnées(seuil,EER) est appelé le point d'égalité des erreurs ou Equal Error Rate (EER) en anglais.Il correspond au seuil où le taux de faux positifs (FPR) est égal au taux de faux négatifs (FNR) dans une courbe DET (Detection Error Tradeoff). "
            description+=savoir
        return description
        
    def dispdescriptionEER(self):
        # Afficher la description sur le graphique
        plt.text(0, 0.4, self.descriptionEER(), fontsize=10, va='center', wrap=True, family='Times New Roman', color='black')
        plt.axis('off')  # Cacher les axes pour le panneau de description



    def displaygraphe(self, taille=(15, 8), save=False, name="criteres_performance",point=False,cp="red"):
        plt.figure(figsize=taille)
        plt.subplot(2, 3, 1)
        self.dispROC()
        plt.subplot(2, 3, 2)
        self.dispPR()
        plt.subplot(2, 3, 3)
        self.dispDET()
        plt.subplot(2, 3, 4)
        self.dispOldDET()
        if point:
            x_intersect, y_intersect = self.getEER()
            plt.scatter(x_intersect, y_intersect, color=cp, zorder=5, label=f"EER({x_intersect:.2f}, {y_intersect:.2f})")
        plt.legend()
        plt.subplot(2,3,5)
        self.dispdescriptionEER()
        if save:
            plt.savefig(name + ".png")

    def show(self):
        # Ajouter les curseurs interactifs avec des annotations
        cursor = mplcursors.cursor(hover=True)
        # Connexion de la fonction on_add à l'événement "add"
        cursor.connect("add", self.on_add)
        # Afficher le graphe
        plt.show()

    def on_add(self, sel):
        # Définir le texte de l'annotation
        sel.annotation.set_text(f'x: {sel.target[0]:.2f}, y: {sel.target[1]:.2f}')
        sel.annotation.get_bbox_patch().set(fc="lightyellow", alpha=0.6)

    def getEER(self):
        diff = np.array(self.__fnr) - np.array(self.__fpr)
        sign_changes = np.where(np.diff(np.sign(diff)))[0]
        if len(sign_changes) > 0:
            for index in sign_changes:
                x_intersect = np.interp(0, diff[index:index + 2], self.__seuil[index:index + 2])
                y_intersect = np.interp(x_intersect, self.__seuil, self.__fnr)
                return x_intersect, y_intersect
        return None,None
        
    def __str__(self) -> str:
        info = (
            f"Informations sur les Criteres de Performances\n"
            f"------------------------------------------------------------------------------------------\n"
            f"Total valeur seuil: {self.__val}\n\n"
            f"Valeurs Seuil: {self.__seuil.tolist()}\n\n"
            f"Classes: {self.__classe.tolist()}\n\n"
            f"Scores: {self.__score.tolist()}\n"
            f"------------------------------------------------------------------------------------------\n"
            f"PPV (Positive Predictive Value): {self.__ppv.tolist()}\n\n"
            f"PNV (Negative Predictive Value): {self.__pnv.tolist()}\n"
            f"------------------------------------------------------------------------------------------\n"
            f"Faux Positifs (FP): {self.__fp}\n\n"
            f"Vrais Positifs (TP): {self.__tp}\n\n"
            f"Total Faux Positifs (TFP): {self.__Tfp}\n\n"
            f"Total Vrais Positifs (TTP): {self.__Ttp}\n"
            f"------------------------------------------------------------------------------------------\n"
            f"Faux Négatifs (FN): {self.__fn}\n\n"
            f"False Negative Rate (FNR): {self.__fnr}\n\n"
            f"False Positive Rate (FPR): {self.__fpr}\n"
            f"------------------------------------------------------------------------------------------\n"
            f"Rappel: {self.__rappel}\n\n"
            f"Précision: {self.__precision}\n"
            f"------------------------------------------------------------------------------------------\n"
            f"Point egale Erreur:{self.getEER()}"
        )
        return info 
    

def asarray2D(arrayA,arrayB):
    try:
        A ,B = arrayA.reshape((arrayA.shape[0],1)),arrayB.reshape((arrayB.shape[0],1)) 
        return np.hstack((A,B))  
    except ValueError as e:
        print(f"Erreur : {e}")
        return None

def asDataFrame(array):
        try:
            y = array.shape[1]
            if y == 2:
                df = pd.DataFrame(array, columns=["classe", "score"])
                return df
            else:
                raise ValueError("Le tableau doit avoir exactement 2 colonnes")
        except ValueError as e:
            print(f"Erreur : {e}")
            return None
        
def Opentxt(url):
    data = np.loadtxt(url)
    return asDataFrame(np.vstack((np.array([[k,v] for k,v in zip(data[:,0],data[:,1]) if k==1 ]),np.array([[k,v] for k,v in zip(data[:,0],data[:,1]) if k!=1 ]))))
