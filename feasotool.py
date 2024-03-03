import streamlit as st
import os
import pandas as pd



def add_bg_image():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://github.com/josh23josh23/pic/blob/main/SUV4-ezgif.com-effects%20(2).gif?raw=true");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }

        /* Ensure the main content is clearly visible by providing a semi-transparent background */
        .main .block-container {
            background-color: rgba(0, 0, 0, 0.65); /* Adjust transparency to ensure readability */
            color: white; /* This makes the text color white, ensuring it stands out */
            border-radius: 10px; /* Optional: Adds rounded corners for a more polished look */
            padding: 2rem; /* Adds padding inside the container for better layout */
            margin-top: 3rem; /* Adds margin at the top for spacing */
            box-shadow: 0 4px 8px rgba(0,0,0,0.1); /* Optional: Adds a subtle shadow for depth */
        }

        /* Center the image in the top center of the page and increase its size */
        .logo-img-container {
            display: flex;
            justify-content: center;
            position: relative;
            width: 100%;
            z-index: 2; /* Ensure the logo overlays any other content */
        }

        .logo-img-container img {
            width: 350px; /* Specify the width to control the logo size */
            margin-top: 1rem; /* Adjust the top margin to position the logo effectively */
            z-index: 2; /* Ensure the logo overlays any other content */
        }

        /* Style markdown elements to ensure they are clearly visible and well-positioned */
        .markdown-text-container {
            padding: 2rem 1rem;
            border-radius: 0.5rem;
            background-color: rgba(255, 255, 255, 0.8); /* Semi-transparent white background for contrast */
            position: relative;
            top: -3rem; /* Adjust to position text effectively below the logo */
            z-index: 1; /* Ensure text is properly layered in the visual hierarchy */
        }

        /* Center the title text for better visual alignment */
        .title-container {
            text-align: center;
        }
        
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_image()


# Logo at the top center with increased size
st.markdown("""
    <div class="logo-img-container">
        <img src="https://github.com/josh23josh23/pic/blob/main/image-removebg-preview.png?raw=true">
    </div>
""", unsafe_allow_html=True)

# Title in a container to ensure it's centered
st.markdown("""
    <div class="title-container">
        <h1>Investments Feasibility Tool</h1>
    </div>
""", unsafe_allow_html=True)



constants = {
    'QLD': {
        'SimplifiedStampDutyRate': 0.065,
        'ProjectManagementFeePercent': 0.02,
    },
    'WA': {
        'SimplifiedStampDutyRate': 0.051,
        'ProjectManagementFeePercent': 0.35,  # Confirm if this is correct or a typo
    }
}

st.write("""
**This system is a financial feasibility tool that calculates project revenue, hard costs (OPC), soft costs, 
total profit, and profit per lot, providing a clear overview of a project's economic viability and potential profitability.**
""")

region = st.radio("Select Your Region", ["QLD", "WA"])

# Check the region selected and set the constants
if region:
    SimplifiedStampDutyRate = constants[region]['SimplifiedStampDutyRate']
    ProjectManagementFeePercent = constants[region]['ProjectManagementFeePercent']

    # Now you can use SimplifiedStampDutyRate and ProjectManagementFeePercent in your calculations
    # For example, if you have input fields that need to display these values:
    #st.write(f"Simplified Stamp Duty Rate for {region}: ", SimplifiedStampDutyRate)
    #st.write(f"Project Management Fee Percent for {region}: ", ProjectManagementFeePercent)



headerText1 =  """
1) **Gross Site area and Net Developable Area/Hectare**
"""

headerText2 = """
2) **Efficiency in Percertage**
"""

headerText3 = """
3) **OPC Cost**
"""
headerText4 = """
4) **Retail Lot Price**
"""
headerText5 = """
5) **The Development Margin Hurdle**
"""

def getNetRevenueLessGST(revenue, GSTRate):
    return revenue/(1+GSTRate)

