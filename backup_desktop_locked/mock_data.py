"""
Realistic COEP (COEP Technological University, Pune) Scopus Benchmark Dataset Generator.
Provides an authentic baseline dataset for testing and immediate dashboard demonstration
covering faculty, departments, international/industry collaborations, CiteScore/SJR, and Quartiles.
"""

import datetime
import random

COEP_DEPARTMENTS = [
    "Computer Engineering & IT",
    "Mechanical Engineering",
    "Electronics & Telecommunication (E&TC)",
    "Electrical Engineering",
    "Civil & Environmental Engineering",
    "Metallurgical & Materials Engineering",
    "Instrumentation & Control Engineering",
    "Manufacturing & Industrial Engineering",
    "Applied Sciences & Mathematics",
    "Physics & Applied Materials",
    "Chemistry & Chemical Sciences"
]

COEP_FACULTY = {
    "Computer Engineering & IT": [
        "Dr. Vandana Inamdar", "Prof. V. Z. Attar", "Dr. S. N. Ghungrad", "Prof. J. V. Aghav",
        "Dr. Sunil B. Mane", "Dr. Yashodhara V. Haribhakta", "Dr. Abhijit A. M.", "Dr. Tanuja Pattanshetti"
    ],
    "Mechanical Engineering": [
        "Dr. S. N. Sapali", "Prof. B. B. Ahuja", "Dr. M. J. Rathod", "Dr. N. K. Chhapkhane",
        "Dr. S. S. Pardeshi", "Dr. P. R. Dhamangaonkar", "Dr. H. P. Jawale", "Dr. S. V. Karanjkar"
    ],
    "Electronics & Telecommunication (E&TC)": [
        "Dr. M. S. Sutaone", "Prof. P. P. Bartakke", "Dr. R. A. Patil", "Dr. S. P. Mahajan",
        "Dr. P. H. Ghare", "Dr. V. N. More", "Dr. A. M. Sapkal"
    ],
    "Electrical Engineering": [
        "Dr. B. N. Chaudhari", "Dr. S. R. Kurode", "Prof. V. N. Pande", "Dr. Archana Thosar",
        "Dr. S. S. Dambhare", "Dr. Meera Murali", "Dr. R. T. Ugale"
    ],
    "Civil & Environmental Engineering": [
        "Dr. S. G. Sonar", "Prof. M. S. Ranadive", "Dr. R. R. Joshi", "Dr. K. A. Patil",
        "Dr. B. M. Dawari", "Dr. N. A. Hedaoo", "Dr. I. P. Sonar"
    ],
    "Metallurgical & Materials Engineering": [
        "Dr. N. B. Dhokte", "Prof. S. P. Butee", "Dr. M. J. Rathod", "Dr. P. P. Deshpande",
        "Dr. K. R. Kambale", "Dr. S. T. Vagge", "Dr. V. S. Poddar"
    ],
    "Instrumentation & Control Engineering": [
        "Dr. D. N. Sonawane", "Prof. C. Y. Patil", "Dr. S. D. Agashe", "Dr. P. D. Shendge",
        "Dr. U. M. Chaskar", "Dr. S. L. Patil"
    ],
    "Manufacturing & Industrial Engineering": [
        "Dr. B. Rajiv", "Prof. N. R. Rajhans", "Dr. M. D. Jaybhaye", "Dr. P. D. Pantawane",
        "Dr. S. U. Ghunbre"
    ],
    "Applied Sciences & Mathematics": [
        "Dr. C. M. Deshpande", "Dr. K. V. Dalvi", "Dr. Y. M. Mahatekar", "Dr. A. B. Dhere"
    ],
    "Physics & Applied Materials": [
        "Dr. R. B. Kamble", "Dr. J. W. Dadge", "Dr. S. R. Jadkar", "Dr. N. A. Patil"
    ],
    "Chemistry & Chemical Sciences": [
        "Dr. K. A. Joshi", "Dr. M. Y. Khaladkar", "Dr. D. T. Shirke", "Dr. R. S. Sonawane"
    ]
}

