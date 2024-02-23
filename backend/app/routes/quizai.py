import os
import random
import pathlib
import textwrap
import google.generativeai as genai
from flask import Blueprint, jsonify, request


quizai_bp = Blueprint('quizai', __name__)


@quizai_bp.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Hello World"})

@quizai_bp.route('/question', methods=['GET'])
def get_question():
    model = genai.GenerativeModel('gemini-pro')
    google_api_key = os.environ.get('GOOGLE_API_KEY')
    print(google_api_key)
    genai.configure(api_key=google_api_key)
    n = request.args.get('n')
    category = request.args.get('category')
    subcategory = request.args.get('subcategory')
    subject = request.args.get('subject')
    unit = request.args.get('unit')
    subunit = request.args.get('subunit')
    tag = request.args.get('tag')
    print(tag)
    question = model.generate_content(f"For the concept: {tag} in  {subunit} under {unit} under {subject} under {subcategory} under {category}. Difficulty level: {4/5}. Distractor type: plausible. Generate {n} five-options multiple choice question. Provide also the correct answer and the explanation for each question. Output your response as a json array of objects with keys question, option_a, option_b, option_c, option_d, option_e, answer, explanation. The answer should be written as A, B, C, D, or E")
    print(question.text)
    return question.text


# Endpoint to get categories
@quizai_bp.route('/categories/')
def get_categories():
    categories = [category['name'] for category in categories_json]
    return categories

# Endpoint to get subcategories based on the parent category
@quizai_bp.route('/subcategories/<category_name>')
def get_subcategories(category_name):
    for category in categories_json:
        if category['name'] == category_name and 'subcategories' in category:
            subcategories = [subcat['name'] for subcat in category['subcategories']]
            return subcategories
    return jsonify({"error": "Category not found"}), 404

# Endpoint to get subjects based on the parent subcategory
@quizai_bp.route('/subjects/<subcategory_name>')
def get_subjects(subcategory_name):
    for category in categories_json:
        if 'subcategories' in category:
            for subcategory in category['subcategories']:
                if subcategory['name'] == subcategory_name and 'subjects' in subcategory:
                    subjects = [subject['name'] for subject in subcategory['subjects']]
                    return subjects
    return jsonify({"error": "Subcategory not found"}), 404

# Endpoint to get units based on the parent subject
@quizai_bp.route('/units/<subject_name>')
def get_units(subject_name):
    for category in categories_json:
        if 'subcategories' in category:
            for subcategory in category['subcategories']:
                if 'subjects' in subcategory:
                    for subject in subcategory['subjects']:
                        if subject['name'] == subject_name and 'units' in subject:
                            units = [unit['name'] for unit in subject['units']]
                            return units
    return jsonify({"error": "Subject not found"}), 404

# Endpoint to get subunits based on the parent unit
@quizai_bp.route('/subunits/<unit_name>')
def get_subunits(unit_name):
    for category in categories_json:
        if 'subcategories' in category:
            for subcategory in category['subcategories']:
                if 'subjects' in subcategory:
                    for subject in subcategory['subjects']:
                        if 'units' in subject:
                            for unit in subject['units']:
                                if unit['name'] == unit_name and 'subunits' in unit:
                                    subunits = [subunit['name'] for subunit in unit['subunits']]
                                    return subunits
    return jsonify({"error": "Unit not found"}), 404

# Endpoint to get tags based on the parent subunit
@quizai_bp.route('/tags/<subunit_name>')
def get_tags(subunit_name):
    for category in categories_json:
        if 'subcategories' in category:
            for subcategory in category['subcategories']:
                if 'subjects' in subcategory:
                    for subject in subcategory['subjects']:
                        if 'units' in subject:
                            for unit in subject['units']:
                                if 'subunits' in unit:
                                    for subunit in unit['subunits']:
                                        if subunit['name'] == subunit_name and 'tags' in subunit:
                                            tags = subunit['tags']
                                            return tags
    return jsonify({"error": "Subunit not found"}), 404

