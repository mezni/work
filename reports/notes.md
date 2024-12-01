-- ##########################################
-- AnneeMois = TransactionGL[Annee] & "-" & FORMAT(TransactionGL[Mois], "00")
GLDate = 
    DATE(
        TransactionGL[Annee], 
        TransactionGL[Mois], 
        1  -- Set to the first day of the month
)

CalendrierFinancier = 
    ADDCOLUMNS(
        FILTER(
            CALENDAR(DATE(2020, 1, 1), DATE(2025, 12, 31)),
            DAY([Date]) = 1
        ),
        "AnneeFinanciere", 
            VAR Annee_Fin_Calc = 
                IF (
                    MONTH([Date]) >= 4, 
                    RIGHT(YEAR([Date]) , 2) & RIGHT(YEAR([Date])+1, 2),
                    RIGHT(YEAR([Date])-1, 2) & RIGHT(YEAR([Date]), 2)
                )
            RETURN Annee_Fin_Calc,
        "AnneeMois", 
            VAR AnneeMois = FORMAT([Date], "YYYY") & "-" & FORMAT([Date], "MM")
            RETURN AnneeMois
)


-- TOT
TOT_Reel_FY = SUM(TransactionGL[MontantTrx]) 

-- YTD
YTD_Reel_FY = 
    TOTALYTD(
        SUM(TransactionGL[MontantTrx]), 
        CalendrierFinancier[Date], 
        "31/03"  
)

-- LAST YEAR
LY_Reel_FY = 
    CALCULATE(
        SUM(TransactionGL[MontantTrx]),
        DATEADD(CalendrierFinancier[Date],-1,YEAR)
)


-- YOY
YOY_Reel_FY = 
IF (
    [TOT_Reel_FY] <> 0 && [LY_Reel_FY]<> 0,
    [TOT_Reel_FY] - [LY_Reel_FY],
    BLANK()
)

-- YOY percentage 
YOY_Reel_PERC = 
DIVIDE (
    [YOY_Reel_FY],
    [TOT_Reel_FY] 
)