import numpy as np
import xarray as xr

def variable_dict():
    """
    Returns the dictionary of variables and their units.

    Returns:
        _type_: _description_
    """    

    variables = {
        # climate
        "ddj": ["daily thermal time","°C.j"],
        "sdj":["sum of thermal time since beginning of emergence","°C.j"],

        # phenology
        "changePhase" : ["indicator of phase transition day","binary"],
        "numPhase":["number of phenological stage","arbitrary units"],
        "initPhase": ["indicator of performed phase transition","binary"],
        "phasePhotoper": ["photoperiodic phase indicator","binary"],
        "seuilTempPhaseSuivante":["sum of thermal time needed to reach the next phenological phase","°C.j"],
        "sommeDegresJourPhasePrec": ["sum of thermal time needed to reach the previous phenological phase","°C.j"],
        "seuilTempPhasePrec": ["",""],

        # carbon balance
        "assim": ["plant biomass assimilation","kg/ha"],
        "assimPot": ["plant potential biomass assimilation","kg/ha"],
        "bM": ["",""],
        "cM": ["",""],
        "rdt": ["grain yield","kg/ha"],
        "rdtPot": ["potential grain yield","kg/ha"],
        "reallocation": ["amount of assimilates reallocated to the yield (supply < demand)","kg/ha"],
        "respMaint": ["amount of assimilates consumed by maintainance respiration","kg/ha"],
        "manqueAssim": ["deficit in assimilates (demand - supply)","kg/ha"],


        # biomass
        "biomTotStadeFloraison": ["total biomass of the plant at the end of the flowering stage","kg/ha"],
        "biomTotStadeIp": ["total biomass at the panicle initiation stage","kg/ha"],
        "deltaBiomasseAerienne": ["",""],
        "deltaBiomasseFeuilles": ["",""],
        "biomasseAerienne":["","kg/ha"],
        "biomasseVegetative":["","kg/ha"],
        "biomasseTotale":["","kg/ha"],
        "biomasseTige":["","kg/ha"],
        "biomasseRacinaire":["","kg/ha"],
        "biomasseFeuille":["","kg/ha"],
        "deltaBiomasseTotale":["","kg/ha"],

        # evapotranspiration
        "kce": ["fraction of kc attributable to soil evaporation","decimal percentage"],
        "kcp": ["fraction of kc attributable to plant transpiration","decimal percentage"],
        "kcTot": ["",""],
        "tr": ["actual crop transpiration","mm/d"],
        "trPot": ["potential crop transpiration","mm/d"],
        "trSurf": ["",""],

        # water balance
        "consoRur": ["",""],
        "water_gathered_by_mulch" : ["water captured by the mulch in one day","mm"], #! replacing eauCaptee by water_gathered_by_mulch
        "eauDispo" : ["available water, sum of rainfall and total irrigation for the day","mm"],
        "eauTranspi": ["water available for transpiration from the surface reservoir","mm"],
        "correctedIrrigation" : ["corrected irrigation","mm/d"],
        "cstr" : ["drought stress coefficient", "arbitrary unit"],
        "dayVrac" : ["modulated daily root growth","mm/day"],
        "delta_root_tank_capacity": ["change in root system water reserve","mm"], #! renaming deltaRur with delta_root_tank_capacity
        "dr": ["",""],
        "etm": ["",""],
        "etp": ["",""],
        "etr": ["",""],
        "evap": ["",""],
        "evapPot": ["",""],
        "FEMcW": ["",""],
        "fesw": ["",""],
        "irrigTotDay" : ["total irrigation for the day","mm"],
        "vRac" : ["reference daily root growth","mm/day"],
        "ftsw": ["fraction of transpirable surface water","decimal percentage"], 
        "lr" : ["daily water runoff","mm/d"],
        "pFact": ["FAO reference for critical FTSW value for transpiration response","none"],

        # water tanks
        "irrigation_tank_stock" : ["?","mm"], #! renaming stockIrr to irrigation_tank_stock
        "mulch_water_stock" : ["water stored in crop residues (mulch)","mm"], #! renaming stockMc to mulch_water_stock
        "root_tank_stock": ["",""], #! renaming stRu to root_tank_stock
        "total_tank_capacity": ["",""], #! renaming stRuMax to total_tank_capacity
        "stRur": ["",""],
        "root_tank_capacity_previous_season": ["",""], #! renaming stRurMaxPrec to root_tank_capacity_previous_season
        "stRurPrec": ["",""],
        "stRurSurf": ["",""],
        "surface_tank_stock": ["",""], #! renaming stRuSurf to surface_tank_stock
        "stRuSurfPrec": ["",""],
        "delta_total_tank_stock": ["",""], #! renaming stRuVar to delta_total_tank_stock
        "irrigation_tank_capacity" : ["irrigation tank capacity","mm"], #! renaming ruIrr to irrigation_tank_capacity
        "ruRac": ["Water column that can potentially be strored in soil volume explored by root system","mm"],
        


        "conv": ["",""],
        "KAssim": ["",""],


        "dayBiomLeaf": ["daily growth of leaf biomass","kg/ha/d"],
        "dRdtPot": ["daily potential demand from yield","kg/ha/d"],
        "FeuilleUp": ["",""],
        
        
        "kRespMaint": ["",""],
        "LitFeuille": ["",""],
        
        
        "nbJourCompte": ["",""],
        "nbjStress": ["",""],
        "NbUBT": ["",""],
        
        "rapDensite": ["",""],
        
        "sla": ["",""],

        "stockRac": ["",""],
        "sumPP": ["",""],
        "TigeUp": ["",""],
        "UBTCulture": ["",""],
        "lai":["leaf area index","m2/m2"],
    }

    return variables





