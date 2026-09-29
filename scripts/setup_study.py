"""
setup_study.py - Create one validation session per predictions folder.

Each session is named after its predictions directory and uses the fields from
GUIDE.md against oncoschema.schema. Sampling of up to 50 documents happens when
the session is first opened.
"""

import uuid

from mesa_validate.models import FieldSelection, Session
from mesa_validate.predictions_loader import (
    get_prediction_files,
    list_prediction_folders,
)
from mesa_validate.session_manager import SessionManager

SCHEMA_MODULE = "oncoschema.schema"
ROOT_CLASS = "OncologyModel"
SAMPLE_SIZE = 50

GUIDE_SELECTIONS = [
    FieldSelection(
        selection_type="basemodel_field",
        class_name="PrimaryCancerFacts",
        field_name="topography",
    ),
    FieldSelection(
        selection_type="basemodel_field",
        class_name="PrimaryCancerFacts",
        field_name="morphology",
    ),
    FieldSelection(
        selection_type="basemodel_field",
        class_name="PrimaryCancerFacts",
        field_name="diagnosis_year",
    ),
    FieldSelection(
        selection_type="basemodel_field",
        class_name="PrimaryCancerFacts",
        field_name="diagnosis_month",
    ),
    FieldSelection(
        selection_type="basemodel_field",
        class_name="PrimaryCancerFacts",
        field_name="tnm_stage",
    ),
    FieldSelection(
        selection_type="basemodel_class",
        class_name="MolecularBiomarkerProfile",
    ),
    FieldSelection(
        selection_type="basemodel_class",
        class_name="PerformanceStatus",
    ),
    FieldSelection(
        selection_type="enum_value",
        class_name="TimelineEventType",
        enum_value="experienced_toxicity_or_complication_related_to_treatment",
    ),
    FieldSelection(
        selection_type="enum_value",
        class_name="TimelineEventType",
        enum_value="evidence_of_metastatic_progression",
    ),
    FieldSelection(
        selection_type="enum_value",
        class_name="TimelineEventType",
        enum_value="radiology_evidence_of_disease_progression",
    ),
    FieldSelection(
        selection_type="enum_value",
        class_name="TimelineEventType",
        enum_value="experienced_treatment_reduction_or_stop",
    ),
]


def main():
    folders = list_prediction_folders()
    if not folders:
        print("No prediction folders found")
        return

    existing_names = {session.name for session in SessionManager.list_all()}

    for folder in folders:
        name = str(folder["name"])
        if name in existing_names:
            print(f"Skipped {name}: session already exists")
            continue

        document_ids = get_prediction_files(str(folder["path"]))
        sample_size = min(SAMPLE_SIZE, len(document_ids))
        session = Session(
            id=str(uuid.uuid4()),
            name=name,
            schema_module=SCHEMA_MODULE,
            root_class=ROOT_CLASS,
            predictions_folder=str(folder["path"]),
            sample_size=sample_size,
            selections=GUIDE_SELECTIONS,
        )
        SessionManager.create_new(session)
        print(
            f"Created {name}: sample size {sample_size} of {len(document_ids)} documents"
        )


if __name__ == "__main__":
    main()
