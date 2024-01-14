from pydantic import BaseModel, HttpUrl


class Icon(BaseModel):
    svg: HttpUrl
    png: HttpUrl
    name: str


class Assets(BaseModel):
    icon: Icon


class Line(BaseModel):
    id: str
    name: str
    displayCode: str
    businessMode: str
    assets: Assets


class SituationMessage(BaseModel):
    isActive: bool
    isPlanned: bool
    criticity: str
    messages: list[str]


class TwitterAccountInfos(BaseModel):
    twitterId: str
    twitterUrl: HttpUrl
    isThreadActive: bool


class LineData(BaseModel):
    line: Line
    situations: list[SituationMessage]
    twitterAccountInfos: TwitterAccountInfos