def initialize_simulation(data, grid_width, grid_height, duration, paramVariete, paramITK, date_start):
    """
    This function initializes variables related to crop growth in the data
    xarray dataset. As the rain is the first variable to be initialized in the
    data xarray dataset, its dimensions are used to initialize the other
    variables.
    
    This code has been adapted from the original InitiationCulture procedure,
    from the MilBilanCarbone.pas code of the SARRA model. 

    Args:
        data (_type_): _description_
        grid_width (_type_): _description_
        grid_height (_type_): _description_
        duration (_type_): _description_
        paramVariete (_type_): _description_

    Returns:
        _type_: _description_
    """

    ### variables to be initialized with values from parameters 

    # from paramVariete : maximum daily thermal time (°C.j) -> #? unused ?
    #// data["sommeDegresJourMaximale"] = (data["rain"].dims, np.full(
    #//     (duration, grid_width, grid_height),
    #//     (paramVariete["SDJLevee"] + paramVariete["SDJBVP"] + paramVariete["SDJRPR"] + paramVariete["SDJMatu1"] + paramVariete["SDJMatu2"])
    #// ))
    #// data["sommeDegresJourMaximale"].attrs = {"units":"°C.j", "long_name":"Maximum thermal time"}

    # from paramITK : sowing date
    data["sowing_date"] = (data["rain"].dims, np.full((duration, grid_width, grid_height), (paramITK["DateSemis"] - date_start).days))
    
    # from paramITK : automatic irrigation indicator
    data["irrigAuto"] = (data["rain"].dims, np.full((duration, grid_width, grid_height), paramITK["irrigAuto"]))
    data["irrigAuto"].attrs = {"units":"binary", "long_name":"automatic irrigation indicator"}

    ####### variables qui viennent de initplotMc
    # Initial biomass of crop residues (mulch) (kg/ha)
    # Biomasse initiale des résidus de culture (mulch) (kg/ha)
    #   BiomMc := BiomIniMc;
    data["biomMc"] = (data["rain"].dims, np.full((duration, grid_width, grid_height), paramITK["biomIniMc"]))
    data["biomMc"].attrs = {"units": "kg/ha", "long_name": "Initial biomass of crop residues (mulch)"}


    # ?
    #   StSurf := StockIniSurf;
    # data["stSurf"] = np.full((grid_width, grid_height, duration), paramTypeSol["stockIniSurf"])


    # ?
    #   Ltr := 1;
    data["ltr"] = (data["rain"].dims, np.full((duration, grid_width, grid_height), 1.0))


    # Initial biomass of stem residues as litter (kg/ha)
    # Biomasse initiale des résidus de tiges sous forme de litière (kg/ha)
    #   LitTiges := BiomIniMc;
    data["LitTige"] = (data["rain"].dims, np.full((duration, grid_width, grid_height), paramITK["biomIniMc"]))
    data["LitTige"].attrs = {"units": "kg/ha", "long_name": "Initial biomass of stem residues as litter"}

    ####### fin variables qui viennent de initplotMc

    ####### variables eau depuis InitPlotMc

    # Initializes variables related to crop residues boimass (mulch) in the data
    # xarray dataset. This code has been adapted from the original InitPlotMc
    # procedure, Bileau.pas code. Comments with tab indentation are from the
    # original code. As the rain is the first variable to be initialized in the
    # data xarray dataset, its dimensions are used to initialize the other
    # variables.

    # Soil maximum water storage capacity (mm)
    # Capacité maximale de la RU (mm)
    #   StRurMax := Ru * ProfRacIni / 1000;
    #! renaming stRurMax with root_tank_capacity
    #// data["stRurMax"] = data["ru"] * paramITK["profRacIni"] / 1000
    data["root_tank_capacity"] = (data["rain"].dims, np.repeat(np.array(data["ru"] * paramITK["profRacIni"] / 1000)[np.newaxis,:,:], duration, axis=0))
    #// data["stRurMax"].attrs = {"units": "mm", "long_name": "Soil maximum water storage capacity"}
    data["root_tank_capacity"].attrs = {"units": "mm", "long_name": "Soil maximum water storage capacity"}


    # Maximum water capacity of surface tank (mm)
    # Reserve utile de l'horizon de surface (mm)
    #   RuSurf := EpaisseurSurf / 1000 * Ru;
    #! renaming ruSurf with surface_tank_capacity
    #// data["ruSurf"] = data["epaisseurSurf"] / 1000 * data["ru"]
    data["surface_tank_capacity"] = data["epaisseurSurf"] / 1000 * data["ru"]
    #// data["ruSurf"].attrs = {"units": "mm", "long_name": "Maximum water capacity of surface tank"}
    data["surface_tank_capacity"].attrs = {"units": "mm", "long_name": "Maximum water capacity of surface tank"}
    

    # ?
    #   //    PfTranspi := EpaisseurSurf * HumPf;
    #   //    StTot := StockIniSurf - PfTranspi/2 + StockIniProf;
    #   StTot := StockIniSurf  + StockIniProf;
    # data["stTot"] = np.full((grid_width, grid_height, duration), (paramTypeSol["stockIniSurf"] + paramTypeSol["stockIniProf"]))
    #! modifié pour faire correspondre les résultats de simulation, à remettre en place pour un calcul correct dès que possible
    # data["stTot"] = np.full((grid_width, grid_height, duration), (paramTypeSol["stockIniProf"]))
    #! renaming stTot to total_tank_stock
    #// data["stTot"] = data["stockIniProf"]
    #//data["total_tank_stock"] = data["stockIniProf"]
    #! coorecting total_tank_stock initialization as it did not have the time dimensions that are required as stock evolves through time
    data["total_tank_stock"] = (data["rain"].dims, np.repeat(np.array(data["stockIniProf"])[np.newaxis,:,:], duration, axis=0))
    #// data["stTot"].attrs = {"units": "mm", "long_name": "?"}
    data["total_tank_stock"].attrs = {"units": "mm", "long_name": "?"}
    

    # Soil maximal depth (mm)
    # Profondeur maximale de sol (mm)
    #   ProfRU := EpaisseurSurf + EpaisseurProf;
    data["profRu"] = data["epaisseurProf"] + data["epaisseurSurf"]
    data["profRu"].attrs = {"units": "mm", "long_name": "Soil maximal depth"}


    # Maximum water capacity to humectation front (mm)
    # Quantité d'eau maximum jusqu'au front d'humectation (mm)
    #   // modif 10/06/2015  resilience stock d'eau
    #   // Front d'humectation egal a RuSurf trop de stress initial
    #   //    Hum := max(StTot, StRurMax);
    #   Hum := max(RuSurf, StRurMax);
    #   // Hum mis a profRuSurf
    #   Hum := max(StTot, Hum);
    data["hum"] = (data["rain"].dims, np.full((duration, grid_width, grid_height),
        np.maximum(
            np.maximum(
                #! renaming ruSurf with surface_tank_capacity
                #// data["ruSurf"],
                data["surface_tank_capacity"].expand_dims({"time":duration}),
                #! renaming stRurMax with root_tank_capacity
                #// data["stRurMax"],
                data["root_tank_capacity"],
            ),
            #! renaming stTot with total_tank_stock
            #// data["stTot"],
            data["total_tank_stock"],
        )
    ))
    data["hum"].attrs = {"units": "mm", "long_name": "Maximum water capacity to humectation front"}


    # Previous value for Maximum water capacity to humectation front (mm)
    #  HumPrec := Hum;
    data["humPrec"] = data["hum"]
    
    
    # ?
    #   StRurPrec := 0;


    # Previous value for stTot
    #   StRurMaxPrec := 0;
    #   //modif 10/06/2015 resilience stock d'eau
    #! renaming stTot with total_tank_stock
    #! renaminog stRuPrec with total_tank_stock_previous_value
    #// data["stRuPrec"] =  data["stTot"]
    data["total_tank_stock_previous_value"] =  data["total_tank_stock"]

    ####### fin variables eau depuis InitPlotMc


    # depuis meteo.pas
    kpar = 0.5
    data["par"] = kpar * data["rg"]
    data["par"].attrs = {"units":"MJ/m2", "long_name":"par"}

    # initialize variables with values at 0
    variables = variable_dict()

    for variable in variables :
        data[variable] = (data["rain"].dims, np.zeros(shape=(duration, grid_width, grid_height)))
        data[variable].attrs = {"units":variables[variable][1], "long_name":variables[variable][0]}

    return data


    


def estimate_kcp(j, data, paramVariete):
    """
    This function estimates the kcp coefficient.
    
    It performs computation of kcp based on the maximum crop coefficient kcMax,
    as well as plant cover ltr.

    This function is based on the EvolKcpKcIni procedure, from the biomasse.pas,
    exmodules 1 & 2.pas files of the original PASCAL code.

    Args:
        j (_type_): _description_
        data (_type_): _description_
        paramVariete (_type_): _description_

    Returns:
        _type_: _description_
    """
    # group 50

    data["kcp"][j:,:,:] = np.where(
        data["numPhase"][j,:,:] >= 1,
        np.maximum(0.3, paramVariete["kcMax"] * (1 - data["ltr"][j,:,:])),
        data["kcp"][j,:,:],
    )
    
    return data




def estimate_ltr(j, data, paramVariete):
    """
    This function estimates ltr, which is the fraction of radiation transmitted
    to the soil. In the water balance part, ltr is used as a proxy for plant
    covering of the soil, with 1 = no plant cover, 0 = full plant cover.

    ltr is computed as a exponential decay function of lai, with a decay
    coefficient kdf.

     This function has been adapted from the EvalLtr procedure, from the
     biomasse.pas, and exmodules 1 & 2.pas files of the original PASCAL code.

    Args:
        j (_type_): _description_
        data (_type_): _description_
        paramVariete (_type_): _description_

    Returns:
        _type_: _description_
    """
    # group 80   
    data["ltr"][j:,:,:] = np.exp(-paramVariete["kdf"] * data["lai"][j,:,:])
    
    return data




