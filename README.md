# finlytx

## Tests
To run tests
```
pytest
```

## Functions

Security Static Data > Security Cashflows > Security Analysis
Underlying rate agnostic with a 'rate wrapper' that adds underlying rate assumptions for a pricing date?
Do we pass in rate assumptions with cashflows?

Variables:

MISC
valuationDateDetails

SECURITY
StaticData: {
    faceValue,

}
CashflowStaticData: {
    securityExchanges: Array of Dict [
        {
            date,
            value
        }
    ],
}

    - Utils
        - Regression
            - NS
            - NSS
        - FinancialMathematics
            - present_value
            - future_value
            - discount_rate
        - Cashflows
            - generate_cashflows
        - Pricing
            - accrued_interest
    - Portfolio Management
        - PortfolioManagement
    - Market Analysis
        - MarketAnalysis
        - YieldReturn
        - Risk
    - Security Analysis
        - SecurityAnalysis
            - security_profile [ risk, return, fairvalue, cashflows ]
                - security_cashflow_profile
                - security_market_profile
                - security_risk_profile
                - security_return_profile [ in->cashflow+market ] (Current and expected)              
        - YieldReturn
            - yield_to_workout
            - current_yield
            - z_spread
            - oas_spread
        - Risk
            - duration
    - Derivatives
        - Forwards
        - Futures
        - Options

TODO: Floating cashflows.
