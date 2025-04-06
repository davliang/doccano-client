from __future__ import annotations

from enum import Enum
from typing import (
    AbstractSet,
    Any,
    Dict,
    List,
    Mapping,
    Optional,
    Union,
)
from typing_extensions import Annotated, TypeAlias

from pydantic import (
    BaseModel,
    StringConstraints,
    computed_field,
    field_serializer,
)

IntStr = Union[int, str]
AbstractSetIntStr = AbstractSet[IntStr]
DictStrAny = Dict[str, Any]
MappingIntStrAny = Mapping[IntStr, Any]


class ProjectType(str, Enum):
    DOCUMENT_CLASSIFICATION = "DocumentClassification"
    SEQUENCE_LABELING = "SequenceLabeling"
    SEQ2SEQ = "Seq2seq"
    SPEECH2TEXT = "Speech2text"
    IMAGE_CLASSIFICATION = "ImageClassification"
    BOUNDING_BOX = "BoundingBox"
    SEGMENTATION = "Segmentation"
    IMAGE_CAPTIONING = "ImageCaptioning"
    INTENT_DETECTION_AND_SLOT_FILLING = "IntentDetectionAndSlotFilling"


Name: TypeAlias = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=100,
        strip_whitespace=True,
    ),
]


Description: TypeAlias = Annotated[
    str,
    StringConstraints(
        min_length=1,
        strip_whitespace=True,
    ),
]


class Project(BaseModel):
    id: Optional[int] = None
    name: Name
    description: Description
    guideline: str = "Please write annotation guideline."
    project_type: ProjectType
    random_order: bool = False
    collaborative_annotation: bool = False
    single_class_classification: bool = False
    allow_overlapping: bool = False
    grapheme_mode: bool = False
    use_relation: bool = False
    tags: List[str] = []

    @property
    @computed_field
    def resource_type(self) -> str:
        PROJECT_TO_RESOURCE_TYPE = {
            ProjectType.DOCUMENT_CLASSIFICATION: "TextClassificationProject",
            ProjectType.SEQUENCE_LABELING: "SequenceLabelingProject",
            ProjectType.SEQ2SEQ: "Seq2seqProject",
            ProjectType.SPEECH2TEXT: "Speech2textProject",
            ProjectType.IMAGE_CLASSIFICATION: "ImageClassificationProject",
            ProjectType.BOUNDING_BOX: "BoundingBoxProject",
            ProjectType.SEGMENTATION: "SegmentationProject",
            ProjectType.IMAGE_CAPTIONING: "ImageCaptioningProject",
            ProjectType.INTENT_DETECTION_AND_SLOT_FILLING: "IntentDetectionAndSlotFillingProject",
        }
        if self.project_type not in PROJECT_TO_RESOURCE_TYPE:
            raise ValueError(f"Unknown project_type: {self.project_type}")
        return PROJECT_TO_RESOURCE_TYPE[self.project_type]

    @field_serializer("project_type")
    def serialize_project_type(self, pt: ProjectType, _info):
        return pt.value