def estimate_KAssim(j, data, paramVariete):
    """
    This function evaluates the conversion factor KAssim, which is used to
    calculate conv (conversion of assimilates into biomass).

    KAssim value depends on the phase of the crop.

    This function has been adapted from the EvalConversion procedure, from the
    milbilancarbone copie, ecopalm2_2, exmodules 1 & 2, ***milbilancarbone***,
    risocas, riz.pas files of the original PASCAL code. 

    Args:
        j (_type_): _description_
        data (_type_): _description_
        paramVariete (_type_): _description_

    Returns:
        _type_: _description_
    """

    phase_equivalences = {
        2: 1,
        3: paramVariete['txAssimBVP'],
        4: paramVariete['txAssimBVP'],
        #! replacing sommeDegresJourPhasePrec with seuilTempPhasePrec
        #// 5: paramVariete["txAssimBVP"] + (data['sdj'][j,:,:] - data['sommeDegresJourPhasePrec'][j,:,:]) * (paramVariete['txAssimMatu1'] -  paramVariete['txAssimBVP']) / (data['seuilTempPhaseSuivante'][j,:,:] - data['sommeDegresJourPhasePrec'][j,:,:]),
        5: paramVariete["txAssimBVP"] + (data['sdj'][j,:,:] - data['seuilTempPhasePrec'][j,:,:]) * (paramVariete['txAssimMatu1'] -  paramVariete['txAssimBVP']) / (data['seuilTempPhaseSuivante'][j,:,:] - data['seuilTempPhasePrec'][j,:,:]),
        #// 6: paramVariete["txAssimMatu1"] + (data["sdj"][j,:,:] - data["sommeDegresJourPhasePrec"][j,:,:]) * (paramVariete["txAssimMatu2"] - paramVariete["txAssimMatu1"]) / (data["seuilTempPhaseSuivante"][j,:,:] - data["sommeDegresJourPhasePrec"][j,:,:]),
        6: paramVariete["txAssimMatu1"] + (data["sdj"][j,:,:] - data["seuilTempPhasePrec"][j,:,:]) * (paramVariete["txAssimMatu2"] - paramVariete["txAssimMatu1"]) / (data["seuilTempPhaseSuivante"][j,:,:] - data["seuilTempPhasePrec"][j,:,:]),
    }

    for phase in range(2,7):
        data["KAssim"][j:,:,:] = np.where(
            data["numPhase"][j,:,:] == phase,
            phase_equivalences[phase],
            data["KAssim"][j,:,:],
        )

    return data



def estimate_conv(j,data,paramVariete):
    """_summary_

    Args:
        j (_type_): _description_
        data (_type_): _description_
        paramVariete (_type_): _description_

    Returns:
        _type_: _description_
    """
    data["conv"][j:,:,:] = (data["KAssim"][j,:,:] * paramVariete["txConversion"])

    return data




def BiomDensOptSarraV4(j, data, paramITK):
    """
    si densité plus faible alors on considére qu'il faut augmenter les biomasses, LAI etc
    en regard de cette situation au niveau de chaque plante (car tout est rapporté é des kg/ha).
    Si elle est plus forte on ne change rien pour lors.
    Valeur fixe en ref au maés é déf en paramétre par variétésé rapDensite := Max(1, 70000/densite);

    """
    """
    if ~np.isnan(paramVariete["densOpti"]) :
        paramITK["rapDensite"] = np.maximum(1,paramVariete["densOpti"]/paramITK["densite"])
        data["rdt"][j,:,:] = data["rdt"][j,:,:] * paramITK["rapDensite"]
        data["biomasseRacinaire"][j,:,:] = data["biomasseRacinaire"][j,:,:] * paramITK["rapDensite"]
        data["biomasseTige"][j,:,:] = data["biomasseTige"][j,:,:] * paramITK["rapDensite"]
        data["biomasseFeuille"][j,:,:] = data["biomasseFeuille"][j,:,:] * paramITK["rapDensite"]
        data["biomasseAerienne"][j,:,:] = data["biomasseTige"][j,:,:] + data["biomasseFeuille"][j,:,:] + data["rdt"][j,:,:] 
        data["lai"][j,:,:]  = data["biomasseFeuille"][j,:,:] * data["sla"][j,:,:]
        data["biomasseTotale"][j,:,:] = data["biomasseAerienne"][j,:,:] + data["biomasseRacinaire"][j,:,:]

    return data
    """
    return data




def BiomDensOptSarV42(j, data, paramITK, paramVariete):
    """
    d'après bilancarbonsarra.pas

    { si densit� plus faible alors on consid�re qu'il faut augmenter les biomasses, LAI etc
    en regard de cette situation au niveau de chaque plante (car tout est rapport� � des kg/ha).
    Si elle est plus forte elle augmente de fa�on asymptotique.
    }

    """

    if ~np.isnan(paramVariete["densOpti"]) :

        # group 88
        data["rapDensite"] = paramVariete["densiteA"] + paramVariete["densiteP"] * np.exp(-(paramITK["densite"] / ( paramVariete["densOpti"]/- np.log((1 - paramVariete['densiteA'])/ paramVariete["densiteP"]))))
        
        # group 89
        data["rdt"][j:,:,:] = (data["rdt"][j,:,:] * data["rapDensite"])#[...,np.newaxis]

        # group 90
        data["rdtPot"][j:,:,:] = (data["rdtPot"][j,:,:] * data["rapDensite"])#[...,np.newaxis]

        # group 91
        data["biomasseRacinaire"][j:,:,:] = (data["biomasseRacinaire"][j,:,:] * data["rapDensite"])#[...,np.newaxis]
        # group 92
        data["biomasseTige"][j:,:,:] = (data["biomasseTige"][j,:,:] * data["rapDensite"])#[...,np.newaxis]
        # group 93
        data["biomasseFeuille"][j:,:,:] = (data["biomasseFeuille"][j,:,:] * data["rapDensite"])#[...,np.newaxis]

        # group 94
        data["biomasseAerienne"][j:,:,:] = (data["biomasseTige"][j,:,:] + data["biomasseFeuille"][j,:,:] + data["rdt"][j,:,:])#[...,np.newaxis]
        #data["biomasseAerienne"][j:,:,:] = data["biomasseAerienne"][j,:,:] * data["rapDensite"]
        
        # group 95
        data["lai"][j:,:,:]  = (data["biomasseFeuille"][j,:,:] * data["sla"][j,:,:])#[...,np.newaxis]
        #data["lai"][j:,:,:]  = data["lai"][j:,:,:]  * data["rapDensite"]

        # group 96
        data["biomasseTotale"][j:,:,:] = (data["biomasseAerienne"][j,:,:] + data["biomasseRacinaire"][j,:,:])#[...,np.newaxis]
        #data["biomasseTotale"][j:,:,:] = data["biomasseTotale"][j:,:,:] * data["rapDensite"]
    
    return data




def EvalAssimSarrahV4(j, data):
    """
    data["parIntercepte"][j,:,:] = 0.5 * (1 - data["ltr"][j,:,:]) * data["rg"][j,:,:]
    data["assimPot"][j:,:,:] = data["parIntercepte"][j,:,:] * data["conv"][j,:,:] * 10

    data["assim"][j,:,:] = np.where(
        data["trPot"][j,:,:] > 0,
        data["assimPot"][j,:,:] * data["tr"][j,:,:] / data["trPot"][j,:,:],
        0,
    )
    """
    return data
    