def getNetDevelopableHectares(GrossHA, AssumedNDA):
    return GrossHA*AssumedNDA

def getLotsPerNDH(AverageLotSize, EfficiencyPercent):
    return (EfficiencyPercent*10000)/AverageLotSize

def getNumberOfLots(NetDevelopableHectares,LotsPerNDH):
    return NetDevelopableHectares*LotsPerNDH

def getAcquisitionCostPerLot(AcquisitionCost, NoOfLots):
    return AcquisitionCost/ NoOfLots

def getSalesAndMarketing(RevenuePerLot, SalesAndMarketingPercent, LegalFees):
    return (RevenuePerLot* SalesAndMarketingPercent) + LegalFees

def getInterestAndFinanceWoRLV(AcquisitionCost, NoOfLots, ConstructionLoanInterestRate,OpinionofProbableCost):
    return (AcquisitionCost/NoOfLots) + (ConstructionLoanInterestRate*OpinionofProbableCost) 

def getStatFeesPerLot(StatFees, NoOfLots):
    return StatFees/NoOfLots

def getManagementFees(RevenuePerLot, ProjectManagementFeePercent):
    return RevenuePerLot*ProjectManagementFeePercent

def getContingency(OpinionatedProductionCost, ProjectContingencyPercent):
    return OpinionatedProductionCost*ProjectContingencyPercent

def getOtherCostPerLotWoRLV(AcquisitionCostPerLot, SalesAndMarketing, InterestAndFinanceWoRLV, StatFeesPerLot,
    ManagementFees, Contingency):
    return AcquisitionCostPerLot + SalesAndMarketing + InterestAndFinanceWoRLV + \
            StatFeesPerLot + ManagementFees + Contingency
    
def getStampDuty(RLVperLot, SimplifiedStampDutyRate):
    return RLVperLot*SimplifiedStampDutyRate

def getInterestandFinanceRLVcomponent(RLVperLot, LandLoanInterestRate):
    return RLVperLot*LandLoanInterestRate

def getLandHolding(RLVperLot,LandHoldingFee ):
    return RLVperLot*LandHoldingFee


def calculateReturnVals(RevenuePerLot,GSTRate, NetDevelopableHectares,LotsPerNDH,
                AcquisitionCost, SalesAndMarketingPercent, LegalFees, ConstructionLoanInterestRate,
                 OpinionofProbableCost, StatFees, ProjectManagementFeePercent, ProjectContingencyPercent,
                SimplifiedStampDutyRate, LandLoanInterestRate, LandHoldingFee, DevelopmentMarginPercent):
    
    
    NetRevenueLessGST = getNetRevenueLessGST(RevenuePerLot,GSTRate)
    NoOfLots = getNumberOfLots(NetDevelopableHectares, LotsPerNDH)
    AcquisitionCostPerLot = getAcquisitionCostPerLot(AcquisitionCost, NoOfLots)
    SalesAndMarketing = getSalesAndMarketing(RevenuePerLot, SalesAndMarketingPercent, LegalFees)
    InterestAndFinanceWoRLV = getInterestAndFinanceWoRLV(AcquisitionCost, NoOfLots, 
                                ConstructionLoanInterestRate,OpinionofProbableCost)
    StatFeesPerLot = getStatFeesPerLot(StatFees, NoOfLots)
    ManagementFees = getManagementFees(RevenuePerLot, ProjectManagementFeePercent)
    Contingency = getContingency(OpinionofProbableCost, ProjectContingencyPercent)
    OtherCostPerLotWoRLV = getOtherCostPerLotWoRLV(AcquisitionCostPerLot, SalesAndMarketing, InterestAndFinanceWoRLV, StatFeesPerLot,
    ManagementFees, Contingency)
    
    RSum = (SimplifiedStampDutyRate + LandLoanInterestRate + LandHoldingFee + 1)*(1+ DevelopmentMarginPercent)
    RLVperLot = (NetRevenueLessGST - OpinionofProbableCost*(1+DevelopmentMarginPercent)\
           - OtherCostPerLotWoRLV*(1+ DevelopmentMarginPercent))/RSum
    RLV = NoOfLots*RLVperLot
    StampDuty = getStampDuty(RLVperLot,SimplifiedStampDutyRate)
    LandLoanInterest = getInterestandFinanceRLVcomponent(RLVperLot, LandLoanInterestRate)
    LandHolding = getLandHolding(RLVperLot,LandHoldingFee)
    OtherCostPerLotWithRLV =  OtherCostPerLotWoRLV + StampDuty + LandLoanInterest + LandHolding
    OtherCostPercent = OtherCostPerLotWithRLV/OpinionofProbableCost
    DevMargin = NetRevenueLessGST - OpinionofProbableCost - OtherCostPerLotWithRLV - RLVperLot 
    #print(NetRevenueLessGST, OpinionofProbableCost, OtherCostPerLotWithRLV, RLVperLot)
    
    
    #Add RLV dev Margin Check
    
    return NoOfLots, RLVperLot, RLV,  OtherCostPerLotWithRLV, OtherCostPercent, DevMargin    

