import os

MEDICAL_ABBREVIATIONS = {
    # 1. ICU / CCU / ER / Resuscitation / Trauma (Massively Expanded)
    "icu", "ccu", "micu", "sicu", "ticu", "nicu", "picu", "eicu", "er", "ed", "or", "pacu",
    "mv", "cpap", "bipap", "ra", "nc", "fm", "nrm", "ett", "trach", "abg", "vbg", "cpr", 
    "dnr", "dni", "dama", "ama", "peep", "saodes", "spo2", "fio2", "map", "cvp", "icp", 
    "paox", "paco2", "hft", "hfo", "ards", "mods", "sirs", "gcs", "avpu", "pef", "fvc", 
    "ecmo", "iabp", "rosc", "fast", "efast", "atls", "acls", "pals", "bls", "mtp", "rsi", 
    "gsw", "mva", "mvc", "doa", "lwbs", "rass", "io", "cco", "scvo2", "svo2", "vad", 
    "lvad", "rvad", "bivad", "prbc", "ffp", "cryo", "teq", "rotem", "cvvh", "cvvhd", 
    "cvvhdf", "sled", "vasop", "etco2", "niv", "nppv", "atn", "rta", "loc", "ams", 
    "bcls", "nrp", "ecls", "pcea", "cpp", "cbf", "camicu", "impella", "ebl",

    # 2. Internal Medicine / Cardiology / Nephrology / Pulmonology (Massively Expanded)
    "ami", "chf", "copd", "ckd", "aki", "cva", "dka", "htn", "dm", "pe", "dvt", "cad", 
    "afib", "svt", "vt", "vfib", "lad", "esrd", "gfr", "crrt", "hhd", "sle", "tbd", "gi", 
    "gerd", "ibd", "ibs", "tia", "hhs", "acs", "pad", "pvd", "ihd", "lbbb", "rbbb", "st", 
    "nst", "nstemi", "stemi", "hcm", "dcm", "rcm", "ie", "paf", "wpw", "tte", "tee", 
    "pfo", "icd", "crt", "pci", "ptca", "tips", "ercp", "mrcp", "osa", "ild", "pft", 
    "vte", "jvp", "pnd", "doe", "sob", "hfref", "hfpef", "ahf", "di", "siadh", "tga", 
    "tof", "phtn", "pah", "sss", "avb", "lafb", "lpfb", "pvc", "pac", "gn", "fsgs", 
    "mcd", "mpgn", "pkd", "adpkd", "crf", "arf", "dlco", "fev1", "tlc", "rv", "frc", 
    "chs", "ohs", "ipf", "uip", "nsip", "cor-p", "pjrt", "ivcd", "renovasc",

    # 3. Surgery / Orthopedics / Anesthesia (Massively Expanded)
    "orif", "crif", "exfix", "tka", "tha", "app", "chole", "nsurg", "cts", "lsc", "rom", 
    "arom", "cabg", "prom", "fx", "dx", "cx", "tx", "hx", "sx", "bx", "px", "qx", "rx", 
    "avf", "avg", "eor", "pod", "bka", "aka", "subqd", "eua", "fna", "ta", "lh", "tah", 
    "bso", "turp", "vats", "lap", "iandd", "sci", "tbi", "preop", "postop", "tramer", 
    "surg", "ortho", "evac", "rupt", "perf", "rct", "acl", "pcl", "mcl", "lcl", "ddd", 
    "tja", "hemi", "amp", "crna", "mac", "ga", "cnb", "pnb", "pca", "ponv", "apr", 
    "lar", "sleeve", "tcar", "cea", "tma", "ray", "arthro", "osteom", "fasci", "debride", 
    "exlap", "lapar", "thoraco", "whipple", "puestow",

    # 4. Pediatrics / OB-GYN (Massively Expanded)
    "asd", "vsd", "pda", "rsv", "fgr", "iugr", "pcos", "pid", "lscs", "bpd", "rds", 
    "ttn", "ne", "ivh", "rop", "mas", "gdm", "ivf", "iui", "lmp", "edd", "ga", "vbac", 
    "pme", "sga", "lga", "fhr", "ctg", "hmd", "fsh", "hcg", "sids", "suid", "apgar", 
    "torch", "prom", "pprom", "gbs", "csec", "cs", "nsd", "svd", "iufd", "g", "p", "a", 
    "mec", "nichd", "cchd", "stq", "grav", "para", "ab", "ptb", "aga", "hellp", 
    "eclampsia", "pree", "pap", "colpo", "leep", "hrt", "ocp", "larc", "iud", "ius", 
    "cvs", "amnio", "nipt", "bpp", "pph", "tolac", "fht", "pms", "pmdd", "leio",

    # 5. Oncology / Hematology (Massively Expanded)
    "all", "aml", "cll", "cml", "dlbcl", "mets", "chemo", "rad", "xrt", "tmt", "bmt", 
    "hsct", "ptld", "gvhd", "dic", "tpa", "fdb", "fn", "anc", "itp", "ttp", "cca", 
    "hcc", "crc", "nsclc", "sclc", "brca", "pnet", "rt", "tnm", "pt", "ptm", "mds", 
    "mpn", "pv", "et", "pmf", "hl", "nhl", "mm", "mgus", "er", "pr", "her2", "tnbc", 
    "mibc", "rcc", "tcc", "psa", "dre", "fap", "gist", "net", "melanoma", "bcc", "scc", 
    "cup", "ecog", "kps", "cart", "vth", "vwd", "tt", "ddimer", "bcrabl", "kras", "braf",

    # 6. Neurology / Psychiatry (Massively Expanded)
    "als", "ms", "sz", "se", "eeg", "emg", "ncs", "lp", "sah", "sdh", "edh", "ich", 
    "mdd", "gad", "ptsd", "ocd", "adhd", "bpd", "szd", "cp", "tia", "cva", "mri", "fhm", 
    "cte", "ect", "cbt", "dbt", "mmse", "moca", "nl", "wfl", "mtbi", "conc", "avm", 
    "cis", "rrms", "ppms", "spms", "nmo", "mg", "gbs", "cidp", "sma", "pd", "hd", 
    "dbs", "ad", "vad", "ftd", "lbd", "mci", "pnes", "vep", "ssep", "psg", "ssri", 
    "snri", "tca", "maoi", "sga", "fga", "eps", "td", "nms", "tms", "asd", "fasd", "dt",

    # 7. Infectious Diseases (Massively Expanded)
    "tb", "hiv", "aids", "hcv", "hbv", "hpv", "hsv", "cmv", "ebv", "mrsa", "vre", "esbl", 
    "cdiff", "uti", "uri", "lrti", "std", "sti", "sars", "mers", "covid", "sirs", "fu", 
    "fuo", "cands", "oandp", "afb", "vdrl", "rpr", "pcr", "hai", "cai", "vap", "hap", 
    "cap", "clabsi", "cauti", "ssi", "sepsis", "mdr", "xdr", "pdr", "mssa", "visa", 
    "vrsa", "cre", "kpc", "hpylori", "lyme", "rmsf", "zika", "dengue", "ebola", "h1n1", 
    "vzv", "prep", "pep", "art", "haart", "mdrtb", "mac", "pcp", "toxo", "malaria",

    # 8. Ophthalmology / ENT (Massively Expanded)
    "od", "os", "ou", "iop", "amd", "cat", "glx", "eom", "ent", "tm", "aom", "ome",'mi',
    "tonsil", "tna", "perrl", "perrla", "eomi", "va", "vf", "myopia", "hyperopia", 
    "astig", "presby", "glauc", "poag", "pacg", "nvamd", "dr", "pdr", "npdr", "rvo", 
    "crao", "crvo", "rd", "uveitis", "lasik", "prk", "iol", "asom", "csom", "oe", "ar", 
    "nar", "fess", "septo", "baha", "ci", "snhl", "chl", "mhl", "bppv", "md", "vn", "tmj",

    # 9. Nutrition / Fluids / Gastroenterology (Massively Expanded)
    "npo", "ngt", "tpn", "ppn", "dat", "nas", "ada", "fl", "ns", "lr", "d5w", "d5ns", 
    "d10w", "d5lr", "kcl", "na", "cl", "mg", "ca", "po4", "ogt", "peg", "njt", "gtube", 
    "jtube", "nausea", "nvd", "bm", "brbpr", "ugi", "lgi", "tft", "ibw", "bmr", "ree", 
    "mnt", "pej", "gerd", "eoe", "pud", "du", "gu", "ugib", "lgib", "sbp", "he", "hrs", 
    "nafld", "nash", "masld", "ald", "hav", "hev", "aih", "pbc", "psc", "cd", "uc", 
    "ibsd", "ibsc", "sibo", "celiac", "fap",

    # 10. Pharmacology / Prescription / Routes (Massively Expanded)
    "stat", "prn", "qid", "tid", "bid", "qd", "qod", "qam", "qpm", "qhs", "ac", "pc", 
    "adlib", "nq", "iv", "im", "sc", "sq", "po", "sl", "pr", "pv", "inh", "neb", "top", 
    "ivpb", "kvo", "meq", "mcg", "gtt", "ung", "supp", "buc", "mdi", "dpi", "transderm", 
    "ivp", "io", "epidural", "it", "q4h", "q6h", "q8h", "q12h", "asdir", "ud", "nr", 
    "daw", "dnc", "rtc", "gtts", "susp", "syr", "elix", "tab", "cap", "amp", "vial",

    # 11. General / Diagnostics / Vital Signs / Labs (Massively Expanded)
    "cbc", "bmp", "cmp", "lft", "rft", "pt", "ptt", "inr", "crp", "esr", "ecg", "ekg", 
    "cxr", "ct", "mri", "us", "echo", "bp", "hr", "rr", "t", "wt", "ht", "bmi", "bsa", 
    "fbs", "rbs", "hba1c", "tsh", "ft4", "ft3", "troponin", "ckmb", "bnp", "ldh", "ast", 
    "alt", "alp", "bun", "cr", "egfr", "wbc", "rbc", "hgb", "hct", "mcv", "mch", "plt", 
    "ua", "kub", "muga", "dexa", "pet", "hx", "cc", "hpi", "pmh", "psh", "fh", "sh", 
    "ros", "pe", "ddx", "spo2", "sao2", "pao2", "pco2", "tmax", "uo", "ins", "outs", 
    "mchc", "rdw", "mpv", "diff", "alc", "amc", "co2", "hco3", "ag", "phos", "ggt", 
    "tbili", "dbili", "tp", "cp", "ck", "ntprobnp", "hscrp", "a1c", "fbg", "ogtt", "abx",

    # 12. Anatomy / Physical Exam / Charting (NEW)
    "llq", "luq", "rlq", "ruq", "abd", "cv", "cns", "pns", "ans", "heent", "msk", "gyn", 
    "ob", "derm", "rheum", "endo", "wnl", "cva", "jvd", "pmi", "rrr", "cta", "bs", 
    "ntnd", "rom", "csm", "nad", "aox3", "aox4", "hnp", "lmp", "dtrs", "lue", "rue", 
    "lle", "rle", "bl", "rt", "lt", "wfl", "nl"
}