def update_assimPot(j, data, paramVariete, paramITK):
    """
    This function updates the assimPot value. It does so differentially
    depending on the value of NI, which is intensification level. Note from
    CB : correction of the conversion rate depending on the intensification
    level

    if the internsification level NI is defined, assimPot is updated 
    using txConversion. if not, it uses conv, which is updated in the
    estimate_conv function from variables KAssim and txConversion.
    
    Is it adapted from the EvalAssimSarraV42 procedure, of the
    bilancarbonsarra.pas file from the original Pascal code
    
    notes from CB reharding the EvalAssimSarraV42 procedure :
    
    Modif du 04/03/2021 : Prise en compte en plus de la densit� de semis de
    l'effet niveau d'intensification NI NI = 1 quand on est � l'optimum du
    niveau d'intensification. Dans le cas de situation contr�l� c'est la
    fertilit� qui est la clef principale en prenant en r�f�rence la qt� d'azote
    (�quivalent phosphore...) optimum Il peut aller � 0 ou �tre sup�rieur � 1 si
    situation sur optimum, ie un peu plus de rdt mais � cout trop �lev�... On
    �value un nouveau tx de conversion en fn du Ni au travers d'une double
    �quation : asympote x gaussienne invers�e Et d'un NI d�fini en fn du
    sc�nario de simulation ou des donn�es observ�es. NIYo = D�calage en Y de
    l'asymptote NIp  = pente de l'asymptote LGauss = Largeur de la Guaussienne
    AGauss = Amplitude de la Guaussienne

    Conversion qui est la valeur du taux de conversion en situation optimum n'a
    plus besoin d'�tre utilis� sinon dans la calibration des param�tres de cette
    �quation en absence de donn�es sur ces param�tres on ne met aucune valeur �
    NI CF fichier ex IndIntensite_txConv_eq.xls}
    
    Args:
        j (_type_): _description_
        data (_type_): _description_
        paramITK (_type_): _description_
    Returns:
        _type_: _description_
    """
    if ~np.isnan(paramITK["NI"]): 
        #? the following (stupidly long) line was found commented, need to check why and if this is correct
        # paramVariete["txConversion"] = paramVariete["NIYo"] + paramVariete["NIp"] * (1-np.exp(-paramVariete["NIp"] * paramITK["NI"])) - (np.exp(-0.5*((paramITK["NI"] - paramVariete["LGauss"])/paramVariete["AGauss"])* (paramITK["NI"]- paramVariete["LGauss"])/paramVariete["AGauss"]))/(paramVariete["AGauss"]*2.506628274631)
        data["assimPot"][j,:,:] = data["par"][j,:,:] * \
            (1-np.exp(-paramVariete["kdf"] * data["lai"][j,:,:])) * \
            paramVariete["txConversion"] * 10
    else :
        data["assimPot"][j,:,:] = data["par"][j,:,:] * \
            (1-np.exp(-paramVariete["kdf"] * data["lai"][j,:,:])) * \
            data["conv"][j,:,:] * 10
    
    return data



def update_assim(j, data):
    """
    This function updates assim. If trPot (potential transpiration from the
    plant, mm) is greater than 0, then assim equals assimPot, multiplied by the
    ratio of effective transpiration over potential transpiration.

    If potential transpiration is null, then assim is null as well.

    Is it adapted from the EvalAssimSarraV42 procedure, of the
    bilancarbonsarra.pas file from the original Pascal code

    Args:
        j (_type_): _description_
        data (_type_): _description_

    Returns:
        _type_: _description_
    """

    data["assim"][j,:,:] = np.where(
        data["trPot"][j,:,:] > 0,
        data["assimPot"][j,:,:] * data["tr"][j,:,:] / data["trPot"][j,:,:],
        0,
    )

    return data




def estimate_maintainance_respiration(j, data, paramVariete):
    """
    This function estimates the respMaint value (kg/ha/j in equivalent dry
    matter ?), which is the maintenance respiration of the plant.
    
    It is calculated by summing the maintenance respiration associated with
    total biomass on one side, and leaves biomass on the other side.

    For phases above 4 and null leaf biomass, respMaint is set to 0.

    #? We need to check if at this stage the total biomass already includes the
    leaves biomass, or if we need to add it to the total biomass.

    this function is adapted from the EvalRespMaintSarrahV3 procedure, of the
    bilancarbonsarra, exmodules 1 & 2.pas file from the original Pascal code

    Args:
        j (_type_): _description_
        data (_type_): _description_
        paramVariete (_type_): _description_

    Returns:
        _type_: _description_
    """
    coefficient_temp = 2**((data["tpMoy"][j,:,:] - paramVariete["tempMaint"]) / 10)
    resp_totale = paramVariete["kRespMaint"] * data["biomasseTotale"][j,:,:] * coefficient_temp
    resp_feuille = paramVariete["kRespMaint"] * data["biomasseFeuille"][j,:,:] * coefficient_temp

    data["respMaint"][j:,:,:] = np.where(
        (data["numPhase"][j,:,:] > 4) & (data["biomasseFeuille"][j,:,:]==0),
        0,
        resp_totale + resp_feuille,
    )

    return data




def update_total_biomass(j, data, paramVariete, paramITK):
    """
    This function updates the total biomass (biomasseTotale) of the plant.

    When passing from phase 1 to phase 2, total biomass is initialized.
    Initialization value is computed from crop density (plants/ha), txResGrain
    (grain yield per plant), and poidsSecGrain. Otherwise, total biomass is
    incremented with the difference between plant assimilation assim and
    maintainance respiration respMaint.

    This function is adapted from the EvolBiomTotSarrahV4 procedure, of the
    bilancarbonsarra.pas file from the original Pascal code.

    Args:
        j (_type_): _description_
        data (_type_): _description_
        paramVariete (_type_): _description_
        paramITK (_type_): _description_

    Returns:
        _type_: _description_
    """

    data["biomasseTotale"][j:,:,:] = np.where(
        (data["numPhase"][j,:,:]==2) & (data["changePhase"][j,:,:]==1),
        paramITK["densite"] *  np.maximum(1,paramVariete['densOpti']/paramITK['densite']) * paramVariete["txResGrain"] *  paramVariete["poidsSecGrain"] / 1000,
        data["biomasseTotale"][j,:,:]  + (data["assim"][j,:,:] - data["respMaint"][j,:,:]),
    )

    # we may want to drop this variable and use the raw computation instead
    data["deltaBiomasseTotale"][j:,:,:] = (data["assim"][j,:,:] - data["respMaint"][j,:,:])

    return data




def update_total_biomass_stade_ip(j, data):
    """
    This function updates the total biomass of the plant at the end of the
    vegetative phase (biomTotStadeIp).

    If the plant is in phase 4, and the phase has changed, then the total
    biomass is copied to the biomTotStadeIp variable.

    This function is adapted from the EvalRdtPotRespSarV42 procedure, of
    the bilancarbonsarra.pas file from the original Pascal code.

    Args:
        j (_type_): _description_
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    data["biomTotStadeIp"][j:,:,:] = np.where(
        (data["numPhase"][j,:,:] == 4) & (data["changePhase"][j,:,:] == 1),
        data["biomasseTotale"][j,:,:],
        data["biomTotStadeIp"][j,:,:],
    )

    return data


def update_total_biomass_at_flowering_stage(j, data):
    """
    This function updates the total biomass of the plant at the end of the
    flowering stage (biomTotStadeFloraison).

    If the plant is in phase 5, and the phase has changed, then the total
    biomass is copied to the biomTotStadeFloraison variable.

    This function is adapted from the EvalRdtPotRespSarV42 procedure, of
    the bilancarbonsarra.pas file from the original Pascal code.

    Args:
        j (_type_): _description_
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    data["biomTotStadeFloraison"][j:,:,:] = np.where(
        (data["numPhase"][j,:,:] == 5) & (data["changePhase"][j,:,:] == 1),
        data["biomasseTotale"][j,:,:],
        data["biomTotStadeFloraison"][j,:,:],
    )

    return data



