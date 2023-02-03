import numpy as np

def InitiationCulture(data, grid_width, grid_height, duration, paramVariete):
    """
    Initializes variables related to crop growth in the data xarray dataset.
    This code has been adapted from the original InitiationCulture procedure, MilBilanCarbone.pas code.
    Comments with tab indentation are from the original code.
    As the rain is the first variable to be initialized in the data xarray dataset, its dimensions are used
    to initialize the other variables.
    """    

    # Maximum thermal time (°C.j)
    # Somme de degré-jour maximale (°C.j)
    #   SommeDegresJourMaximale := SeuilTempLevee + SeuilTempBVP + SeuilTempRPR + SeuilTempMatu1 + SeuilTempMatu2;
    data["sommeDegresJourMaximale"] = (data["rain"].dims, np.full(
        (duration, grid_width, grid_height),
        (paramVariete["SDJLevee"] + paramVariete["SDJBVP"] + paramVariete["SDJRPR"] + paramVariete["SDJMatu1"] + paramVariete["SDJMatu2"])
    ))
    data["sommeDegresJourMaximale"].attrs = {"units":"°C.j", "long_name":"Maximum thermal time"}

    
    # Other variables to be initialized at 0
    # Autres variables à initialiser à 0
    #   NumPhase := 0;
    #   SommeDegresJour := 0;
    #   BiomasseAerienne := 0;
    #   BiomasseVegetative := 0;
    #   BiomasseTotale := 0;
    #   BiomasseTiges := 0;
    #   BiomasseRacinaire := 0;
    #   BiomasseFeuilles := 0;
    #   DeltaBiomasseTotale := 0;
    #   SeuilTempPhaseSuivante:=0;
    #   Lai := 0;
    variables = {
        "numPhase":"arbitrary units",
        "sdj":"°C.j",
        "biomasseAerienne":"kg/ha",
        "biomasseVegetative":"kg/ha",
        "biomasseTotale":"kg/ha",
        "biomasseTige":"kg/ha",
        "biomasseRacinaire":"kg/ha",
        "biomasseFeuille":"kg/ha",
        "deltaBiomasseTotale":"kg/ha",
        "seuilTempPhaseSuivante":"°C.j",
        "lai":"m2/m2",
    }
        
    for variable in variables :
        data[variable] = (data["rain"].dims, np.zeros(shape=(duration, grid_width, grid_height)))
        data[variable].attrs = {"units":variables[variable], "long_name":variable}

    return data





