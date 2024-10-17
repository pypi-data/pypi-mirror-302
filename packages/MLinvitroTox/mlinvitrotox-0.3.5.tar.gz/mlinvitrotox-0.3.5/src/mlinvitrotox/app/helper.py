dict_rename = {
    "hitcall": "hitcall",
    "hitcall_c": "hitcall (c)",
    "True": "positive",
    "False": "negative",
    "macro avg": "macro avg",
    "weighted avg": "weighted avg",
    "test": "Internal validation",
    "mb_val_structure": "MB validation from structure",
    "mb_val_sirius": "MB validation SIRIUS-predicted",
    "Internal validation": "Internal",
    "MB validation from structure": "MB structure",
    "MB validation SIRIUS-predicted": "MB SIRIUS",
    "default": "default=0.5",
    "tpr": "TPR≈0.5",
    "tnr": "TNR≈0.5",
    "optimal": "cost(TPR,TNR)",
    "XGBClassifier": "XGBoost",
    "XGBoost": "XGB",
    "RF": "RF",
    "RBF SVM": "SVM",
    "MLP": "MLP",
    "LR": "LR",
    "RandomForestClassifier": "RF",
    "LogisticRegression": "LR",
    "SVC": "RBF SVM",
    "MLPClassifier": "MLP",
    "accuracy": "accuracy",
}

acronym_mapping = {
    "Cell Cycle": "CP",
    "Not Annotated": "na",
    "not_annotated": "na",
    "Constitutive Androstane Receptor Modulation": "AN",
    "PPARG": "PPARG",  # Peroxisome proliferator activated receptor gamma
    "Pregnane X Receptor Modulation": "PXR",
    "RAR-related Orphan Receptor Modulation": "ROR",
    "Other Transcription Factors": "TF",
    "Other Developmental Signaling Transcription Factors": "TF",
    "Oxidative Stress": "OSR",
    "Inflammation": "INF",
    "p53 Modulation": "GTX",
    "Farnesoid X-activated Receptor Modulation": "FXR",
    "Peroxisome Proliferator Activated Receptor Modulation": "PPARG",
    "Vitamin D Modulation": "IM",
    "DNA Repair": "GTX",
    "Estrogen Receptor Modulation": "ER",
    "Liver X Receptor Modulation": "LXR",
    "TP53": "GTX",
    "Retinoic Acid Receptor Modulation": "RAR",
    "Retinoid X Receptor Modulation": "RXR",
    "Thyroid Receptor Modulation": "THR",
    "ICAM1": "IM",
    "VascularTissue": "CP",
    "Cell Growth": "CP",
    "TF": "TF",
    "Extracellular Matrix Degradation": "CP",
    "Vascularization": "CP",
    "Androgen Receptor Modulation": "AR",
    "VEGF": "PR",
    "Histone Modification": "GTX",
    "Mt Dys": "MF",
    "t-PA": "PR",
    "Estrogen-related Receptor Modulation": "ER",
    "IL6": "INF",
    "Progesterone Receptor Modulation": "P4",
    "SAA1": "PR",
    "Clotting": "CP",
    "Gene Expression Regulation, Xenobiotic Response": "XNR",
    "Apoptosis": "APO",
    "PAI -1(SERPINE1)": "PR",
    "Proliferation": "CP",
    "Cell Morphology": "CP",
    "Mitochondrial Function": "MF",
    "Aryl Hydrocarbon Receptor Modulation": "AhR",
    "ER Alpha": "ER",  # Same acronym as "Estrogen Receptor Modulation"
    "Aromatase Activity Modulation": "AA",
    "Glucocorticoid Receptor Modulation": "GC",
    "Malformation": "CP",
    "Receptors, Thyrotropin-Releasing Hormone": "TRH",
    "Neurotransmission": "NR",
    "DNA Damage": "GTX",
    "NR3C1": "GC",
    "Progesterone-related Steroid Hormone Metabolism": "P4",
    "Progestogen Biosynthesis and Metabolism": "NRC",
    "Androgen-related Steroid Hormone Metabolism": "AR",
    "Glucocorticoid Biosynthesis and Metabolism": "GC",
    "Glucocorticoid-related Steroid Hormone Metabolism": "GC",
    "Estrogen Biosynthesis and Metabolism": "ER",
    "Androgen Biosynthesis and Metabolism": "AR",
    "Sodium/Iodide Cotransporter": "NIS",
    "Pregnane X Receptor Modulation": "PXR",
    "Constitutive Androstane Receptor Modulation": "AN",
}


def _blank_to_underscore(x):
    return x.replace(" ", "_")


def predict_for_endpoint(endpoint, clf_data, features):
    feature_selection_model = clf_data[0]
    features = feature_selection_model.transform(features)
    clf = clf_data[1]
    prediction = clf.predict(features)
    return endpoint, prediction


def pandas_df_to_latex(data, caption="", label=""):
    # Initialize the LaTeX table with the longtable environment
    latex_table = f'\\begin{{longtable}}{{{"l" * len(data.columns)}}}\n'
    latex_table += (
        "\\caption{"
        + caption
        + "}\\label{tab:"
        + label.lower().replace(" ", "_")
        + "}\\\\\n"
    )
    latex_table += "\\toprule\n\\midrule\n"

    # Extract the header and remove it from the DataFrame
    header = data.columns
    data = data.values

    # Add the header row with \small to the LaTeX table
    latex_table += " & ".join(["\\small " + col for col in header]) + "\\\\\n\\hline\n"

    # Iterate through the data rows and add them to the table
    for row in data:
        latex_table += " & ".join(map(str, row)) + "\\\\\n"

    # Add table footer and replace \endtabular with \endlongtable
    latex_table += "\\bottomrule\n\\end{longtable}"
    latex_table = latex_table.replace("\\endtabular", "\\endlongtable")

    return latex_table