def update_potential_yield(j, data, paramVariete):
    """
    This function updates the potential yield (rdtPot) of the plant.

    If the plant is in phase 5, and the phase has changed, then the potential
    yield is initialized from an affine function of the biomass delta between
    the end of the vegetative phase and the end of the flowering stage, added to
    a linear function of the total biomass at the end of the flowering stage.

    After this first update and at the same point in time, if potential yield is
    2 times higher than the biomass of the stem, potential yield is forced at a
    value of 2 times the biomass of the stem.

    This means we do not allow the potential yield above a certain value that
    depends on the stem biomass.

    This function is adapted from the EvalRdtPotRespSarV42 procedure, of the
    bilancarbonsarra.pas file from the original Pascal code.

    Args:
        j (_type_): _description_
        data (_type_): _description_
        paramVariete (_type_): _description_

    Returns:
        _type_: _description_
    """

    delta_biomass_flowering_ip = data["biomTotStadeFloraison"][j,:,:] - data["biomTotStadeIp"][j,:,:]

    data["rdtPot"][j:,:,:] = np.where(
        (data["numPhase"][j,:,:] == 5) & (data["changePhase"][j,:,:] == 1),
        (paramVariete["KRdtPotA"] * delta_biomass_flowering_ip + paramVariete["KRdtPotB"]) + paramVariete["KRdtBiom"] * data["biomTotStadeFloraison"][j,:,:],
        data["rdtPot"][j,:,:],
    )

    #! phaseDevVeg pas utilisé ? attention c'est un paramètre variétal et pas un jeu de donées
    data["rdtPot"][j:,:,:] = np.where(
        (data["numPhase"][j,:,:] == 5) & (data["changePhase"][j,:,:] == 1) & (data["rdtPot"][j,:,:] > data["biomasseTige"][j,:,:] * 2) & (paramVariete["phaseDevVeg"] < 6),
        data["biomasseTige"][j,:,:] * 2,
        data["rdtPot"][j,:,:],
    )
    
    return data

def update_potential_yield_delta(j, data, paramVariete):
    """
    This function updates the potential yield delta (dRdtPot) of the plant.

    If the plant is in phase 5, and the potential transpiration is not null,
    then the potential yield delta is computed as potential yield, times the ratio
    between actual sum of degree day over the sum of degree day at maturity, times the
    ratio between actual transpiration over potential transpiration. This value has a minimum bound of
    15% of the maintenance respiration.

    if the potential transpiration is not above 0, then the potential yield delta is null.
    
    For all other phases, potential yield delta is unchanged.

    This function is adapted from the EvalRdtPotRespSarV42 procedure, of the
    bilancarbonsarra.pas file from the original Pascal code.

    Args:
        j (_type_): _description_
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    data["dRdtPot"][j:,:,:] = np.where(
        (data["numPhase"][j,:,:] == 5),
        np.where(
            (data["trPot"][j,:,:] > 0),
            np.maximum(
                data["rdtPot"][j,:,:] * (data["ddj"][j,:,:] / paramVariete["SDJMatu1"]) * (data["tr"][j,:,:] / data["trPot"][j,:,:]),
                data["respMaint"][j,:,:] * 0.15,
            ),
            0,
        ),
        data["dRdtPot"][j,:,:],
    )

    return data

def update_aboveground_biomass(j, data, paramVariete):
    """
    This function updates the aboveground biomass (biomasseAerienne) of the
    plant.

    If the plant is in phase 2, 3 or 4, then the aboveground biomass is computed
    as the minimum between 90% of the total biomass and a linear function of the
    total biomass, with a slope and an intercept that depend on the variety.

    If the plant is in any other phase, then the aboveground biomass is
    incremented with the total biomass delta, updated in update_total_biomass().

    This function is based on the EvolBiomAeroSarrahV3 procedure, of the
    ***bilancarbonsarra***, exmodules 1 & 2.pas file from the original Pascal
    code.

    Args:
        j (_type_): _description_
        data (_type_): _description_
        paramVariete (_type_): _description_

    Returns:
        _type_: _description_
    """
    #// data["deltaBiomasseAerienne"][j:,:,:] = np.copy(data["biomasseAerienne"][j,:,:])

    data["biomasseAerienne"][j:,:,:] = np.where(
        (data["numPhase"][j,:,:] >= 2) & (data["numPhase"][j,:,:] <= 4),
        np.minimum(0.9, paramVariete["aeroTotPente"] * data["biomasseTotale"][j,:,:] + paramVariete["aeroTotBase"]) * data["biomasseTotale"][j,:,:],
        data["biomasseAerienne"][j,:,:] + data["deltaBiomasseTotale"][j,:,:],
    )

    #//data["deltaBiomasseAerienne"][j:,:,:] = (data["biomasseAerienne"][j,:,:] - data["deltaBiomasseAerienne"][j,:,:])#[...,np.newaxis]
    
    data["deltaBiomasseAerienne"][j:,:,:] = data["biomasseAerienne"][j,:,:] - data["biomasseAerienne"][j-1,:,:]

    return data





def estimate_reallocation(j, data, paramVariete):
    """
    This function estimates the amount of biomass that can be reallocated
    between stem and leaves.

    If the plant is in phase 5, this function first computes manqueAssim, which
    is the difference between the potential yield delta and the aboveground
    biomass delta bound in 0. This difference is also bound in 0. This
    manqueAssim represents the daily variation in biomass that remains after the
    plant has built its aboveground biomass.

    Then, reallocation is computed as the minimum between manqueAssim multiplied
    by the reallocation rate and the leaf biomass minus 30, bound in 0. 

    The value of 30 seems quite arbitrary. However this allows for reallocation
    to be null if the leaf biomass is below 30. If the leaf biomass is above 30,
    then reallocation is still bounded by biomasseFeuille - 30.

    If we're not at phase 5, then reallocation is null.

    This function is adapted from the EvalReallocationSarrahV3 procedure, of the
    bilancarbonsarra.pas and exmodules 1 & 2.pas files from the original Pascal
    code.

    Args:
        j (_type_): _description_
        data (_type_): _description_
        paramVariete (_type_): _description_

    Returns:
        _type_: _description_
    """

    condition = (data["numPhase"][j,:,:] == 5)

    data["manqueAssim"][j:,:,:] = np.where(
        condition,
        np.maximum(0, (data["dRdtPot"][j,:,:] -  np.maximum(0.0, data["deltaBiomasseAerienne"][j,:,:]))),
        0,
    )

    data["reallocation"][j:,:,:] = np.where(
        condition,
        np.minimum(
            data["manqueAssim"][j,:,:] * paramVariete["txRealloc"], 
            np.maximum(0.0, data["biomasseFeuille"][j,:,:] - 30),
        ),
        0,
    )

    return data





def update_root_biomass(j, data):
    """
    This function computes the root biomass (biomasseRacinaire) as the
    difference between the total biomass and the aboveground biomass.

    This function is based on the EvalBiomasseRacinaire procedure, of the
    milbilancarbone, exmodules 1 & 2, ***milbilancarbone***.pas file from the
    original Pascal code

    Args:
        j (_type_): _description_
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    data["biomasseRacinaire"][j,:,:] = data["biomasseTotale"][j,:,:] - data["biomasseAerienne"][j,:,:]

    return data





def update_leaf_biomass(j, data, paramVariete):
    """
    For phase above 1 and if the delta of aerial biomass is negative,
    meaning that the plant is losing aerial biomass, the leaf biomass is
    updated as the difference between the leaf biomass and the reallocation
    minus the delta of aerial biomass multiplied by the reallocation rate in
    leaves. This value is bound in 0.00000001.

    Otherwise, the leaf biomass is not updated.

    This function is adapted from the EvalFeuilleTigeSarrahV4 procedure, of
    the bilancarbonsarra.pas and exmodules 1 & 2.pas files from the original
    Pascal code.

    Args:
        j (_type_): _description_
        data (_type_): _description_

    Returns:
        _type_: _description_
    """

    data["biomasseFeuille"][j:,:,:] = np.where(
        (data["numPhase"][j,:,:] > 1) & (data["deltaBiomasseAerienne"][j,:,:] < 0),
        np.maximum(
            0.00000001,
            data["biomasseFeuille"][j,:,:] - (data["reallocation"][j,:,:] - data["deltaBiomasseAerienne"][j,:,:]) * paramVariete["pcReallocFeuille"]
        ),
        data["biomasseFeuille"][j,:,:],
    )

    return data