JOURNAL_POOL = [
    # Q1 Journals
    {"title": "IEEE Transactions on Industrial Informatics", "issn": "1551-3203", "citescore": 21.4, "sjr": 3.82, "quartile": "Q1", "publisher": "IEEE"},
    {"title": "Applied Energy", "issn": "0306-2619", "citescore": 20.8, "sjr": 3.25, "quartile": "Q1", "publisher": "Elsevier"},
    {"title": "Journal of Cleaner Production", "issn": "0959-6526", "citescore": 18.5, "sjr": 2.15, "quartile": "Q1", "publisher": "Elsevier"},
    {"title": "IEEE Internet of Things Journal", "issn": "2327-4662", "citescore": 19.2, "sjr": 2.94, "quartile": "Q1", "publisher": "IEEE"},
    {"title": "Materials Science and Engineering: A", "issn": "0921-5093", "citescore": 11.2, "sjr": 1.76, "quartile": "Q1", "publisher": "Elsevier"},
    {"title": "IEEE Transactions on Power Systems", "issn": "0885-8950", "citescore": 16.3, "sjr": 3.10, "quartile": "Q1", "publisher": "IEEE"},
    {"title": "Sensors and Actuators B: Chemical", "issn": "0925-4005", "citescore": 14.7, "sjr": 2.08, "quartile": "Q1", "publisher": "Elsevier"},
    {"title": "Expert Systems with Applications", "issn": "0957-4174", "citescore": 15.6, "sjr": 2.21, "quartile": "Q1", "publisher": "Elsevier"},
    {"title": "Renewable and Sustainable Energy Reviews", "issn": "1364-0321", "citescore": 30.5, "sjr": 4.12, "quartile": "Q1", "publisher": "Elsevier"},
    {"title": "Composite Structures", "issn": "0263-8223", "citescore": 12.8, "sjr": 1.85, "quartile": "Q1", "publisher": "Elsevier"},
    {"title": "IEEE Transactions on Smart Grid", "issn": "1949-3053", "citescore": 18.1, "sjr": 3.45, "quartile": "Q1", "publisher": "IEEE"},
    {"title": "Chemical Engineering Journal", "issn": "1385-8947", "citescore": 22.1, "sjr": 3.01, "quartile": "Q1", "publisher": "Elsevier"},
    
    # Q2 Journals
    {"title": "IEEE Access", "issn": "2169-3536", "citescore": 7.4, "sjr": 0.92, "quartile": "Q2", "publisher": "IEEE"},
    {"title": "Journal of Materials Engineering and Performance", "issn": "1059-9495", "citescore": 4.5, "sjr": 0.65, "quartile": "Q2", "publisher": "Springer"},
    {"title": "International Journal of Thermal Sciences", "issn": "1290-0729", "citescore": 8.1, "sjr": 1.18, "quartile": "Q2", "publisher": "Elsevier"},
    {"title": "IET Control Theory & Applications", "issn": "1751-8644", "citescore": 5.9, "sjr": 0.88, "quartile": "Q2", "publisher": "IET"},
    {"title": "Computers & Electrical Engineering", "issn": "0045-7906", "citescore": 7.8, "sjr": 0.95, "quartile": "Q2", "publisher": "Elsevier"},
    {"title": "Measurement", "issn": "0263-2241", "citescore": 9.3, "sjr": 1.22, "quartile": "Q2", "publisher": "Elsevier"},
    {"title": "Journal of Building Engineering", "issn": "2352-7102", "citescore": 9.8, "sjr": 1.34, "quartile": "Q2", "publisher": "Elsevier"},
    {"title": "Surface and Coatings Technology", "issn": "0257-8972", "citescore": 8.9, "sjr": 1.15, "quartile": "Q2", "publisher": "Elsevier"},

    # Q3 Journals & Conferences
    {"title": "Journal of Electronic Materials", "issn": "0361-5235", "citescore": 3.8, "sjr": 0.48, "quartile": "Q3", "publisher": "Springer"},
    {"title": "Arabian Journal for Science and Engineering", "issn": "2191-4281", "citescore": 4.2, "sjr": 0.54, "quartile": "Q3", "publisher": "Springer"},
    {"title": "Materials Today: Proceedings", "issn": "2214-7853", "citescore": 3.4, "sjr": 0.38, "quartile": "Q3", "publisher": "Elsevier"},
    {"title": "IEEE Conference on Decision and Control (CDC)", "issn": "0191-2216", "citescore": 3.9, "sjr": 0.58, "quartile": "Q3", "publisher": "IEEE"},
    {"title": "Advances in Manufacturing", "issn": "2095-3127", "citescore": 4.8, "sjr": 0.61, "quartile": "Q3", "publisher": "Springer"},
    {"title": "International Journal of Civil Engineering", "issn": "1735-0522", "citescore": 3.6, "sjr": 0.45, "quartile": "Q3", "publisher": "Springer"},

    # Q4 Journals
    {"title": "Indian Journal of Engineering & Materials Sciences", "issn": "0971-4588", "citescore": 1.5, "sjr": 0.22, "quartile": "Q4", "publisher": "NIScPR"},
    {"title": "Journal of The Institution of Engineers (India): Series B", "issn": "2250-2106", "citescore": 2.1, "sjr": 0.29, "quartile": "Q4", "publisher": "Springer"},
    {"title": "International Journal of Emerging Electric Power Systems", "issn": "1553-779X", "citescore": 2.3, "sjr": 0.31, "quartile": "Q4", "publisher": "De Gruyter"}
]