categories_json = [
        {
            
            "name": "Dental Surgery",
            "subcategories": [
                {
                    
                    "name": "General Dentistry",
                    "subjects": [
                        {
                            
                            "name": "Dental Anatomy",
                            "units": [
                                {
                                    
                                    "name": "Tooth Morphology",
                                    "subunits": [
                                        {
                                            
                                            "name": "Incisors",
                                            "description": "Detailed study of incisors' anatomy.",
                                            "tags": [
                                                "dental-anatomy",
                                                "tooth-morphology"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Canines",
                                            "description": "In-depth analysis of canine teeth structure.",
                                            "tags": [
                                                "dental-anatomy",
                                                "tooth-morphology"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Premolars",
                                            "description": "Examination of premolars' dental characteristics.",
                                            "tags": [
                                                "dental-anatomy",
                                                "tooth-morphology"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Molars",
                                            "description": "Comprehensive study of molar teeth anatomy.",
                                            "tags": [
                                                "dental-anatomy",
                                                "tooth-morphology"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Dental Nomenclature",
                                    "subunits": [
                                        {
                                            
                                            "name": "FDI World Dental Federation System",
                                            "description": "Understanding the FDI tooth numbering system.",
                                            "tags": [
                                                "dental-nomenclature"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Universal Numbering System",
                                            "description": "Exploring the Universal Numbering System for teeth.",
                                            "tags": [
                                                "dental-nomenclature"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Dental Materials",
                            "units": [
                                {
                                    
                                    "name": "Restorative Materials",
                                    "subunits": [
                                        {
                                            
                                            "name": "Composite Resins",
                                            "description": "Study of composite resin materials for dental restorations.",
                                            "tags": [
                                                "dental-materials",
                                                "restorative-materials"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Amalgam",
                                            "description": "Analysis of amalgam as a restorative dental material.",
                                            "tags": [
                                                "dental-materials",
                                                "restorative-materials"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Impression Materials",
                                    "subunits": [
                                        {
                                            
                                            "name": "Alginate",
                                            "description": "Overview of alginate as a dental impression material.",
                                            "tags": [
                                                "dental-materials",
                                                "impression-materials"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Polyvinyl Siloxane",
                                            "description": "Examining polyvinyl siloxane in dental impressions.",
                                            "tags": [
                                                "dental-materials",
                                                "impression-materials"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    
                    "name": "Oral Surgery",
                    "subjects": [
                        {
                            
                            "name": "Exodontia",
                            "units": [
                                {
                                    
                                    "name": "Simple Extractions",
                                    "subunits": [
                                        {
                                            
                                            "name": "Indications",
                                            "description": "Understanding when simple extractions are indicated.",
                                            "tags": [
                                                "exodontia",
                                                "simple-extractions"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Techniques",
                                            "description": "Detailed examination of techniques for simple extractions.",
                                            "tags": [
                                                "exodontia",
                                                "simple-extractions"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Surgical Extractions",
                                    "subunits": [
                                        {
                                            
                                            "name": "Impacted Teeth",
                                            "description": "Study of surgical extraction techniques for impacted teeth.",
                                            "tags": [
                                                "exodontia",
                                                "surgical-extractions"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Socket Preservation",
                                            "description": "Exploring socket preservation methods in surgical extractions.",
                                            "tags": [
                                                "exodontia",
                                                "surgical-extractions"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Oral Pathology",
                            "units": [
                                {
                                    
                                    "name": "Dental Cysts and Tumors",
                                    "subunits": [
                                        {
                                            
                                            "name": "Odontogenic Cysts",
                                            "description": "Analysis of odontogenic cysts in oral pathology.",
                                            "tags": [
                                                "oral-pathology",
                                                "odontogenic-cysts"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Ameloblastoma",
                                            "description": "In-depth study of ameloblastoma as a dental tumor.",
                                            "tags": [
                                                "oral-pathology",
                                                "ameloblastoma"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Oral Precancerous Lesions",
                                    "subunits": [
                                        {
                                            
                                            "name": "Leukoplakia",
                                            "description": "Understanding leukoplakia as an oral precancerous lesion.",
                                            "tags": [
                                                "oral-pathology",
                                                "leukoplakia"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Erythroplakia",
                                            "description": "Exploring erythroplakia and its significance in oral pathology.",
                                            "tags": [
                                                "oral-pathology",
                                                "erythroplakia"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    
                    "name": "Orthodontics",
                    "subjects": [
                        {
                            
                            "name": "Orthodontic Diagnosis",
                            "units": [
                                {
                                    
                                    "name": "Malocclusion Classification",
                                    "subunits": [
                                        {
                                            
                                            "name": "Class I",
                                            "description": "Understanding Class I malocclusion and its characteristics.",
                                            "tags": [
                                                "orthodontics",
                                                "malocclusion-classification"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Class II",
                                            "description": "Analysis of Class II malocclusion and its diagnostic features.",
                                            "tags": [
                                                "orthodontics",
                                                "malocclusion-classification"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Class III",
                                            "description": "Examining Class III malocclusion and its diagnostic criteria.",
                                            "tags": [
                                                "orthodontics",
                                                "malocclusion-classification"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Cephalometric Analysis",
                                    "subunits": [
                                        {
                                            
                                            "name": "Skeletal Analysis",
                                            "description": "Study of skeletal cephalometric analysis in orthodontics.",
                                            "tags": [
                                                "orthodontics",
                                                "cephalometric-analysis"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Dental Analysis",
                                            "description": "Comprehensive examination of dental cephalometric analysis.",
                                            "tags": [
                                                "orthodontics",
                                                "cephalometric-analysis"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Orthodontic Appliances",
                            "units": [
                                {
                                    
                                    "name": "Fixed Appliances",
                                    "subunits": [
                                        {
                                            
                                            "name": "Braces",
                                            "description": "Exploring various types of braces in orthodontic treatment.",
                                            "tags": [
                                                "orthodontics",
                                                "fixed-appliances",
                                                "braces"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Space Maintainers",
                                            "description": "Understanding the role of space maintainers in orthodontics.",
                                            "tags": [
                                                "orthodontics",
                                                "fixed-appliances",
                                                "space-maintainers"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Removable Appliances",
                                    "subunits": [
                                        {
                                            
                                            "name": "Retainers",
                                            "description": "Analysis of different types of retainers used in orthodontics.",
                                            "tags": [
                                                "orthodontics",
                                                "removable-appliances",
                                                "retainers"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Aligners",
                                            "description": "Examining the use of aligners in orthodontic treatment.",
                                            "tags": [
                                                "orthodontics",
                                                "removable-appliances",
                                                "aligners"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    
                    "name": "Periodontics",
                    "subjects": [
                        {
                            
                            "name": "Gingival Diseases",
                            "units": [
                                {
                                    
                                    "name": "Gingivitis",
                                    "subunits": [
                                        {
                                            
                                            "name": "Plaque-Induced Gingivitis",
                                            "description": "Understanding the causes and treatment of plaque-induced gingivitis.",
                                            "tags": [
                                                "gingival-diseases",
                                                "gingivitis"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Non-Plaque-Induced Gingivitis",
                                            "description": "Analysis of non-plaque-induced gingivitis and its management.",
                                            "tags": [
                                                "gingival-diseases",
                                                "gingivitis"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Periodontitis",
                                    "subunits": [
                                        {
                                            
                                            "name": "Chronic Periodontitis",
                                            "description": "Study of chronic periodontitis, its progression, and treatment.",
                                            "tags": [
                                                "periodontitis",
                                                "chronic-periodontitis"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Aggressive Periodontitis",
                                            "description": "Examining aggressive periodontitis and its clinical features.",
                                            "tags": [
                                                "periodontitis",
                                                "aggressive-periodontitis"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Periodontal Surgery",
                            "units": [
                                {
                                    
                                    "name": "Gingivectomy",
                                    "subunits": [
                                        {
                                            
                                            "name": "Techniques",
                                            "description": "Exploring various techniques used in gingivectomy procedures.",
                                            "tags": [
                                                "periodontal-surgery",
                                                "gingivectomy"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Indications",
                                            "description": "Understanding the indications for performing a gingivectomy.",
                                            "tags": [
                                                "periodontal-surgery",
                                                "gingivectomy"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Flap Surgery",
                                    "subunits": [
                                        {
                                            
                                            "name": "Open Flap Debridement",
                                            "description": "Analysis of open flap debridement in periodontal flap surgery.",
                                            "tags": [
                                                "periodontal-surgery",
                                                "flap-surgery",
                                                "open-flap-debridement"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Guided Tissue Regeneration",
                                            "description": "Study of guided tissue regeneration in periodontal flap surgery.",
                                            "tags": [
                                                "periodontal-surgery",
                                                "flap-surgery",
                                                "guided-tissue-regeneration"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            
            "name": "Basic Medical Sciences",
            "subcategories": [
                {
                    
                    "name": "Human Anatomy",
                    "subjects": [
                        {
                            
                            "name": "Gross Anatomy",
                            "description": "The study of the structure of the body and its parts as visible to the naked eye.",
                            "units": [
                                {
                                    
                                    "name": "Surface Anatomy",
                                    "description": "Study of the external features and markings on the body's surface"
                                },
                                {
                                    
                                    "name": "Skeletal System Anatomy",
                                    "description": "Examination of the bones, their structure, and interactions"
                                },
                                {
                                    
                                    "name": "Muscular System Anatomy",
                                    "description": "Investigation of the muscles and their attachments and functions"
                                },
                                {
                                    
                                    "name": "Cardiovascular System Anatomy",
                                    "description": "Analysis of the heart and blood vessels in the body"
                                },
                                {
                                    
                                    "name": "Digestive System Anatomy",
                                    "description": "Exploration of the organs involved in digestion and nutrient absorption"
                                },
                                {
                                    
                                    "name": "Respiratory System Anatomy",
                                    "description": "Study of the organs responsible for breathing and gas exchange"
                                },
                                {
                                    
                                    "name": "Urinary System Anatomy",
                                    "description": "Examination of the structures involved in urine production and excretion"
                                },
                                {
                                    
                                    "name": "Reproductive System Anatomy",
                                    "description": "Analysis of the male and female reproductive organs and their functions"
                                },
                                {
                                    
                                    "name": "Endocrine System Anatomy",
                                    "description": "Investigation of the glands and hormones regulating bodily functions"
                                },
                                {
                                    
                                    "name": "Integumentary System Anatomy",
                                    "description": "Study of the skin, hair, and nails and their functions"
                                },
                                {
                                    
                                    "name": "Lymphatic System Anatomy",
                                    "description": "Exploration of the lymph nodes, vessels, and immune system components"
                                }
                            ]
                        },
                        {
                            
                            "name": "Histology (Microscopic Anatomy)",
                            "description": "The examination of tissues and cells under a microscope.",
                            "units": [
                                {
                                    
                                    "name": "Epithelial Tissue",
                                    "description": "Study of the tissue that covers surfaces and lines cavities",
                                    "units": [
                                        {
                                            
                                            "name": "Simple Epithelium",
                                            "description": "Single layer of cells for absorption and diffusion"
                                        },
                                        {
                                            
                                            "name": "Stratified Epithelium",
                                            "description": "Multiple layers of cells for protection"
                                        },
                                        {
                                            
                                            "name": "Pseudostratified Epithelium",
                                            "description": "Single layer of cells with varying heights"
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Connective Tissue",
                                    "description": "Examination of tissue that supports and connects various structures",
                                    "units": [
                                        {
                                            
                                            "name": "Bone Tissue",
                                            "description": "Hard connective tissue with a mineralized matrix"
                                        },
                                        {
                                            
                                            "name": "Blood Tissue",
                                            "description": "Fluid connective tissue with cells suspended in plasma"
                                        },
                                        {
                                            
                                            "name": "Adipose Tissue",
                                            "description": "Connective tissue storing fat cells"
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Muscle Tissue",
                                    "description": "Analysis of tissue responsible for movement and force generation",
                                    "units": [
                                        {
                                            
                                            "name": "Skeletal Muscle",
                                            "description": "Striated muscle attached to bones for voluntary movement"
                                        },
                                        {
                                            
                                            "name": "Smooth Muscle",
                                            "description": "Non-striated muscle found in walls of organs for involuntary movement"
                                        },
                                        {
                                            
                                            "name": "Cardiac Muscle",
                                            "description": "Striated muscle forming the heart walls for involuntary contraction"
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Nervous Tissue",
                                    "description": "Investigation of tissue involved in transmitting electrical signals",
                                    "units": [
                                        {
                                            
                                            "name": "Neurons",
                                            "description": "Cellular units transmitting nerve impulses"
                                        },
                                        {
                                            
                                            "name": "Neuroglia",
                                            "description": "Support cells providing structural and metabolic support to neurons"
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Neuroanatomy",
                            "description": "Focuses on the structure and organization of the nervous system.",
                            "units": [
                                {
                                    
                                    "name": "Central Nervous System",
                                    "description": "Brain and spinal cord"
                                },
                                {
                                    
                                    "name": "Peripheral Nervous System",
                                    "description": "Nerves and ganglia outside the brain and spinal cord"
                                },
                                {
                                    
                                    "name": "Autonomic Nervous System",
                                    "description": "Controls involuntary bodily functions"
                                }
                            ]
                        },
                        {
                            
                            "name": "Embryology",
                            "description": "The study of the development of embryos and fetuses.",
                            "units": [
                                {
                                    
                                    "name": "Germ Layers",
                                    "description": "Formation of ectoderm, mesoderm, and endoderm"
                                },
                                {
                                    
                                    "name": "Organogenesis",
                                    "description": "Development of specific organs and structures"
                                },
                                {
                                    
                                    "name": "Fetal Development",
                                    "description": "Growth and maturation of the fetus"
                                }
                            ]
                        },
                        {
                            
                            "name": "Systemic Anatomy",
                            "description": "Examines the structures of the body's systems, such as the circulatory, respiratory, digestive, and musculoskeletal systems.",
                            "units": [
                                {
                                    
                                    "name": "Circulatory System",
                                    "description": "Heart, blood vessels, and blood"
                                },
                                {
                                    
                                    "name": "Respiratory System",
                                    "description": "Lungs and airways"
                                },
                                {
                                    
                                    "name": "Digestive System",
                                    "description": "Organs involved in digestion and nutrient absorption"
                                },
                                {
                                    
                                    "name": "Musculoskeletal System",
                                    "description": "Bones, muscles, and joints"
                                }
                            ]
                        },
                        {
                            
                            "name": "Regional Anatomy",
                            "description": "Studies the anatomy of specific regions of the body, such as the head and neck, thorax, abdomen, and limbs.",
                            "units": [
                                {
                                    
                                    "name": "Head and Neck Anatomy",
                                    "description": "Skull, face, and neck structures"
                                },
                                {
                                    
                                    "name": "Thoracic Anatomy",
                                    "description": "Chest and organs within the thoracic cavity"
                                },
                                {
                                    
                                    "name": "Abdominal Anatomy",
                                    "description": "Organs within the abdominal cavity"
                                },
                                {
                                    
                                    "name": "Limbs Anatomy",
                                    "description": "Arms and legs"
                                }
                            ]
                        },
                        {
                            
                            "name": "Radiological Anatomy",
                            "description": "Understanding anatomy through medical imaging techniques like X-rays, CT scans, and MRIs.",
                            "units": [
                                {
                                    
                                    "name": "X-ray Anatomy",
                                    "description": "Interpretation of X-ray images"
                                },
                                {
                                    
                                    "name": "CT Scan Anatomy",
                                    "description": "Analysis of cross-sectional images"
                                },
                                {
                                    
                                    "name": "MRI Anatomy",
                                    "description": "Study of detailed images using magnetic resonance"
                                }
                            ]
                        },
                        {
                            
                            "name": "Comparative Anatomy",
                            "description": "Compares the anatomical structures of different species to understand evolutionary relationships.",
                            "units": [
                                {
                                    
                                    "name": "Vertebrate Comparative Anatomy",
                                    "description": "Comparison of anatomical structures in vertebrates"
                                },
                                {
                                    
                                    "name": "Invertebrate Comparative Anatomy",
                                    "description": "Comparison of anatomical structures in invertebrates"
                                },
                                {
                                    
                                    "name": "Functional Comparative Anatomy",
                                    "description": "Comparisons based on functional adaptations"
                                }
                            ]
                        },
                        {
                            
                            "name": "Anatomical Techniques",
                            "description": "Covers the methods and tools used in anatomical research and dissection.",
                            "units": [
                                {
                                    
                                    "name": "Dissection Techniques",
                                    "description": "Procedures for systematically cutting and exposing anatomical structures"
                                },
                                {
                                    
                                    "name": "Microscopic Techniques",
                                    "description": "Methods for studying tissues and cells under a microscope"
                                },
                                {
                                    
                                    "name": "Imaging Techniques",
                                    "description": "Utilization of various imaging technologies in anatomical research"
                                }
                            ]
                        },
                        {
                            
                            "name": "Clinical Anatomy",
                            "description": "Emphasizes the practical application of anatomical knowledge in a clinical setting, often used in medical education.",
                            "units": [
                                {
                                    
                                    "name": "Surgical Anatomy",
                                    "description": "Anatomy relevant to surgical procedures"
                                },
                                {
                                    
                                    "name": "Clinical Radiological Anatomy",
                                    "description": "Application of radiological techniques in clinical settings"
                                },
                                {
                                    
                                    "name": "Medical Imaging Interpretation",
                                    "description": "Understanding and interpreting medical imaging results"
                                }
                            ]
                        },
                        {
                            
                            "name": "Functional Anatomy",
                            "description": "Explores the relationship between the structure of organs and tissues and their physiological functions.",
                            "units": [
                                {
                                    
                                    "name": "Physiological Anatomy",
                                    "description": "Integration of anatomy with physiological processes"
                                },
                                {
                                    
                                    "name": "Biomechanics",
                                    "description": "Study of the mechanical aspects of living organisms"
                                },
                                {
                                    
                                    "name": "Functional Neuroanatomy",
                                    "description": "Understanding the anatomical basis of neurological functions"
                                }
                            ]
                        },
                        {
                            
                            "name": "Pathological Anatomy",
                            "description": "Examines the anatomical changes that occur due to diseases and disorders.",
                            "units": [
                                {
                                    
                                    "name": "Pathophysiology",
                                    "description": "Study of functional changes associated with diseases"
                                },
                                {
                                    
                                    "name": "Histopathology",
                                    "description": "Microscopic examination of tissues for disease diagnosis"
                                },
                                {
                                    
                                    "name": "Forensic Anatomy",
                                    "description": "Application of anatomical knowledge in legal and forensic contexts"
                                }
                            ]
                        }
                    ]
                },
                {
                    
                    "name": "Human Physiology",
                    "subjects": [
                        {
                            
                            "name": "Cell Physiology",
                            "description": "Study of the physiological processes within cells",
                            "units": [
                                {
                                    
                                    "name": "Cellular Respiration",
                                    "description": "Process of generating energy within cells"
                                },
                                {
                                    
                                    "name": "Cellular Transport",
                                    "description": "Movement of substances across cell membranes"
                                },
                                {
                                    
                                    "name": "Cell Signaling",
                                    "description": "Communication between cells through molecular signals"
                                }
                            ]
                        },
                        {
                            
                            "name": "Neurophysiology",
                            "description": "Study of the function of the nervous system",
                            "units": [
                                {
                                    
                                    "name": "Neuronal Action Potentials",
                                    "description": "Generation and propagation of nerve impulses"
                                },
                                {
                                    
                                    "name": "Synaptic Transmission",
                                    "description": "Communication between neurons at synapses"
                                },
                                {
                                    
                                    "name": "Sensory Physiology",
                                    "description": "Processing of sensory information by the nervous system"
                                }
                            ]
                        },
                        {
                            
                            "name": "Cardiovascular Physiology",
                            "description": "Study of the function of the heart and blood vessels",
                            "units": [
                                {
                                    
                                    "name": "Cardiac Cycle",
                                    "description": "Events occurring during one heartbeat"
                                },
                                {
                                    
                                    "name": "Blood Pressure Regulation",
                                    "description": "Control mechanisms maintaining blood pressure"
                                },
                                {
                                    
                                    "name": "Vascular Dynamics",
                                    "description": "Flow of blood through blood vessels"
                                }
                            ]
                        },
                        {
                            
                            "name": "Respiratory Physiology",
                            "description": "Study of the function of the respiratory system",
                            "units": [
                                {
                                    
                                    "name": "Gas Exchange",
                                    "description": "Oxygen and carbon dioxide exchange in the lungs"
                                },
                                {
                                    
                                    "name": "Ventilation",
                                    "description": "Breathing and air movement in the respiratory system"
                                },
                                {
                                    
                                    "name": "Respiratory Control",
                                    "description": "Regulation of breathing rate and depth"
                                }
                            ]
                        },
                        {
                            
                            "name": "Gastrointestinal Physiology",
                            "description": "Study of the function of the digestive system",
                            "units": [
                                {
                                    
                                    "name": "Digestive Enzymes",
                                    "description": "Enzymes involved in breaking down food"
                                },
                                {
                                    
                                    "name": "Nutrient Absorption",
                                    "description": "Uptake of nutrients from the digestive tract"
                                },
                                {
                                    
                                    "name": "Motility",
                                    "description": "Movement of food through the digestive system"
                                }
                            ]
                        },
                        {
                            
                            "name": "Renal Physiology",
                            "description": "Study of the function of the kidneys and urinary system",
                            "units": [
                                {
                                    
                                    "name": "Filtration",
                                    "description": "Removal of waste products from the blood"
                                },
                                {
                                    
                                    "name": "Reabsorption",
                                    "description": "Reuptake of essential substances from the filtrate"
                                },
                                {
                                    
                                    "name": "Concentration and Dilution",
                                    "description": "Adjustment of urine concentration based on body needs"
                                }
                            ]
                        },
                        {
                            
                            "name": "Endocrine Physiology",
                            "description": "Study of the function of the endocrine system and hormones",
                            "units": [
                                {
                                    
                                    "name": "Hormone Secretion",
                                    "description": "Release of hormones by endocrine glands"
                                },
                                {
                                    
                                    "name": "Endocrine Regulation",
                                    "description": "Control of physiological processes by hormones"
                                },
                                {
                                    
                                    "name": "Feedback Mechanisms",
                                    "description": "Homeostatic regulation through feedback loops"
                                }
                            ]
                        },
                        {
                            
                            "name": "Reproductive Physiology",
                            "description": "Study of the function of the male and female reproductive systems",
                            "units": [
                                {
                                    
                                    "name": "Gametogenesis",
                                    "description": "Formation of gametes (sperm and eggs)"
                                },
                                {
                                    
                                    "name": "Menstrual Cycle",
                                    "description": "Regulation of reproductive events in females"
                                },
                                {
                                    
                                    "name": "Hormonal Control of Reproduction",
                                    "description": "Endocrine regulation of reproductive processes"
                                }
                            ]
                        },
                        {
                            
                            "name": "Immunology",
                            "description": "Study of the immune system and its responses to pathogens",
                            "units": [
                                {
                                    
                                    "name": "Innate Immunity",
                                    "description": "Immediate, non-specific immune responses"
                                },
                                {
                                    
                                    "name": "Adaptive Immunity",
                                    "description": "Specific immune responses involving memory"
                                },
                                {
                                    
                                    "name": "Immunological Disorders",
                                    "description": "Diseases related to immune system dysfunction"
                                }
                            ]
                        },
                        {
                            
                            "name": "Exercise Physiology",
                            "description": "Study of the effects of exercise on the body's physiological processes",
                            "units": [
                                {
                                    
                                    "name": "Cardiovascular Adaptations",
                                    "description": "Changes in the cardiovascular system during exercise"
                                },
                                {
                                    
                                    "name": "Muscular Adaptations",
                                    "description": "Responses and adaptations of muscles to exercise"
                                },
                                {
                                    
                                    "name": "Metabolic Responses",
                                    "description": "Energy metabolism during physical activity"
                                }
                            ]
                        },
                        {
                            
                            "name": "Environmental Physiology",
                            "description": "Study of how the body responds to environmental factors",
                            "units": [
                                {
                                    
                                    "name": "Temperature Regulation",
                                    "description": "Physiological responses to changes in temperature"
                                },
                                {
                                    
                                    "name": "Altitude Physiology",
                                    "description": "Adaptations to changes in altitude and oxygen levels"
                                },
                                {
                                    
                                    "name": "Water and Electrolyte Balance",
                                    "description": "Regulation of body fluids and electrolyte concentrations"
                                }
                            ]
                        },
                        {
                            
                            "name": "Neuromuscular Physiology",
                            "description": "Study of the interaction between the nervous system and muscles",
                            "units": [
                                {
                                    
                                    "name": "Motor Control",
                                    "description": "Regulation of muscle contraction by the nervous system"
                                },
                                {
                                    
                                    "name": "Muscle Contraction Mechanisms",
                                    "description": "Biochemical and physiological processes involved in muscle contraction"
                                },
                                {
                                    
                                    "name": "Neuromuscular Disorders",
                                    "description": "Conditions affecting the nervous-muscular interface"
                                }
                            ]
                        },
                        {
                            
                            "name": "Sensory Physiology",
                            "description": "Study of how the body perceives and responds to sensory stimuli",
                            "units": [
                                {
                                    
                                    "name": "Vision Physiology",
                                    "description": "Processes involved in visual perception"
                                },
                                {
                                    
                                    "name": "Auditory Physiology",
                                    "description": "Hearing and the physiology of the auditory system"
                                },
                                {
                                    
                                    "name": "Somatosensory Physiology",
                                    "description": "Processing of touch, pain, and other somatic sensations"
                                }
                            ]
                        },
                        {
                            
                            "name": "Circadian Rhythms",
                            "description": "Study of biological rhythms and their synchronization with the day-night cycle",
                            "units": [
                                {
                                    
                                    "name": "Sleep Physiology",
                                    "description": "Physiological processes during sleep cycles"
                                },
                                {
                                    
                                    "name": "Hormonal Rhythms",
                                    "description": "Cyclic variations in hormone levels"
                                },
                                {
                                    
                                    "name": "Biological Clocks",
                                    "description": "Internal timekeeping mechanisms in the body"
                                }
                            ]
                        },
                        {
                            
                            "name": "Integrative Physiology",
                            "description": "Study of how different physiological systems work together to maintain homeostasis",
                            "units": [
                                {
                                    
                                    "name": "Homeostatic Regulation",
                                    "description": "Coordination of physiological processes to maintain internal balance"
                                },
                                {
                                    
                                    "name": "Physiological Adaptations",
                                    "description": "Adaptive responses to changes in the external environment"
                                },
                                {
                                    
                                    "name": "Multisystem Interactions",
                                    "description": "Integration of functions across multiple physiological systems"
                                }
                            ]
                        }
                    ]
                },
                {
                    
                    "name": "Biochemistry",
                    "subjects": [
                        {
                            
                            "name": "Molecular Biology",
                            "description": "Study of biological processes at the molecular level",
                            "units": [
                                {
                                    
                                    "name": "DNA Structure and Replication",
                                    "description": "Molecular structure of DNA and its replication process"
                                },
                                {
                                    
                                    "name": "RNA and Transcription",
                                    "description": "Roles of RNA and transcription in gene expression"
                                },
                                {
                                    
                                    "name": "Protein Synthesis",
                                    "description": "Translation of genetic information into proteins"
                                }
                            ]
                        },
                        {
                            
                            "name": "Enzymology",
                            "description": "Study of enzymes and their catalytic functions",
                            "units": [
                                {
                                    
                                    "name": "Enzyme Kinetics",
                                    "description": "Rates of enzyme-catalyzed reactions"
                                },
                                {
                                    
                                    "name": "Enzyme Mechanisms",
                                    "description": "Molecular mechanisms underlying enzyme catalysis"
                                },
                                {
                                    
                                    "name": "Regulation of Enzyme Activity",
                                    "description": "Control of enzyme function in metabolic pathways"
                                }
                            ]
                        },
                        {
                            
                            "name": "Metabolism",
                            "description": "Study of biochemical pathways for energy production and molecule synthesis",
                            "units": [
                                {
                                    
                                    "name": "Glycolysis",
                                    "description": "Breakdown of glucose to produce energy"
                                },
                                {
                                    
                                    "name": "Citric Acid Cycle",
                                    "description": "Catabolism of acetyl-CoA in cellular respiration"
                                },
                                {
                                    
                                    "name": "Gluconeogenesis",
                                    "description": "Synthesis of glucose from non-carbohydrate precursors"
                                }
                            ]
                        },
                        {
                            
                            "name": "Biochemical Genetics",
                            "description": "Study of the relationship between genes and biochemical pathways",
                            "units": [
                                {
                                    
                                    "name": "Inborn Errors of Metabolism",
                                    "description": "Genetic disorders affecting metabolic pathways"
                                },
                                {
                                    
                                    "name": "Genetic Mutations and Enzyme Function",
                                    "description": "Effects of genetic mutations on enzyme activity"
                                },
                                {
                                    
                                    "name": "Molecular Basis of Genetic Diseases",
                                    "description": "Understanding genetic diseases at the molecular level"
                                }
                            ]
                        },
                        {
                            
                            "name": "Structural Biochemistry",
                            "description": "Study of the three-dimensional structures of biological molecules",
                            "units": [
                                {
                                    
                                    "name": "Protein Structure",
                                    "description": "Primary, secondary, tertiary, and quaternary protein structures"
                                },
                                {
                                    
                                    "name": "Nucleic Acid Structure",
                                    "description": "Molecular structures of DNA and RNA"
                                },
                                {
                                    
                                    "name": "Lipid Structures",
                                    "description": "Structures and functions of lipids in biological systems"
                                }
                            ]
                        },
                        {
                            
                            "name": "Cellular Biochemistry",
                            "description": "Study of biochemical processes within cells",
                            "units": [
                                {
                                    
                                    "name": "Cellular Signaling",
                                    "description": "Molecular mechanisms of cell communication"
                                },
                                {
                                    
                                    "name": "Cellular Transport",
                                    "description": "Movement of molecules across cell membranes"
                                },
                                {
                                    
                                    "name": "Cell Cycle Regulation",
                                    "description": "Control of cell division and proliferation"
                                }
                            ]
                        },
                        {
                            
                            "name": "Hormone Biochemistry",
                            "description": "Study of the structure and function of hormones",
                            "units": [
                                {
                                    
                                    "name": "Peptide Hormones",
                                    "description": "Structure and signaling pathways of peptide hormones"
                                },
                                {
                                    
                                    "name": "Steroid Hormones",
                                    "description": "Biosynthesis and actions of steroid hormones"
                                },
                                {
                                    
                                    "name": "Hormone Receptor Interactions",
                                    "description": "Mechanisms of hormone binding and cellular responses"
                                }
                            ]
                        },
                        {
                            
                            "name": "Biochemical Pharmacology",
                            "description": "Study of the interaction of drugs with biochemical systems",
                            "units": [
                                {
                                    
                                    "name": "Drug Metabolism",
                                    "description": "Biological transformation of drugs in the body"
                                },
                                {
                                    
                                    "name": "Enzyme Inhibition",
                                    "description": "Mechanisms and types of enzyme inhibition by drugs"
                                },
                                {
                                    
                                    "name": "Drug-Target Interactions",
                                    "description": "Molecular interactions between drugs and their targets"
                                }
                            ]
                        },
                        {
                            
                            "name": "Nutritional Biochemistry",
                            "description": "Study of the biochemical processes involved in nutrition",
                            "units": [
                                {
                                    
                                    "name": "Nutrient Metabolism",
                                    "description": "Biochemical pathways for the metabolism of nutrients"
                                },
                                {
                                    
                                    "name": "Vitamins and Coenzymes",
                                    "description": "Roles of vitamins and coenzymes in biochemical reactions"
                                },
                                {
                                    
                                    "name": "Mineral Metabolism",
                                    "description": "Biochemical processes involving essential minerals"
                                }
                            ]
                        },
                        {
                            
                            "name": "Immunobiochemistry",
                            "description": "Study of the biochemical aspects of the immune system",
                            "units": [
                                {
                                    
                                    "name": "Antibody Structure and Function",
                                    "description": "Molecular structure and roles of antibodies"
                                },
                                {
                                    
                                    "name": "Complement System",
                                    "description": "Biochemical pathways of the complement system"
                                },
                                {
                                    
                                    "name": "Immune Cell Biochemistry",
                                    "description": "Biochemical processes in immune cell activation and response"
                                }
                            ]
                        },
                        {
                            
                            "name": "Environmental Biochemistry",
                            "description": "Study of biochemical processes in relation to environmental factors",
                            "units": [
                                {
                                    
                                    "name": "Biodegradation",
                                    "description": "Breakdown of organic substances by living organisms"
                                },
                                {
                                    
                                    "name": "Toxicology",
                                    "description": "Study of the adverse effects of chemicals on living organisms"
                                },
                                {
                                    
                                    "name": "Ecological Biochemistry",
                                    "description": "Biochemical processes in ecological systems"
                                }
                            ]
                        },
                        {
                            
                            "name": "Bioinformatics",
                            "description": "Application of computational techniques to analyze biological data",
                            "units": [
                                {
                                    
                                    "name": "Protein Structure Prediction",
                                    "description": "Computational methods for predicting protein structures"
                                },
                                {
                                    
                                    "name": "Genomic Analysis",
                                    "description": "Bioinformatic tools for analyzing genomic data"
                                },
                                {
                                    
                                    "name": "Metabolic Pathway Analysis",
                                    "description": "Computational modeling of biochemical pathways"
                                }
                            ]
                        },
                        {
                            
                            "name": "Biophysical Chemistry",
                            "description": "Study of the physical principles underlying biochemical processes",
                            "units": [
                                {
                                    
                                    "name": "Spectroscopy in Biochemistry",
                                    "description": "Application of spectroscopic techniques in studying biomolecules"
                                },
                                {
                                    
                                    "name": "Thermodynamics of Biological Systems",
                                    "description": "Application of thermodynamic principles to biological processes"
                                },
                                {
                                    
                                    "name": "Kinetics of Biochemical Reactions",
                                    "description": "Analysis of reaction rates in biochemical systems"
                                }
                            ]
                        },
                        {
                            
                            "name": "Biochemical Engineering",
                            "description": "Application of biochemical principles to industrial processes",
                            "units": [
                                {
                                    
                                    "name": "Fermentation Processes",
                                    "description": "Industrial processes involving microbial fermentation"
                                },
                                {
                                    
                                    "name": "Bioprocess Optimization",
                                    "description": "Improvement and optimization of biochemical production processes"
                                },
                                {
                                    
                                    "name": "Bioreactor Design",
                                    "description": "Design and operation of bioreactors for biochemical production"
                                }
                            ]
                        },
                        {
                            
                            "name": "Medical Biochemistry",
                            "description": "Application of biochemical principles to medical science",
                            "units": [
                                {
                                    
                                    "name": "Clinical Biochemistry",
                                    "description": "Application of biochemical tests in clinical diagnosis"
                                },
                                {
                                    
                                    "name": "Molecular Medicine",
                                    "description": "Application of molecular techniques in medical research and treatment"
                                },
                                {
                                    
                                    "name": "Pharmacological Biochemistry",
                                    "description": "Biochemical aspects of drug action and development"
                                }
                            ]
                        },
                        {
                            
                            "name": "Biogeochemistry",
                            "description": "Study of the cycling of chemical elements between living organisms and the environment",
                            "units": [
                                {
                                    
                                    "name": "Carbon Cycle",
                                    "description": "Movement of carbon through the biosphere"
                                },
                                {
                                    
                                    "name": "Nitrogen Cycle",
                                    "description": "Transformation of nitrogen compounds in ecosystems"
                                },
                                {
                                    
                                    "name": "Biological Weathering",
                                    "description": "Biochemical processes contributing to rock and mineral breakdown"
                                }
                            ]
                        },
                        {
                            
                            "name": "Evolutionary Biochemistry",
                            "description": "Study of biochemical processes in the context of evolutionary biology",
                            "units": [
                                {
                                    
                                    "name": "Molecular Evolution",
                                    "description": "Evolutionary changes at the molecular level"
                                },
                                {
                                    
                                    "name": "Comparative Biochemistry",
                                    "description": "Comparison of biochemical processes across different species"
                                },
                                {
                                    
                                    "name": "Adaptation and Biochemistry",
                                    "description": "Biochemical adaptations in response to evolutionary pressures"
                                }
                            ]
                        },
                        {
                            
                            "name": "Synthetic Biology",
                            "description": "Application of biochemistry and molecular biology principles to design and construct biological systems",
                            "units": [
                                {
                                    
                                    "name": "Genetic Engineering",
                                    "description": "Manipulation of genes and genomes for practical purposes"
                                },
                                {
                                    
                                    "name": "Metabolic Engineering",
                                    "description": "Modification of metabolic pathways for desired outcomes"
                                },
                                {
                                    
                                    "name": "Biochemical Synthesis",
                                    "description": "Design and construction of novel biochemical pathways"
                                }
                            ]
                        },
                        {
                            
                            "name": "Astrobiology",
                            "description": "Study of the biochemical processes that may occur in extraterrestrial environments",
                            "units": [
                                {
                                    
                                    "name": "Exoplanetary Biochemistry",
                                    "description": "Hypothetical biochemical processes on exoplanets"
                                },
                                {
                                    
                                    "name": "Search for Extraterrestrial Life",
                                    "description": "Biochemical indicators in the search for life beyond Earth"
                                },
                                {
                                    
                                    "name": "Extreme Environments",
                                    "description": "Biochemical adaptations to extreme conditions on Earth and in space"
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            
            "name": "Clinical Sciences",
            "subcategories": [
                {
                    
                    "name": "Clinical Medicine",
                    "subjects": [
                        {
                            
                            "name": "Internal Medicine",
                            "units": [
                                {
                                    
                                    "name": "Cardiology",
                                    "subunits": [
                                        {
                                            
                                            "name": "Coronary Artery Diseases",
                                            "tags": [
                                                "Atherosclerosis",
                                                "Myocardial Infarction"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Heart Failure",
                                            "tags": [
                                                "Systolic Heart Failure",
                                                "Diastolic Heart Failure"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Gastroenterology",
                                    "subunits": [
                                        {
                                            
                                            "name": "Gastrointestinal Disorders",
                                            "tags": [
                                                "Inflammatory Bowel Disease",
                                                "Gastroesophageal Reflux Disease"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Liver Diseases",
                                            "tags": [
                                                "Hepatitis",
                                                "Cirrhosis"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Pediatrics",
                            "units": [
                                {
                                    
                                    "name": "Neonatology",
                                    "subunits": [
                                        {
                                            
                                            "name": "Prematurity",
                                            "tags": [
                                                "Respiratory Distress Syndrome",
                                                "Necrotizing Enterocolitis"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Congenital Disorders",
                                            "tags": [
                                                "Congenital Heart Defects",
                                                "Genetic Syndromes"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Pediatric Infectious Diseases",
                                    "subunits": [
                                        {
                                            
                                            "name": "Vaccine-Preventable Diseases",
                                            "tags": [
                                                "Measles",
                                                "Mumps",
                                                "Rubella"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Childhood Infections",
                                            "tags": [
                                                "Chickenpox",
                                                "Streptococcal Infections"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Surgery",
                            "units": [
                                {
                                    
                                    "name": "General Surgery",
                                    "subunits": [
                                        {
                                            
                                            "name": "Abdominal Surgery",
                                            "tags": [
                                                "Appendectomy",
                                                "Cholecystectomy"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Trauma Surgery",
                                            "tags": [
                                                "Polytrauma Management",
                                                "Emergency Surgery"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Orthopedic Surgery",
                                    "subunits": [
                                        {
                                            
                                            "name": "Joint Replacement",
                                            "tags": [
                                                "Total Hip Replacement",
                                                "Total Knee Replacement"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Spinal Surgery",
                                            "tags": [
                                                "Herniated Disc Surgery",
                                                "Spinal Fusion"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    
                    "name": "Clinical Anatomy",
                    "subjects": [
                        {
                            
                            "name": "Surgical Anatomy",
                            "units": [
                                {
                                    
                                    "name": "Head and Neck Anatomy",
                                    "subunits": [
                                        {
                                            
                                            "name": "Cranial Nerves",
                                            "tags": [
                                                "Olfactory Nerve",
                                                "Optic Nerve"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Facial Anatomy",
                                            "tags": [
                                                "Muscles of Facial Expression",
                                                "Salivary Glands"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Abdominal Anatomy",
                                    "subunits": [
                                        {
                                            
                                            "name": "Digestive System",
                                            "tags": [
                                                "Stomach Anatomy",
                                                "Small Intestine"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Vascular Anatomy",
                                            "tags": [
                                                "Abdominal Aorta",
                                                "Hepatic Artery"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Radiological Anatomy",
                            "units": [
                                {
                                    
                                    "name": "X-ray Anatomy",
                                    "subunits": [
                                        {
                                            
                                            "name": "Chest X-ray Anatomy",
                                            "tags": [
                                                "Lung Fields",
                                                "Cardiac Silhouette"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Abdominal X-ray Anatomy",
                                            "tags": [
                                                "Abdominal Organs",
                                                "Bony Structures"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "CT Scan Anatomy",
                                    "subunits": [
                                        {
                                            
                                            "name": "Brain CT Anatomy",
                                            "tags": [
                                                "Cerebral Hemispheres",
                                                "Ventricular System"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Abdominal CT Anatomy",
                                            "tags": [
                                                "Liver",
                                                "Pancreas"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    
                    "name": "Clinical Pathology",
                    "subjects": [
                        {
                            
                            "name": "Pathophysiology",
                            "units": [
                                {
                                    
                                    "name": "Cardiovascular Pathophysiology",
                                    "subunits": [
                                        {
                                            
                                            "name": "Ischemic Heart Disease",
                                            "tags": [
                                                "Coronary Artery Disease",
                                                "Myocardial Infarction"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Heart Failure",
                                            "tags": [
                                                "Systolic Heart Failure",
                                                "Diastolic Heart Failure"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Gastrointestinal Pathophysiology",
                                    "subunits": [
                                        {
                                            
                                            "name": "Inflammatory Bowel Disease",
                                            "tags": [
                                                "Crohn's Disease",
                                                "Ulcerative Colitis"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Liver Pathology",
                                            "tags": [
                                                "Hepatitis",
                                                "Cirrhosis"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Clinical Microbiology",
                            "units": [
                                {
                                    
                                    "name": "Bacterial Infections",
                                    "subunits": [
                                        {
                                            
                                            "name": "Respiratory Infections",
                                            "tags": [
                                                "Pneumonia",
                                                "Tuberculosis"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Urinary Tract Infections",
                                            "tags": [
                                                "Cystitis",
                                                "Pyelonephritis"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Viral Infections",
                                    "subunits": [
                                        {
                                            
                                            "name": "Influenza",
                                            "tags": [
                                                "Seasonal Influenza",
                                                "Pandemic Influenza"
                                            ]
                                        },
                                        {
                                            
                                            "name": "HIV/AIDS",
                                            "tags": [
                                                "HIV Infection",
                                                "AIDS"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Clinical Hematology",
                            "units": [
                                {
                                    
                                    "name": "Red Blood Cell Disorders",
                                    "subunits": [
                                        {
                                            
                                            "name": "Anemia",
                                            "tags": [
                                                "Iron-Deficiency Anemia",
                                                "Hemolytic Anemia"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Sickle Cell Disease",
                                            "tags": [
                                                "Genetics of Sickle Cell",
                                                "Clinical Manifestations"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "White Blood Cell Disorders",
                                    "subunits": [
                                        {
                                            
                                            "name": "Leukemia",
                                            "tags": [
                                                "Acute Myeloid Leukemia",
                                                "Chronic Lymphocytic Leukemia"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Lymphoma",
                                            "tags": [
                                                "Hodgkin Lymphoma",
                                                "Non-Hodgkin Lymphoma"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    
                    "name": "Clinical Pharmacology",
                    "subjects": [
                        {
                            
                            "name": "Pharmacokinetics",
                            "units": [
                                {
                                    
                                    "name": "Drug Absorption",
                                    "subunits": [
                                        {
                                            
                                            "name": "Oral Absorption",
                                            "tags": [
                                                "Absorption Process",
                                                "Factors Affecting Absorption"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Parenteral Absorption",
                                            "tags": [
                                                "Intravenous Absorption",
                                                "Subcutaneous Absorption"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Drug Distribution",
                                    "subunits": [
                                        {
                                            
                                            "name": "Volume of Distribution",
                                            "tags": [
                                                "Physiological Factors",
                                                "Pathological Conditions"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Plasma Protein Binding",
                                            "tags": [
                                                "Albumin Binding",
                                                "Alpha-1 Acid Glycoprotein Binding"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Pharmacodynamics",
                            "units": [
                                {
                                    
                                    "name": "Receptor Pharmacology",
                                    "subunits": [
                                        {
                                            
                                            "name": "Drug-Receptor Interactions",
                                            "tags": [
                                                "Agonists",
                                                "Antagonists"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Signal Transduction",
                                            "tags": [
                                                "Intracellular Signaling Pathways",
                                                "Second Messengers"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Enzyme Pharmacology",
                                    "subunits": [
                                        {
                                            
                                            "name": "Enzyme Inhibition",
                                            "tags": [
                                                "Competitive Inhibition",
                                                "Non-Competitive Inhibition"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Enzyme Induction",
                                            "tags": [
                                                "Cytochrome P450 Induction",
                                                "Phase II Enzyme Induction"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Clinical Toxicology",
                            "units": [
                                {
                                    
                                    "name": "Drug Overdose",
                                    "subunits": [
                                        {
                                            
                                            "name": "Common Overdose Scenarios",
                                            "tags": [
                                                "Analgesic Overdose",
                                                "Benzodiazepine Overdose"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Management of Overdose",
                                            "tags": [
                                                "Supportive Measures",
                                                "Antidotes"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Poisoning",
                                    "subunits": [
                                        {
                                            
                                            "name": "Toxic Agents",
                                            "tags": [
                                                "Heavy Metal Poisoning",
                                                "Plant Toxins"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Clinical Assessment",
                                            "tags": [
                                                "Symptoms",
                                                "Diagnostic Tests"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    
                    "name": "Clinical Biochemistry",
                    "subjects": [
                        {
                            
                            "name": "Diagnostic Enzymology",
                            "units": [
                                {
                                    
                                    "name": "Cardiac Enzymes",
                                    "subunits": [
                                        {
                                            
                                            "name": "Troponins",
                                            "tags": [
                                                "Troponin I",
                                                "Troponin T"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Creatine Kinase-MB",
                                            "tags": [
                                                "CK-MB Isoenzyme",
                                                "Clinical Significance"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Liver Enzymes",
                                    "subunits": [
                                        {
                                            
                                            "name": "Alanine Aminotransferase (ALT)",
                                            "tags": [
                                                "Physiology",
                                                "Elevated Levels"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Aspartate Aminotransferase (AST)",
                                            "tags": [
                                                "Normal Range",
                                                "Clinical Applications"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Clinical Immunology",
                            "units": [
                                {
                                    
                                    "name": "Immunoglobulins",
                                    "subunits": [
                                        {
                                            
                                            "name": "IgG",
                                            "tags": [
                                                "Functions",
                                                "Quantitative Measurement"
                                            ]
                                        },
                                        {
                                            
                                            "name": "IgM",
                                            "tags": [
                                                "Structure",
                                                "Clinical Significance"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Autoimmune Diseases",
                                    "subunits": [
                                        {
                                            
                                            "name": "Rheumatoid Arthritis",
                                            "tags": [
                                                "Pathogenesis",
                                                "Laboratory Markers"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Systemic Lupus Erythematosus",
                                            "tags": [
                                                "Clinical Manifestations",
                                                "Diagnostic Tests"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Endocrinology",
                            "units": [
                                {
                                    
                                    "name": "Thyroid Function Tests",
                                    "subunits": [
                                        {
                                            
                                            "name": "Thyroid Stimulating Hormone (TSH)",
                                            "tags": [
                                                "Regulation",
                                                "Diagnostic Use"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Free Thyroxine (FT4)",
                                            "tags": [
                                                "Physiological Role",
                                                "Abnormal Levels"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Adrenal Function Tests",
                                    "subunits": [
                                        {
                                            
                                            "name": "Cortisol",
                                            "tags": [
                                                "Circadian Rhythm",
                                                "Stress Response"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Adrenocorticotropic Hormone (ACTH)",
                                            "tags": [
                                                "Regulation",
                                                "Clinical Implications"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    
                    "name": "Clinical Radiology",
                    "subjects": [
                        {
                            
                            "name": "Diagnostic Radiology",
                            "units": [
                                {
                                    
                                    "name": "X-ray Imaging",
                                    "subunits": [
                                        {
                                            
                                            "name": "Chest X-ray",
                                            "tags": [
                                                "Normal Anatomy",
                                                "Abnormal Findings"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Abdominal X-ray",
                                            "tags": [
                                                "Gastrointestinal Tract",
                                                "Abdominal Organs"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "CT Scan",
                                    "subunits": [
                                        {
                                            
                                            "name": "Head CT",
                                            "tags": [
                                                "Brain Anatomy",
                                                "Pathological Findings"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Abdominal CT",
                                            "tags": [
                                                "Liver",
                                                "Pancreas"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Interventional Radiology",
                            "units": [
                                {
                                    
                                    "name": "Vascular Interventions",
                                    "subunits": [
                                        {
                                            
                                            "name": "Angioplasty",
                                            "tags": [
                                                "Balloon Angioplasty",
                                                "Stent Placement"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Embolization",
                                            "tags": [
                                                "Uterine Fibroid Embolization",
                                                "Peripheral Vascular Embolization"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Musculoskeletal Interventions",
                                    "subunits": [
                                        {
                                            
                                            "name": "Joint Injections",
                                            "tags": [
                                                "Corticosteroid Injections",
                                                "Viscosupplementation"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Vertebroplasty",
                                            "tags": [
                                                "Procedure Overview",
                                                "Clinical Applications"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Nuclear Medicine",
                            "units": [
                                {
                                    
                                    "name": "SPECT Imaging",
                                    "subunits": [
                                        {
                                            
                                            "name": "Myocardial Perfusion Scan",
                                            "tags": [
                                                "Indications",
                                                "Interpretation"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Bone Scan",
                                            "tags": [
                                                "Detection of Bone Metastases",
                                                "Inflammatory Conditions"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "PET Imaging",
                                    "subunits": [
                                        {
                                            
                                            "name": "FDG-PET",
                                            "tags": [
                                                "Oncology Applications",
                                                "Infectious Diseases"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Amyloid PET",
                                            "tags": [
                                                "Alzheimer's Disease Diagnosis",
                                                "Research Applications"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    
                    "name": "Clinical Epidemiology",
                    "subjects": [
                        {
                            
                            "name": "Epidemiological Methods",
                            "units": [
                                {
                                    
                                    "name": "Study Designs",
                                    "subunits": [
                                        {
                                            
                                            "name": "Observational Studies",
                                            "tags": [
                                                "Cohort Studies",
                                                "Case-Control Studies"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Experimental Studies",
                                            "tags": [
                                                "Randomized Controlled Trials",
                                                "Quasi-Experimental Designs"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Biostatistics",
                                    "subunits": [
                                        {
                                            
                                            "name": "Descriptive Statistics",
                                            "tags": [
                                                "Measures of Central Tendency",
                                                "Measures of Dispersion"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Inferential Statistics",
                                            "tags": [
                                                "Hypothesis Testing",
                                                "Confidence Intervals"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Evidence-Based Medicine",
                            "units": [
                                {
                                    
                                    "name": "Critical Appraisal",
                                    "subunits": [
                                        {
                                            
                                            "name": "Systematic Reviews",
                                            "tags": [
                                                "Meta-Analysis",
                                                "Quality Assessment"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Clinical Practice Guidelines",
                                            "tags": [
                                                "Development Process",
                                                "Implementation Strategies"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Applying Evidence",
                                    "subunits": [
                                        {
                                            
                                            "name": "Shared Decision Making",
                                            "tags": [
                                                "Patient Involvement",
                                                "Communication Strategies"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Implementation Science",
                                            "tags": [
                                                "Barriers and Facilitators",
                                                "Sustainability"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Outcomes Research",
                            "units": [
                                {
                                    
                                    "name": "Quality of Life Assessment",
                                    "subunits": [
                                        {
                                            
                                            "name": "Measurement Tools",
                                            "tags": [
                                                "Generic Instruments",
                                                "Disease-Specific Instruments"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Interpreting Results",
                                            "tags": [
                                                "Clinically Meaningful Changes",
                                                "Limitations"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Health Services Research",
                                    "subunits": [
                                        {
                                            
                                            "name": "Healthcare Delivery",
                                            "tags": [
                                                "Access to Care",
                                                "Cost-Effectiveness"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Health Policy",
                                            "tags": [
                                                "Policy Analysis",
                                                "Healthcare Reform"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    
                    "name": "Clinical Psychology",
                    "subjects": [
                        {
                            
                            "name": "Psychopathology",
                            "units": [
                                {
                                    
                                    "name": "Mood Disorders",
                                    "subunits": [
                                        {
                                            
                                            "name": "Major Depressive Disorder",
                                            "tags": [
                                                "Symptoms",
                                                "Treatment Approaches"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Bipolar Disorder",
                                            "tags": [
                                                "Manic Episodes",
                                                "Psychosocial Interventions"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Anxiety Disorders",
                                    "subunits": [
                                        {
                                            
                                            "name": "Generalized Anxiety Disorder",
                                            "tags": [
                                                "Worrying",
                                                "Treatment Options"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Panic Disorder",
                                            "tags": [
                                                "Panic Attacks",
                                                "Cognitive-Behavioral Therapy"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Psychotherapy",
                            "units": [
                                {
                                    
                                    "name": "Cognitive-Behavioral Therapy (CBT)",
                                    "subunits": [
                                        {
                                            
                                            "name": "Basic Principles",
                                            "tags": [
                                                "Cognitive Restructuring",
                                                "Behavioral Activation"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Applications",
                                            "tags": [
                                                "Depression",
                                                "Anxiety Disorders"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Psychodynamic Therapy",
                                    "subunits": [
                                        {
                                            
                                            "name": "Psychoanalytic Techniques",
                                            "tags": [
                                                "Free Association",
                                                "Transference"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Applications",
                                            "tags": [
                                                "Personality Disorders",
                                                "Trauma"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Neuropsychology",
                            "units": [
                                {
                                    
                                    "name": "Neurocognitive Disorders",
                                    "subunits": [
                                        {
                                            
                                            "name": "Alzheimer's Disease",
                                            "tags": [
                                                "Pathophysiology",
                                                "Cognitive Decline"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Traumatic Brain Injury",
                                            "tags": [
                                                "Concussion",
                                                "Long-Term Effects"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Neuropsychological Assessment",
                                    "subunits": [
                                        {
                                            
                                            "name": "Cognitive Testing",
                                            "tags": [
                                                "Memory Assessment",
                                                "Executive Function"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Emotional Functioning",
                                            "tags": [
                                                "Mood Assessment",
                                                "Personality Measures"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    
                    "name": "Clinical Nutrition",
                    "subjects": [
                        {
                            
                            "name": "Medical Nutrition Therapy",
                            "units": [
                                {
                                    
                                    "name": "Cardiovascular Nutrition",
                                    "subunits": [
                                        {
                                            
                                            "name": "Dietary Approaches",
                                            "tags": [
                                                "DASH Diet",
                                                "Mediterranean Diet"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Nutraceuticals",
                                            "tags": [
                                                "Omega-3 Fatty Acids",
                                                "Plant Sterols"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Oncology Nutrition",
                                    "subunits": [
                                        {
                                            
                                            "name": "Nutrition in Cancer Treatment",
                                            "tags": [
                                                "Cachexia",
                                                "Nutritional Support"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Dietary Guidelines for Cancer Prevention",
                                            "tags": [
                                                "Antioxidant-Rich Foods",
                                                "Limiting Processed Meats"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Nutritional Assessment",
                            "units": [
                                {
                                    
                                    "name": "Anthropometric Measurements",
                                    "subunits": [
                                        {
                                            
                                            "name": "Body Mass Index (BMI)",
                                            "tags": [
                                                "Interpretation",
                                                "Limitations"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Waist-to-Hip Ratio",
                                            "tags": [
                                                "Metabolic Risk",
                                                "Measurement Technique"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Biochemical Assessment",
                                    "subunits": [
                                        {
                                            
                                            "name": "Blood Tests",
                                            "tags": [
                                                "Nutrient Levels",
                                                "Markers of Inflammation"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Urinary Tests",
                                            "tags": [
                                                "Nutrient Excretion",
                                                "Metabolite Analysis"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Enteral and Parenteral Nutrition",
                            "units": [
                                {
                                    
                                    "name": "Enteral Nutrition",
                                    "subunits": [
                                        {
                                            
                                            "name": "Tube Feeding",
                                            "tags": [
                                                "Nasogastric Feeding",
                                                "Gastrostomy Feeding"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Complications",
                                            "tags": [
                                                "Aspiration",
                                                "Tube Displacement"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Parenteral Nutrition",
                                    "subunits": [
                                        {
                                            
                                            "name": "Total Parenteral Nutrition (TPN)",
                                            "tags": [
                                                "Indications",
                                                "Complications"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Peripheral Parenteral Nutrition (PPN)",
                                            "tags": [
                                                "Limited Nutrient Concentrations",
                                                "Short-Term Use"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    
                    "name": "Clinical Genetics",
                    "subjects": [
                        {
                            
                            "name": "Genetic Counseling",
                            "units": [
                                {
                                    
                                    "name": "Communication Skills",
                                    "subunits": [
                                        {
                                            
                                            "name": "Building Rapport",
                                            "tags": [
                                                "Empathy",
                                                "Active Listening"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Breaking Difficult News",
                                            "tags": [
                                                "Conveying Genetic Risks",
                                                "Supporting Emotional Reactions"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Ethical Considerations",
                                    "subunits": [
                                        {
                                            
                                            "name": "Autonomy",
                                            "tags": [
                                                "Respecting Patient Choices",
                                                "Informed Consent"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Confidentiality",
                                            "tags": [
                                                "Genetic Information Sharing",
                                                "Exceptions"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Molecular Diagnostics",
                            "units": [
                                {
                                    
                                    "name": "Polymerase Chain Reaction (PCR)",
                                    "subunits": [
                                        {
                                            
                                            "name": "Principle",
                                            "tags": [
                                                "Denaturation",
                                                "Annealing"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Applications",
                                            "tags": [
                                                "DNA Amplification",
                                                "Genotyping"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Next-Generation Sequencing (NGS)",
                                    "subunits": [
                                        {
                                            
                                            "name": "Sequencing Platforms",
                                            "tags": [
                                                "Illumina",
                                                "Ion Torrent"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Bioinformatics Analysis",
                                            "tags": [
                                                "Variant Calling",
                                                "Annotation"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Inherited Diseases",
                            "units": [
                                {
                                    
                                    "name": "Cystic Fibrosis",
                                    "subunits": [
                                        {
                                            
                                            "name": "Genetics",
                                            "tags": [
                                                "CFTR Gene Mutations",
                                                "Inheritance Pattern"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Clinical Features",
                                            "tags": [
                                                "Respiratory Symptoms",
                                                "Digestive Issues"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Hemophilia",
                                    "subunits": [
                                        {
                                            
                                            "name": "Coagulation Factors",
                                            "tags": [
                                                "Factor VIII Deficiency",
                                                "Factor IX Deficiency"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Treatment",
                                            "tags": [
                                                "Clotting Factor Replacement",
                                                "Gene Therapy"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    
                    "name": "Clinical Nursing",
                    "subjects": [
                        {
                            
                            "name": "Medical-Surgical Nursing",
                            "units": [
                                {
                                    
                                    "name": "Cardiac Nursing",
                                    "subunits": [
                                        {
                                            
                                            "name": "Coronary Artery Bypass Graft (CABG) Surgery",
                                            "tags": [
                                                "Preoperative Care",
                                                "Postoperative Care"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Heart Failure Nursing",
                                            "tags": [
                                                "Assessment",
                                                "Interventions"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Neurological Nursing",
                                    "subunits": [
                                        {
                                            
                                            "name": "Stroke",
                                            "tags": [
                                                "Ischemic Stroke",
                                                "Hemorrhagic Stroke"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Spinal Cord Injury Nursing",
                                            "tags": [
                                                "Autonomic Dysreflexia",
                                                "Rehabilitation"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Pediatric Nursing",
                            "units": [
                                {
                                    
                                    "name": "Neonatal Nursing",
                                    "subunits": [
                                        {
                                            
                                            "name": "Neonatal Intensive Care Unit (NICU)",
                                            "tags": [
                                                "Preterm Infants",
                                                "Neonatal Respiratory Distress Syndrome"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Neonatal Infections",
                                            "tags": [
                                                "Sepsis",
                                                "Congenital Infections"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Pediatric Infectious Disease Nursing",
                                    "subunits": [
                                        {
                                            
                                            "name": "Vaccination",
                                            "tags": [
                                                "Immunization Schedule",
                                                "Vaccine Administration"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Pediatric Respiratory Infections",
                                            "tags": [
                                                "Bronchiolitis",
                                                "Pneumonia"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Psychiatric Nursing",
                            "units": [
                                {
                                    
                                    "name": "Mood Disorders Nursing",
                                    "subunits": [
                                        {
                                            
                                            "name": "Major Depressive Disorder",
                                            "tags": [
                                                "Assessment",
                                                "Therapeutic Communication"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Bipolar Disorder Nursing",
                                            "tags": [
                                                "Mood Stabilizers",
                                                "Crisis Intervention"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Anxiety Disorders Nursing",
                                    "subunits": [
                                        {
                                            
                                            "name": "Panic Disorder",
                                            "tags": [
                                                "Psychoeducation",
                                                "Relaxation Techniques"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Generalized Anxiety Disorder Nursing",
                                            "tags": [
                                                "Cognitive-Behavioral Strategies",
                                                "Medication Management"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    
                    "name": "Surgery",
                    "subjects": [
                        {
                            
                            "name": "General Surgery",
                            "units": [
                                {
                                    
                                    "name": "Abdominal Surgery",
                                    "subunits": [
                                        {
                                            
                                            "name": "Appendectomy",
                                            "tags": [
                                                "Open Appendectomy",
                                                "Laparoscopic Appendectomy"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Cholecystectomy",
                                            "tags": [
                                                "Open Cholecystectomy",
                                                "Laparoscopic Cholecystectomy"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Gastrointestinal Surgery",
                                    "subunits": [
                                        {
                                            
                                            "name": "Bariatric Surgery",
                                            "tags": [
                                                "Gastric Bypass",
                                                "Sleeve Gastrectomy"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Colorectal Surgery",
                                            "tags": [
                                                "Colectomy",
                                                "Rectal Resection"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Orthopedic Surgery",
                            "units": [
                                {
                                    
                                    "name": "Joint Replacement",
                                    "subunits": [
                                        {
                                            
                                            "name": "Total Knee Replacement",
                                            "tags": [
                                                "Procedure Steps",
                                                "Rehabilitation"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Total Hip Replacement",
                                            "tags": [
                                                "Surgical Techniques",
                                                "Postoperative Care"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Spine Surgery",
                                    "subunits": [
                                        {
                                            
                                            "name": "Lumbar Discectomy",
                                            "tags": [
                                                "Indications",
                                                "Complications"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Spinal Fusion",
                                            "tags": [
                                                "Types of Fusion",
                                                "Instrumentation"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Cardiothoracic Surgery",
                            "units": [
                                {
                                    
                                    "name": "Coronary Artery Bypass Grafting (CABG)",
                                    "subunits": [
                                        {
                                            
                                            "name": "On-Pump CABG",
                                            "tags": [
                                                "Surgical Steps",
                                                "Postoperative Care"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Off-Pump CABG",
                                            "tags": [
                                                "Advantages",
                                                "Patient Selection"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Valve Replacement",
                                    "subunits": [
                                        {
                                            
                                            "name": "Aortic Valve Replacement",
                                            "tags": [
                                                "Mechanical Valves",
                                                "Bioprosthetic Valves"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Mitral Valve Replacement",
                                            "tags": [
                                                "Indications",
                                                "Complications"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Neurosurgery",
                            "units": [
                                {
                                    
                                    "name": "Brain Surgery",
                                    "subunits": [
                                        {
                                            
                                            "name": "Craniotomy",
                                            "tags": [
                                                "Approaches",
                                                "Intraoperative Monitoring"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Brain Tumor Resection",
                                            "tags": [
                                                "Preoperative Planning",
                                                "Postoperative Care"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Spinal Surgery",
                                    "subunits": [
                                        {
                                            
                                            "name": "Microdiscectomy",
                                            "tags": [
                                                "Patient Selection",
                                                "Outcomes"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Spinal Cord Decompression",
                                            "tags": [
                                                "Stenosis",
                                                "Herniated Discs"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            
                            "name": "Plastic Surgery",
                            "units": [
                                {
                                    
                                    "name": "Cosmetic Surgery",
                                    "subunits": [
                                        {
                                            
                                            "name": "Facelift",
                                            "tags": [
                                                "Surgical Techniques",
                                                "Recovery"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Rhinoplasty",
                                            "tags": [
                                                "Functional Rhinoplasty",
                                                "Aesthetic Rhinoplasty"
                                            ]
                                        }
                                    ]
                                },
                                {
                                    
                                    "name": "Reconstructive Surgery",
                                    "subunits": [
                                        {
                                            
                                            "name": "Breast Reconstruction",
                                            "tags": [
                                                "Implant-Based Reconstruction",
                                                "Autologous Tissue Reconstruction"
                                            ]
                                        },
                                        {
                                            
                                            "name": "Scar Revision",
                                            "tags": [
                                                "Techniques",
                                                "Scar Management"
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        ]