def update_stem_biomass(j, data, paramVariete):
    """
    For phase above 1 and if the delta of aerial biomass is negative,
    meaning that the plant is losing aerial biomass, the stem biomass is
    updated as the difference between the leaf biomass and the reallocation
    minus the delta of aerial biomass multiplied by (1-reallocation rate in
    leaves) (if it's not leaves, it's stems...). This value is bound in 0.00000001.

    Otherwise, the stem biomass is not updated.

    This function is adapted from the EvalFeuilleTigeSarrahV4 procedure, of
    the bilancarbonsarra.pas and exmodules 1 & 2.pas files from the original
    Pascal code.

    Args:
        j (_type_): _description_
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    # group 122
    data["biomasseTige"][j:,:,:] = np.where(
        (data["numPhase"][j,:,:] > 1) & (data["deltaBiomasseAerienne"][j,:,:] < 0),
        np.maximum(
            0.00000001,
            data["biomasseTige"][j,:,:] - (data["reallocation"][j,:,:] - data["deltaBiomasseAerienne"][j,:,:]) * (1 - paramVariete["pcReallocFeuille"]),
            ),
        data["biomasseTige"][j,:,:],
    )

    return data





def condition_positive_delta_biomass(j, data, paramVariete):


        condition = (data["numPhase"][j,:,:] > 1) & \
            (data["deltaBiomasseAerienne"][j,:,:] >= 0) & \
            ((data["numPhase"][j,:,:] <= 4) | (data["numPhase"][j,:,:] <= paramVariete["phaseDevVeg"]))
            # (data["numPhase"][j,:,:] <= 4)
        
        return condition


def update_bM_and_cM(j, data, paramVariete):
    """
    This function returns the updated values of bM and cM.
    bM and cM are updated if the delta of aerial biomass is positive, 
    meaning that the plant is gaining aerial biomass, and if the phase is
    above 1 and below 4 or the phase is below the vegetative phase.

    This function is adapted from the EvalFeuilleTigeSarrahV4 procedure, of
    the bilancarbonsarra.pas files from the original Pascal code.

    Args:
        j (_type_): _description_
        data (_type_): _description_

    Returns:
        _type_: _description_
    """

    data["bM"][j,:,:] = np.where(
        condition_positive_delta_biomass(j, data, paramVariete),
        paramVariete["feuilAeroBase"] - 0.1,
        data["bM"][j,:,:],
    )


    data["cM"][j,:,:] = np.where(
        condition_positive_delta_biomass(j, data, paramVariete),
        ((paramVariete["feuilAeroPente"] * 1000)/ data["bM"][j,:,:] + 0.78) / 0.75,
        data["cM"][j,:,:],
    )

    return data


def update_leaf_biomass_positive_delta_aboveground_biomass(j, data, paramVariete):
    """

    Args:
        j (_type_): _description_
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    data["biomasseFeuille"][j:,:,:] = np.where(
        condition_positive_delta_biomass(j, data, paramVariete),
        (0.1 + data["bM"][j,:,:] * data["cM"][j,:,:] ** ((data["biomasseAerienne"][j,:,:] - data["rdt"][j,:,:]) / 1000)) \
            * (data["biomasseAerienne"][j,:,:] - data["rdt"][j,:,:]),
        data["biomasseFeuille"][j,:,:],
    )

    return data



def update_stem_biomass_positive_delta_aboveground_biomass(j, data, paramVariete):
    """_summary_

    Args:
        j (_type_): _description_
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    data["biomasseTige"][j:,:,:] = np.where(
        condition_positive_delta_biomass(j, data, paramVariete),
        data["biomasseAerienne"][j,:,:] - data["biomasseFeuille"][j,:,:] - data["rdt"][j,:,:],
        data["biomasseTige"][j,:,:],
    )

    return data




def condition_positive_delta_aboveground_biomass_all_phases(j, data):
        #// condition = (data["numPhase"][j,:,:] > 1) & (data["deltaBiomasseAerienne"][j,:,:] >= 0)
    condition = (data["numPhase"][j,:,:] > 1) & (data["deltaBiomasseAerienne"][j,:,:] > 0)
    return condition




def update_leaf_biomass_all_phases(j, data, paramVariete):
    """_summary_

    Args:
        j (_type_): _description_
        data (_type_): _description_

    Returns:
        _type_: _description_
    """

    data["biomasseFeuille"][j:,:,:] = np.where(
        condition_positive_delta_aboveground_biomass_all_phases(j, data),
        data["biomasseFeuille"][j,:,:] - data["reallocation"][j,:,:] * paramVariete["pcReallocFeuille"],
        data["biomasseFeuille"][j,:,:],
    )
    return data




def update_stem_biomass_all_phases(j, data, paramVariete):
    """_summary_

    Args:
        j (_type_): _description_
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    data["biomasseTige"][j:,:,:] = np.where(
        condition_positive_delta_aboveground_biomass_all_phases(j, data),
        data["biomasseTige"][j,:,:] - (data["reallocation"][j,:,:] * (1- paramVariete["pcReallocFeuille"])),
        data["biomasseTige"][j,:,:],
    )

    return data


def update_aboveground_biomass_step_2(j, data):
    """_summary_

    Args:
        j (_type_): _description_
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    data["biomasseAerienne"][j:,:,:] = np.where(
        (data["numPhase"][j,:,:] > 1),
        data["biomasseTige"][j,:,:] + data["biomasseFeuille"][j,:,:] + data["rdt"][j,:,:],
        data["biomasseAerienne"][j,:,:],
    )
    return data

def EvalFeuilleTigeSarrahV4(j, data, paramVariete):
    """
    This function is a wrapper

    It is adapted from the EvalFeuilleTigeSarrahV4 procedure from the bilancarbonsarra.pas file
    of the original Pascal code.

    Args:
        j (_type_): _description_
        data (_type_): _description_
        paramVariete (_type_): _description_

    Returns:
        _type_: _description_
    """

    # data["deltaBiomasseFeuilles"][j:,:,:] = np.where(
    #     (data["numPhase"][j,:,:] > 1),
    #     data["biomasseFeuille"][j,:,:],
    #     data["deltaBiomasseFeuilles"][j,:,:],
    # )

    # if (data["numPhase"][j,:,:] > 1) & (data["deltaBiomasseAerienne"][j,:,:] < 0)
    data = update_leaf_biomass(j, data, paramVariete)
    data = update_stem_biomass(j, data, paramVariete)

    # if deltaBiomasseAerienne >= 0 and (numPhase <= 4 or numPhase <= phaseDevVeg)
    data = update_bM_and_cM(j, data, paramVariete)
    data = update_leaf_biomass_positive_delta_aboveground_biomass(j, data, paramVariete)
    data = update_stem_biomass_positive_delta_aboveground_biomass(j, data, paramVariete)

    # if deltaBiomasseAerienne > 0 and numPhase > 1
    data = update_leaf_biomass_all_phases(j, data, paramVariete)
    data = update_stem_biomass_all_phases(j, data, paramVariete)

    # condition = (data["numPhase"][j,:,:] > 1) 
    # data["deltaBiomasseFeuilles"][j:,:,:] = np.where(
    #     (data["numPhase"][j,:,:] > 1),
    #     data["biomasseFeuille"][j,:,:] - data["deltaBiomasseFeuilles"][j,:,:],
    #     data["deltaBiomasseFeuilles"][j,:,:],
    # )

    # simpler formulation for updating the deltaBiomasseFeuilles
    data["deltaBiomasseFeuilles"][j:,:,:] = data["biomasseFeuille"][j,:,:] - data["biomasseFeuille"][j-1,:,:]

    data = update_aboveground_biomass_step_2(j, data)

    return data




def update_vegetative_biomass(j, data):
    """_summary_

    This function is adapted from the EvalBiomasseVegetati procedure from the copie milbilancarbon, exmodules 1 & 2, ***milbilancarbone*** file
    of the original Pascal code.

    Args:
        j (_type_): _description_
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    data["biomasseVegetative"][j:,:,:] = (data["biomasseTige"][j,:,:] + data["biomasseFeuille"][j,:,:])
    return data