def GenerateRLVString(RevenuePerLot,GSTRate,GrossHA,AssumedNDA, NetDevelopableHectares,
                      AverageLotSize,EfficiencyPercent,LotsPerNDH,
                AcquisitionCost, SalesAndMarketingPercent, LegalFees, ConstructionLoanInterestRate,
                 OpinionofProbableCost, StatFees, ProjectManagementFeePercent, ProjectContingencyPercent,
                SimplifiedStampDutyRate, LandLoanInterestRate, LandHoldingFee, DevelopmentMarginPercent):

    NoOfLots, RLVperLot, RLV,  OtherCostPerLotWithRLV, OtherCostPercent, DevMargin= calculateReturnVals(RevenuePerLot,GSTRate, NetDevelopableHectares,LotsPerNDH,
                AcquisitionCost, SalesAndMarketingPercent, LegalFees, ConstructionLoanInterestRate,
                 OpinionofProbableCost, StatFees, ProjectManagementFeePercent, ProjectContingencyPercent,
                SimplifiedStampDutyRate, LandLoanInterestRate, LandHoldingFee, DevelopmentMarginPercent)
        
    

    Rstring = f"""**Results:**

- **RLV:** ${int(RLV):,}
- **RLV Per Lot:** ${int(RLVperLot):,}

**Based on:**

- **Gross HA:** {int(GrossHA) if GrossHA > 0 else int(NetDevelopableHectares)}
- **Net Developable Hectare (NDH):** {int(NetDevelopableHectares)}
- **Average Lot Size:** {int(AverageLotSize) if AverageLotSize > 0 else int(7000/LotsPerNDH)}
- **Number of Lots:** {int(NoOfLots)}
- **Opinion of Probable Cost (OPC):** ${int(OpinionofProbableCost):,}
- **Retail Lot Price (RLP):** ${int(RevenuePerLot):,}
- **Other Costs:** {int(OtherCostPercent * 100)}%
- **Development Margin:** {int(DevelopmentMarginPercent * 100)}%

**Therefore:**

- **Revenue:** ${int(RevenuePerLot * NoOfLots):,}
- **Hard Costs (OPC):** ${int(OpinionofProbableCost * NoOfLots):,}
- **Soft Costs (Other Costs):** ${int(OtherCostPerLotWithRLV * NoOfLots):,}
- **Total Profit:** ${int(DevMargin * NoOfLots):,}
- **Profit per Lot:** ${int(DevMargin):,}"""
    
    return Rstring   
   
