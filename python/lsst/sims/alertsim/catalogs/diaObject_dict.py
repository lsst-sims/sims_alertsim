""" a method to get diaObject as dictionary according to the schema
This is a temporary, semi-dirty solution to avoid another catsim query for.
diaObject data.
"""
import numpy as np

def getDiaObject_dict(diaObjectId, ra, decl):

    return {"diaObjectId" : diaObjectId,
  "ra" : ra,
  "decl" : decl,
  "ra_decl_Cov" : {"raSigma" : 0.28920996,
      "declSigma" : 0.25138605, "ra_decl_Cov" : 0.47942978},
  "radecTai" : 0.5384099483823307,
  "pmRa" : 0.8551473,
  "pmDecl" : 0.68943334,
  "parallax" : 0.8253294,
  "pm_parallax_Cov" : {"pmRaSigma" : 0.8295793, "pmDeclSigma" : 0.20050234,
      "parallaxSigma" : 0.32330728, "pmRa_pmDecl_Cov" : 0.8616924,
      "pmRa_parallax_Cov" : 0.3034612, "pmDecl_parallax_Cov" : 0.059243202},
  "pmParallaxLnL" : 0.29995412,
  "pmParallaxChi2" : 0.78219104,
  "pmParallaxNdata" : 1227051013,
  "uPSFluxMean" : 0.4107687,
  "uPSFluxMeanErr" : 0.85751665,
  "uPSFluxSigma" : 0.47688764,
  "uPSFluxChi2" : 0.56457865,
  "uPSFluxNdata" : 1626528003,
  "gPSFluxMean" : 0.69664824,
  "gPSFluxMeanErr" : 0.61562824,
  "gPSFluxSigma" : 0.27989817,
  "gPSFluxChi2" : 0.5823938,
  "gPSFluxNdata" : -1447046860,
  "rPSFluxMean" : 0.9725589,
  "rPSFluxMeanErr" : 0.4009825,
  "rPSFluxSigma" : 0.05032754,
  "rPSFluxChi2" : 0.90101,
  "rPSFluxNdata" : -596239373,
  "iPSFluxMean" : 0.028420031,
  "iPSFluxMeanErr" : 0.73197657,
  "iPSFluxSigma" : 0.7863265,
  "iPSFluxChi2" : 0.5983339,
  "iPSFluxNdata" : -1948540010,
  "zPSFluxMean" : 0.25571924,
  "zPSFluxMeanErr" : 0.77885556,
  "zPSFluxSigma" : 0.6979338,
  "zPSFluxChi2" : 0.77662224,
  "zPSFluxNdata" : -308704861,
  "yPSFluxMean" : 0.4511538,
  "yPSFluxMeanErr" : 0.60250914,
  "yPSFluxSigma" : 0.2209661,
  "yPSFluxChi2" : 0.2592802,
  "yPSFluxNdata" : 373660560,
  "uFPFluxMean" : 0.17985207,
  "uFPFluxMeanErr" : 0.46610427,
  "uFPFluxSigma" : 0.96096104,
  "gFPFluxMean" : 0.8373919,
  "gFPFluxMeanErr" : 0.6622091,
  "gFPFluxSigma" : 0.82595634,
  "rFPFluxMean" : 0.47039467,
  "rFPFluxMeanErr" : 0.74643636,
  "rFPFluxSigma" : 0.17253017,
  "iFPFluxMean" : 0.20049852,
  "iFPFluxMeanErr" : 0.56423014,
  "iFPFluxSigma" : 0.3624664,
  "zFPFluxMean" : 0.96688205,
  "zFPFluxMeanErr" : 0.05519402,
  "zFPFluxSigma" : 0.64746535,
  "yFPFluxMean" : 0.8079089,
  "yFPFluxMeanErr" : 0.2910043,
  "yFPFluxSigma" : 0.92416835,
  "uLcPeriodic" : {
      "uLcPeriodic01" : 0.3496368,
      "uLcPeriodic02" : 0.5843135,
      "uLcPeriodic03" : 0.1785202,
      "uLcPeriodic04" : 0.010906637,
      "uLcPeriodic05" : 0.77285975,
      "uLcPeriodic06" : 0.21431375,
      "uLcPeriodic07" : 0.19384503,
      "uLcPeriodic08" : 0.68082434,
      "uLcPeriodic09" : 0.37712842,
      "uLcPeriodic10" : 0.051814556,
      "uLcPeriodic11" : 0.91718906,
      "uLcPeriodic12" : 0.44725686,
      "uLcPeriodic13" : 0.6720161,
      "uLcPeriodic14" : 0.83170134,
      "uLcPeriodic15" : 0.045308232,
      "uLcPeriodic16" : 0.24342573,
      "uLcPeriodic17" : 0.9198879,
      "uLcPeriodic18" : 0.2299686,
      "uLcPeriodic19" : 0.15848166,
      "uLcPeriodic20" : 0.43285733,
      "uLcPeriodic21" : 0.44936883,
      "uLcPeriodic22" : 0.035665393,
      "uLcPeriodic23" : 0.7355372,
      "uLcPeriodic24" : 0.9577542,
      "uLcPeriodic25" : 0.11931813,
      "uLcPeriodic26" : 0.33229852,
      "uLcPeriodic27" : 0.7376391,
      "uLcPeriodic28" : 0.783087,
      "uLcPeriodic29" : 0.7510642,
      "uLcPeriodic30" : 0.6186808,
      "uLcPeriodic31" : 0.5753278,
      "uLcPeriodic32" : 0.5573582
  },
  "gLcPeriodic" : {
      "gLcPeriodic01" : 0.70143986,
      "gLcPeriodic02" : 0.65298986,
      "gLcPeriodic03" : 0.8419279,
      "gLcPeriodic04" : 0.17673212,
      "gLcPeriodic05" : 0.65325874,
      "gLcPeriodic06" : 0.15819371,
      "gLcPeriodic07" : 0.10928142,
      "gLcPeriodic08" : 0.65841377,
      "gLcPeriodic09" : 0.3408845,
      "gLcPeriodic10" : 0.3740912,
      "gLcPeriodic11" : 0.2666778,
      "gLcPeriodic12" : 0.41503644,
      "gLcPeriodic13" : 0.9391151,
      "gLcPeriodic14" : 0.038436532,
      "gLcPeriodic15" : 0.4059307,
      "gLcPeriodic16" : 0.7964965,
      "gLcPeriodic17" : 0.43108535,
      "gLcPeriodic18" : 0.35290194,
      "gLcPeriodic19" : 0.1339153,
      "gLcPeriodic20" : 0.4557373,
      "gLcPeriodic21" : 0.5865706,
      "gLcPeriodic22" : 0.3145942,
      "gLcPeriodic23" : 0.41368502,
      "gLcPeriodic24" : 0.010623634,
      "gLcPeriodic25" : 0.05968833,
      "gLcPeriodic26" : 0.45444667,
      "gLcPeriodic27" : 0.69536,
      "gLcPeriodic28" : 0.24731433,
      "gLcPeriodic29" : 0.5719062,
      "gLcPeriodic30" : 0.6340439,
      "gLcPeriodic31" : 0.98237723,
      "gLcPeriodic32" : 0.76508766
  },
  "rLcPeriodic" : {
      "rLcPeriodic01" : 0.786128,
      "rLcPeriodic02" : 0.7460612,
      "rLcPeriodic03" : 0.7522093,
      "rLcPeriodic04" : 0.14824903,
      "rLcPeriodic05" : 0.85035807,
      "rLcPeriodic06" : 0.54419476,
      "rLcPeriodic07" : 0.8293973,
      "rLcPeriodic08" : 0.35835767,
      "rLcPeriodic09" : 0.32378936,
      "rLcPeriodic10" : 0.2323876,
      "rLcPeriodic11" : 0.34100044,
      "rLcPeriodic12" : 0.32466632,
      "rLcPeriodic13" : 0.9370814,
      "rLcPeriodic14" : 0.5862096,
      "rLcPeriodic15" : 0.43154567,
      "rLcPeriodic16" : 0.27500862,
      "rLcPeriodic17" : 0.8078245,
      "rLcPeriodic18" : 0.42357773,
      "rLcPeriodic19" : 0.86233336,
      "rLcPeriodic20" : 0.23649544,
      "rLcPeriodic21" : 0.78991747,
      "rLcPeriodic22" : 0.26766157,
      "rLcPeriodic23" : 0.022900403,
      "rLcPeriodic24" : 0.95065403,
      "rLcPeriodic25" : 0.61407703,
      "rLcPeriodic26" : 0.69815254,
      "rLcPeriodic27" : 0.5271871,
      "rLcPeriodic28" : 0.12154055,
      "rLcPeriodic29" : 0.23388386,
      "rLcPeriodic30" : 0.67128354,
      "rLcPeriodic31" : 0.2840203,
      "rLcPeriodic32" : 0.7260751
  },
  "iLcPeriodic" : {
      "iLcPeriodic01" : 0.755278,
      "iLcPeriodic02" : 0.95406437,
      "iLcPeriodic03" : 0.7896173,
      "iLcPeriodic04" : 0.8928149,
      "iLcPeriodic05" : 0.8273708,
      "iLcPeriodic06" : 0.28683323,
      "iLcPeriodic07" : 0.5923068,
      "iLcPeriodic08" : 0.20622814,
      "iLcPeriodic09" : 0.8512069,
      "iLcPeriodic10" : 0.33595198,
      "iLcPeriodic11" : 0.92702866,
      "iLcPeriodic12" : 0.5756611,
      "iLcPeriodic13" : 0.82996106,
      "iLcPeriodic14" : 0.9209943,
      "iLcPeriodic15" : 0.9977655,
      "iLcPeriodic16" : 0.21883374,
      "iLcPeriodic17" : 0.48221642,
      "iLcPeriodic18" : 0.7104042,
      "iLcPeriodic19" : 0.31290746,
      "iLcPeriodic20" : 0.48735636,
      "iLcPeriodic21" : 0.076405406,
      "iLcPeriodic22" : 0.7908754,
      "iLcPeriodic23" : 0.49279547,
      "iLcPeriodic24" : 0.60413486,
      "iLcPeriodic25" : 0.78799814,
      "iLcPeriodic26" : 0.74086225,
      "iLcPeriodic27" : 0.040961027,
      "iLcPeriodic28" : 0.88159084,
      "iLcPeriodic29" : 0.9047754,
      "iLcPeriodic30" : 0.794521,
      "iLcPeriodic31" : 0.6064394,
      "iLcPeriodic32" : 0.40293062
  },
  "zLcPeriodic" : {
      "zLcPeriodic01" : 0.2503277,
      "zLcPeriodic02" : 0.13800651,
      "zLcPeriodic03" : 0.7386524,
      "zLcPeriodic04" : 0.677964,
      "zLcPeriodic05" : 0.5070364,
      "zLcPeriodic06" : 0.1637165,
      "zLcPeriodic07" : 0.9901334,
      "zLcPeriodic08" : 0.84022456,
      "zLcPeriodic09" : 0.987768,
      "zLcPeriodic10" : 0.54978615,
      "zLcPeriodic11" : 0.673565,
      "zLcPeriodic12" : 0.66900414,
      "zLcPeriodic13" : 0.308259,
      "zLcPeriodic14" : 0.8464155,
      "zLcPeriodic15" : 0.7558901,
      "zLcPeriodic16" : 0.39139694,
      "zLcPeriodic17" : 0.7531389,
      "zLcPeriodic18" : 0.3249038,
      "zLcPeriodic19" : 0.5580769,
      "zLcPeriodic20" : 0.9390409,
      "zLcPeriodic21" : 0.91819483,
      "zLcPeriodic22" : 0.17639059,
      "zLcPeriodic23" : 0.4814633,
      "zLcPeriodic24" : 0.5987158,
      "zLcPeriodic25" : 0.058666408,
      "zLcPeriodic26" : 0.96932495,
      "zLcPeriodic27" : 0.27461922,
      "zLcPeriodic28" : 0.76755804,
      "zLcPeriodic29" : 0.63358593,
      "zLcPeriodic30" : 0.25757003,
      "zLcPeriodic31" : 0.22887349,
      "zLcPeriodic32" : 0.2449876
  },
  "yLcPeriodic" : {
      "yLcPeriodic01" : 0.36673468,
      "yLcPeriodic02" : 0.6111761,
      "yLcPeriodic03" : 0.09387469,
      "yLcPeriodic04" : 0.09510684,
      "yLcPeriodic05" : 0.5513674,
      "yLcPeriodic06" : 0.35724676,
      "yLcPeriodic07" : 0.9427462,
      "yLcPeriodic08" : 0.5714184,
      "yLcPeriodic09" : 0.36414915,
      "yLcPeriodic10" : 0.55307907,
      "yLcPeriodic11" : 0.85959023,
      "yLcPeriodic12" : 0.8570715,
      "yLcPeriodic13" : 0.67991114,
      "yLcPeriodic14" : 0.22900993,
      "yLcPeriodic15" : 0.42736632,
      "yLcPeriodic16" : 0.9926862,
      "yLcPeriodic17" : 0.10752851,
      "yLcPeriodic18" : 0.13105816,
      "yLcPeriodic19" : 0.10357052,
      "yLcPeriodic20" : 0.38016438,
      "yLcPeriodic21" : 0.75248283,
      "yLcPeriodic22" : 0.27551895,
      "yLcPeriodic23" : 0.20368636,
      "yLcPeriodic24" : 0.16609824,
      "yLcPeriodic25" : 0.47873896,
      "yLcPeriodic26" : 0.54445124,
      "yLcPeriodic27" : 0.15423346,
      "yLcPeriodic28" : 0.32259214,
      "yLcPeriodic29" : 0.99278414,
      "yLcPeriodic30" : 0.35440147,
      "yLcPeriodic31" : 0.89919794,
      "yLcPeriodic32" : 0.12253082
  },
  "uLcNonPeriodic" : {
      "uLcNonPeriodic01" : 0.49429548,
      "uLcNonPeriodic02" : 0.28830326,
      "uLcNonPeriodic03" : 0.16618621,
      "uLcNonPeriodic04" : 0.5081264,
      "uLcNonPeriodic05" : 0.7498414,
      "uLcNonPeriodic06" : 0.841899,
      "uLcNonPeriodic07" : 0.67875755,
      "uLcNonPeriodic08" : 0.66557693,
      "uLcNonPeriodic09" : 0.53309387,
      "uLcNonPeriodic10" : 0.78087074,
      "uLcNonPeriodic11" : 0.28136778,
      "uLcNonPeriodic12" : 0.8863646,
      "uLcNonPeriodic13" : 0.7422267,
      "uLcNonPeriodic14" : 0.57719684,
      "uLcNonPeriodic15" : 0.48670387,
      "uLcNonPeriodic16" : 0.3449967,
      "uLcNonPeriodic17" : 0.7663699,
      "uLcNonPeriodic18" : 0.35850728,
      "uLcNonPeriodic19" : 0.50852096,
      "uLcNonPeriodic20" : 0.9323741
  },
  "gLcNonPeriodic" : {
      "gLcNonPeriodic01" : 0.26578587,
      "gLcNonPeriodic02" : 0.65338564,
      "gLcNonPeriodic03" : 0.64533436,
      "gLcNonPeriodic04" : 0.42569506,
      "gLcNonPeriodic05" : 0.6853463,
      "gLcNonPeriodic06" : 0.21320206,
      "gLcNonPeriodic07" : 0.26309478,
      "gLcNonPeriodic08" : 0.17447364,
      "gLcNonPeriodic09" : 0.16321427,
      "gLcNonPeriodic10" : 0.8562436,
      "gLcNonPeriodic11" : 0.47838533,
      "gLcNonPeriodic12" : 0.67369264,
      "gLcNonPeriodic13" : 0.66145986,
      "gLcNonPeriodic14" : 0.558745,
      "gLcNonPeriodic15" : 0.6686431,
      "gLcNonPeriodic16" : 0.7815195,
      "gLcNonPeriodic17" : 0.6718924,
      "gLcNonPeriodic18" : 0.99284637,
      "gLcNonPeriodic19" : 0.3843059,
      "gLcNonPeriodic20" : 0.49859238
  },
  "rLcNonPeriodic" : {
      "rLcNonPeriodic01" : 0.43220794,
      "rLcNonPeriodic02" : 0.116720974,
      "rLcNonPeriodic03" : 0.3358333,
      "rLcNonPeriodic04" : 0.7775859,
      "rLcNonPeriodic05" : 0.9244388,
      "rLcNonPeriodic06" : 0.9728243,
      "rLcNonPeriodic07" : 0.709231,
      "rLcNonPeriodic08" : 0.7096629,
      "rLcNonPeriodic09" : 0.058235705,
      "rLcNonPeriodic10" : 0.028524876,
      "rLcNonPeriodic11" : 0.70792645,
      "rLcNonPeriodic12" : 0.034974396,
      "rLcNonPeriodic13" : 0.7995737,
      "rLcNonPeriodic14" : 0.624249,
      "rLcNonPeriodic15" : 0.85096365,
      "rLcNonPeriodic16" : 0.03358662,
      "rLcNonPeriodic17" : 0.840299,
      "rLcNonPeriodic18" : 0.9865865,
      "rLcNonPeriodic19" : 0.86828524,
      "rLcNonPeriodic20" : 0.86828524,
  },
  "iLcNonPeriodic" : {
      "iLcNonPeriodic01" : 0.8572866,
      "iLcNonPeriodic02" : 0.32877123,
      "iLcNonPeriodic03" : 0.30743134,
      "iLcNonPeriodic04" : 0.37990117,
      "iLcNonPeriodic05" : 0.34845263,
      "iLcNonPeriodic06" : 0.5112901,
      "iLcNonPeriodic07" : 0.6269358,
      "iLcNonPeriodic08" : 0.7068065,
      "iLcNonPeriodic09" : 0.8497846,
      "iLcNonPeriodic10" : 0.14592028,
      "iLcNonPeriodic11" : 0.4585247,
      "iLcNonPeriodic12" : 0.941728,
      "iLcNonPeriodic13" : 0.33483768,
      "iLcNonPeriodic14" : 0.11690587,
      "iLcNonPeriodic15" : 0.37631267,
      "iLcNonPeriodic16" : 0.47233838,
      "iLcNonPeriodic17" : 0.9588649,
      "iLcNonPeriodic18" : 0.44485027,
      "iLcNonPeriodic19" : 0.84209245,
      "iLcNonPeriodic20" : 0.8563482
  },
  "zLcNonPeriodic" : {
      "zLcNonPeriodic01" : 0.58457404,
      "zLcNonPeriodic02" : 0.6935413,
      "zLcNonPeriodic03" : 0.25114423,
      "zLcNonPeriodic04" : 0.72851497,
      "zLcNonPeriodic05" : 0.47153544,
      "zLcNonPeriodic06" : 0.16014832,
      "zLcNonPeriodic07" : 0.48195457,
      "zLcNonPeriodic08" : 0.4441983,
      "zLcNonPeriodic09" : 0.7114319,
      "zLcNonPeriodic10" : 0.48165685,
      "zLcNonPeriodic11" : 0.90623796,
      "zLcNonPeriodic12" : 0.795557,
      "zLcNonPeriodic13" : 0.67538756,
      "zLcNonPeriodic14" : 0.5562037,
      "zLcNonPeriodic15" : 0.3827697,
      "zLcNonPeriodic16" : 0.034484804,
      "zLcNonPeriodic17" : 0.08092928,
      "zLcNonPeriodic18" : 0.16781157,
      "zLcNonPeriodic19" : 0.08720499,
      "zLcNonPeriodic20" : 0.30901492
  },
  "yLcNonPeriodic" : {
      "yLcNonPeriodic01" : 0.91610205,
      "yLcNonPeriodic02" : 0.32412225,
      "yLcNonPeriodic03" : 0.6839698,
      "yLcNonPeriodic04" : 0.37810862,
      "yLcNonPeriodic05" : 0.31635016,
      "yLcNonPeriodic06" : 0.389194,
      "yLcNonPeriodic07" : 0.96325207,
      "yLcNonPeriodic08" : 0.054047108,
      "yLcNonPeriodic09" : 0.86719507,
      "yLcNonPeriodic10" : 0.532832,
      "yLcNonPeriodic11" : 0.66048,
      "yLcNonPeriodic12" : 0.75425977,
      "yLcNonPeriodic13" : 0.549007,
      "yLcNonPeriodic14" : 0.095166266,
      "yLcNonPeriodic15" : 0.5118531,
      "yLcNonPeriodic16" : 0.60379595,
      "yLcNonPeriodic17" : 0.9612441,
      "yLcNonPeriodic18" : 0.42642683,
      "yLcNonPeriodic19" : 0.241912,
      "yLcNonPeriodic20" : 0.6263556
  },
  "nearbyObj1" : -8929902506652872202,
  "nearbyObj1Dist" : 0.6770757,
  "nearbyObj1LnP" : 0.15936244,
  "nearbyObj2" : 937855216345424587,
  "nearbyObj2Dist" : 0.06697929,
  "nearbyObj2LnP" : 0.2156207,
  "nearbyObj3" : 6015580302067737806,
  "nearbyObj3Dist" : 0.69879913,
  "nearbyObj3LnP" : 0.5303466,
  "flags" : -1386978521806683430
}