def InitSup(data, grid_width, grid_height, duration, paramTypeSol, paramITK):
    """
    Initializes supplementary variables needed for computations.
    As the rain is the first variable to be initialized in the data xarray dataset, its dimensions are used
    to initialize the other variables.
    """   

    data = data.copy(deep=True)

    variables = {
        "assim": ["",""],
        "assimPot": ["",""],
        "biomTotStadeFloraison": ["",""],
        "biomTotStadeIp": ["",""],
        "bM": ["",""],
        "changePhase" : ["indicator of phase transition","binary"],
        "cM": ["",""],
        "consoRur": ["",""],
        "conv": ["",""],
        "correctedIrrigation" : ["corrected irrigation","mm"],
        "cstr" : ["drought stress coefficient", "arbitrary unit"],
        "dayBiomLeaf": ["",""],
        "dayVrac" : ["modulated daily root growth","mm/day"],
        "ddj": ["daily thermal time","°C"],
        "deltaBiomasseAerienne": ["",""],
        "deltaBiomasseFeuilles": ["",""],
        #! renaming deltaRur with delta_root_tank_capacity
        #// "deltaRur": ["change in root system water reserve","mm"],
        "delta_root_tank_capacity": ["change in root system water reserve","mm"],
        "dr": ["",""],
        "dRdtPot": ["",""],
        "dureeDuJour": ["",""],
        #! replacing eauCaptee by water_gathered_by_mulch
        #// "eauCaptee" : ["water captured by the mulch in one day","mm"],
        "water_gathered_by_mulch" : ["water captured by the mulch in one day","mm"],
        "eauDispo" : ["available water, sum of rainfall and total irrigation for the day","mm"],
        "eauTranspi": ["",""],
        "etm": ["",""],
        "etp": ["",""],
        "etr": ["",""],
        "evap": ["",""],
        "evapPot": ["",""],
        "FEMcW": ["",""],
        "fesw": ["",""],
        "FeuilleUp": ["",""],
        "ftsw": ["",""],
        "initPhase": ["",""],
        "irrigTotDay" : ["total irrigation for the day","mm"],
        "KAssim": ["",""],
        "kce": ["",""],
        "kcp": ["",""],
        "kcTot": ["",""],
        "kRespMaint": ["",""],
        "LitFeuille": ["",""],
        "lr" : ["daily water runoff","mm"],
        "manqueAssim": ["",""],
        "nbJourCompte": ["",""],
        "nbjStress": ["",""],
        "NbUBT": ["",""],
        "pFact": ["",""],
        "phaseDevVeg": ["",""],
        "phasePhotoper": ["photoperiodic phase indicator","binary"],
        "rapDensite": ["",""],
        "rdt": ["",""],
        "rdtPot": ["",""],
        "reallocation": ["",""],
        "respMaint": ["",""],

        #! renaming ruIrr to irrigation_tank_capacity
        #//"ruIrr" : ["?","mm"],
        "irrigation_tank_capacity" : ["irrigation tank capacity","mm"],
        "ruRac": ["Water column that can potentially be strored in soil volume explored by root system","mm"],
        "seuilTempPhasePrec": ["",""],
        "sla": ["",""],
        "sommeDegresJourPhasePrec": ["",""],
        "startLock": ["",""],
        #! renaming stockIrr to irrigation_tank_stock
        #// "stockIrr" : ["?","mm"],
        "irrigation_tank_stock" : ["?","mm"],
        #! renaming stockMc to mulch_water_stock
        #// "stockMc" : ["water stored in crop residues (mulch)","mm"],
        "mulch_water_stock" : ["water stored in crop residues (mulch)","mm"],
        "stockRac": ["",""],
        # renaming stRu to root_tank_stock
        #// "stRu": ["",""],
        "root_tank_stock": ["",""],

        #! renaming stRuMax to total_tank_capacity
        #//"stRuMax": ["",""],
        "total_tank_capacity": ["",""],
        # renaming stRur to 
        "stRur": ["",""],
        #! renaming stRurMaxPrec to root_tank_capacity_previous_season
        # "stRurMaxPrec": ["",""],
        "root_tank_capacity_previous_season": ["",""],
        "stRurPrec": ["",""],
        "stRurSurf": ["",""],
        #! renaming stRuSurf to surface_tank_stock
        #// "stRuSurf": ["",""],
        "surface_tank_stock": ["",""],
        "stRuSurfPrec": ["",""],

        #! renaming stRuVar to delta_total_tank_stock
        #// "stRuVar": ["",""],
        "delta_total_tank_stock": ["",""],
        "sumPP": ["",""],
        "TigeUp": ["",""],
        "tr": ["",""],
        "trPot": ["",""],
        "trSurf": ["",""],
        "UBTCulture": ["",""],
        "vRac" : ["reference daily root growth","mm/day"],
    }
    


    for variable in variables :
        data[variable] = (data["rain"].dims, np.zeros(shape=(duration, grid_width, grid_height)))
        data[variable].attrs = {"units":variables[variable][1], "long_name":variables[variable][0]}


    data["irrigAuto"] = (data["rain"].dims, np.full((duration, grid_width, grid_height), paramITK["irrigAuto"]))
    data["irrigAuto"].attrs = {"units":"binary", "long_name":"automatic irrigation indicator"}


    return data


def InitSup2(data, grid_width, grid_height, duration, df_weather):
    data["tpMoy"] = df_weather["TEMP"].copy().values.reshape(grid_width, grid_height, duration)
    data["rain"] = df_weather["RAIN"].copy().values.reshape(grid_width, grid_height, duration)
    data["ET0"] = df_weather["ET0"].copy().values.reshape(grid_width, grid_height, duration)
    data["rg"] = df_weather["IRRAD"].copy().values.reshape(grid_width, grid_height, duration)
    return data


def EvalPar(data):
    #depuis meteo.par
    kpar = 0.5
    data["par"] = kpar * data["rg"]
    data["par"].attrs = {"units":"MJ/m2", "long_name":"par"}
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
        5: paramVariete["txAssimBVP"] + (data['sdj'][j,:,:] - data['sommeDegresJourPhasePrec'][j,:,:]) * (paramVariete['txAssimMatu1'] -  paramVariete['txAssimBVP']) / (data['seuilTempPhaseSuivante'][j,:,:] - data['sommeDegresJourPhasePrec'][j,:,:]),
        6: paramVariete["txAssimMatu1"] + (data["sdj"][j,:,:] - data["sommeDegresJourPhasePrec"][j,:,:]) * (paramVariete["txAssimMatu2"] - paramVariete["txAssimMatu1"]) / (data["seuilTempPhaseSuivante"][j,:,:] - data["sommeDegresJourPhasePrec"][j,:,:]),
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
    

