from typing import List, Literal, Optional, Type, TypeVar

from pydantic import BaseModel, ConfigDict, HttpUrl, field_validator

from zibal.response_codes import STATUS_CODES, WAGE_CODES
from zibal.utils import to_camel_case_dict, to_snake_case_dict

# All of the data models with the word 'Request' ending in their name are
# the data structures used in body of HTTP requests, while the data models
# ending  with 'Response' are the data structures that are expected to be
# received from the IPG APIs responses.

ResultCode = Literal[100, 102, 103, 104, 105, 106, 113]
FeeDeductionCodes = Literal[0, 1, 2]
StatusCode = Literal[-1, -2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
WageCode = Literal[0, 1, 2]
IsoDate = str  # e.g. '2024-08-11T16:06:44.731255'
T = TypeVar("T", bound="TransactionBase")


class TransactionBase(BaseModel):
    def model_dump_to_camel(self, **kwargs) -> dict:
        """
        Same as model_dump method, but convert the snake case keys into camel
        case keys. Pass any passed kwargs to model_dump.
        """
        data = self.model_dump(**kwargs)
        return to_camel_case_dict(data)

    @classmethod
    def from_camel_case(cls: Type[T], data: dict) -> T:
        """Initialize an instance by converting the dict camel case keys to snake case keys."""
        data = to_snake_case_dict(data)
        return cls(**data)


class TransactionRequireRequest(TransactionBase):
    """Used for starting a transaction process."""

    model_config = ConfigDict(strict=True)

    merchant: str
    amount: int
    callback_url: HttpUrl
    description: Optional[str] = None
    order_id: Optional[str] = None
    mobile: Optional[str] = None
    allowed_cards: Optional[List[str]] = None
    ledger_id: Optional[str] = None
    national_code: Optional[str] = None

    @field_validator("amount")
    def in_correct_range(cls, amount):
        if not (2000000000 > amount > 1500):
            raise ValueError(
                "Amount must be in the range (2,000,000,000, 1,500)"
            )
        return amount


class FailedResultDetail(BaseModel):
    """Used for result codes where the code is not 100 (i.e. not success)"""

    result_code: int
    result_meaning: str


class TransactionRequireResponse(TransactionBase):
    track_id: int
    result: ResultCode
    pay_link: Optional[str] = None
    message: str


class TransactionCallbackQueryParams(TransactionBase):
    """
    A GET HTTP request is called from zibal's webservice to the provided callbackUrl
    (the callbackUrl should have been provided in earlier levels of
    transaction process).
    The request is called with query parameters following this class's data
    structure.
    """

    success: Literal[1, 0]  # 1 for success, 0 for failure
    track_id: int
    order_id: str
    status: StatusCode


class TransactionVerifyRequest(TransactionBase):
    """Transactions that need to be verified by the app"""

    model_config = ConfigDict(strict=True)

    merchant: str
    track_id: int


class TransactionVerifyResponse(TransactionBase):
    paid_at: IsoDate
    card_number: Optional[str] = None
    status: StatusCode
    status_meaning: str
    amount: int
    ref_number: Optional[int] = None  # if successful
    description: Optional[str] = None  # if successful
    order_id: Optional[str] = None  # if successful
    result: ResultCode
    message: str
    multiplexing_info: List[str] = []

    @classmethod
    def from_camel_case(cls: Type[T], data: dict) -> T:
        status = data.get("status")
        if status is not None:
            data["status_meaning"] = STATUS_CODES.get(
                status, "Unknown status"
            )
        return super().from_camel_case(data)


class TransactionInquiryRequest(TransactionBase):
    """For inquirying the state of an already started transaction"""

    model_config = ConfigDict(strict=True)

    merchant: str
    track_id: int


class TransactionInquiryResponse(TransactionBase):
    created_at: IsoDate
    paid_at: IsoDate
    verified_at: IsoDate
    card_number: Optional[str] = None
    status: Optional[StatusCode]
    status_meaning: Optional[str]
    amount: int
    ref_number: Optional[int] = None  # if successful
    description: str
    order_id: Optional[str] = None
    wage: Optional[WageCode]
    wage_meaning: Optional[str]
    shaparak_fee: int
    result: ResultCode
    message: str
    multiplexing_info: List[str] = []

    @classmethod
    def from_camel_case(cls: Type[T], data: dict) -> T:
        status = data.get("status")
        wage = data.get("wage")
        if status is not None and wage is not None:
            data["status_meaning"] = STATUS_CODES.get(
                status, "Unknown status"
            )
            data["wage_meaning"] = WAGE_CODES.get(wage, "Unknown wage")
        return super().from_camel_case(data)
