import time
import requests
import json
import os
import logging
import sys 

# Get the API key from the config.py file
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.config import apiKey

# Setup logging
logging.basicConfig(level=logging.INFO)

# all at start of calendar year
sp500_symbols_2004 = ['A', 'AABA', 'AAPL', 'ABC', 'ABI', 'ABKFQ', 'ABS', 'ABT', 'ACV', 'ADBE', 'ADCT', 'ADI', 'ADM', 'ADP', 'ADSK', 'AEE', 'AEP', 'AES', 'AET', 'AFL', 'AGN', 'AIG', 'AIV', 'ALL', 'ALTR', 'AM', 'AMAT', 'AMCC', 'AMD', 'AMGN', 'AN', 'ANDW', 'ANTM', 'AON', 'APA', 'APC', 'APCC', 'APD', 'APOL', 'ARNC', 'ASH', 'ASO', 'AT', 'ATI', 'AV', 'AVP', 'AVY', 'AW', 'AWE', 'AXP', 'AYE', 'AZO', 'BA', 'BAC', 'BAX', 'BBBY', 'BBT', 'BBY', 'BC', 'BCR', 'BDK', 'BDX', 'BEAM', 'BEN', 'BF.B', 'BHGE', 'BIG', 'BIIB', 'BJS', 'BK', 'BLL', 'BLS', 'BMC', 'BMET', 'BMS', 'BMY', 'BNI', 'BOL', 'BR', 'BRCM', 'BSC', 'BSX', 'BUD', 'C', 'CA', 'CAG', 'CAH', 'CAR', 'CAT', 'CB', 'CBE', 'CBS', 'CCE', 'CCL', 'CCTYQ', 'CCU', 'CE', 'CEG', 'CF', 'CFC', 'CHIR', 'CI', 'CIEN', 'CIN', 'CINF', 'CL', 'CLX', 'CMA', 'CMCSA', 'CMI', 'CMS', 'CMVT', 'CNP', 'COF', 'COL', 'COP', 'COST', 'CPB', 'CPNLQ', 'CPWR', 'CR', 'CSCO', 'CSX', 'CTAS', 'CTB', 'CTL', 'CTX', 'CTXS', 'CVG', 'CVS', 'CVX', 'D', 'DALRQ', 'DCNAQ', 'DD', 'DDS', 'DE', 'DELL', 'DG', 'DGX', 'DHR', 'DIS', 'DJ', 'DLX', 'DOV', 'DOW', 'DPHIQ', 'DRI', 'DTE', 'DUK', 'DVN', 'DXC', 'DYN', 'EA', 'EBAY', 'EC', 'ECL', 'ED', 'EDS', 'EFX', 'EIX', 'EKDKQ', 'EMC', 'EMN', 'EMR', 'EOG', 'EOP', 'EP', 'EQR', 'ESRX', 'ETN', 'ETR', 'EXC', 'F', 'FBF', 'FCX', 'FDC', 'FDO', 'FDX', 'FE', 'FHN', 'FII', 'FISV', 'FITB', 'FLR', 'FMCC', 'FNMA', 'FRX', 'FTR', 'G', 'GAS', 'GD', 'GDT', 'GDW', 'GE', 'GENZ', 'GIS', 'GLK', 'GLW', 'GP', 'GPC', 'GPS', 'GR', 'GS', 'GT', 'GTW', 'GWW', 'HAL', 'HAS', 'HBAN', 'HCA', 'HCR', 'HD', 'HES', 'HET', 'HIG', 'HLT', 'HMA', 'HNZ', 'HOG', 'HON', 'HOT', 'HPC', 'HPQ', 'HRB', 'HSH', 'HSY', 'HUM', 'IBM', 'IFF', 'IGT', 'INTC', 'INTU', 'IP', 'IPG', 'IR', 'ITT', 'ITW', 'JAVA', 'JBL', 'JCI', 'JCP', 'JHF', 'JNJ', 'JNS', 'JNY', 'JP', 'JPM', 'JWN', 'K', 'KATE', 'KBH', 'KEY', 'KG', 'KLAC', 'KMB', 'KMG', 'KMI', 'KO', 'KR', 'KRB', 'KRI', 'KSE', 'KSS', 'L', 'LB', 'LEG', 'LEHMQ', 'LLTC', 'LLY', 'LMT', 'LNC', 'LOW', 'LPX', 'LSI', 'LU', 'LUV', 'LXK', 'M', 'MAR', 'MAS', 'MAT', 'MAY', 'MBI', 'MCD', 'MCK', 'MCO', 'MDP', 'MDT', 'MEDI', 'MEL', 'MER', 'MERQ', 'MET', 'MHS', 'MI', 'MIL', 'MKC', 'MMC', 'MMM', 'MO', 'MOLX', 'MON', 'MRK', 'MRO', 'MS', 'MSFT', 'MSI', 'MTG', 'MTLQQ', 'MU', 'MWV', 'MWW', 'MXIM', 'MYG', 'NAV', 'NBR', 'NCC', 'NCR', 'NE', 'NEE', 'NEM', 'NFB', 'NI', 'NKE', 'NOC', 'NOVL', 'NSC', 'NSM', 'NTAP', 'NTRS', 'NUE', 'NVDA', 'NVLS', 'NWL', 'NXTL', 'NYT', 'ODP', 'OMC', 'OMX', 'ONE', 'ORCL', 'OXY', 'PAYX', 'PBG', 'PBI', 'PCAR', 'PCG', 'PCL', 'PCS', 'PD', 'PEG', 'PEP', 'PFE', 'PFG', 'PG', 'PGL', 'PGN', 'PGR', 'PH', 'PHM', 'PKI', 'PLD', 'PLL', 'PMCS', 'PNC', 'PNW', 'PPG', 'PPL', 'PRU', 'PSFT', 'PTC', 'PTV', 'PVN', 'PWER', 'PX', 'Q', 'QCOM', 'QLGC', 'R', 'RAI', 'RBK', 'RDC', 'RF', 'RHI', 'RIG', 'ROH', 'ROK', 'RRD', 'RSHCQ', 'RTN', 'RX', 'S', 'SAF', 'SANM', 'SBL', 'SBUX', 'SCHW', 'SDS', 'SEBL', 'SEE', 'SFA', 'SGP', 'SHW', 'SIAL', 'SLB', 'SLM', 'SLR', 'SNA', 'SNV', 'SO', 'SOTR', 'SPG', 'SPGI', 'SPLS', 'SRE', 'STI', 'STJ', 'STT', 'SUN', 'SVU', 'SWK', 'SWY', 'SYK', 'SYMC', 'SYY', 'T', 'TAP', 'TE', 'TEK', 'TER', 'TGNA', 'TGT', 'THC', 'TIF', 'TIN', 'TJX', 'TLAB', 'TMK', 'TMO', 'TNB', 'TOY', 'TRB', 'TROW', 'TRV', 'TSG', 'TT', 'TUP', 'TWX', 'TXN', 'TXT', 'TXU', 'UCL', 'UIS', 'UNH', 'UNM', 'UNP', 'UPC', 'UPS', 'USB', 'UST', 'UTX', 'UVN', 'VFC', 'VIAV', 'VMC', 'VRTS', 'VSTNQ', 'VZ', 'WAMUQ', 'WAT', 'WB', 'WBA', 'WEN', 'WFC', 'WHR', 'WLP', 'WM', 'WMB', 'WMT', 'WNDXQ', 'WOR', 'WWY', 'WY', 'WYE', 'X', 'XEL', 'XL', 'XLNX', 'XOM', 'XRX', 'YUM', 'ZBH', 'ZION']
sp500_symbols_2014 = ['A', 'AABA', 'AAPL', 'ABBV', 'ABC', 'ABT', 'ACN', 'ADBE', 'ADI', 'ADM', 'ADP', 'ADS', 'ADSK', 'ADT', 'AEE', 'AEP', 'AES', 'AET', 'AFL', 'AGN', 'AIG', 'AIV', 'AIZ', 'AKAM', 'ALL', 'ALLE', 'ALTR', 'ALXN', 'AMAT', 'AME', 'AMGN', 'AMP', 'AMT', 'AMZN', 'AN', 'ANDV', 'ANTM', 'AON', 'APA', 'APC', 'APD', 'APH', 'APTV', 'ARG', 'ARNC', 'ATI', 'AVB', 'AVP', 'AVY', 'AXP', 'AZO', 'BA', 'BAC', 'BAX', 'BBBY', 'BBT', 'BBY', 'BCR', 'BDX', 'BEAM', 'BEN', 'BF.B', 'BHGE', 'BIIB', 'BK', 'BKNG', 'BLK', 'BLL', 'BMS', 'BMY', 'BRCM', 'BRK.B', 'BSX', 'BTUUQ', 'BWA', 'BXP', 'C', 'CA', 'CAG', 'CAH', 'CAM', 'CAT', 'CB', 'CBRE', 'CBS', 'CCE', 'CCI', 'CCL', 'CELG', 'CERN', 'CF', 'CFN', 'CHK', 'CHRW', 'CI', 'CINF', 'CL', 'CLF', 'CLX', 'CMA', 'CMCSA', 'CME', 'CMG', 'CMI', 'CMS', 'CNP', 'CNX', 'COF', 'COG', 'COL', 'COP', 'COST', 'COV', 'CPB', 'CRM', 'CSCO', 'CSX', 'CTAS', 'CTL', 'CTSH', 'CTXS', 'CVC', 'CVS', 'CVX', 'D', 'DAL', 'DD', 'DE', 'DFS', 'DG', 'DGX', 'DHI', 'DHR', 'DIS', 'DISCA', 'DLTR', 'DNB', 'DNR', 'DO', 'DOV', 'DOW', 'DRI', 'DTE', 'DTV', 'DUK', 'DVA', 'DVN', 'DXC', 'EA', 'EBAY', 'ECL', 'ED', 'EFX', 'EIX', 'EL', 'EMC', 'EMN', 'EMR', 'EOG', 'EQR', 'EQT', 'ES', 'ESRX', 'ESV', 'ETFC', 'ETN', 'ETR', 'EW', 'EXC', 'EXPD', 'EXPE', 'F', 'FAST', 'FB', 'FCX', 'FDO', 'FDX', 'FE', 'FFIV', 'FIS', 'FISV', 'FITB', 'FLIR', 'FLR', 'FLS', 'FMC', 'FOSL', 'FOXA', 'FRX', 'FSLR', 'FTI', 'FTR', 'GAS', 'GD', 'GE', 'GGP', 'GHC', 'GILD', 'GIS', 'GLW', 'GM', 'GME', 'GNW', 'GOOGL', 'GPC', 'GPS', 'GRMN', 'GS', 'GT', 'GWW', 'HAL', 'HAR', 'HAS', 'HBAN', 'HCBK', 'HCP', 'HD', 'HES', 'HIG', 'HOG', 'HON', 'HOT', 'HP', 'HPQ', 'HRB', 'HRL', 'HRS', 'HSP', 'HST', 'HSY', 'HUM', 'IBM', 'ICE', 'IFF', 'IGT', 'INTC', 'INTU', 'IP', 'IPG', 'IR', 'IRM', 'ISRG', 'ITW', 'IVZ', 'JBL', 'JCI', 'JEC', 'JEF', 'JNJ', 'JNPR', 'JOY', 'JPM', 'JWN', 'K', 'KDP', 'KEY', 'KIM', 'KLAC', 'KMB', 'KMI', 'KMX', 'KO', 'KORS', 'KR', 'KRFT', 'KSS', 'KSU', 'L', 'LB', 'LEG', 'LEN', 'LH', 'LIFE', 'LLL', 'LLTC', 'LLY', 'LM', 'LMT', 'LNC', 'LO', 'LOW', 'LRCX', 'LSI', 'LUV', 'LYB', 'M', 'MA', 'MAC', 'MAR', 'MAS', 'MAT', 'MCD', 'MCHP', 'MCK', 'MCO', 'MDLZ', 'MDT', 'MET', 'MHK', 'MJN', 'MKC', 'MMC', 'MMM', 'MNST', 'MO', 'MON', 'MOS', 'MPC', 'MRK', 'MRO', 'MS', 'MSFT', 'MSI', 'MTB', 'MU', 'MUR', 'MWV', 'MYL', 'NBL', 'NBR', 'NDAQ', 'NE', 'NEE', 'NEM', 'NFLX', 'NFX', 'NI', 'NKE', 'NLSN', 'NOC', 'NOV', 'NRG', 'NSC', 'NTAP', 'NTRS', 'NUE', 'NVDA', 'NWL', 'NWSA', 'OI', 'OKE', 'OMC', 'ORCL', 'ORLY', 'OXY', 'PAYX', 'PBCT', 'PBI', 'PCAR', 'PCG', 'PCL', 'PCP', 'PDCO', 'PEG', 'PEP', 'PETM', 'PFE', 'PFG', 'PG', 'PGR', 'PH', 'PHM', 'PKI', 'PLD', 'PLL', 'PM', 'PNC', 'PNR', 'PNW', 'POM', 'PPG', 'PPL', 'PRGO', 'PRU', 'PSA', 'PSX', 'PVH', 'PWR', 'PX', 'PXD', 'QCOM', 'QEP', 'R', 'RAI', 'RDC', 'REGN', 'RF', 'RHI', 'RHT', 'RIG', 'RL', 'ROK', 'ROP', 'ROST', 'RRC', 'RSG', 'RTN', 'SBUX', 'SCG', 'SCHW', 'SE', 'SEE', 'SHW', 'SIAL', 'SJM', 'SLB', 'SLM', 'SNA', 'SNDK', 'SNI', 'SO', 'SPG', 'SPGI', 'SPLS', 'SRCL', 'SRE', 'STI', 'STJ', 'STT', 'STX', 'STZ', 'SWK', 'SWN', 'SWY', 'SYK', 'SYMC', 'SYY', 'T', 'TAP', 'TDC', 'TE', 'TEG', 'TEL', 'TGNA', 'TGT', 'THC', 'TIF', 'TJX', 'TMK', 'TMO', 'TPR', 'TRIP', 'TROW', 'TRV', 'TSN', 'TSS', 'TWC', 'TWX', 'TXN', 'TXT', 'UNH', 'UNM', 'UNP', 'UPS', 'URBN', 'USB', 'UTX', 'V', 'VAR', 'VFC', 'VIAB', 'VLO', 'VMC', 'VNO', 'VRSN', 'VRTX', 'VTR', 'VZ', 'WAT', 'WBA', 'WDC', 'WEC', 'WELL', 'WFC', 'WFM', 'WHR', 'WIN', 'WM', 'WMB', 'WMT', 'WPX', 'WU', 'WY', 'WYND', 'WYNN', 'X', 'XEL', 'XL', 'XLNX', 'XOM', 'XRAY', 'XRX', 'XYL', 'YUM', 'ZBH', 'ZION', 'ZTS']
sp500_symbols_2024 = ['A', 'AAL', 'AAPL', 'ABBV', 'ABNB', 'ABT', 'ACGL', 'ACN', 'ADBE', 'ADI', 'ADM', 'ADP', 'ADSK', 'AEE', 'AEP', 'AES', 'AFL', 'AIG', 'AIZ', 'AJG', 'AKAM', 'ALB', 'ALGN', 'ALL', 'ALLE', 'AMAT', 'AMCR', 'AMD', 'AME', 'AMGN', 'AMP', 'AMT', 'AMZN', 'ANET', 'ANSS', 'AON', 'AOS', 'APA', 'APD', 'APH', 'APTV', 'ARE', 'ATO', 'AVB', 'AVGO', 'AVY', 'AWK', 'AXON', 'AXP', 'AZO', 'BA', 'BAC', 'BALL', 'BAX', 'BBWI', 'BBY', 'BDX', 'BEN', 'BF.B', 'BG', 'BIIB', 'BIO', 'BK', 'BKNG', 'BKR', 'BLDR', 'BLK', 'BMY', 'BR', 'BRK.B', 'BRO', 'BSX', 'BWA', 'BX', 'BXP', 'C', 'CAG', 'CAH', 'CARR', 'CAT', 'CB', 'CBOE', 'CBRE', 'CCI', 'CCL', 'CDAY', 'CDNS', 'CDW', 'CE', 'CEG', 'CF', 'CFG', 'CHD', 'CHRW', 'CHTR', 'CI', 'CINF', 'CL', 'CLX', 'CMA', 'CMCSA', 'CME', 'CMG', 'CMI', 'CMS', 'CNC', 'CNP', 'COF', 'COO', 'COP', 'COR', 'COST', 'CPB', 'CPRT', 'CPT', 'CRL', 'CRM', 'CSCO', 'CSGP', 'CSX', 'CTAS', 'CTLT', 'CTRA', 'CTSH', 'CTVA', 'CVS', 'CVX', 'CZR', 'D', 'DAL', 'DD', 'DE', 'DFS', 'DG', 'DGX', 'DHI', 'DHR', 'DIS', 'DLR', 'DLTR', 'DOV', 'DOW', 'DPZ', 'DRI', 'DTE', 'DUK', 'DVA', 'DVN', 'DXCM', 'EA', 'EBAY', 'ECL', 'ED', 'EFX', 'EG', 'EIX', 'EL', 'ELV', 'EMN', 'EMR', 'ENPH', 'EOG', 'EPAM', 'EQIX', 'EQR', 'EQT', 'ES', 'ESS', 'ETN', 'ETR', 'ETSY', 'EVRG', 'EW', 'EXC', 'EXPD', 'EXPE', 'EXR', 'F', 'FANG', 'FAST', 'FCX', 'FDS', 'FDX', 'FE', 'FFIV', 'FI', 'FICO', 'FIS', 'FITB', 'FLT', 'FMC', 'FOX', 'FOXA', 'FRT', 'FSLR', 'FTNT', 'FTV', 'GD', 'GE', 'GEHC', 'GEN', 'GILD', 'GIS', 'GL', 'GLW', 'GM', 'GNRC', 'GOOG', 'GOOGL', 'GPC', 'GPN', 'GRMN', 'GS', 'GWW', 'HAL', 'HAS', 'HBAN', 'HCA', 'HD', 'HES', 'HIG', 'HII', 'HLT', 'HOLX', 'HON', 'HPE', 'HPQ', 'HRL', 'HSIC', 'HST', 'HSY', 'HUBB', 'HUM', 'HWM', 'IBM', 'ICE', 'IDXX', 'IEX', 'IFF', 'ILMN', 'INCY', 'INTC', 'INTU', 'INVH', 'IP', 'IPG', 'IQV', 'IR', 'IRM', 'ISRG', 'IT', 'ITW', 'IVZ', 'J', 'JBHT', 'JBL', 'JCI', 'JKHY', 'JNJ', 'JNPR', 'JPM', 'K', 'KDP', 'KEY', 'KEYS', 'KHC', 'KIM', 'KLAC', 'KMB', 'KMI', 'KMX', 'KO', 'KR', 'KVUE', 'L', 'LDOS', 'LEN', 'LH', 'LHX', 'LIN', 'LKQ', 'LLY', 'LMT', 'LNT', 'LOW', 'LRCX', 'LULU', 'LUV', 'LVS', 'LW', 'LYB', 'LYV', 'MA', 'MAA', 'MAR', 'MAS', 'MCD', 'MCHP', 'MCK', 'MCO', 'MDLZ', 'MDT', 'MET', 'META', 'MGM', 'MHK', 'MKC', 'MKTX', 'MLM', 'MMC', 'MMM', 'MNST', 'MO', 'MOH', 'MOS', 'MPC', 'MPWR', 'MRK', 'MRNA', 'MRO', 'MS', 'MSCI', 'MSFT', 'MSI', 'MTB', 'MTCH', 'MTD', 'MU', 'NCLH', 'NDAQ', 'NDSN', 'NEE', 'NEM', 'NFLX', 'NI', 'NKE', 'NOC', 'NOW', 'NRG', 'NSC', 'NTAP', 'NTRS', 'NUE', 'NVDA', 'NVR', 'NWS', 'NWSA', 'NXPI', 'O', 'ODFL', 'OKE', 'OMC', 'ON', 'ORCL', 'ORLY', 'OTIS', 'OXY', 'PANW', 'PARA', 'PAYC', 'PAYX', 'PCAR', 'PCG', 'PEAK', 'PEG', 'PEP', 'PFE', 'PFG', 'PG', 'PGR', 'PH', 'PHM', 'PKG', 'PLD', 'PM', 'PNC', 'PNR', 'PNW', 'PODD', 'POOL', 'PPG', 'PPL', 'PRU', 'PSA', 'PSX', 'PTC', 'PWR', 'PXD', 'PYPL', 'QCOM', 'QRVO', 'RCL', 'REG', 'REGN', 'RF', 'RHI', 'RJF', 'RL', 'RMD', 'ROK', 'ROL', 'ROP', 'ROST', 'RSG', 'RTX', 'RVTY', 'SBAC', 'SBUX', 'SCHW', 'SHW', 'SJM', 'SLB', 'SNA', 'SNPS', 'SO', 'SPG', 'SPGI', 'SRE', 'STE', 'STLD', 'STT', 'STX', 'STZ', 'SWK', 'SWKS', 'SYF', 'SYK', 'SYY', 'T', 'TAP', 'TDG', 'TDY', 'TECH', 'TEL', 'TER', 'TFC', 'TFX', 'TGT', 'TJX', 'TMO', 'TMUS', 'TPR', 'TRGP', 'TRMB', 'TROW', 'TRV', 'TSCO', 'TSLA', 'TSN', 'TT', 'TTWO', 'TXN', 'TXT', 'TYL', 'UAL', 'UBER', 'UDR', 'UHS', 'ULTA', 'UNH', 'UNP', 'UPS', 'URI', 'USB', 'V', 'VFC', 'VICI', 'VLO', 'VLTO', 'VMC', 'VRSK', 'VRSN', 'VRTX', 'VTR', 'VTRS', 'VZ', 'WAB', 'WAT', 'WBA', 'WBD', 'WDC', 'WEC', 'WELL', 'WFC', 'WHR', 'WM', 'WMB', 'WMT', 'WRB', 'WRK', 'WST', 'WTW', 'WY', 'WYNN', 'XEL', 'XOM', 'XRAY', 'XYL', 'YUM', 'ZBH', 'ZBRA', 'ZION', 'ZTS']
sp500_symbols_unique = sorted(list(set(sp500_symbols_2004 + sp500_symbols_2014 + sp500_symbols_2024)))

