import pandas as pd

companies = [
    {"name": "AFMA","TICKER":"AFM", "ISIN": "MA0000012296"},
    {"name": "AFRIC INDUSTRIES SA","TICKER":"AFI", "ISIN": "MA0000012114"},
    {"name": "AFRIQUIA GAZ","TICKER":"GAZ", "ISIN": "MA0000010951"},
    {"name": "AGMA","TICKER":"AGM", "ISIN": "MA0000010944"},
    {"name": "AKDITAL","TICKER":"AKT", "ISIN": "MA0000012585"},
    {"name": "ALLIANCES","TICKER":"ADI", "ISIN": "MA0000011819"},
    {"name": "ALUMINIUM DU MAROC","TICKER":"ALM", "ISIN": "MA0000010936"},
    {"name": "ARADEI CAPITAL","TICKER":"ARD", "ISIN": "MA0000012460"},
    {"name": "ATLANTASANAD","TICKER":"ATL", "ISIN": "MA0000011710"},
    {"name": "ATTIJARIWAFA BANK","TICKER":"ATW", "ISIN": "MA0000012445"},
    {"name": "AUTO HALL","TICKER":"ATH", "ISIN": "MA0000010969"},
    {"name": "AUTO NEJMA","TICKER":"NEJ", "ISIN": "MA0000011009"},
    {"name": "BALIMA","TICKER":"BAL", "ISIN": "MA0000011991"},
    {"name": "BANK OF AFRICA","TICKER":"BOA", "ISIN": "MA0000012437"},
    {"name": "BANQUE CENTRALE POPULAIRE","TICKER":"BCP", "ISIN": "MA0000011884"},
    {"name": "BMCI","TICKER":"BCI", "ISIN": "MA0000010811"},
    {"name": "CARTIER SAADA","TICKER":"CRS", "ISIN": "MA0000011868"},
    {"name": "CREDIT DU MAROC","TICKER":"CDM", "ISIN": "MA0000010381"},
    {"name": "CFG BANK","TICKER":"CFG", "ISIN": "MA0000012627"},
    {"name": "CIH","TICKER":"CIH", "ISIN": "MA0000011454"},
    {"name": "CIMENTS DU MAROC","TICKER":"CMA", "ISIN": "MA0000010506"},
    {"name": "COLORADO","TICKER":"COL", "ISIN": "MA0000011934"},
    {"name": "COSUMAR","TICKER":"CSR", "ISIN": "MA0000012247"},
    {"name": "CTM","TICKER":"CTM", "ISIN": "MA0000010340"},
    {"name": "DARI COUSPATE","TICKER":"DRI", "ISIN": "MA0000011421"},
    {"name": "DELATTRE LEVIVIER MAROC","TICKER":"DLM", "ISIN": "MA0000012551"},
    {"name": "DELTA HOLDING","TICKER":"DHO", "ISIN": "MA0000011850"},
    {"name": "DIAC SALAF","TICKER":"DIS", "ISIN": "MA0000010639"},
    {"name": "DISTY TECHNOLOGIES","TICKER":"DYT", "ISIN": "MA0000012536"},
    {"name": "DISWAY","TICKER":"DWY", "ISIN": "MA0000011637"},
    {"name": "DOUJA PROM ADDOHA","TICKER":"ADH", "ISIN": "MA0000011512"},
    {"name": "ENNAKL","TICKER":"NKL", "ISIN": "MA0000011942"},
    {"name": "EQDOM","TICKER":"EQD", "ISIN": "MA0000010357"},
    {"name": "FENIE BROSSETTE","TICKER":"FBR", "ISIN": "MA0000011587"},
    {"name": "HPS","TICKER":"HPS", "ISIN": "MA0000012619"},
    {"name": "IB MAROC.COM","TICKER":"IBC", "ISIN": "MA0000011132"},
    {"name": "IMMORENTE INVEST","TICKER":"IMO", "ISIN": "MA0000012387"},
    {"name": "INVOLYS","TICKER":"INV", "ISIN": "MA0000011579"},
    {"name": "ITISSALAT AL-MAGHRIB","TICKER":"IAM", "ISIN": "MA0000011488"},
    {"name": "JET CONTRACTORS","TICKER":"JET", "ISIN": "MA0000012080"},
    {"name": "LABEL VIE","TICKER":"LBV", "ISIN": "MA0000011801"},
    {"name": "LAFARGEHOLCIM MAROC","TICKER":"LHM", "ISIN": "MA0000012320"},
    {"name": "LESIEUR CRISTAL","TICKER":"LES", "ISIN": "MA0000012031"},
    {"name": "M2M Group","TICKER":"M2M", "ISIN": "MA0000011678"},
    {"name": "MAGHREB OXYGENE","TICKER":"MOX", "ISIN": "MA0000010985"},
    {"name": "MAGHREBAIL","TICKER":"MAB", "ISIN": "MA0000011215"},
    {"name": "MANAGEM","TICKER":"MNG", "ISIN": "MA0000011058"},
    {"name": "MAROC LEASING","TICKER":"MLE", "ISIN": "MA0000010035"},
    {"name": "MED PAPER","TICKER":"MDP", "ISIN": "MA0000012593"},
    {"name": "MICRODATA","TICKER":"MIC", "ISIN": "MA0000012163"},
    {"name": "MINIERE TOUISSIT","TICKER":"CMT", "ISIN": "MA0000011793"},
    {"name": "MUTANDIS SCA","TICKER":"MUT", "ISIN": "MA0000012395"},
    {"name": "OULMES","TICKER":"OUL", "ISIN": "MA0000010415"},
    {"name": "PROMOPHARM S.A.","TICKER":"PRO", "ISIN": "MA0000011660"},
    {"name": "REALISATIONS MECANIQUES","TICKER":"SRM", "ISIN": "MA0000011595"},
    {"name": "REBAB COMPANY","TICKER":"REB", "ISIN": "MA0000010993"},
    {"name": "RESIDENCES DAR SAADA","TICKER":"RDS", "ISIN": "MA0000012239"},
    {"name": "RISMA","TICKER":"RIS", "ISIN": "MA0000011462"},
    {"name": "S.M MONETIQUE","TICKER":"S2M", "ISIN": "MA0000012106"},
    {"name": "SALAFIN","TICKER":"SLF", "ISIN": "MA0000011744"},
    {"name": "SAMIR","TICKER":"SAM", "ISIN": "MA0000010803"},
    {"name": "SANLAM MAROC","TICKER":"SAH", "ISIN": "MA0000012007"},
    {"name": "SMI","TICKER":"SMI", "ISIN": "MA0000010068"},
    {"name": "SNEP","TICKER":"SNP", "ISIN": "MA0000011728"},
    {"name": "SOCIETE DES BOISSONS DU MAROC","TICKER":"SBM", "ISIN": "MA0000010365"},
    {"name": "SODEP-Marsa Maroc","TICKER":"MSA", "ISIN": "MA0000012312"},
    {"name": "SONASID","TICKER":"SID", "ISIN": "MA0000010019"},
    {"name": "STOKVIS NORD AFRIQUE","TICKER":"SNA", "ISIN": "MA0000012692"},
    {"name": "STROC INDUSTRIE","TICKER":"STR", "ISIN": "MA0000012056"},
    {"name": "TAQA MOROCCO","TICKER":"TQM", "ISIN": "MA0000012205"},
    {"name": "TGCC S.A","TICKER":"TGC", "ISIN": "MA0000012528"},
    {"name": "TOTALENERGIES MARKETING MAROC","TICKER":"TMA", "ISIN": "MA0000012262"},
    {"name": "UNIMER","TICKER":"UMR", "ISIN": "MA0000012023"},
    {"name": "WAFA ASSURANCE","TICKER":"WAA", "ISIN": "MA0000010928"},
    {"name": "ZELLIDJA S.A","TICKER":"ZDJ", "ISIN": "MA0000010571"},
]