def update_assimPot(j, data, paramITK):
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
        (data["numPhase"][j,:,:] == 5) & (data["changePhase"][j,:,:] == 1) & (data["rdtPot"][j,:,:] > data["biomasseTige"][j,:,:] * 2) & (data["phaseDevVeg"][j,:,:] < 6),
        data["biomasseTige"][j,:,:] * 2,
        data["rdtPot"][j,:,:],
    )
    
    return data

def update_potential_yield_delta(j, data):
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
                #! original code used ddj instead of sdj, but that did not make sense so it was modified
                data["rdtPot"][j,:,:] * (data["sdj"][j,:,:] / paramVariete["SDJMatu1"]) * (data["tr"][j,:,:] / data["trPot"][j,:,:]),
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



def condition_phase_above_1_and_negative_delta_biomass(j, data):
    condition = (data["numPhase"][j,:,:] > 1) & (data["deltaBiomasseAerienne"][j,:,:] < 0)
    return condition 


def update_leaf_biomass(j, data):
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
        condition_phase_above_1_and_negative_delta_biomass(j, data),
        np.maximum(
            0.00000001,
            data["biomasseFeuille"][j,:,:] - (data["reallocation"][j,:,:] - data["deltaBiomasseAerienne"][j,:,:]) * paramVariete["pcReallocFeuille"]
        ),
        data["biomasseFeuille"][j,:,:],
    )

    return data



def update_stem_biomass(j, data):
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
        condition_phase_above_1_and_negative_delta_biomass(j, data),
        np.maximum(
            0.00000001,
            data["biomasseTige"][j,:,:] - (data["reallocation"][j,:,:] - data["deltaBiomasseAerienne"][j,:,:]) * (1 - paramVariete["pcReallocFeuille"]),
            ),
        data["biomasseTige"][j,:,:],
    )

    return data





def condition_positive_delta_biomass(j, data):

        condition = (data["numPhase"][j,:,:] > 1) & \
            (data["deltaBiomasseAerienne"][j,:,:] >= 0) & \
            ((data["numPhase"][j,:,:] <= 4) | (data["numPhase"][j,:,:] <= paramVariete["phaseDevVeg"]))
            # (data["numPhase"][j,:,:] <= 4)
        
        return condition


def update_bM_and_cM(j, data):
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
        condition_positive_delta_biomass(j, data),
        paramVariete["feuilAeroBase"] - 0.1,
        data["bM"][j,:,:],
    )


    data["cM"][j,:,:] = np.where(
        condition_positive_delta_biomass(j, data),
        ((paramVariete["feuilAeroPente"] * 1000)/ data["bM"][j,:,:] + 0.78) / 0.75,
        data["cM"][j,:,:],
    )

    return data


def update_leaf_biomass_positive_delta_aboveground_biomass(j, data):
    """

    Args:
        j (_type_): _description_
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    data["biomasseFeuille"][j:,:,:] = np.where(
        condition_positive_delta_biomass(j, data),
        (0.1 + data["bM"][j,:,:] * data["cM"][j,:,:] ** ((data["biomasseAerienne"][j,:,:] - data["rdt"][j,:,:]) / 1000)) \
            * (data["biomasseAerienne"][j,:,:] - data["rdt"][j,:,:]),
        data["biomasseFeuille"][j,:,:],
    )

    return data



def update_stem_biomass_positive_delta_aboveground_biomass(j, data):
    """_summary_

    Args:
        j (_type_): _description_
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    data["biomasseTige"][j:,:,:] = np.where(
        condition_positive_delta_biomass(j, data),
        data["biomasseAerienne"][j,:,:] - data["biomasseFeuille"][j,:,:] - data["rdt"][j,:,:],
        data["biomasseTige"][j,:,:],
    )

    return data




def condition_positive_delta_aboveground_biomass_all_phases(j, data):
        #// condition = (data["numPhase"][j,:,:] > 1) & (data["deltaBiomasseAerienne"][j,:,:] >= 0)
    condition = (data["numPhase"][j,:,:] > 1) & (data["deltaBiomasseAerienne"][j,:,:] > 0)
    return condition




def update_leaf_biomass_all_phases(j, data):
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