# Use an environment variable or a safer way to specify paths
earnings_file = os.path.join(os.getenv('DATA_DIR', '.'), 'EarningsTest.json')
time_series_file = os.path.join(os.getenv('DATA_DIR', '.'), 'TimeSeriesTest.json')
sma_file_50 = os.path.join(os.getenv('DATA_DIR', '.'), 'SmaTest50.json')
sma_file_200 = os.path.join(os.getenv('DATA_DIR', '.'), 'SmaTest200.json')

for symbol in sp500_symbols_unique:
	api_function1 = "EARNINGS"
	url1 = f"https://www.alphavantage.co/query?function={api_function1}&symbol={symbol}&apikey={apiKey}"
	logging.info(f"Fetching {api_function1} data for {symbol}")
	r1 = requests.get(url1)
	if r1.status_code == 200:
		with open(earnings_file, "a") as fileToPrintTo:
			json.dump(r1.json(), fileToPrintTo)
			fileToPrintTo.write("\n")
		logging.info(f"Successfully fetched and saved {api_function1} data for {symbol}")
	else:
		logging.error(f"Failed to fetch {api_function1} data for {symbol}")

	api_function2 = "TIME_SERIES_DAILY_ADJUSTED"
	url2 = f"https://www.alphavantage.co/query?function={api_function2}&symbol={symbol}&apikey={apiKey}"
	logging.info(f"Fetching {api_function2} data for {symbol}")
	r2 = requests.get(url2)
	if r2.status_code == 200:
		with open(time_series_file, "a") as fileToPrintTo:
			json.dump(r2.json(), fileToPrintTo)
			fileToPrintTo.write("\n")
		logging.info(f"Successfully fetched and saved {api_function2} data for {symbol}")
	else:
		logging.error(f"Failed to fetch {api_function2} data for {symbol}")

	api_function3 = "SMA"
	url3 = f"https://www.alphavantage.co/query?function={api_function3}&symbol={symbol}&interval=daily&time_period=50&series_type=open&apikey={apiKey}"
	logging.info(f"Fetching {api_function3} (50-day) data for {symbol}")
	r3 = requests.get(url3)
	if r3.status_code == 200:
		with open(sma_file_50, "a") as fileToPrintTo:
			json.dump(r3.json(), fileToPrintTo)
			fileToPrintTo.write("\n")
		logging.info(f"Successfully fetched and saved {api_function3} (50-day) data for {symbol}")
	else:
		logging.error(f"Failed to fetch {api_function3} (50-day) data for {symbol}")

	api_function4 = "SMA"
	url4 = f"https://www.alphavantage.co/query?function={api_function4}&symbol={symbol}&interval=daily&time_period=200&series_type=open&apikey={apiKey}"
	logging.info(f"Fetching {api_function4} (200-day) data for {symbol}")
	r4 = requests.get(url4)
	if r4.status_code == 200:
		with open(sma_file_200, "a") as fileToPrintTo:
			json.dump(r4.json(), fileToPrintTo)
			fileToPrintTo.write("\n")
		logging.info(f"Successfully fetched and saved {api_function4} (200-day) data for {symbol}")
	else:
		logging.error(f"Failed to fetch {api_function4} (200-day) data for {symbol}")
	
	# sleep for 3 seconds to avoid hitting the API rate limit
	time.sleep(4)

# Loop through the following functions for the API
functions = ["UNEMPLOYMENT", "GDP", "CPI", "TREASURY_YIELD", "REAL_GDP", "FEDERAL_FUNDS_RATE", "INFLATION"]
for function in functions:
	url = f"https://www.alphavantage.co/query?function={function}&apikey={apiKey}"
	logging.info(f"Fetching {function} data")
	r = requests.get(url)
	if r.status_code == 200:
		with open(os.path.join(os.getenv('DATA_DIR', '.'), f"{function}.json"), "a") as fileToPrintTo:
			json.dump(r.json(), fileToPrintTo)
			fileToPrintTo.write("\n")
		logging.info(f"Successfully fetched and saved {function} data")
	else:
		logging.error(f"Failed to fetch {function} data")