def update_sla(j, data, paramVariete):
    """
    This function estimates the specific leaf area (SLA) of the canopy.
    
    First, if the leaf biomass is positive, if numPhase = 2 and changePhase = 1,
    which means we are at the transition day between phases 1 and 2, sla is set
    to be equal to slaMax.

    Then, if the leaf biomass is positive, and if deltaBiomasseFeuilles is
    positive (meaning that the leaf biomass is increasing), SLA for already
    existing leaves is calculated by removing a value that is an affine function
    of SLA itself, and SLA for new leaves is calculated as the mean between SLA
    and slaMax ; then the SLA is calculated as the weighted mean of the two SLA
    values.

    Logically, if there is no newly produced leaf biomass (deltaBiomasseFeuilles
    is negative), only the SLA for already existing leaves is calculated.

    If biomasseFeuille is negative, SLA is unchanged.

    Finally, if biomasseFeuille is positive, SLA value is bounded between slaMin
    and slaMax.

    This function is adapted from the EvalSlaSarrahV3 procedure from the
    bilancarbonsarra.pas and  exmodules 1 & 2.pas file of the original Pascal
    code.  We note that multiple versions of the calculation methods have been
    used in the original procecure. We may want to go back to that if this
    function is problematic.

    Notes :
    In this approach, it is assumed that young leaves have a higher SLA than old
    leaves. The fraction of young leaves makes the canopy SLA increase. The
    penteSLA parameter causes a general decrease in SLA (penteSLA = relative
    decrease per day = fraction of difference between SLAmax and SLAmin). This
    approach is known for legumes, but can also be adapted to other species.

    Generic/expected parameters :
    SLAmax [0.001, 0.01]
    SLAmin [0.001, 0.01]
    penteSLA [0, 0.2]
    SLAini = SLAmax

    Args:
        j (_type_): _description_
        data (_type_): _description_
        paramVariete (_type_): _description_

    Returns:
        _type_: _description_
    """

    condition = (data["biomasseFeuille"][j,:,:] > 0) & \
                (data["numPhase"][j,:,:] == 2) & \
                (data["changePhase"][j,:,:] == 1)

    data["sla"][j:,:,:] = np.where(
        condition,
        paramVariete["slaMax"],
        data["sla"][j,:,:],
    )

    ratio_old_leaf_biomass = data["biomasseFeuille"][j-1,:,:] / data["biomasseFeuille"][j,:,:]
    ratio_new_leaf_biomass = data["deltaBiomasseFeuilles"][j,:,:] / data["biomasseFeuille"][j,:,:]
    sla_decrease_step = paramVariete["slaPente"] * (data["sla"][j,:,:] - paramVariete["slaMin"])

    # Modif du 10/07/2018, DeltaBiomasse neg si reallocation ne pas fair l'evol du SLA dans ces conditions
    data["sla"][j:,:,:] = np.where(
        (data["biomasseFeuille"][j,:,:] > 0),
        np.where(
            (data["deltaBiomasseFeuilles"][j,:,:] > 0),
            #// (data["sla"][j,:,:] - paramVariete["slaPente"] * (data["sla"][j,:,:] - paramVariete["slaMin"])) * (data["biomasseFeuille"][j,:,:] - data["deltaBiomasseFeuilles"][j,:,:]) / data["biomasseFeuille"][j,:,:] + (paramVariete["slaMax"] + data["sla"][j,:,:])/2 * (data["deltaBiomasseFeuilles"][j,:,:] / data["biomasseFeuille"][j,:,:]),
            (data["sla"][j,:,:] - sla_decrease_step) * ratio_old_leaf_biomass + (paramVariete["slaMax"] + data["sla"][j,:,:])/2 * ratio_new_leaf_biomass,
            #//(data["sla"][j,:,:] - paramVariete["slaPente"] * (data["sla"][j,:,:] - paramVariete["slaMin"])) * (data["biomasseFeuille"][j,:,:] / data["biomasseFeuille"][j,:,:]),
            (data["sla"][j,:,:] - sla_decrease_step) * ratio_old_leaf_biomass,
        ),
        data["sla"][j,:,:],
    )

    data["sla"][j:,:,:] = np.where(
        (data["biomasseFeuille"][j,:,:] > 0),
        #// np.minimum(paramVariete["slaMin"], np.maximum(paramVariete["slaMax"], data["sla"][j,:,:])), # according to original
        # according to ocelet version
        np.minimum(
            paramVariete["slaMax"],
            np.maximum(
                paramVariete["slaMin"],
                data["sla"][j,:,:],
            ),
        ), 
        data["sla"][j,:,:],
    )

    return data





def update_LAI(j, data):
    """
    This function estimates and updates the value of the leaf area index (LAI).

    When numPhase is under 2 (before the first leaf appearance), the LAI is set
    to 0. When numPhase is between 2 and 6, the LAI is calculated from the
    biomass of the leaves and the SLA.
    
    When numPhase is above 6, the LAI is set back to 0.

    This function is adapted from the EvolLAIPhases procedure from the
    milbilancarbone.pas and exmodules 1 & 2.pas file of the original Pascal
    code.

    Args:
        j (_type_): _description_
        data (_type_): _description_

    Returns:
        _type_: _description_
    """

    data["lai"][j:,:,:] = xr.where(
        (data["numPhase"][j,:,:] <= 1),
        0,
        np.where(
            data["numPhase"][j,:,:] <= 6,
            data["biomasseFeuille"][j,:,:] * data["sla"][j,:,:],
            0,
        )
    )

    return data





def update_yield(j, data):
    """
    This function updates the yield value.

    If numPhase is 5 (filling phase), the yield is updated by incrementing it
    with the sum of deltaBioAerienne and reallocation, bounded in minimum by 0
    and maximum by dRdtPot.

    That is to say construction of yield is done during phase 5 only, from the
    variation of aerial biomass and reallocation, with a maximum of dRdtPot
    (daily potential yield).

    Notes :
    On tend vers le potentiel en fn du rapport des degresJours/sumDegresJours
    pour la phase de remplissage. Frein sup fn du flux de sève estimé par le
    rapport Tr/TrPot.
    dRdtPot = RdtPotDuJour

    This function is adapted from the EvolDayRdtSarraV3 procedure from the
    ***bilancarbonesarra***, exmodules 1 & 2.pas file of the original Pascal
    code.

    Args:
        j (_type_): _description_
        data (_type_): _description_

    Returns:
        _type_: _description_
    """

    data["rdt"][j:,:,:] = np.where(
        (data["numPhase"][j,:,:] == 5),
        data["rdt"][j,:,:] + np.minimum(data["dRdtPot"][j,:,:],  np.maximum(0.0, data["deltaBiomasseAerienne"][j,:,:]) + data['reallocation'][j,:,:]),
        data["rdt"][j,:,:],
    )

    return data




def BiomDensiteSarraV42(j, data, paramITK, paramVariete):
    # depuis bilancarbonsarra.pas
    #group 160
    
    if ~np.isnan(paramVariete["densOpti"]):

        #! confusion entre rapDensite dataset et parametre
        #group 151
        paramITK["rapDensite"] = paramVariete["densiteA"] + paramVariete["densiteP"] * np.exp(-(paramITK["densite"] / ( paramVariete["densOpti"]/- np.log((1 - paramVariete['densiteA'])/ paramVariete["densiteP"]))))

        # group 152
        data["rdt"][j:,:,:] = (data["rdt"][j,:,:] / data["rapDensite"])#[...,np.newaxis]


        # group 153
        data["rdtPot"][j:,:,:] = (data["rdtPot"][j,:,:]/ data["rapDensite"])#[...,np.newaxis]

        # group 154
        data["biomasseRacinaire"][j:,:,:] = (data["biomasseRacinaire"][j,:,:] / data["rapDensite"])#[...,np.newaxis]

        # group 155
        data["biomasseTige"][j:,:,:] = (data["biomasseTige"][j,:,:] / data["rapDensite"])#[...,np.newaxis]

        # group 156
        data["biomasseFeuille"][j:,:,:] = (data["biomasseFeuille"][j,:,:] / data["rapDensite"])#[...,np.newaxis]

        # group 157
        data["biomasseAerienne"][j:,:,:] = (data["biomasseTige"][j,:,:] + data["biomasseFeuille"][j,:,:] + data["rdt"][j,:,:])#[...,np.newaxis] 
        #data["biomasseAerienne"][j:,:,:] = data["biomasseAerienne"][j,:,:] / data["rapDensite"]


        #? conflit avec fonction evolLAIphase ?
        #  group 158
        #data["lai"][j:,:,:]  = data["biomasseFeuille"][j,:,:] * data["sla"][j,:,:]
        data["lai"][j:,:,:]  = data["lai"][j:,:,:]  / data["rapDensite"]

        # group 159
        data["biomasseTotale"][j:,:,:] = (data["biomasseAerienne"][j,:,:] + data["biomasseRacinaire"][j,:,:])#[...,np.newaxis]
        #data["biomasseTotale"][j:,:,:] = data["biomasseTotale"][j:,:,:] / data["rapDensite"]






    return data