def update_stem_biomass_all_phases(j, data):
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
    data = update_leaf_biomass(j, data)
    data = update_stem_biomass(j, data)

    # if deltaBiomasseAerienne >= 0 and (numPhase <= 4 or numPhase <= phaseDevVeg)
    data = update_bM_and_cM(j, data)
    data = update_leaf_biomass_positive_delta_aboveground_biomass(j, data)
    data = update_stem_biomass_positive_delta_aboveground_biomass(j, data)

    # if deltaBiomasseAerienne > 0 and numPhase > 1
    data = update_leaf_biomass_all_phases(j, data)
    data = update_stem_biomass_all_phases(j, data)

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




def EvalBiomasseVegetati(j, data):
    # group 132
    #d'après milbilancarbone.pas
    data["biomasseVegetative"][j:,:,:] = (data["biomasseTige"][j,:,:] + data["biomasseFeuille"][j,:,:])#[...,np.newaxis]
    return data




def EvalSlaSarrahV3(j, data, paramVariete):
    # check vs code pascal OK
    """
    groupe 136
    d'après bulancarbonsarra.pas

    On suppose que les jeunes feuilles on un SLA supérieur aux vieilles feuilles.
    La fraction de jeunes (nouvelles) feuilles fait donc monter le SLA global
    du couvert. Le paramétre penteSLA provoque une chute générale du SLA
    (penteSLA = chute relative par jour = fraction de différence entre SLAmax
    et SLAmin). Fonctionnement conéu surtout pour les légumineuses, mais
    peut étre aussi adapté aux autres espéces.
    Paramétres :
    SLAmax (0.001 é 0.01), ex : 0.007
    SLAmin (0.001 é 0.01), ex : 0.002
    penteSLA (0 é 0.2), ex : 0.1
    Avec : SLAini = SLAmax
    }
    """
    # group 133
    data["sla"][j:,:,:] = np.where(
        (data["biomasseFeuille"][j,:,:] > 0) & \
            (data["numPhase"][j,:,:] == 2) & \
            (data["changePhase"][j,:,:] == 1),
        paramVariete["slaMax"],
        data["sla"][j,:,:],
    )#[...,np.newaxis]

    # Modif du 10/07/2018, DeltaBiomasse neg si reallocation ne pas fair l'evol du SLA dans ces conditions
    
    # original
    # groupe 134
    data["sla"][j:,:,:] = np.where(
        (data["biomasseFeuille"][j,:,:] > 0),
        np.where(
            (data["deltaBiomasseFeuilles"][j,:,:] > 0),
            (data["sla"][j,:,:] - paramVariete["slaPente"] * (data["sla"][j,:,:] - paramVariete["slaMin"])) \
              * (data["biomasseFeuille"][j,:,:] - data["deltaBiomasseFeuilles"][j,:,:]) / data["biomasseFeuille"][j,:,:] \
              + (paramVariete["slaMax"] + data["sla"][j,:,:])/2 * (data["deltaBiomasseFeuilles"][j,:,:] / data["biomasseFeuille"][j,:,:]),
            (data["sla"][j,:,:] - paramVariete["slaPente"] * (data["sla"][j,:,:] - paramVariete["slaMin"])) \
                * (data["biomasseFeuille"][j,:,:] / data["biomasseFeuille"][j,:,:]),
        ),
        data["sla"][j,:,:],
    )#[...,np.newaxis]

    # d'après version ocelet
    # data["sla"][j:,:,:] = np.where(
    #     (data["biomasseFeuille"][j,:,:] > 0),
    #     (data["sla"][j,:,:] - paramVariete["slaPente"] * (data["sla"][j,:,:] - paramVariete["slaMin"])) \
    #         * (data["biomasseFeuille"][j,:,:] - data["deltaBiomasseFeuilles"][j,:,:]) / data["biomasseFeuille"][j,:,:] \
    #         + (paramVariete["slaMax"] + data["sla"][j,:,:])/2 * (data["deltaBiomasseFeuilles"][j,:,:] / data["biomasseFeuille"][j,:,:]),
    #     data["sla"][j,:,:],
    # )

    # mix original/ocelet
    # data["sla"][j:,:,:] = np.where(
    #     (data["biomasseFeuille"][j,:,:] > 0),
    #     np.where(
    #         (data["deltaBiomasseFeuilles"][j,:,:] > 0),
    #         (data["sla"][j,:,:] - paramVariete["slaPente"] * (data["sla"][j,:,:] - paramVariete["slaMin"])) * (data["biomasseFeuille"][j,:,:] - data["deltaBiomasseFeuilles"][j,:,:]) / data["biomasseFeuille"][j,:,:] + (paramVariete["slaMax"] + data["sla"][j,:,:])/2 * (data["deltaBiomasseFeuilles"][j,:,:] / data["biomasseFeuille"][j,:,:]),
    #         (data["sla"][j,:,:] - paramVariete["slaPente"] * (data["sla"][j,:,:] - paramVariete["slaMin"])) * (data["biomasseFeuille"][j,:,:] / data["deltaBiomasseFeuilles"][j,:,:]),
    #     ),
    #     data["sla"][j,:,:],
    # )

    # original modifié
    # data["sla"][j:,:,:] = np.where(
    #     (data["biomasseFeuille"][j,:,:] > 0),
    #     np.where(
    #         (data["deltaBiomasseFeuilles"][j,:,:] > 0),
    #         (data["sla"][j,:,:] - paramVariete["slaPente"] * (data["sla"][j,:,:] - paramVariete["slaMin"])) * (data["biomasseFeuille"][j,:,:] - data["deltaBiomasseFeuilles"][j,:,:]) / data["biomasseFeuille"][j,:,:] + (paramVariete["slaMax"] + data["sla"][j,:,:])/2 * (data["deltaBiomasseFeuilles"][j,:,:] / data["biomasseFeuille"][j,:,:]),
    #         (data["sla"][j,:,:] - paramVariete["slaPente"] * (data["sla"][j,:,:] - paramVariete["slaMin"])) * (data["biomasseFeuille"][j,:,:] / data["biomasseFeuille"][j,:,:]),
    #         # data["sla"][j,:,:],
    #     ),
    #     data["sla"][j,:,:],
    # )


    # groupe 135
    data["sla"][j:,:,:] = np.where(
        (data["biomasseFeuille"][j,:,:] > 0),
        # np.minimum(paramVariete["slaMin"], np.maximum(paramVariete["slaMax"], data["sla"][j,:,:])),
        np.minimum(paramVariete["slaMax"], np.maximum(paramVariete["slaMin"], data["sla"][j,:,:])), # d'après version ocelet
        data["sla"][j,:,:],
    )#[...,np.newaxis]

    

    return data