INTERNATIONAL_COLLABORATORS = [
    {"country": "United States", "institution": "Purdue University"},
    {"country": "United States", "institution": "University of Michigan"},
    {"country": "United States", "institution": "Georgia Institute of Technology"},
    {"country": "Germany", "institution": "Technical University of Munich (TUM)"},
    {"country": "Germany", "institution": "RWTH Aachen University"},
    {"country": "United Kingdom", "institution": "Imperial College London"},
    {"country": "United Kingdom", "institution": "University of Sheffield"},
    {"country": "Singapore", "institution": "National University of Singapore (NUS)"},
    {"country": "Singapore", "institution": "Nanyang Technological University (NTU)"},
    {"country": "Australia", "institution": "University of Melbourne"},
    {"country": "Australia", "institution": "UNSW Sydney"},
    {"country": "Japan", "institution": "Tokyo Institute of Technology"},
    {"country": "South Korea", "institution": "KAIST"},
    {"country": "Canada", "institution": "University of Toronto"},
    {"country": "France", "institution": "CNRS / Université Paris-Saclay"},
    {"country": "Malaysia", "institution": "Universiti Malaya"}
]

NATIONAL_COLLABORATORS = [
    "IIT Bombay",
    "Savitribai Phule Pune University (SPPU)",
    "Bhabha Atomic Research Centre (BARC)",
    "IISc Bangalore",
    "IIT Madras",
    "IIT Kharagpur",
    "Defence Institute of Advanced Technology (DIAT) Pune",
    "National Chemical Laboratory (CSIR-NCL Pune)",
    "ARDE Pune (DRDO)",
    "VNIT Nagpur",
    "VJTI Mumbai"
]

INDUSTRY_COLLABORATORS = [
    "Tata Motors R&D",
    "Bharat Forge Ltd.",
    "Siemens Corporate Technology",
    "Larsen & Toubro (L&T)",
    "John Deere Technology Center Pune",
    "Thermax Ltd.",
    "Kirloskar Brothers Limited",
    "KPIT Technologies",
    "Cummins India R&D",
    "Bajaj Auto R&D"
]

