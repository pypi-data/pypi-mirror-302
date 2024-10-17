from pydantic import BaseModel, Field


class Record(BaseModel):
    r_number: str = Field(..., title="R Number", description="The R number")
    flowcell: str = Field(..., title="Flowcell", description="The flowcell")
    lane: int = Field(..., title="Lane", description="The lane number")
    test_code: int = Field(..., title="Test Code", description="The test code")
    test: str = Field(..., title="Test", description="The test")
    midpool: str = Field(..., title="Midpool", description="The midpool")
    sample: str = Field(..., title="Sample", description="The sample")
    index_id: str = Field(..., title="Index ID", description="The index ID")
    library: str = Field(..., title="Library", description="The library")
    family_id: str = Field(..., title="Family ID", description="The family ID")
    slims_number: str = Field(..., title="SLIMS Number", description="The SLIMS number")