def BiomMcUBTSV3(j, data, paramITK):
    """
    depuis bilancarbonsarra.pas

    group 174

    Pendant la croissance des cultures la d�gradation des r�sidusest calcul�e sans les UBT
    Ici c'est pendant la saion s�che quand il n'y a des cultures pas de b�tes.
    Sur le mulch dress� (Up) ou couch� Lit), on calcul sa d�gradation journali�re
    sur les feuilles et les tiges en fn de coef KN (climat, termites...),
    KI ingestion par les b�tes pression en UBT seulement pour les feuilles, KT (effet pi�tinement) qui va faire passer
    du stade lev� en couch� et du stade couch� en ensevelissement pression en UBT
    Par D�faut :
    KNUp = 0.001 /jour
    KNLit = 0.011
    KN est soit une constante soit peut varier en fn climat (pas fait ref STEP)
    KT = 0.003
    KI = 0.005
    NbUBT = 10 (zone Fakara)
    """
    condition = (data["numPhase"][j,:,:] > 0)

    #   group 161
    data["UBTCulture"][j:,:,:] = np.where(condition, 0, data["NbUBT"][j,:,:])#[...,np.newaxis]
    #  group 162
    data["LitFeuille"][j:,:,:] = np.where(condition, data["LitFeuille"][j,:,:] + data["FeuilleUp"][j,:,:], data["LitFeuille"][j,:,:])#[...,np.newaxis]
    # group 163
    data["LitTige"][j:,:,:] = np.where(condition, data["LitTige"][j,:,:] + data["TigeUp"][j,:,:], data["LitTige"][j,:,:])#[...,np.newaxis]
    # group 164
    data["FeuilleUp"][j:,:,:] = np.where(condition, 0, data["FeuilleUp"][j,:,:])#[...,np.newaxis]
    # group 165
    data["TigeUp"][j:,:,:] = np.where(condition, 0, data["TigeUp"][j,:,:])#[...,np.newaxis]
    # group 166
    data["biomMc"][j:,:,:] = np.where(condition, data["LitFeuille"][j,:,:] + data["LitTige"][j,:,:], data["biomMc"][j,:,:])#[...,np.newaxis]

    #// D�gradation des feuilles et tiges dress�es
    # FeuilleUp := max(0, (FeuilleUp -  FeuilleUp * KNUp - FeuilleUp * KI * UBTCulture  - FeuilleUp * KT * UBTCulture));
    # group 167
    data["FeuilleUp"][j:,:,:] = np.maximum(
        0,
        data["FeuilleUp"][j,:,:] - data["FeuilleUp"][j,:,:] * paramITK["KNUp"] - data["FeuilleUp"][j,:,:] \
            * paramITK["KI"] * data["UBTCulture"][j,:,:] - data["FeuilleUp"][j,:,:] * paramITK["KT"] * data["UBTCulture"][j,:,:],
    )#[...,np.newaxis]


    # group 168
    # TigeUp := max(0, (TigeUp -  TigeUp * KNUp - TigeUp * KT * UBTCulture));
    data["TigeUp"][j:,:,:] = np.maximum(
        0,
        data["TigeUp"][j,:,:] - data["TigeUp"][j,:,:] * paramITK["KNUp"] - data["TigeUp"][j,:,:] * paramITK["KT"] * data["UBTCulture"][j,:,:],
    )#[...,np.newaxis]
    
    #// D�gradation des feuilles et tiges couch�es (liti�re)
    # group 169
    # LitFeuille :=  max(0, (LitFeuille -  LitFeuille * KNLit - LitFeuille * KI * UBTCulture  - LitFeuille * KT * UBTCulture));
    data["LitFeuille"][j:,:,:] = np.maximum(
        0,
        data["LitFeuille"][j,:,:] - data["LitFeuille"][j,:,:] * paramITK["KNLit"] - data["LitFeuille"][j,:,:] * paramITK["KI"] \
            * data["UBTCulture"][j,:,:] - data["LitFeuille"][j,:,:] * paramITK["KT"] * data["UBTCulture"][j,:,:],
    )#[...,np.newaxis]

    # group 170
    # LitTige :=  max(0, (LitTige -  LitTige * KNLit - LitTige * KT * UBTCulture));
    data["LitTige"][j:,:,:] = np.maximum(
        0,
        data["LitTige"][j,:,:] - data["LitTige"][j,:,:] * paramITK["KNLit"] - data["LitTige"][j,:,:] * paramITK["KT"] * data["UBTCulture"][j,:,:],
    )#[...,np.newaxis]

    # group 171
    #BiomMc := LitFeuille + LitTige;
    data["biomMc"][j:,:,:] = (data["LitFeuille"][j,:,:] + data["LitTige"][j,:,:])#[...,np.newaxis]
     
    # #// transfert dress� � liti�re effet pi�tinement
    # LitFeuille :=  LitFeuille + FeuilleUp * KT * UBTCulture;
    # group 172
    data["LitFeuille"][j:,:,:] = (data["LitFeuille"][j,:,:] + data["FeuilleUp"][j,:,:] * paramITK["KT"] * data["UBTCulture"][j,:,:])#[...,np.newaxis]

    # LitTige :=  LitTige + TigeUp * KT * UBTCulture;
    # group 173
    data["LitTige"][j:,:,:] = (data["LitTige"][j,:,:] + data["TigeUp"][j,:,:] * paramITK["KT"] * data["UBTCulture"][j,:,:])#[...,np.newaxis]

    # // le 01/03 on consid�re que toutes les pailles et feuilles dressees sont couchees

    #       if (trunc(DayOfTheYear(DateEnCours)) = 61) then
    #   begin
    #     LitFeuille :=  LitFeuille + FeuilleUp;
    #     LitTige :=  LitTige + TigeUp;
    #     FeuilleUp :=  0;
    #     TigeUp :=  0;
    #     BiomMc := LitFeuille + LitTige;
    #  end;

    return data




def MAJBiomMcSV3(data):
    """
    groupe 182
 A la Recolte, on calcul la part des biomasses qui restent sur place (Up), non r�colt�es
 et la part qui est mise � terre (Liti�re) sur ce qui est laiss� sur place
 On met a jour aussi la biomasse des liti�res pour les calculs effet mulch sue lr bilan hydrique
    """
#         if (NumPhase =7) then
#     begin
        # groupe 175
#       FeuilleUp := FeuilleUp +  BiomasseFeuilles * (1-TxRecolte);
        # groupe 176
#       TigeUp := TigeUp + BiomasseTiges *  (1-TxRecolte);

        # groupe 177
#       LitFeuille := LitFeuille + FeuilleUp * TxaTerre;

        # groupe 178
#       LitTige := LitTige + TigeUp * TxaTerre;

        # groupe 179
#       FeuilleUp := FeuilleUp * (1-TxaTerre);

        # groupe 180
#       TigeUp := TigeUp * (1-TxaTerre);
# //      LitTige := LitTige + BiomMc;
        # groupe 181
#       BiomMC := LitFeuille + LitTige;
#  {     BiomasseFeuilles := 0;
#       BiomasseTiges := 0;
    return data