def EvolLAIPhases(j, data):
    # d'après milbilancarbone.pas
    # group 137
    data["lai"][j:,:,:] = np.where(
        #(data["numPhase"][j,:,:] <= 1),
        (data["numPhase"][j,:,:] <= 1) | (data["startLock"][j,:,:] == 1),
        0,
        np.where(
            data["numPhase"][j,:,:] <= 6,
            data["biomasseFeuille"][j,:,:] * data["sla"][j,:,:],
            0,
        )
    )#[...,np.newaxis]


    return data




def EvolDayRdtSarraV3(j, data):
    # groupe 138
    # d'après bilancarbonsarra.pas
    # {
    # On tend vers le potentiel en fn du rapport des degresJours/sumDegresJours
    # pour la phase de remplissage
    # Frein sup fn du flux de s�ve estim� par le rapport Tr/TrPot
    # }

    # dRdtPot = RdtPotDuJour
    # on cast sur j
    data["rdt"][j:,:,:] = np.where(
        (data["numPhase"][j,:,:] == 5),
        data["rdt"][j,:,:] + np.minimum(data["dRdtPot"][j,:,:],  np.maximum(0.0, data["deltaBiomasseAerienne"][j,:,:]) + data['reallocation'][j,:,:]),
        data["rdt"][j,:,:],
    )#[...,np.newaxis]


    return data




def BiomDensiteSarraV4(j, data, paramITK):
    """
    if ~np.isnan(paramVariete["densOpti"]):
        data["rapDensite"][j,:,:] = np.minimum(1, paramITK["densite"]/paramVariete["densOpti"])
        data["rdt"][j,:,:] = data["rdt"][j,:,:] * data["rapDensite"][j,:,:]
        data["rdtPot"][j,:,:] = data["rdtPot"][j,:,:] * data["rapDensite"][j,:,:]
        data["biomasseRacinaire"][j,:,:] = data["biomasseRacinaire"][j,:,:] * data["rapDensite"][j,:,:]
        data["biomasseTige"][j,:,:] = data["biomasseTige"][j,:,:] * data["rapDensite"][j,:,:]
        data["biomasseFeuille"][j,:,:] = data["biomasseFeuille"][j,:,:] * data["rapDensite"][j,:,:]
        data["biomasseAerienne"][j,:,:] = data["biomasseFeuille"][j,:,:] + data["biomasseTige"][j,:,:] + data["rdt"][j,:,:]
        data["lai"][j,:,:] = data["biomasseFeuille"][j,:,:] * data["sla"][j,:,:]
        data["biomasseTotale"][j,:,:] = data["biomasseAerienne"][j,:,:] + data["biomasseRacinaire"][j,:,:]
    """
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