RESEARCH_TOPICS = {
    "Computer Engineering & IT": [
        "Explainable AI for Early Detection of Multi-Modal Cyber Threats in Critical IoT Infrastructure",
        "Federated Learning Framework with Differential Privacy for Edge-Cloud Orchestration",
        "Deep Reinforcement Learning for Dynamic Traffic Congestion Management and Autonomous Vehicles",
        "Blockchain-Enabled Zero-Trust Architecture for Decentralized Smart City Data Sharing",
        "Vision Transformers for Real-Time Automated Defect Detection in High-Speed Manufacturing",
        "Quantum-Resilient Cryptographic Protocols for Secure Cyber-Physical Systems",
        "Adaptive Graph Neural Networks for Recommendation Systems in Enterprise Knowledge Graphs",
        "Self-Supervised Contrastive Learning for Multi-Spectral Satellite Imagery Analysis",
        "Fault-Tolerant Consensus Algorithm for High-Throughput Edge Computing Clusters"
    ],
    "Mechanical Engineering": [
        "Thermo-Hydraulic Performance Optimization of Microchannel Heat Sinks using Hybrid Nanofluids",
        "Experimental and Numerical Investigation of Additively Manufactured Inconel 718 Lattice Structures",
        "Combustion and Emission Characteristics of Bio-Ethanol Blended Fuel in CRDI Diesel Engines",
        "Multi-Objective Topology Optimization of Electric Vehicle Battery Enclosure Under Crashworthiness",
        "Tribological Behaviour of Plasma Sprayed Ceramic Coatings at Elevated Operating Temperatures",
        "Computational Fluid Dynamics Analysis of Aerodynamic Drag Reduction in Commercial Vehicles",
        "Phase Change Material Integrated Thermal Management System for High-Rate Lithium-Ion Battery Packs",
        "Fatigue Life Prediction of Friction Stir Welded Dissimilar Aluminium-Magnesium Alloys"
    ],
    "Electronics & Telecommunication (E&TC)": [
        "Reconfigurable Intelligent Surfaces (RIS) for 6G Terahertz Ultra-Reliable Low-Latency Communications",
        "Design and Optimization of Dual-Band Metamaterial Absorber for Millimeter-Wave Radar Stealth",
        "Energy-Efficient VLSI Architecture for Deep Neural Network Inference on Edge Devices",
        "MIMO Antenna Array with Decoupling Structure for 5G Sub-6 GHz Mobile Terminals",
        "Real-Time Compressive Sensing Architecture for Biomedical Signal Processing and Tele-Health",
        "FPGA Implementation of Fault-Tolerant Neural Accelerators for Autonomous Systems",
        "Deep Learning-Assisted Channel Estimation in Massive MIMO Multi-User Systems"
    ],
    "Electrical Engineering": [
        "Model Predictive Control of Multi-Level Inverter for Grid-Tied Solar Photovoltaic Systems",
        "Coordinated Voltage and Frequency Regulation in Microgrids with High Penetration of Renewables",
        "Health Estimation and Remaining Useful Life Prediction of EV Lithium-Ion Batteries via Physics-Informed ML",
        "Sliding Mode Controller for Permanent Magnet Synchronous Motor in Heavy Electric Traction",
        "Dynamic Wireless Power Transfer System with High Misalignment Tolerance for Electric Vehicles",
        "Resilient State Estimation Against False Data Injection Attacks in Smart Power Grids",
        "Optimal Energy Management and Demand Response in Zero-Energy Industrial Microgrids"
    ],
    "Civil & Environmental Engineering": [
        "Seismic Vulnerability Assessment and Retrofitting of Reinforced Concrete Structures using FRP",
        "Sustainable Utilization of Industrial Waste Slag in High-Performance Geopolymer Concrete",
        "Hydrological Modeling of Extreme Urban Flood Events under Changing Climate Scenarios",
        "Advanced Oxidation Processes for Removal of Emerging Micro-Pollutants from Wastewater",
        "GIS-Based Spatial Multi-Criteria Decision Analysis for Sustainable Urban Solid Waste Management",
        "Pavement Performance Evaluation of Bio-Asphalt Modified Bituminous Mixtures",
        "Real-Time Structural Health Monitoring of Cable-Stayed Bridges Using Fiber Bragg Grating Sensors"
    ],
    "Metallurgical & Materials Engineering": [
        "Microstructural Evolution and Mechanical Behaviour of High Entropy Alloys Synthesized by Spark Plasma Sintering",
        "Electrochemical Corrosion and Biocompatibility of Surface-Modified Ti-6Al-4V Medical Implants",
        "Superplastic Deformation Mechanisms in Ultrafine-Grained Magnesium Alloys Processed by ECAP",
        "Graphene-Reinforced Metal Matrix Composites: Synthesis, Mechanical Properties, and Wear Resistance",
        "Development of Wear-Resistant Superhydrophobic Coatings for Marine Applications",
        "Thermal Degradation and Oxidation Kinetics of High-Temperature Thermal Barrier Coatings"
    ],
    "Instrumentation & Control Engineering": [
        "Fractional-Order Robust Sliding Mode Control for Non-Linear MIMO Twin Rotor Aerodynamic Systems",
        "Self-Calibrating Optical Fiber Sensor for Cryogenic Temperature and Pressure Measurement",
        "Digital Twin-Driven Predictive Maintenance of Smart Actuators in Process Industries",
        "Adaptive Sliding Mode Observer for Sensor Fault Detection and Isolation in Quadrotor UAVs",
        "Multivariate Statistical Process Monitoring and Root Cause Analysis Using Deep Autoencoders",
        "Design and Implementation of MEMS-Based Piezoresistive Micro-Pressure Sensors"
    ],
    "Manufacturing & Industrial Engineering": [
        "Sustainable Machining of Titanium Alloys under Minimum Quantity Lubrication (MQL) with Nano-Fluids",
        "Digital Twin Framework for Energy-Aware Flexible Job-Shop Scheduling in Industry 4.0",
        "Laser Powder Bed Fusion of Ti-6Al-4V: Influence of Process Parameters on Porosity and Surface Roughness",
        "Supply Chain Resilience Optimization for Manufacturing Networks Under Global Disruptions",
        "Wire Arc Additive Manufacturing (WAAM) of Austenitic Stainless Steel: Microstructure and Residual Stress"
    ],
    "Applied Sciences & Mathematics": [
        "Analytical Solutions for Fractional-Order Non-Linear Differential Equations in Continuum Mechanics",
        "Stochastic Modeling and Optimal Control in Financial Risk Management and Portfolios",
        "Mathematical Modeling of Infectious Disease Dynamics with Vaccination and Spatial Heterogeneity"
    ],
    "Physics & Applied Materials": [
        "Synthesis and Photovoltaic Characteristics of Perovskite Solar Cells with Novel Electron Transport Layers",
        "High-Performance Supercapacitor Electrodes Based on Nitrogen-Doped Reduced Graphene Oxide",
        "Magnetic and Magnetoresistance Properties of Sol-Gel Derived Manganite Nanostructures"
    ],
    "Chemistry & Chemical Sciences": [
        "Visible-Light Active Heterogeneous Photocatalysts for Hydrogen Evolution and Dye Degradation",
        "Green Synthesis of Silver Nanoparticles Using Plant Extracts and Their Antibacterial Activity",
        "Functionalized Porous Organic Polymers for Selective Carbon Dioxide Capture and Storage"
    ]
}