def DirectRLVFromInput(GrossHA, AssumedNDA, NetDevelopableHectares, EfficiencyPercent, AverageLotSize,
                       LotsPerNDH, RevenuePerLot, OpinionofProbableCost, DevelopmentMarginPercent, region):
    
    if region == 'QLD':
        # Constants for QLD
        SimplifiedStampDutyRate = 0.065
        ProjectManagementFeePercent = 0.02
        # ... (rest of your QLD-specific constants)
    
    elif region == 'WA':
        # Constants for WA
        SimplifiedStampDutyRate = 0.051
        ProjectManagementFeePercent = 0.035
        # ... (rest of your WA-specific constants)
    
    # Constants that are common across regions should be assigned outside the if-else block
    AcquisitionCost = 100000
    SalesAndMarketingPercent = 0.035
    LegalFees = 1000
    LandLoanInterestRate = .1
    ConstructionLoanInterestRate = 0.1
    StatFees = 50000
    ProjectContingencyPercent = 0.05
    LandHoldingFee = 0.052
    TargetProfitability = 0.2
    GSTRate = 0.1
    TimePeriod = 0 
    CPIAnnualRate = 0.02
    TPIAnnualRate = 0.03
    AnnualCapitalGrowth = 0.07

    # Now call the GenerateRLVString function with all the parameters
    ResultString = GenerateRLVString(RevenuePerLot, GSTRate, GrossHA, AssumedNDA, NetDevelopableHectares,
                                     AverageLotSize, EfficiencyPercent, LotsPerNDH, AcquisitionCost,
                                     SalesAndMarketingPercent, LegalFees, ConstructionLoanInterestRate,
                                     OpinionofProbableCost, StatFees, ProjectManagementFeePercent,
                                     ProjectContingencyPercent, SimplifiedStampDutyRate,
                                     LandLoanInterestRate, LandHoldingFee, DevelopmentMarginPercent)
    
    return ResultString


    

GrossHA = 0
AssumedNDA = 0
NetDevelopableHectares = 0 
EfficiencyPercent = 0.7
AverageLotSize = 0
LotsPerNDH = 0


st.markdown(headerText1)

enable_NDH= st.checkbox("Enable NDH")# Check if the checkbox is selected
if enable_NDH:
    NetDevelopableHectares = st.number_input("Net Developable Hectares",  value=20.0, step=0.1, format="%.2f")
else:
    GrossHA = st.number_input("Gross Hectare", value=20.0, step=0.1, format="%.2f")
    AssumedNDA = st.number_input("Net Developable Hectares", min_value= 1, max_value = 100 , value = 100)
    AssumedNDA = AssumedNDA/100


st.markdown(headerText2)

enable_LNDH= st.checkbox("Enable Lots per NDH")# Check if the checkbox is selected
if enable_LNDH:
    LotsPerNDH = st.number_input("Lots per NDH", value=20.0, step=0.1, format="%.2f") 
else:
    EfficiencyPercent = st.number_input("Efficiency Percent",min_value = 1, max_value = 100, value = 70) 
    EfficiencyPercent = EfficiencyPercent/100 
    AverageLotSize = st.number_input("Average Lot Size", value = 500)
 
st.markdown(headerText3)
OpinionofProbableCost = st.number_input("Opinion of Probable Cost", value=110000) 
st.markdown(headerText4)
RevenuePerLot = st.number_input("Retail Lot Price", value=200000) 
st.markdown(headerText5)
DevelopmentMarginPercent = st.number_input("Development Margin Percent", min_value = 1, max_value=100 ,  value=20) 
DevelopmentMarginPercent = DevelopmentMarginPercent/100 

if enable_NDH == False :
    NetDevelopableHectares = getNetDevelopableHectares(GrossHA, AssumedNDA)

if enable_LNDH == False:
    LotsPerNDH = getLotsPerNDH(AverageLotSize, EfficiencyPercent)
 

with st.form('my_form'):
    submittedreg = st.form_submit_button('Calculate')
    if submittedreg:
        result = DirectRLVFromInput(GrossHA, AssumedNDA, NetDevelopableHectares, EfficiencyPercent, AverageLotSize,
                                    LotsPerNDH, RevenuePerLot, OpinionofProbableCost, DevelopmentMarginPercent, region)
        st.markdown(result)
