

I'm starting to write API routes in my FastAPI app.

I need you to help me think about to model my postgres db to best serve my API.


My goal is to serve a web page which will compute a CSRD scoring for a given company.

The CSRD (Corporate Sustainability Reporting Directive) directive plans for the creation of detailed European sustainability Reporting Standards, known as ESRS (European Sustainability Reporting Standards).
These standards aim to regulate and harmonize corporate publications and will be progressively applied from January 2024.

Thus, the API will have to check if the scores and summaries are available in Postgres, and if not, it will compute scores, summaries depending on the company's data.


The standards are divided into transversal norms:

- ESRS 1 - General Requirements
- ESRS 2 - General Disclosures
- Environmental (ESRS E) (and more)

Each section has a set of subsections and each subsection has a set of indicators.

As an example for the ESRS E, we have the following sections:

- Climat
- Biodiversity
    - Land Use
    - Funds allocation to Biodiversity studies etc ...


My API is looking like this at the moment:


 1 General API Structure: /api/v1/csrd/{company_id}/
 2 Summaries and Scores:
    • General Summary: /api/v1/csrd/{company_id}/summary
    • Section Summary: /api/v1/csrd/{company_id}/{section}/summary
    • Section Score: /api/v1/csrd/{company_id}/{section}/score
    • Subsection Summary: /api/v1/csrd/{company_id}/{section}/{subsection}/summary
    • Subsection Score: /api/v1/csrd/{company_id}/{section}/{subsection}/score
    • Indicator Score: /api/v1/csrd/{company_id}/{section}/{subsection}/{indicator}/score
 3 Detailed Data:
    • Section Details: /api/v1/csrd/{company_id}/{section}
    • Subsection Details: /api/v1/csrd/{company_id}/{section}/{subsection}
    • Indicator Details: /api/v1/csrd/{company_id}/{section}/{subsection}/{indicator}


Give me suggestions on how to model my Postgres db to best serve my API.