def generate_coep_publications(total_count: int = 420) -> list[dict]:
    """Generates an authentic synthetic dataset representing COEP's Scopus research output."""
    random.seed(42)  # Deterministic seed for consistent baseline
    publications = []

    current_date = datetime.date(2026, 8, 24)
    # Comprehensive distribution of publications from 1950 to 2026
    year_distribution = {}
    
    # 1950 to 1979 (Early foundational engineering papers)
    for y in range(1950, 1980):
        year_distribution[y] = random.choice([1, 2, 2, 3])
    
    # 1980 to 1999 (Growing industrial & research papers)
    for y in range(1980, 2000):
        year_distribution[y] = random.randint(3, 8)

    # 2000 to 2015 (Modern era expansion)
    for y in range(2000, 2016):
        year_distribution[y] = random.randint(10, 25)

    # 2016 to 2026 (High volume era)
    year_distribution[2016] = 32
    year_distribution[2017] = 38
    year_distribution[2018] = 45
    year_distribution[2019] = 52
    year_distribution[2020] = 58
    year_distribution[2021] = 65
    year_distribution[2022] = 78
    year_distribution[2023] = 95
    year_distribution[2024] = 135
    year_distribution[2025] = 160
    year_distribution[2026] = 52

    doc_counter = 1001

    for year, count in year_distribution.items():
        for _ in range(count):
            doc_counter += 1
            dept = random.choice(COEP_DEPARTMENTS)
            coep_author = random.choice(COEP_FACULTY[dept])
            journal = random.choice(JOURNAL_POOL)
            
            # Select topic
            dept_topics = RESEARCH_TOPICS.get(dept, RESEARCH_TOPICS["Computer Engineering & IT"])
            base_title = random.choice(dept_topics)
            # Add slight variance to title to make unique
            variant_prefixes = ["", "Comprehensive Analysis of ", "A Novel Approach to ", "Design and Implementation of ", "Enhanced Framework for "]
            prefix = random.choice(variant_prefixes) if random.random() > 0.6 else ""
            title = f"{prefix}{base_title}" if prefix and not base_title.startswith(prefix) else base_title
            
            # Month & Day
            if year == 2026:
                # Up to August 2026
                month = random.randint(1, 8)
                day = random.randint(1, 28)
            else:
                month = random.randint(1, 12)
                day = random.randint(1, 28)
            
            pub_date = datetime.date(year, month, day)

            # Collaboration categorization
            rand_val = random.random()
            is_intl = False
            is_ind = False
            collab_type = "Institutional"
            countries = ["India"]
            institutions = ["COEP Technological University, Pune"]

            if rand_val < 0.28:  # ~28% International Collaboration
                is_intl = True
                collab_type = "International"
                intl_partner = random.choice(INTERNATIONAL_COLLABORATORS)
                countries.append(intl_partner["country"])
                institutions.append(intl_partner["institution"])
                external_author = f"Prof. {random.choice(['John Smith', 'Hans Meyer', 'David Lee', 'Kenji Sato', 'Elena Rostova', 'Michael Chang', 'Sarah Jenkins'])}"
            elif rand_val < 0.44:  # ~16% Industry Collaboration
                is_ind = True
                collab_type = "Industry"
                ind_partner = random.choice(INDUSTRY_COLLABORATORS)
                institutions.append(ind_partner)
                external_author = f"Dr. {random.choice(['Rajesh Verma', 'Sanjay Deshmukh', 'Vikram Joshi', 'Sunil Godbole', 'Priya Kulkarni'])} ({ind_partner})"
            elif rand_val < 0.78:  # ~34% National Collaboration
                collab_type = "National"
                nat_partner = random.choice(NATIONAL_COLLABORATORS)
                institutions.append(nat_partner)
                external_author = f"Dr. {random.choice(['A. K. Sharma', 'R. P. Nair', 'S. K. Gupta', 'P. K. Banerjee', 'Anjali Rao'])}"
            else:
                # Intra-institution only
                collab_type = "Institutional"
                other_faculty = random.choice([f for f in COEP_FACULTY[dept] if f != coep_author] or [coep_author])
                external_author = other_faculty

            student_coauthor = f"{random.choice(['Amit', 'Pooja', 'Rohan', 'Sneha', 'Nikhil', 'Tanvi', 'Abhishek', 'Shreya'])} {random.choice(['Patil', 'Kulkarni', 'Deshpande', 'Shinde', 'Joshi', 'Chavan'])}"
            authors = [coep_author, student_coauthor, external_author]
            authors_str = ", ".join(authors)

            # Citations calculation (older papers naturally have more citations)
            years_old = (2026 - year) + (1.0 - month / 12.0)
            base_cite_rate = 5.5 if journal["quartile"] == "Q1" else (3.2 if journal["quartile"] == "Q2" else 1.5)
            citations = int(max(0, random.gauss(years_old * base_cite_rate, 4.0)))
            
            # Add some outlier highly cited papers
            if random.random() < 0.04 and year <= 2024:
                citations = random.randint(75, 260)
            elif random.random() < 0.08 and year <= 2025:
                citations = random.randint(35, 85)

            is_top_10 = citations >= 30 or (journal["citescore"] >= 18.0 and journal["quartile"] == "Q1")

            doi = f"10.1016/j.{journal['title'][:6].lower().replace(' ', '')}.{year}.{random.randint(100000, 999999)}"
            scopus_eid = f"2-s2.0-85{random.randint(10000000, 99999999)}"
            scopus_id = f"{random.randint(85000000000, 85999999999)}"

            doc_type = random.choices(["Article", "Conference Paper", "Review", "Book Chapter"], weights=[72, 20, 6, 2])[0]
            is_oa = random.random() < 0.42

            pub_item = {
                "id": str(doc_counter),
                "eid": scopus_eid,
                "scopus_id": scopus_id,
                "title": title,
                "authors": authors,
                "authors_str": authors_str,
                "coep_authors": [coep_author],
                "primary_author": coep_author,
                "department": dept,
                "journal": journal["title"],
                "issn": journal["issn"],
                "publisher": journal["publisher"],
                "publication_date": pub_date.strftime("%Y-%m-%d"),
                "year": year,
                "month": pub_date.strftime("%B"),
                "month_num": month,
                "doi": doi,
                "doi_url": f"https://doi.org/{doi}",
                "scopus_url": f"https://www.scopus.com/record/display.uri?eid={scopus_eid}&origin=resultslist",
                "citations": citations,
                "citescore": journal["citescore"],
                "sjr": journal["sjr"],
                "quartile": journal["quartile"],
                "is_top_10_percent": is_top_10,
                "collaboration_type": collab_type,
                "is_international_collab": is_intl,
                "is_industry_collab": is_ind,
                "collaborating_countries": countries,
                "foreign_countries": [c for c in countries if c != "India"],
                "collaborating_institutions": institutions,
                "external_institutions": [inst for inst in institutions if "COEP" not in inst],
                "document_type": doc_type,
                "open_access": is_oa,
                "abstract": f"This study presents an investigation into {title.lower()} with application to modern engineering systems. Rigorous computational modeling, empirical validation, and benchmark evaluations were conducted at COEP Technological University in collaboration with partner research groups. Results show significant performance enhancements with robust accuracy and reproducible metrics."
            }
            publications.append(pub_item)

    # Sort descending by publication date
    publications.sort(key=lambda x: x["publication_date"], reverse=True)
    return publications