urlbc = [
    {"TICKER":"AFM", "URBC": "AFM151215"},
    {"TICKER":"AFI", "URBC": "AFI050112"},
    {"TICKER":"GAZ", "URBC": "GAZ030599"},
    {"TICKER":"AGM", "URBC": "AGM091198"},
    {"TICKER":"AKT", "URBC": "AKT"},
    {"TICKER":"ADI", "URBC": "ADI170708"},
    {"TICKER":"ALM", "URBC": "ALM271098"},
    {"TICKER":"ARD", "URBC": "ARD"},
    {"TICKER":"ATL", "URBC": "ATL161007"},
    {"TICKER":"ATW", "URBC": "BCM130843"},
    {"TICKER":"ATH", "URBC": "ATH040941"},
    {"TICKER":"NEJ", "URBC": "NEJ030599"},
    {"TICKER":"BAL", "URBC": "BAL050746"},
    {"TICKER":"BOA", "URBC": "BCE260675"},
    {"TICKER":"BCP", "URBC": "BCP060704"},
    {"TICKER":"BCI", "URBC": "BCI280272"},
    {"TICKER":"CRS", "URBC": "CRS210606"},
    {"TICKER":"CDM", "URBC": "CDM030576"},
    {"TICKER":"CFG", "URBC": "CFG"},
    {"TICKER":"CIH", "URBC": "CIH230667"},
    {"TICKER":"CMA", "URBC": "CMA240669"},
    {"TICKER":"COL", "URBC": "COL271006"},
    {"TICKER":"CSR", "URBC": "CSR030685"},
    {"TICKER":"CTM", "URBC": "CTM030693"},
    {"TICKER":"DRI", "URBC": "DARI110705"},
    {"TICKER":"DLM", "URBC": "DLM290408"},
    {"TICKER":"DHO", "URBC": "DHO150508"},
    {"TICKER":"DIS", "URBC": "DIS010662"},
    {"TICKER":"DYT", "URBC": "DYT"},
    {"TICKER":"DWY", "URBC": "MAR280207"},
    {"TICKER":"ADH", "URBC": "ADH060706"},
    {"TICKER":"NKL", "URBC": "NAKL130710"},
    {"TICKER":"EQD", "URBC": "EQD210978"},
    {"TICKER":"FBR", "URBC": "FBR041206"},
    {"TICKER":"HPS", "URBC": "HPS271206"},
    {"TICKER":"IBC", "URBC": "IBMC100701"},
    {"TICKER":"IMO", "URBC": "IMO110518"},
    {"TICKER":"INV", "URBC": "INV141206"},
    {"TICKER":"IAM", "URBC": "IAM131204"},
    {"TICKER":"JET", "URBC": "JALU091211"},
    {"TICKER":"LBV", "URBC": "LBV020708"},
    {"TICKER":"LHM", "URBC": "LAC190297"},
    {"TICKER":"LES", "URBC": "LES071272"},
    {"TICKER":"M2M", "URBC": "M2M040707"},
    {"TICKER":"MOX", "URBC": "MOX170699"},
    {"TICKER":"MAB", "URBC": "MAB100797"},
    {"TICKER":"MNG", "URBC": "MNG110700"},
    {"TICKER":"MLE", "URBC": "MLE270297"},
    {"TICKER":"MDP", "URBC": "PDT280798"},
    {"TICKER":"MIC", "URBC": "MIC311207"},
    {"TICKER":"CMT", "URBC": "CMT040608"},
    {"TICKER":"MUT", "URBC": "MUT181218"},
    {"TICKER":"OUL", "URBC": "OUL130843"},
    {"TICKER":"PRO", "URBC": "PRO150607"},
    {"TICKER":"SRM", "URBC": "SRM121206"},
    {"TICKER":"REB", "URBC": "REB121184"},
    {"TICKER":"RDS", "URBC": "RDS250612"},
    {"TICKER":"RIS", "URBC": "RISMA"},
    {"TICKER":"S2M", "URBC": "S2M271211"},
    {"TICKER":"SLF", "URBC": "SLF171207"},
    {"TICKER":"SAM", "URBC": "SAM190396"},
    {"TICKER":"SAH", "URBC": "CNIA221110"},
    {"TICKER":"SMI", "URBC": "SMI180697"},
    {"TICKER":"SNP", "URBC": "SNP071107"},
    {"TICKER":"SBM", "URBC": "SBM130843"},
    {"TICKER":"MSA", "URBC": "MSA190716"},
    {"TICKER":"SID", "URBC": "SID020796"},
    {"TICKER":"SNA", "URBC": "SNA031207"},
    {"TICKER":"STR", "URBC": "STR300611"},
    {"TICKER":"TQM", "URBC": "JLC241213"},
    {"TICKER":"TGC", "URBC": "TGC"},
    {"TICKER":"TMA", "URBC": "TMA290515"},
    {"TICKER":"UMR", "URBC": "UMR290301"},
    {"TICKER":"WAA", "URBC": "WAA130798"},
    {"TICKER":"ZDJ", "URBC": "ZDJ200655"},
]


def get_company_info(company_name=None):
    
    if company_name is None:
        return [(company["name"], company["TICKER"], company["ISIN"]) for company in companies]
    
    
    for company in companies:
        if company["name"].lower() == company_name.lower():
            return company
    return "Société non trouvée."





def get_isin(company_name):
    for company in companies:
        if company["TICKER"].lower() == company_name.lower():
            return company["ISIN"]
    return None  



def get_URBC(company_name):
    for company in urlbc:
        if company["TICKER"].lower() == company_name.lower():
            return company["URBC"]
    return None  




